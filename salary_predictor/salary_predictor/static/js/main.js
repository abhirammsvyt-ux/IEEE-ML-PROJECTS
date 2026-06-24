/* ── Pill groups ─────────────────────────────────────────────── */
document.querySelectorAll('.pill-group').forEach(group => {
  group.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', () => {
      pill.closest('.pill-group').querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
    });
  });
});

/* ── Remote slider ───────────────────────────────────────────── */
const slider   = document.getElementById('remote_ratio');
const remoteVal = document.getElementById('remote_val');
slider.addEventListener('input', () => {
  remoteVal.textContent = slider.value + '%';
  const pct = (slider.value / slider.max) * 100;
  slider.style.background =
    `linear-gradient(to right, var(--accent) 0%, var(--accent) ${pct}%, var(--border) ${pct}%, var(--border) 100%)`;
});

/* ── Helpers ─────────────────────────────────────────────────── */
const fmt = n => '$' + Math.round(n).toLocaleString('en-US');

function getSelected(name) {
  const el = document.querySelector(`input[name="${name}"]:checked`);
  return el ? el.value : null;
}

/* ── Predict ─────────────────────────────────────────────────── */
const btn      = document.getElementById('btn_predict');
const btnText  = btn.querySelector('.btn-text');
const btnLoad  = btn.querySelector('.btn-loader');
const errMsg   = document.getElementById('error_msg');

const resultPlaceholder = document.getElementById('result_placeholder');
const resultContent     = document.getElementById('result_content');
const annualEl          = document.getElementById('result_annual');
const monthlyEl         = document.getElementById('result_monthly');
const weeklyEl          = document.getElementById('result_weekly');
const metaEl            = document.getElementById('result_meta');
const confFill          = document.getElementById('conf_fill');

btn.addEventListener('click', async () => {
  errMsg.hidden = true;

  const payload = {
    work_year:        document.getElementById('work_year').value,
    experience_level: getSelected('experience_level'),
    employment_type:  getSelected('employment_type'),
    company_size:     getSelected('company_size'),
    job_title:        document.getElementById('job_title').value,
    remote_ratio:     slider.value,
  };

  if (!payload.experience_level || !payload.employment_type || !payload.company_size) {
    showError('Please select all options before predicting.');
    return;
  }

  // loading state
  btnText.hidden = true;
  btnLoad.hidden = false;
  btn.disabled   = true;

  try {
    const res  = await fetch('/predict', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok || data.error) {
      showError(data.error || 'Prediction failed — check the server logs.');
      return;
    }

    // populate result
    annualEl.textContent  = fmt(data.annual);
    monthlyEl.textContent = fmt(data.monthly);
    weeklyEl.textContent  = fmt(data.weekly);

    const expLabel  = document.querySelector(`input[name="experience_level"]:checked`)?.closest('.pill')?.querySelector('.pill-label')?.textContent;
    const empLabel  = document.querySelector(`input[name="employment_type"]:checked`)?.closest('.pill')?.querySelector('.pill-label')?.textContent;
    const compLabel = document.querySelector(`input[name="company_size"]:checked`)?.closest('.pill')?.querySelector('.pill-label')?.textContent;

    metaEl.textContent =
      `Role       : ${payload.job_title}\n` +
      `Experience : ${expLabel || payload.experience_level}\n` +
      `Employment : ${empLabel || payload.employment_type}\n` +
      `Company    : ${compLabel || payload.company_size}\n` +
      `Remote     : ${payload.remote_ratio}%\n` +
      `Year       : ${payload.work_year}`;

    // animate confidence bar (visual, not real CI)
    confFill.style.width = '0%';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { confFill.style.width = '82%'; });
    });

    // show
    resultPlaceholder.hidden = true;
    resultContent.hidden     = false;

  } catch (err) {
    showError('Network error — is the Flask server running?');
  } finally {
    btnText.hidden = false;
    btnLoad.hidden = true;
    btn.disabled   = false;
  }
});

function showError(msg) {
  errMsg.textContent = msg;
  errMsg.hidden = false;
}
