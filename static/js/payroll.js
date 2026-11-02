/* ===========================================================================
   AureliaHRMS · Payroll — New Design Controller
   Talks to the Flask API in app.py.
   =========================================================================== */

const API = {
  periods:      ()          => fetch('/api/periods').then(r => r.json()),
  employees:    ()          => fetch('/api/employees').then(r => r.json()),
  createRun:    (body)       => fetch('/api/runs', {
                    method:'POST', headers:{'Content-Type':'application/json'},
                    body: JSON.stringify(body) }).then(r => r.json()),
};

const SS_RATE = 0.075;

/* ---------- formatting helpers ---------- */
const num = v => Number(v || 0);
const r3  = n => Math.round(n * 1000) / 1000;
const fmt = n => num(n).toLocaleString('en-US', {minimumFractionDigits:3, maximumFractionDigits:3});
const initials = n => n.split(' ').slice(0,2).map(w => w[0]).join('').toUpperCase();

let state = { employees: [] };
let runInputs = {};

/* ======================= Calculations ======================= */
function computeRun(emp, inp) {
  const basic = num(emp.basic), housing = num(emp.housing), transport = num(emp.transport);
  const lop = Math.max(0, inp.wd - inp.pd);
  const earn = [['Basic Salary', basic], ['Housing Allowance', housing], ['Transport Allowance', transport]];
  if (inp.ot   > 0) earn.push(['Overtime', r3(inp.ot)]);
  if (inp.comm > 0) earn.push(['Sales Commission', r3(inp.comm)]);

  const ss = r3((basic + housing + transport) * SS_RATE);
  const ded = [['Social Security (7.5%)', ss], ['Income Tax', r3(num(emp.income_tax))]];
  if (num(emp.loan_installment) > 0) ded.push(['Loan Installment', r3(num(emp.loan_installment))]);
  if (lop > 0) ded.push([`Loss of Pay (${lop} ${lop>1?'days':'day'})`, r3(basic/inp.wd*lop)]);

  const G = r3(earn.reduce((t,[,v]) => t+v, 0));
  const D = r3(ded.reduce((t,[,v]) => t+v, 0));
  return {lop, gross:G, deds:D, net:r3(G-D)};
}

/* ======================= Init & Render ======================= */
async function init() {
  state.employees = await API.employees();
  
  // Set default inputs
  state.employees.forEach(e => {
    runInputs[e.id] = {wd:22, pd:22, ot:0, comm:0};
  });

  renderGrid();
}

function renderGrid() {
  const g = document.getElementById('runGrid');
  const scope = document.getElementById('rDept').value;
  
  // Filter by department if selected
  const list = state.employees.filter(e => !scope || e.department === scope);

  g.innerHTML = list.map(e => {
    const inp = runInputs[e.id];
    const c = computeRun(e, inp);
    const allowances = num(e.housing) + num(e.transport);

    return `<tr data-id="${e.id}">
      <td>
        <div class="emp-cell">
          <div class="emp-avatar">${initials(e.name)}</div>
          <div class="emp-details">
            <span class="emp-name">${e.name}</span>
            <span class="emp-meta">${e.employee_code} · ${e.department || ''}</span>
          </div>
        </div>
      </td>
      <td class="r fig">${fmt(e.basic)}</td>
      <td class="r fig">${fmt(allowances)}</td>
      <td class="c"><input class="cell-input" data-f="wd" value="${inp.wd}"></td>
      <td class="c"><input class="cell-input" data-f="pd" value="${inp.pd}"></td>
      <td class="c"><input class="cell-input" data-f="ot" value="${inp.ot}"></td>
      <td class="c"><input class="cell-input" data-f="comm" value="${inp.comm}"></td>
      <td class="r fig fig-gross" data-g>${fmt(c.gross)}</td>
      <td class="r fig fig-deduction" data-d>${fmt(c.deds)}</td>
      <td class="r fig fig-net" data-n>${fmt(c.net)}</td>
    </tr>`;
  }).join('');

  // Attach event listeners to inputs
  g.querySelectorAll('tr[data-id]').forEach(tr => {
    const id = Number(tr.dataset.id);
    tr.querySelectorAll('input.cell-input').forEach(el => {
      el.addEventListener('input', () => {
        const f = el.dataset.f;
        let v = parseFloat(el.value); 
        if (isNaN(v) || v < 0) v = 0;
        runInputs[id][f] = v;
        
        // Cap paid days to working days
        if (runInputs[id].pd > runInputs[id].wd) {
          runInputs[id].pd = runInputs[id].wd;
          if(f === 'pd') el.value = runInputs[id].wd; // Update UI if user typed it
        }

        const c = computeRun(state.employees.find(x => x.id === id), runInputs[id]);
        tr.querySelector('[data-g]').textContent = fmt(c.gross);
        tr.querySelector('[data-d]').textContent = fmt(c.deds);
        tr.querySelector('[data-n]').textContent = fmt(c.net);
      });
    });
  });
}

// Department Filter Listener
document.getElementById('rDept').addEventListener('change', renderGrid);

// Search Box Listener (simplified front-end search)
const searchInput = document.querySelector('.search-box .form-input');
if(searchInput) {
  searchInput.addEventListener('input', (e) => {
    const val = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#runGrid tr');
    rows.forEach(row => {
      const name = row.querySelector('.emp-name').textContent.toLowerCase();
      const meta = row.querySelector('.emp-meta').textContent.toLowerCase();
      if(name.includes(val) || meta.includes(val)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  });
}

/* ======================= toast ======================= */
let toastTimer;
function toast(msg) {
  const t = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  t.classList.add('show'); clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
}

/* Run Init */
init();
