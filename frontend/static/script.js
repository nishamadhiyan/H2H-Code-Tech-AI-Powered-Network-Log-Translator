const SAMPLES = {
  brute: `Jun 12 10:23:01 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:03 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:05 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:07 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:09 server sshd[1234]: Failed password for root from 192.168.1.105 port 22`,

  ddos: `Jun 12 11:00:01 server kernel: WARNING flood detected from 45.33.32.156
Jun 12 11:00:02 server firewall: DENIED TCP 45.33.32.156 -> 192.168.1.1 port 80
Jun 12 11:00:03 server nginx: rate limit exceeded for 45.33.32.156
Jun 12 11:00:04 server kernel: DDoS attack detected bandwidth exceeded
Jun 12 11:00:05 server firewall: DROPPED UDP 45.33.32.156 -> 192.168.1.1`,

  memory: `Jun 12 12:00:01 server kernel: WARNING memory usage exceeded 90% threshold
Jun 12 12:00:05 server kernel: CRITICAL memory usage exceeded 95% threshold
Jun 12 12:00:10 server kernel: ERROR out of memory killing process nginx
Jun 12 12:00:15 server kernel: CRITICAL RAM overflow detected
Jun 12 12:00:20 server app: fatal memory allocation failed`
};

function loadSample(type) {
  document.getElementById('logInput').value = SAMPLES[type];
}

async function analyzeLogs() {
  const logText = document.getElementById('logInput').value.trim();
  const fileInput = document.getElementById('fileInput');
  const btnText = document.getElementById('btnText');
  const btnLoader = document.getElementById('btnLoader');
  const btn = document.getElementById('analyzeBtn');

  if (!logText && fileInput.files.length === 0) {
    alert('Please paste logs or upload a file.');
    return;
  }

  btnText.classList.add('hidden');
  btnLoader.classList.remove('hidden');
  btn.disabled = true;

  try {
    let data;
    if (fileInput.files.length > 0) {
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);
      const res = await fetch('/analyze-file', { method: 'POST', body: formData });
      data = await res.json();
    } else {
      const formData = new FormData();
      formData.append('log_text', logText);
      const res = await fetch('/analyze', { method: 'POST', body: formData });
      data = await res.json();
    }
    renderResults(data);
  } catch (err) {
    alert('Error: ' + err.message);
  } finally {
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
    btn.disabled = false;
  }
}

function renderResults(data) {
  const ai = data.ai_analysis;
  const parsed = data.parsed;

  document.getElementById('results').classList.remove('hidden');

  // Show chart
  renderChart(parsed.severity_counts);
  
  // Store logs for chat
  currentLogs = parsed.parsed_lines.map(p => p.line).join('\n');
  document.getElementById('chatSection').classList.remove('hidden');

  const sev = ai.severity_assessment || 'UNKNOWN';
  const badge = document.getElementById('severityBadge');
  badge.textContent = `⚡ Severity: ${sev}`;
  badge.className = `severity-badge sev-${sev}`;

  document.getElementById('plainEnglish').textContent = ai.plain_english_summary || '—';

  const sc = parsed.severity_counts;
  document.getElementById('statsGrid').innerHTML = `
    <div class="stat-box"><div class="stat-num">${parsed.total_lines}</div><div class="stat-label">Total Lines</div></div>
    <div class="stat-box"><div class="stat-num" style="color:#ff3860">${sc.CRITICAL || 0}</div><div class="stat-label">Critical</div></div>
    <div class="stat-box"><div class="stat-num" style="color:#ff6b35">${sc.ERROR || 0}</div><div class="stat-label">Errors</div></div>
    <div class="stat-box"><div class="stat-num" style="color:#ffdd57">${sc.WARNING || 0}</div><div class="stat-label">Warnings</div></div>
    <div class="stat-box"><div class="stat-num" style="color:#23d160">${sc.INFO || 0}</div><div class="stat-label">Info</div></div>
  `;

  const anomalies = [...new Set([
    ...(parsed.anomalies_detected || []),
    ...(ai.anomalies || [])
  ])];
  document.getElementById('anomalyList').innerHTML = anomalies.length
    ? anomalies.map(a => `<li>${a}</li>`).join('')
    : '<li>No anomalies detected</li>';

  document.getElementById('patternSummary').textContent = ai.pattern_summary || '—';

  document.getElementById('keyEvents').innerHTML =
    (ai.key_events || []).map(e => `<li>${e}</li>`).join('') || '<li>—</li>';

  document.getElementById('suggestions').innerHTML =
    (ai.suggested_actions || []).map(s => `<li>${s}</li>`).join('') || '<li>—</li>';

  const logLinesDiv = document.getElementById('logLines');
  logLinesDiv.innerHTML = (parsed.parsed_lines || []).map(item => `
    <div class="log-line log-${item.severity}" onclick="explainLine(this, '${item.line.replace(/'/g, "\\'")}')">
      <span>[${item.severity}]</span> ${item.line}
    </div>
  `).join('');

  document.getElementById('results').scrollIntoView({ behavior: 'smooth' });

  window._lastData = data;
}

