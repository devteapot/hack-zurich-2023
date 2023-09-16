import { json } from '@sveltejs/kit';
import functionsBaseURL from '$lib/functionsBaseURL';

export async function GET({ request }) {
  const res = await fetch(`${functionsBaseURL}/plant-locations?limit=100`, { method: "GET", headers: { 'Content-Type': 'application/json' } });
  const data = await res.json()
  return json(data);
}
