#!/usr/bin/env python3
"""
Replace hero iframes and #form iframes across all Noranda Service Centre pages.

Change 1: Replace hero-right block (including orphaned form fields where present)
          with a simple CTA button.
Change 2: Replace the #form section iframe wrapper with the inlined booking form.
"""

import re
import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = '/Volumes/KINGSTON/noranda-service-centre'

FILES = [
    'index.html',
    'car-repair/index.html',
    'general-repairs/index.html',
    '4x4-mechanic/index.html',
    '4x4-mechanic-weekend/index.html',
    'ac-repair/index.html',
    'ac-heater-repair-call/index.html',
    'car-emergency-repair-weekend/index.html',
    'car-repair-weekend/index.html',
    'car-servicing-weekend/index.html',
    'nissan-repair/index.html',
    'bmw/index.html',
    'audi/index.html',
]

# ---------------------------------------------------------------------------
# Replacement strings
# ---------------------------------------------------------------------------

HERO_CTA_REPLACEMENT = '''      <div class="hero-right">
        <div class="hero-form-card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 32px;gap:20px;">
          <h3 style="margin-bottom:0;">Book a Service</h3>
          <p style="font-size:0.9rem;color:#666;margin-bottom:0;">Mon–Fri 8:00am–4:30pm  ·  08 9376 1155</p>
          <a href="#form" class="btn btn-red" style="width:100%;font-size:1rem;padding:14px 20px;margin-top:8px;">Book Online &rarr;</a>
          <p style="font-size:0.85rem;color:#aaa;">Or call <a href="tel:0893761155" style="color:var(--nsc-red);font-weight:600;">08 9376 1155</a></p>
        </div>
      </div>
    </div>
  </div>
</section>'''

FORM_EMBED = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- WhatConverts -->
<script>var $wc_load=function(a){return JSON.parse(JSON.stringify(a))},$wc_leads=$wc_leads||{doc:{url:$wc_load(document.URL),ref:$wc_load(document.referrer),search:$wc_load(location.search),hash:$wc_load(location.hash)}};</script>
<script src="//s.ksrndkehqnwntyxlhgto.com/155600.js"></script>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

