import functions_framework
from google.cloud import bigquery
import googlemaps
import pandas as pd
import shapely.geometry
import shapely.wkt
from flask import jsonify

gmaps = googlemaps.Client(key='AIzaSyAHMnz118xRAj130zJXl9S09mlcepfoUfY')
client = bigquery.Client()
table_id = 'hackzurich23-8233.truck_info.plants'


def get_lat_lng(point):
    lng = shapely.wkt.loads(point).coords[0][0]
    lat = shapely.wkt.loads(point).coords[0][1]
    return (lat, lng)


def get_gmaps_distance(A, B, points=True):
    if points:
        directions = gmaps.directions(get_lat_lng(A), get_lat_lng(B), 'driving')
    else:
        directions = gmaps.directions(A, B, 'driving')
    dist = directions[0]['legs'][0]['distance']['value']
    duration = directions[0]['legs'][0]['duration']['value']
    return (dist, duration)


@functions_framework.http
def optimize_routes(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)

    if request_json and 'outboundRoutes' in request_json:
        outbuond_routes = request_json['outboundRoutes']
    else:
      outbuond_routes = []
    if request_json and 'inboundRoutes' in request_json:
        inbuond_routes = request_json['inboundRoutes']
    else:
        inbuond_routes = []

    completed = []
    return_couples = []
    for oroute in outbuond_routes:
        A = oroute['from']
        B = oroute['to']
        AB = get_gmaps_distance((A['lat'], A['lng']), (B['lat'], B['lng']), points=False)
        BA = get_gmaps_distance((B['lat'], B['lng']), (A['lat'], A['lng']), points=False)

        date_codes = [inb['from']['code'] for inb in inbuond_routes]

        query = f'''
            WITH StartingPoint AS (
                SELECT ST_GEOGPOINT({B['lng']}, {B['lat']}) as geometry
            )

            select * from {table_id}, StartingPoint
            where ST_DWithin(StartingPoint.geometry, plants.geometry, {BA[0]})
            and code in ({','.join([f'"{a}"' for a in date_codes])})
        '''
        query_job = client.query(query)
        
        query_geometries = [str(c.geometry) for c in query_job]
        
        candidates = [(c['id'], get_gmaps_distance((c["from"]["lat"], c["from"]["lng"]), (A["lat"], A["lng"]), points=False)) for c in inbuond_routes if (any(str(c["from"]["lng"])[:10] in item for item in query_geometries) and any(str(c["from"]["lat"])[:10] in item for item in query_geometries))]
        candidates = [cand for cand in candidates if (cand[0] not in completed and cand[1][0] <= BA[0])]
        
        route_indexes = {str(c['id']): idx for idx, c in enumerate(inbuond_routes)}

        best_emission_cand = {'id': -1, 'opt_emission': -1, 'normal_emission': -1, 'cost_save': 0}

        for cand in candidates:
            cand_route = inbuond_routes[route_indexes[cand[0]]]
            cand_tons = cand_route['cargoWeight']

            if cand_tons > oroute['maxCargoWeight']:
                continue
                        
            vehicle_emission_per_ton_km = oroute['truckEmission']
            vehicle_emission_with_backhauling = oroute['backHauling']
            ab_emission = vehicle_emission_per_ton_km * oroute['cargoWeight'] * AB[0]
            ab_emission_backhauling = vehicle_emission_with_backhauling * oroute['cargoWeight'] * AB[0]
            
            ba_emission = vehicle_emission_per_ton_km * BA[0]
            
            ca_emission = vehicle_emission_per_ton_km * cand_tons * cand[1][0]
            ca_emission_backhauling = vehicle_emission_with_backhauling * cand_tons * cand[1][0]
            BC = get_gmaps_distance((B['lat'], B['lng']), (cand_route['to']['lat'], cand_route['to']['lng']), points=False)
            bc_emission_backhauling = vehicle_emission_with_backhauling * BC[0]

            emission_without_backhauling = ab_emission + ba_emission + ca_emission
            emission_with_cand = ab_emission_backhauling + bc_emission_backhauling + ca_emission_backhauling
            
            best_emission_cand['normal_emission'] = emission_without_backhauling
            if best_emission_cand['opt_emission'] == -1 or (emission_with_cand < best_emission_cand['opt_emission']):
                cand_cost = cand_route['costPerTon'] * cand_tons * 0.25
                best_emission_cand = {'id': cand[0], 'opt_emission': emission_with_cand, 'normal_emission': best_emission_cand['normal_emission'], 'cost_save': cand_cost}
        
        inbound_id = best_emission_cand.pop('id')
        if inbound_id == -1:
            inb = None
        else: 
            inb = [inb for inb in inbuond_routes if inb['id'] == inbound_id]
            if len(inb):
                inb = inb[0]
        return_couples.append({
            'outbound': oroute,
            'inbound': inb,
            'savings': best_emission_cand,
            # 'routes': inbuond_routes,
            # 'candidates': candidates,
            # 'query': query_geometries,
            # 'input_inb': date_codes,
            # 'inboundroutes': inbuond_routes
        })
        completed.append(inbound_id)
    return jsonify(return_couples)