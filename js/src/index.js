import { calculateHexagramFromText, calculateHexagramFromNumbers, getZhugeFromText, getRandomDivination, getCurrentTimeDivination } from './utils.js';
import { getBaziAnalysis, checkMarriageCompatibility } from './bazi.js';
import { ZiweiChart } from './ziwei.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Content-Type': 'application/json'
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: CORS_HEADERS
  });
}

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  const method = request.method;

  if (method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  if (path === '/health' || path === '/api/health') {
    return jsonResponse({ status: 'ok', timestamp: new Date().toISOString(), version: '1.0.0' });
  }

  if (method === 'POST') {
    let body;
    try {
      body = await request.json();
    } catch {
      return jsonResponse({ error: 'Invalid JSON' }, 400);
    }

    if (path === '/divine/text' || path === '/api/divine/text') {
      const result = calculateHexagramFromText(body.text || '', body.focus || 'general');
      return jsonResponse(result);
    }

    if (path === '/divine/zhuge' || path === '/api/divine/zhuge') {
      const result = getZhugeFromText(body.text || '');
      return jsonResponse(result);
    }

    if (path === '/divine/pair' || path === '/api/divine/pair') {
      const result = calculateHexagramFromNumbers(body.num1 || 0, body.num2 || 0);
      return jsonResponse(result);
    }

    if (path === '/divine/ziwei' || path === '/api/divine/ziwei') {
      const chart = new ZiweiChart(
        body.year || 1990,
        body.month || 1,
        body.day || 1,
        body.hour || 12
      );
      return jsonResponse(chart.toJSON());
    }

    if (path === '/divine/bazi' || path === '/api/divine/bazi') {
      const result = getBaziAnalysis(
        body.year || 1990,
        body.month || 1,
        body.day || 1,
        body.hour || 12
      );
      return jsonResponse(result);
    }

    if (path === '/divine/match' || path === '/api/divine/match') {
      const male = getBaziAnalysis(
        body.male_year || 1990,
        body.male_month || 1,
        body.male_day || 1,
        body.male_hour || 12
      );
      const female = getBaziAnalysis(
        body.female_year || 1990,
        body.female_month || 1,
        body.female_day || 1,
        body.female_hour || 12
      );
      const result = checkMarriageCompatibility(male, female);
      return jsonResponse(result);
    }
  }

  if (path === '/divine/random' || path === '/api/divine/random') {
    const result = getRandomDivination();
    return jsonResponse(result);
  }

  if (path === '/divine/current' || path === '/api/divine/current') {
    const result = getCurrentTimeDivination();
    return jsonResponse(result);
  }

  return jsonResponse({ error: 'Not found' }, 404);
}

export default {
  async fetch(request, env, ctx) {
    return handleRequest(request);
  }
};