async function explainLine(el, line) {
  el.innerHTML += ' <span style="color:#00d4ff">⏳ explaining...</span>';
  const formData = new FormData();
  formData.append('log_line', line);
  const res = await fetch('/explain-line', { method: 'POST', body: formData });
  const data = await res.json();
  el.innerHTML = `<span style="color:#00d4ff">💡 ${data.explanation}</span>`;
}

function exportReport() {
  const data = window._lastData;
  if (!data) return;
  const ai = data.ai_analysis;
  const parsed = data.parsed;
  const report = `
AI NETWORK LOG TRANSLATOR — REPORT
====================================
Severity: ${ai.severity_assessment}
Total Lines: ${parsed.total_lines}

SUMMARY
-------
${ai.plain_english_summary}

ANOMALIES
---------
${(ai.anomalies || []).join('\n')}

PATTERN SUMMARY
---------------
${ai.pattern_summary}

KEY EVENTS
----------
${(ai.key_events || []).join('\n')}

SUGGESTED ACTIONS
-----------------
${(ai.suggested_actions || []).join('\n')}
  `.trim();

  const blob = new Blob([report], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'network-log-report.txt';
  a.click();
}
// ── Chart.js severity chart ──
function renderChart(sc) {
  const existing = document.getElementById('severityChart');
  if (existing) existing.remove();

  const statsGrid = document.getElementById('statsGrid');
  const canvas = document.createElement('canvas');
  canvas.id = 'severityChart';
  canvas.style.marginTop = '1.5rem';
  canvas.style.maxHeight = '200px';
  statsGrid.after(canvas);

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: ['Critical', 'Error', 'Warning', 'Info', 'Unknown'],
      datasets: [{
        label: 'Log Count',
        data: [
          sc.CRITICAL || 0,
          sc.ERROR || 0,
          sc.WARNING || 0,
          sc.INFO || 0,
          sc.UNKNOWN || 0
        ],
        backgroundColor: [
          'rgba(255,56,96,0.7)',
          'rgba(255,107,53,0.7)',
          'rgba(255,221,87,0.7)',
          'rgba(35,209,96,0.7)',
          'rgba(74,96,128,0.7)'
        ],
        borderColor: [
          '#ff3860','#ff6b35','#ffdd57','#23d160','#4a6080'
        ],
        borderWidth: 1,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: { ticks: { color: '#4a6080' }, grid: { color: '#1e3a5f' } },
        y: { ticks: { color: '#4a6080' }, grid: { color: '#1e3a5f' }, beginAtZero: true }
      }
    }
  });
}

// ── Chat with logs ──
let currentLogs = '';

async function sendChat() {
  const input = document.getElementById('chatInput');
  const question = input.value.trim();
  if (!question) return;

  addChatMsg(question, 'user');
  input.value = '';
  addChatMsg('🤖 Thinking...', 'bot', 'thinking');

  const formData = new FormData();
  formData.append('question', question);
  formData.append('log_context', currentLogs);

  const res = await fetch('/chat', { method: 'POST', body: formData });
  const data = await res.json();

  const thinking = document.querySelector('.thinking');
  if (thinking) thinking.remove();
  addChatMsg(data.answer, 'bot');
}

function askSuggestion(btn) {
  document.getElementById('chatInput').value = btn.textContent;
  sendChat();
}

function addChatMsg(text, type, cls = '') {
  const messages = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = `chat-msg ${type}-msg ${cls}`;
  const icon = type === 'bot' ? '🤖' : '👤';
  div.innerHTML = `<span>${icon}</span><span>${text}</span>`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}