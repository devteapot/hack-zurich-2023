import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  const requestBody = await request.json()

  const res = await fetch(
    `https://europe-west6-hackzurich23-8233.cloudfunctions.net/optimize-routes`,
    {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    }
  );

  return json(await res.json());
}
