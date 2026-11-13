// Photo-to-fighter: draws one 3-row chunk of a fighter sprite sheet with Cloudflare Workers AI.
// The photo is forwarded once to Cloudflare and never written anywhere by this function.
const fs = require('fs');
const path = require('path');

const MODEL = '@cf/black-forest-labs/flux-2-klein-4b';
const OUTFITS = [
  'a plain {c} t-shirt, blue jeans and white sneakers',
  'a {c} zip-up track jacket, black track pants and white sneakers',
  'a {c} hoodie, grey cargo pants and white sneakers',
  'a {c} leather jacket, dark blue jeans and brown boots',
  'a {c} karate jacket with a black belt, white karate pants and white shoes',
];
const COLOURS = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'black', 'white'];
const BASE = 'Retro arcade pixel art sprite sheet with a plain white background. Keep exactly the same grid layout, the same poses, the same positions, the same size and the same detailed pixel art style as the first image, with empty white margins around it. ';
const MAX_REF = 1.6e6; // bytes of base64

// best-effort limiter per warm instance (the Cloudflare free tier is the real cap)
const hits = new Map();
function limited(ip) {
  const now = Date.now(), h = (hits.get(ip) || []).filter(t => now - t < 3600e3);
  h.push(now); hits.set(ip, h);
  return h.length > 24; // 6 fighters an hour per address
}

function layout(k) {
  return fs.readFileSync(path.join(__dirname, 'layout', 'sp' + k + '.png'));
}

function decodeRef(s) {
  const m = /^data:image\/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)$/.exec(s || '');
  if (!m || m[2].length > MAX_REF) return null;
  return { type: 'image/' + m[1], buf: Buffer.from(m[2], 'base64') };
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ error: 'method' });
  const acct = process.env.CF_ACCOUNT_ID, tok = process.env.CF_AI_TOKEN;
  if (!acct || !tok) return res.status(503).json({ error: 'off' });
  const origin = req.headers.origin || '';
  if (origin && !/^https:\/\/columbus-clash[\w-]*\.vercel\.app$|^http:\/\/localhost(:\d+)?$/.test(origin)) return res.status(403).json({ error: 'origin' });
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'x';
  if (limited(ip)) return res.status(429).json({ error: 'busy' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body) return res.status(400).json({ error: 'body' });
  const k = Number(body.k), o = Number(body.o), c = Number(body.c);
  if (![0, 1, 2, 3].includes(k) || !OUTFITS[o] || !COLOURS[c]) return res.status(400).json({ error: 'args' });
  const ref = decodeRef(body.ref);
  if (!ref) return res.status(400).json({ error: 'ref' });

  const outfit = OUTFITS[o].replace('{c}', COLOURS[c]);
  const prompt = BASE + (k === 0
    ? 'Replace the character in every frame with a fighter who looks like the person in the second image: the same face, hairstyle, facial hair and skin tone, wearing ' + outfit + '. Draw only one character per frame. No red jacket.'
    : 'Replace the character in every frame with the character shown in the second image, with exactly the same face, hair, clothes and colours (' + outfit + '). No red jacket.');

  const form = new FormData();
  form.append('prompt', prompt);
  form.append('input_image_0', new Blob([layout(k)], { type: 'image/png' }), 'layout.png');
  form.append('input_image_1', new Blob([ref.buf], { type: ref.type }), 'ref');
  form.append('width', '1536');
  form.append('height', '768');
  try {
    const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + acct + '/ai/run/' + MODEL, {
      method: 'POST', headers: { Authorization: 'Bearer ' + tok }, body: form,
    });
    const j = await r.json().catch(() => ({}));
    const img = j && j.result && j.result.image;
    if (img) return res.status(200).json({ img: 'data:image/png;base64,' + img });
    const msg = JSON.stringify(j.errors || '').toLowerCase();
    if (msg.includes('flagged')) return res.status(422).json({ error: 'flagged' });
    if (r.status === 429 || msg.includes('neuron') || msg.includes('quota') || msg.includes('limit')) return res.status(429).json({ error: 'limit' });
    return res.status(502).json({ error: 'ai' });
  } catch (e) {
    return res.status(502).json({ error: 'net' });
  }
};
