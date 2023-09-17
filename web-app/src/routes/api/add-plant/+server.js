import { json } from '@sveltejs/kit';
import functionsBaseURL from '$lib/functionsBaseURL';

export async function POST({ request }) {
  const requestBody = await request.json()

  const res = await fetch(
    `${functionsBaseURL}/add-plant`,
    {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    }
  );

  return json(await res.json());
}
