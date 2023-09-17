const functions = require('@google-cloud/functions-framework');
const { BigQuery } = require('@google-cloud/bigquery');

functions.http('plants', async (req, res) => {
  const { mapBounds } = req.body;
  const { ne, sw } = mapBounds

  const bigquery = new BigQuery();

  const query = `
    SELECT *, ST_X(ST_Centroid(geometry)) AS lng, ST_Y(ST_Centroid(geometry)) AS lat
    FROM hackzurich23-8233.truck_info.plants
    WHERE ST_Contains(
      ST_GeogFromText('POLYGON((${ne.lng} ${ne.lat}, ${ne.lng} ${sw.lat}, ${sw.lng} ${sw.lat}, ${sw.lng} ${ne.lat}, ${ne.lng} ${ne.lat}))'), 
      geometry
    )
  `;

  const options = {
    query: query,
    timeoutMs: 10000,
    useLegacySql: false
  };

  const [job] = await bigquery.createQueryJob(options);

  const [rows] = await job.getQueryResults();

  res.status(200).send(rows);
});
