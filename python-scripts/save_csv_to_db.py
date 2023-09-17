import pandas as pd
import firebase_admin
from firebase_admin import firestore
from sys import maxsize
from itertools import permutations

V = 4
AVG_VEL = 50
MAX_TIME = 10
SLEEP = 8


def get_firebase_db():
    cred_obj = firebase_admin.credentials.Certificate('hack-zurich-2023-firebase-adminsdk-954o6-6d83532ec1.json')
    default_app = firebase_admin.initialize_app(cred_obj)
    
    db = firestore.client()
    return db


def price_to_float(x):
    if x == '-':
        return 0
    x = float(remove_aposto(str(x).split()[-1]))
    return x


def remove_aposto(x):
    return float(str(x).replace('\'', ''))


def get_data(country, dir):
    filename = f'csv/{dir}bound {country}-Table 1.csv'
    df = pd.read_csv(filename)
    df['Freight Cost Per Ton [$/ton]'] = df['Freight Cost Per Ton [$/ton]'].apply(price_to_float)
    df['Distance [km]'] = df['Distance [km]'].apply(remove_aposto)
    return df


def get_col_rename(old, new):
    return {col: new[i] for i, col in enumerate(old)}


def aggregate_plnts(df, dir):
    final_cols = ['code', 'plant', 'lat', 'long']
    trio_final_cols = ['code', 'lat', 'long']
    if dir == 'In':
        origin_cols = ['Origin Code', 'Origin', 'Origin Latitude', 'Origin Longitude']
        dest_cols = ['Destination Code', 'Destination', 'Destination Latitude', 'Destination Longitude']
        new_cols = get_col_rename(dest_cols, final_cols)
        dest_df = df[dest_cols].drop_duplicates().rename(columns=new_cols)
    else:
        origin_cols = ['Plant', 'Plant Name', 'Plant Latitude', 'Plant Longitude']
        dest_cols = ['Client Code', 'Client Latitude', 'Client Longitude']
        new_cols = get_col_rename(dest_cols, trio_final_cols)
        dest_df = df[dest_cols].drop_duplicates().rename(columns=new_cols)
    new_cols = get_col_rename(origin_cols, final_cols)
    origin_df = df[origin_cols].drop_duplicates().rename(columns=new_cols)
    all_plants = pd.concat([origin_df, dest_df])
    return all_plants


def cook(db, all_plants):
    batch = db.batch()
    plants_ref = db.collection('plants')
    
    for _, row in all_plants.iterrows():
        new_plant = plants_ref.document()
        batch.set(new_plant, row.to_dict())
    
    batch.commit()


def main():
    db = get_firebase_db()
    
    in_arg = get_data('ARG', 'In')
    all_plants = aggregate_plnts(in_arg, 'In')
    cook(db, all_plants)
    
    out_arg = get_data('ARG', 'Out')
    all_plants = aggregate_plnts(out_arg, 'Out')
    cook(db, all_plants)
    
    in_mex = get_data('MEX', 'In')
    all_plants = aggregate_plnts(in_mex, 'In')
    cook(db, all_plants)
    
    out_mex = get_data('MEX', 'Out')
    all_plants = aggregate_plnts(out_mex, 'Out')
    cook(db, all_plants)

 
# implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, s):
 
    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)
 
    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:
 
        # store current Path weight(cost)
        current_pathweight = 0
 
        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]
 
        # update minimum
        min_path = min(min_path, current_pathweight)
         
    return min_path


if __name__ == '__main__':
    main()
    # matrix representation of graph
    graph = [[0, 10, 15, 20], [10, 0, 35, 25],
            [15, 35, 0, 30], [20, 25, 30, 0]]
    s = 0
    print(travellingSalesmanProblem(graph, s))