<style>
.ns-booking-form *, .ns-booking-form *::before, .ns-booking-form *::after {
  box-sizing: border-box; margin: 0; padding: 0;
}
.ns-booking-form {
  --red: #cc0000;
  --green: #a7cd0c;
  --black: #000000;
  --white: #ffffff;
  font-family: Arial, Helvetica, sans-serif;
  color: var(--black);
  background: var(--white);
  width: 100%;
  padding-bottom: 48px;
}
.ns-booking-form .ns-hero {
  background: var(--red);
  padding: 28px 28px 22px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.ns-booking-form .ns-hero::after {
  content: \'\';
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: 130px;
  background: repeating-linear-gradient(90deg, transparent 0px, transparent 8px, rgba(0,0,0,0.08) 8px, rgba(0,0,0,0.08) 10px);
  pointer-events: none;
}
.ns-booking-form .ns-hero h2 {
  font-family: Roboto, Arial, Helvetica, sans-serif !important;
  font-size: 38px !important;
  font-weight: 700 !important;
  line-height: 1.1 !important;
  color: #fff !important;
  margin-bottom: 8px !important;
  text-transform: uppercase !important;
  position: relative;
  z-index: 1;
  border: none !important;
  padding: 0 !important;
}
.ns-booking-form .ns-hero p {
  font-size: 13px;
  color: #fff;
  opacity: 0.75;
  position: relative;
  z-index: 1;
}
.ns-booking-form .ns-body { padding: 0 28px; }
.ns-booking-form .ns-section {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--green);
  margin: 24px 0 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: Roboto, Arial, sans-serif;
}
.ns-booking-form .ns-section::after {
  content: \'\';
  flex: 1;
  height: 1px;
  background: var(--black);
  opacity: 0.15;
}
.ns-booking-form .ns-grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
.ns-booking-form .ns-full  { display: grid; grid-template-columns: 1fr; gap: 12px; margin-bottom: 12px; }
@media (max-width: 600px) {
  .ns-booking-form .ns-grid2 { grid-template-columns: 1fr; }
}
.ns-booking-form .ns-field { display: flex; flex-direction: column; gap: 5px; }
.ns-booking-form .ns-field label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--black);
  font-family: Arial, Helvetica, sans-serif;
}
.ns-booking-form .ns-field label .req { color: var(--red); margin-left: 2px; }
.ns-booking-form .ns-field input,
.ns-booking-form .ns-field select,
.ns-booking-form .ns-field textarea {
  background: var(--white);
  border: 2px solid var(--black);
  border-radius: 0;
  color: var(--black);
  font-size: 14px;
  font-family: Arial, Helvetica, sans-serif;
  padding: 9px 11px;
  -webkit-appearance: none;
  appearance: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  width: 100%;
}
.ns-booking-form .ns-field select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'8\' viewBox=\'0 0 12 8\'%3E%3Cpath d=\'M1 1l5 5 5-5\' stroke=\'%23000\' stroke-width=\'2\' fill=\'none\' stroke-linecap=\'round\'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
  cursor: pointer;
}
.ns-booking-form .ns-field input:focus,
.ns-booking-form .ns-field select:focus,
.ns-booking-form .ns-field textarea:focus {
  outline: none;
  border-color: var(--red);
  box-shadow: 0 0 0 3px rgba(204,0,0,0.12);
}
.ns-booking-form .ns-field input.invalid,
.ns-booking-form .ns-field select.invalid,
.ns-booking-form .ns-field textarea.invalid { border-color: var(--red); }
.ns-booking-form .ns-field input::placeholder,
.ns-booking-form .ns-field textarea::placeholder { color: #aaa; }
.ns-booking-form .ns-field textarea { resize: vertical; min-height: 80px; }
.ns-booking-form .ns-note {
  background: #f9f9f9;
  border-left: 3px solid var(--red);
  padding: 10px 14px;
  font-size: 12px;
  color: #555;
  margin-top: 4px;
  margin-bottom: 12px;
}
.ns-booking-form .ns-submit {
  width: 100%;
  background: var(--red);
  border: none;
  border-radius: 0;
  color: var(--white);
  font-family: Roboto, Arial, sans-serif;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.08em;
  padding: 16px;
  cursor: pointer;
  margin-top: 24px;
  text-transform: uppercase;
  transition: background 0.15s;
  display: block;
}
.ns-booking-form .ns-submit:hover { background: #aa0000; }
.ns-booking-form .ns-submit:disabled { background: #aaa; cursor: not-allowed; }
.ns-booking-form .ns-disclaimer {
  font-size: 11px;
  color: #888;
  text-align: center;
  margin-top: 12px;
}
.ns-booking-form .ns-hint {
  font-size: 12px;
  color: var(--red);
  margin-top: 4px;
  line-height: 1.4;
}
.ns-booking-form .ns-error {
  display: none;
  color: var(--red);
  font-size: 13px;
  margin-top: 12px;
  padding: 10px 14px;
  background: #f9f9f9;
  border-left: 3px solid var(--red);
}
</style>

<div class="ns-booking-form">

  <div class="ns-hero">
    <h2>Book a Service</h2>
    <p>Mon&ndash;Fri 8:00am&ndash;4:30pm &nbsp;&middot;&nbsp; 08 9376 1155</p>
  </div>

  <form id="ns-enfold-form">
    <div class="ns-body">

      <div class="ns-section">Your details</div>
      <div class="ns-grid2">
        <div class="ns-field">
          <label>Full name <span class="req">*</span></label>
          <input type="text" name="customer_name" id="ns-customer_name" placeholder="e.g. Sarah Smith" required />
        </div>
        <div class="ns-field">
          <label>Phone <span class="req">*</span></label>
          <input type="tel" name="customer_phone" id="ns-customer_phone" placeholder="04xx xxx xxx" required />
        </div>
      </div>
      <div class="ns-full">
        <div class="ns-field">
          <label>Email <span class="req">*</span></label>
          <input type="email" name="customer_email" id="ns-customer_email" placeholder="your@email.com" required />
        </div>
      </div>

      <div class="ns-section">Vehicle details</div>
      <div class="ns-full">
        <div class="ns-field">
          <label>Registration <span class="req">*</span></label>
          <input type="text" name="registration" id="ns-registration" placeholder="e.g. 1ABC123" required style="text-transform: uppercase;" />
        </div>
      </div>

      <div class="ns-section">Service required</div>
      <div class="ns-full" style="margin-bottom:12px">
        <div class="ns-field">
          <label>Service type <span class="req">*</span></label>
          <select name="service_type" id="ns-service_type" required>
            <option value="" disabled selected>&#8212; Select a service &#8212;</option>
            <option>Logbook Service</option>
            <option>Roadworthy / Safety Inspection</option>
            <option>Brakes</option>
            <option>Steering &amp; Suspension</option>
            <option>Exhaust Repairs &amp; Replacement</option>
            <option>Air Conditioning</option>
            <option>Clutch &amp; Transmission</option>
            <option>Engine Repairs</option>
            <option>Cooling System</option>
            <option>Auto Electrical</option>
            <option>Tyres</option>
            <option>Windscreen</option>
            <option>Other</option>
          </select>
        </div>
      </div>
      <div class="ns-full">
        <div class="ns-field">
          <label>Notes / description</label>
          <textarea name="notes" id="ns-notes" placeholder="Describe the issue or anything we should know..."></textarea>
        </div>
      </div>

      <div class="ns-section">Preferred booking time</div>
      <div class="ns-grid2">
        <div class="ns-field">
          <label>Preferred date <span class="req">*</span></label>
          <input type="date" name="preferred_date" id="ns-preferred_date" required />
          <p class="ns-hint" id="ns-hint-date"></p>
        </div>
        <div class="ns-field">
          <label>Preferred time <span class="req">*</span></label>
          <select name="preferred_time" id="ns-preferred_time" required>
            <option value="" disabled selected>&#8212; Select &#8212;</option>
            <option>Morning (8am&ndash;12pm)</option>
            <option>Afternoon (12pm&ndash;4:30pm)</option>
            <option>Either</option>
          </select>
        </div>
      </div>
      <div class="ns-note">
        Preferred times are a request only &mdash; we&rsquo;ll confirm your actual slot by phone or email within 1 business day.
      </div>

      <button type="submit" class="ns-submit" id="ns-enfold-submit">Submit Booking Request &rarr;</button>
      <p class="ns-disclaimer">By submitting you agree to be contacted regarding your booking request.</p>
      <p class="ns-error" id="ns-enfold-error">Something went wrong. Please call us on <strong>08 9376 1155</strong> or try again.</p>

    </div>
  </form>

</div>

<script>
(function() {
  var SUPABASE_URL      = 'https://prqbvbhuwfpdkkrkqizj.supabase.co';
  var SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBycWJ2Ymh1d2ZwZGtrcmtxaXpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5OTA1MzQsImV4cCI6MjA5MjU2NjUzNH0.Io5IHsyp23yThoyZD7Ccs4UygTtwx_0rIRTlnS3pYZQ';

  var sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  var dateInput = document.getElementById('ns-preferred_date');
  var hintDate  = document.getElementById('ns-hint-date');

  if (dateInput) dateInput.min = new Date().toISOString().split('T')[0];

  function getLocalDateString() {
    var now = new Date();
    return now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0');
  }

  function updateHints() {
    var dateVal = dateInput ? dateInput.value : '';
    if (hintDate) hintDate.textContent = '';
    if (!dateVal) return;
    var parts    = dateVal.split('-');
    var selected = new Date(parts[0], parts[1] - 1, parts[2]);
    var dow      = selected.getDay();
    if (dow === 0 || dow === 6) {
      if (hintDate) hintDate.textContent = "We're closed on weekends — we'll contact you to arrange a suitable date.";
      return;
    }
    if (dateVal === getLocalDateString()) {
      if (hintDate) hintDate.textContent = "Same-day bookings are subject to availability — call us on 08 9376 1155 to confirm we can fit you in today.";
    }
  }

  if (dateInput) dateInput.addEventListener('change', updateHints);

  var form      = document.getElementById('ns-enfold-form');
  var submitBtn = document.getElementById('ns-enfold-submit');
  var errorMsg  = document.getElementById('ns-enfold-error');

  var requiredFields = ['ns-customer_name', 'ns-customer_email', 'ns-customer_phone', 'ns-registration', 'ns-service_type', 'ns-preferred_date', 'ns-preferred_time'];

  function validate() {
    var valid = true;
    requiredFields.forEach(function(id) {
      var el    = document.getElementById(id);
      var empty = !el.value.trim();
      el.classList.toggle('invalid', empty);
      if (empty) valid = false;
    });
    var emailEl = document.getElementById('ns-customer_email');
    if (emailEl.value && !emailEl.value.includes('@')) {
      emailEl.classList.add('invalid');
      valid = false;
    }
    return valid;
  }

  requiredFields.forEach(function(id) {
    document.getElementById(id).addEventListener('input', function() {
      this.classList.remove('invalid');
    });
  });

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (!validate()) return;

    submitBtn.disabled    = true;
    submitBtn.textContent = 'Sending...';
    errorMsg.style.display = 'none';

    var payload = {
      customer_name:  document.getElementById('ns-customer_name').value.trim(),
      customer_email: document.getElementById('ns-customer_email').value.trim(),
      customer_phone: document.getElementById('ns-customer_phone').value.trim(),
      registration:   document.getElementById('ns-registration').value.toUpperCase(),
      service_type:   document.getElementById('ns-service_type').value,
      preferred_date: document.getElementById('ns-preferred_date').value,
      preferred_time: document.getElementById('ns-preferred_time').value,
      notes:          document.getElementById('ns-notes').value.trim() || null,
    };

    sb.from('noranda_bookings').insert([payload]).then(function(result) {
      if (result.error) {
        console.error(result.error);
        errorMsg.style.display = 'block';
        submitBtn.disabled     = false;
        submitBtn.textContent  = 'Submit Booking Request →';
        return;
      }

      try {
        if (typeof window.wc_capture_form === 'function') {
          window.wc_capture_form(form);
        } else if (typeof window.__wc !== 'undefined' && typeof window.__wc.trackFormSubmission === 'function') {
          window.__wc.trackFormSubmission(form);
        }
      } catch (wcErr) {
        console.warn('WhatConverts capture failed:', wcErr);
      }

      if (typeof gtag === 'function') {
        gtag('event', 'generate_lead', {
          service_type: document.getElementById('ns-service_type').value
        });
      }

      window.location.href = 'https://mechanicsnoranda.com.au/booking-confirmed/';
    });
  });
})();
</script>'''

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Pattern A: Pages WITH orphaned form fields
# Matches from <div class="hero-right"> through the iframe, the orphaned
# form-field divs, the stray </form></div></div></div></div></section> tail.
# The button text varies ("Get My Free Quote", "Send My Request", etc.)
PATTERN_HERO_WITH_ORPHANS = re.compile(
    r'<div class="hero-right">.*?<iframe src="https://noranda-booking\.vercel\.app"[^>]*></iframe>\s*'
    r'</div>\s*</div>\s*'           # closes hero-form-card and hero-right
    r'(?:[\s\S]*?<button[^>]*>.*?</button>\s*)?'  # optional stray button (some pages)
    r'(?:<div class="form-field">[\s\S]*?</div>\s*)*'  # zero or more form-field divs
    r'(?:<button[^>]*>.*?</button>\s*)?'          # optional stray button after fields
    r'</form>\s*</div>\s*</div>\s*</div>\s*</div>\s*</section>',
    re.DOTALL
)

# Pattern B: Pages WITHOUT orphaned fields (BMW, Audi)
# The iframe closing tag has different indentation (6 spaces vs 4 spaces)
PATTERN_HERO_CLEAN = re.compile(
    r'<div class="hero-right">\s*'
    r'<div class="hero-form-card"[^>]*>\s*'
    r'<iframe src="https://noranda-booking\.vercel\.app"[^>]*></iframe>\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'</div>\s*'
    r'</section>',
    re.DOTALL
)

# Pattern for the #form section iframe wrapper
# Handles both 4-space and 6-space indented iframes, and 2-space or 4-space closing divs
PATTERN_FORM_IFRAME = re.compile(
    r'<div style="width:100%;overflow:hidden;border-radius:8px;">\s*'
    r'<iframe src="https://noranda-booking\.vercel\.app"[^>]*></iframe>\s*'
    r'</div>',
    re.DOTALL
)

# ---------------------------------------------------------------------------
# Process files
# ---------------------------------------------------------------------------

def process_file(rel_path):
    full_path = os.path.join(BASE, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # --- Change 1: Hero block ---
    if PATTERN_HERO_WITH_ORPHANS.search(content):
        content, n = PATTERN_HERO_WITH_ORPHANS.subn(HERO_CTA_REPLACEMENT, content)
        if n:
            changes.append(f'hero (with orphans): {n} replacement(s)')
    elif PATTERN_HERO_CLEAN.search(content):
        content, n = PATTERN_HERO_CLEAN.subn(HERO_CTA_REPLACEMENT, content)
        if n:
            changes.append(f'hero (clean): {n} replacement(s)')
    else:
        changes.append('WARNING: no hero pattern matched')

    # --- Change 2: #form iframe ---
    n = len(PATTERN_FORM_IFRAME.findall(content))
    if n:
        content, _ = PATTERN_FORM_IFRAME.subn(FORM_EMBED, content)
        changes.append(f'form iframe: {n} replacement(s)')
    else:
        changes.append('WARNING: no form iframe pattern matched')

    if content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[OK] {rel_path}: {"; ".join(changes)}')
    else:
        print(f'[NO CHANGE] {rel_path}: {"; ".join(changes)}')

for rel in FILES:
    process_file(rel)

print('\nDone.')
