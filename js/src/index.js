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

  if (path === '/' || path === '') {
    return new Response(`<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>周易占卜系统</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; color: #fff; }
    .container { max-width: 800px; margin: 0 auto; padding: 20px; }
    h1 { text-align: center; padding: 30px 0; font-size: 2.5em; background: linear-gradient(90deg, #f39c12, #e74c3c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .api-list { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin: 20px 0; }
    .api-item { padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .api-item:last-child { border-bottom: none; }
    .api-path { color: #f39c12; font-family: monospace; font-size: 1.1em; }
    .api-desc { color: #aaa; margin-top: 5px; }
    .status { text-align: center; padding: 20px; color: #2ecc71; }
  </style>
</head>
<body>
  <div class="container">
    <h1>☯ 周易占卜系统</h1>
    <div class="status">✅ 系统运行正常</div>
    <div class="api-list">
      <h3 style="margin-bottom:15px;color:#f39c12;">API 端点</h3>
      <div class="api-item">
        <div class="api-path">GET /health</div>
        <div class="api-desc">健康检查</div>
      </div>
      <div class="api-item">
        <div class="api-path">POST /divine/text</div>
        <div class="api-desc">文字起卦 - 参数: text, focus</div>
      </div>
      <div class="api-item">
        <div class="api-path">POST /divine/bazi</div>
        <div class="api-desc">八字分析 - 参数: year, month, day, hour</div>
      </div>
      <div class="api-item">
        <div class="api-path">POST /divine/ziwei</div>
        <div class="api-desc">紫微斗数 - 参数: year, month, day, hour</div>
      </div>
      <div class="api-item">
        <div class="api-path">GET /divine/random</div>
        <div class="api-desc">随机占卜</div>
      </div>
    </div>
  </div>
</body>
</html>`, {
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  }

  if (path === '/health' || path === '/api/health') {
    return jsonResponse({ status: 'ok', timestamp: new Date().toISOString(), version: '1.0.0' });
  }

  async function getParams() {
    if (method === 'POST') {
      try {
        return await request.json();
      } catch {
        return {};
      }
    } else {
      const params = {};
      url.searchParams.forEach((value, key) => {
        params[key] = isNaN(value) ? value : parseInt(value);
      });
      return params;
    }
  }

  if (path === '/divine/text' || path === '/api/divine/text') {
    const body = await getParams();
    const result = calculateHexagramFromText(body.text || '占卜', body.focus || 'general');
    return jsonResponse(result);
  }

  if (path === '/divine/zhuge' || path === '/api/divine/zhuge') {
    const body = await getParams();
    const result = getZhugeFromText(body.text || '诸葛神数');
    return jsonResponse(result);
  }

  if (path === '/divine/pair' || path === '/api/divine/pair') {
    const body = await getParams();
    const result = calculateHexagramFromNumbers(body.num1 || 1, body.num2 || 2);
    return jsonResponse(result);
  }

  if (path === '/divine/ziwei' || path === '/api/divine/ziwei') {
    const body = await getParams();
    const chart = new ZiweiChart(
      body.year || 1990,
      body.month || 1,
      body.day || 1,
      body.hour || 12
    );
    return jsonResponse(chart.toJSON());
  }

  if (path === '/divine/bazi' || path === '/api/divine/bazi') {
    const body = await getParams();
    const result = getBaziAnalysis(
      body.year || 1990,
      body.month || 1,
      body.day || 1,
      body.hour || 12
    );
    return jsonResponse(result);
  }

  if (path === '/divine/match' || path === '/api/divine/match') {
    const body = await getParams();
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

  if (path === '/divine/random' || path === '/api/divine/random') {
    const result = getRandomDivination();
    return jsonResponse(result);
  }

  if (path === '/divine/current' || path === '/api/divine/current') {
    const result = getCurrentTimeDivination();
    return jsonResponse(result);
  }

  return jsonResponse({ error: 'Not found', hint: 'Use GET with query params or POST with JSON body' }, 404);
}

export default {
  async fetch(request, env, ctx) {
    return handleRequest(request);
  }
};
