const functions = require('@google-cloud/functions-framework');
const { BigQuery } = require('@google-cloud/bigquery');

functions.http('add-plant', async (req, res) => {
  const newPlant = req.body;

  const bigquery = new BigQuery();

  await bigquery
    .dataset("truck_info")
    .table("plants")
    .insert([newPlant]);

  res.status(200);
});
