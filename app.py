"""
HRMS · Payroll module — Flask backend
-------------------------------------
Serves the Process-Payroll screen and drives the New-Run generator against the
PostgreSQL schema in hrms_schema.sql.

Notes on the schema this targets:
  * PKs are <table>_id (employee_id, period_id, payslip_id ...)
  * payslips.net_pay is a GENERATED column  -> never inserted
  * paid_days is derived as (working_days - lop_days), not stored
  * payslip_lines references pay_components(component_id) by id
  * enums are Title-Case ('Draft','Processed','Approved','Paid'...)

Endpoints
    GET  /                              render the screen
    GET  /api/periods                   list payroll periods
    GET  /api/periods/<id>/payslips     grid rows for a period (+ totals)
    GET  /api/payslips/<id>             one payslip with its lines
    GET  /api/employees                 salary master (for New Run)
    POST /api/runs                      create a run + generate payslips
    POST /api/periods/<id>/process      advance a run's status

Config:  DATABASE_URL=postgresql://user:pass@host:5432/hrms
"""
import os
import io
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from flask import Flask, jsonify, render_template, request, abort, send_file
import psycopg2
import psycopg2.extras
from openpyxl import load_workbook
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hrms"
)
JOB_PLATFORMS = os.environ.get(
    "JOB_PLATFORMS", "Naukri, LinkedIn, Indeed"
)

SS_RATE = Decimal("0.075")     # Jordan employee social-security rate
CURRENCY = "JOD"
Q3 = Decimal("0.01")           # payslips store NUMERIC(14,2)


def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    return conn


def q(value) -> Decimal:
    return Decimal(str(value)).quantize(Q3, rounding=ROUND_HALF_UP)


def rows_to_dicts(cur):
    cols = [c.name for c in cur.description]
    out = []
    for r in cur.fetchall():
        d = dict(zip(cols, r))
        for k, v in d.items():
            if isinstance(v, Decimal):
                d[k] = str(v)
        out.append(d)
    return out


# --------------------------------------------------------------------------- #
#  Payroll calculation — single source of truth (mirrored in payroll.js).
#  Returns lines keyed by component_code so the caller can map to component_id.
# --------------------------------------------------------------------------- #
def compute_payslip(emp, inp):
    basic = Decimal(str(emp["basic"]))
    housing = Decimal(str(emp["housing"]))
    transport = Decimal(str(emp["transport"]))

    wd = int(inp.get("working_days", 22))
    pd = min(int(inp.get("paid_days", wd)), wd)
    lop_days = max(0, wd - pd)

    overtime = q(inp.get("overtime", 0) or 0)
    commission = q(inp.get("commission", 0) or 0)
    bonus = q(inp.get("bonus", 0) or 0)

    earnings = [
        ("BASIC", "Earning", q(basic)),
        ("HRA", "Earning", q(housing)),
        ("TRANS", "Earning", q(transport)),
    ]
    if overtime > 0:
        earnings.append(("OT", "Earning", overtime))
    if commission > 0:
        earnings.append(("COMM", "Earning", commission))
    if bonus > 0:
        earnings.append(("BONUS", "Earning", bonus))

    ss = q((basic + housing + transport) * SS_RATE)
    deductions = [
        ("SSC", "Deduction", ss),
        ("INCOMETAX", "Deduction", q(emp.get("income_tax", 0) or 0)),
    ]
    loan = q(emp.get("loan_installment", 0) or 0)
    if loan > 0:
        deductions.append(("LOAN", "Deduction", loan))
    if lop_days > 0:
        deductions.append(("LOP", "Deduction", q(basic / Decimal(wd) * Decimal(lop_days))))

    gross = q(sum(a for _, _, a in earnings))
    total_ded = q(sum(a for _, _, a in deductions))
    return {
        "lines": earnings + deductions,
        "gross": gross,
        "deductions": total_ded,
        "net": q(gross - total_ded),
        "working_days": wd,
        "paid_days": pd,
        "lop_days": lop_days,
    }


# --------------------------------------------------------------------------- #
#  Views
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login.html")
def login_page():
    return render_template("login.html")

@app.route("/payroll.html")
def route_payroll_html():
    platforms = [p.strip() for p in JOB_PLATFORMS.split(",")]
    return render_template("payroll.html", job_platforms=platforms)

@app.route("/team_temp.html")
def route_team_temp_html():
    return render_template("team_temp.html")

@app.route("/erpset")
@app.route("/erpset.html")
@app.route("/settings")
@app.route("/settings.html")
def route_erpset_html():
    return render_template("erpset.html")

@app.route("/manufacture")
@app.route("/manufacture.html")
def route_manufacture_html():
    return render_template("manufacture.html")

@app.route("/procurement")
@app.route("/procurement.html")
def route_procurement_html():
    return render_template("procurement.html")

@app.route("/desk")
@app.route("/desk.html")
@app.route("/servicedesk")
def route_desk_html():
    return render_template("desk.html")

@app.route("/project")
@app.route("/project.html")
@app.route("/projects")
def route_project_html():
    return render_template("project.html")

@app.route("/inventory")
@app.route("/inventory.html")
def route_inventory_html():
    return render_template("inventory.html")

@app.route("/finance")
@app.route("/finance.html")
def route_finance_html():
    return render_template("finance.html")

@app.route("/asset")
@app.route("/asset.html")
@app.route("/assets")
def route_asset_html():
    return render_template("asset.html")

@app.route("/crm")
@app.route("/crm.html")
def route_crm_html():
    return render_template("crm.html")

@app.route("/sales")
@app.route("/sales.html")
@app.route("/sd")
def route_sales_html():
    return render_template("sales.html")


@app.route("/test")
@app.route("/test.html")
def route_test_html():
    return render_template("test.html")


@app.route("/api/periods")
def api_periods():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT period_id AS id, period_code, period_name, start_date, end_date,
                       to_char(pay_date,'DD Mon YYYY') AS pay_date, status
                FROM payroll_periods
                ORDER BY start_date DESC
            """)
            return jsonify(rows_to_dicts(cur))
    finally:
        conn.close()


@app.route("/api/periods/<int:period_id>/payslips")
def api_period_payslips(period_id):
    dept = request.args.get("department") or None
    search = request.args.get("search") or None
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT p.payslip_id AS id, e.employee_code,
                       e.first_name||' '||e.last_name AS name,
                       d.department_name AS department, g.designation_name AS designation,
                       p.working_days, p.lop_days,
                       (p.working_days - p.lop_days) AS paid_days,
                       p.gross_earnings, p.total_deductions, p.net_pay, p.status
                FROM payslips p
                JOIN employees e          ON e.employee_id = p.employee_id
                LEFT JOIN departments d    ON d.department_id = e.department_id
                LEFT JOIN designations g   ON g.designation_id = e.designation_id
                WHERE p.period_id = %s
            """
            params = [period_id]
            if dept:
                sql += " AND d.department_name = %s"; params.append(dept)
            if search:
                sql += (" AND (e.first_name||' '||e.last_name ILIKE %s "
                        "OR e.employee_code ILIKE %s)")
                params += [f"%{search}%", f"%{search}%"]
            sql += " ORDER BY e.employee_code"
            cur.execute(sql, params)
            rows = rows_to_dicts(cur)

        totals = {
            "count": len(rows),
            "gross": str(q(sum(Decimal(r["gross_earnings"]) for r in rows) if rows else 0)),
            "deductions": str(q(sum(Decimal(r["total_deductions"]) for r in rows) if rows else 0)),
            "net": str(q(sum(Decimal(r["net_pay"]) for r in rows) if rows else 0)),
        }
        return jsonify({"rows": rows, "totals": totals})
    finally:
        conn.close()


@app.route("/api/payslips/<int:payslip_id>")
def api_payslip(payslip_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.payslip_id AS id, p.payslip_no,
                       e.employee_code, e.first_name||' '||e.last_name AS name,
                       g.designation_name AS designation, d.department_name AS department,
                       to_char(e.date_of_joining,'DD Mon YYYY') AS date_of_joining,
                       COALESCE(b.iban, b.account_no, '—') AS bank_account,
                       p.working_days, p.lop_days,
                       (p.working_days - p.lop_days) AS paid_days,
                       p.gross_earnings, p.total_deductions, p.net_pay,
                       per.period_name
                FROM payslips p
                JOIN employees e           ON e.employee_id = p.employee_id
                LEFT JOIN departments d     ON d.department_id = e.department_id
                LEFT JOIN designations g    ON g.designation_id = e.designation_id
                LEFT JOIN employee_bank_accounts b ON b.bank_account_id = p.bank_account_id
                JOIN payroll_periods per    ON per.period_id = p.period_id
                WHERE p.payslip_id = %s
            """, (payslip_id,))
            head = rows_to_dicts(cur)
            if not head:
                abort(404)
            head = head[0]
            cur.execute("""
                SELECT c.component_name, pl.component_type, pl.amount
                FROM payslip_lines pl
                JOIN pay_components c ON c.component_id = pl.component_id
                WHERE pl.payslip_id = %s
                ORDER BY c.display_order, pl.payslip_line_id
            """, (payslip_id,))
            lines = rows_to_dicts(cur)
            # normalise type to lowercase for the front-end
            for l in lines:
                l["component_type"] = l["component_type"].lower()
            head["lines"] = lines
        return jsonify(head)
    finally:
        conn.close()


@app.route("/api/employees")
def api_employees():
    """Salary master used to pre-fill the New Run screen."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT e.employee_id AS id, e.employee_code,
                       e.first_name||' '||e.last_name AS name,
                       COALESCE(p.department_name, d.department_name) AS department,
                       CASE WHEN p.department_name IS NOT NULL THEN d.department_name ELSE NULL END AS sub_department,
                       g.designation_name AS designation,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='BASIC'),0)     AS basic,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='HRA'),0)   AS housing,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='TRANS'),0) AS transport,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='INCOMETAX'),0) AS income_tax
                FROM employees e
                LEFT JOIN departments  d ON d.department_id = e.department_id
                LEFT JOIN departments  p ON p.department_id = d.parent_department_id
                LEFT JOIN designations g ON g.designation_id = e.designation_id
                JOIN employee_salary_structures ss
                     ON ss.employee_id = e.employee_id AND ss.effective_to IS NULL
                JOIN salary_structure_lines sl ON sl.structure_id = ss.structure_id
                JOIN pay_components c           ON c.component_id = sl.component_id
                WHERE e.status = 'Active'
                GROUP BY e.employee_id, e.employee_code, name, d.department_name, p.department_name, g.designation_name
                ORDER BY e.employee_code
            """)
            emps = rows_to_dicts(cur)
            cur.execute("""
                SELECT employee_id, COALESCE(SUM(installment_amount),0) AS loan
                FROM employee_loans WHERE status = 'active' GROUP BY employee_id
            """)
            loans = {r["employee_id"]: r["loan"] for r in rows_to_dicts(cur)}
        for e in emps:
            e["loan_installment"] = loans.get(e["id"], "0")
        return jsonify(emps)
    finally:
        conn.close()


def _component_ids(cur):
    """Map component_code -> component_id, creating any missing variable heads."""
    cur.execute("SELECT component_code, component_id FROM pay_components")
    ids = {code: cid for code, cid in cur.fetchall()}
    wanted = [
        ("BASIC", "Basic Salary", "Earning"),
        ("HRA", "Housing Allowance", "Earning"),
        ("TRANS", "Transport Allowance", "Earning"),
        ("OT", "Overtime", "Earning"),
        ("COMM", "Sales Commission", "Earning"),
        ("BONUS", "Bonus", "Earning"),
        ("LOP", "Loss of Pay", "Deduction"),
        ("INCOMETAX", "Income Tax", "Deduction"),
    ]
    for code, name, ctype in wanted:
        if code not in ids:
            cur.execute("""INSERT INTO pay_components
                (component_code, component_name, component_type) VALUES (%s,%s,%s)
                RETURNING component_id""", (code, name, ctype))
            ids[code] = cur.fetchone()[0]
    return ids


@app.route("/api/runs", methods=["POST"])
def api_create_run():
    body = request.get_json(force=True)
    inputs = body.get("inputs", [])
    if not inputs:
        return jsonify({"error": "No employees supplied for this run."}), 400

    emp_ids = [i["employee_id"] for i in inputs]
    status = "Draft" if body.get("is_draft") else "Processed"
    period_code = f"{body['year']}-{int(body['month']):02d}"
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO payroll_periods
                    (period_code, period_name, start_date, end_date, pay_date, status)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT (period_code) DO UPDATE
                    SET pay_date = EXCLUDED.pay_date, status = EXCLUDED.status,
                        period_name = EXCLUDED.period_name
                RETURNING period_id
            """, (period_code, body["period_name"], body["start_date"],
                  body["end_date"], body["pay_date"], status))
            period_id = cur.fetchone()[0]
            cur.execute("DELETE FROM payslips WHERE period_id = %s", (period_id,))

            comp_ids = _component_ids(cur)

            cur.execute("""
                SELECT e.employee_id,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='BASIC'),0)     AS basic,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='HRA'),0)   AS housing,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='TRANS'),0) AS transport,
                       COALESCE(SUM(sl.amount) FILTER (WHERE c.component_code='INCOMETAX'),0) AS income_tax
                FROM employees e
                JOIN employee_salary_structures ss
                     ON ss.employee_id = e.employee_id AND ss.effective_to IS NULL
                JOIN salary_structure_lines sl ON sl.structure_id = ss.structure_id
                JOIN pay_components c           ON c.component_id = sl.component_id
                WHERE e.employee_id = ANY(%s) GROUP BY e.employee_id
            """, (emp_ids,))
            master = {r["employee_id"]: r for r in rows_to_dicts(cur)}

            cur.execute("""
                SELECT employee_id, COALESCE(SUM(installment_amount),0) AS loan
                FROM employee_loans WHERE status='active' AND employee_id = ANY(%s)
                GROUP BY employee_id
            """, (emp_ids,))
            loans = {r["employee_id"]: r["loan"] for r in rows_to_dicts(cur)}

            # primary bank account per employee
            cur.execute("""
                SELECT DISTINCT ON (employee_id) employee_id, bank_account_id
                FROM employee_bank_accounts
                WHERE employee_id = ANY(%s)
                ORDER BY employee_id, is_primary DESC
            """, (emp_ids,))
            banks = {eid: bid for eid, bid in cur.fetchall()}

            generated = 0
            for inp in inputs:
                eid = inp["employee_id"]
                emp = master.get(eid)
                if not emp:
                    continue
                emp["loan_installment"] = loans.get(eid, 0)
                res = compute_payslip(emp, inp)
                payslip_no = f"PS-{period_code}-{eid:04d}"

                cur.execute("""
                    INSERT INTO payslips
                        (payslip_no, period_id, employee_id, working_days, lop_days,
                         gross_earnings, total_deductions, status, bank_account_id, generated_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING payslip_id
                """, (payslip_no, period_id, eid, res["working_days"], res["lop_days"],
                      res["gross"], res["deductions"], status, banks.get(eid), datetime.utcnow()))
                payslip_id = cur.fetchone()[0]

                psycopg2.extras.execute_values(
                    cur,
                    """INSERT INTO payslip_lines
                         (payslip_id, component_id, component_type, amount) VALUES %s""",
                    [(payslip_id, comp_ids[code], ctype, amt)
                     for code, ctype, amt in res["lines"]],
                )
                generated += 1
        conn.commit()
        return jsonify({"period_id": period_id, "generated": generated,
                        "status": status.lower()}), 201
    except Exception as exc:
        conn.rollback()
        return jsonify({"error": str(exc)}), 500
    finally:
        conn.close()


@app.route("/api/employees/template")
def api_template():
    """Download the blank Excel upload template."""
    path = os.path.join(os.path.dirname(__file__), "employee_upload_template.xlsx")
    if not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True,
                     download_name="employee_upload_template.xlsx")


# Expected column order in the template's "Employees" sheet
IMPORT_COLS = [
    "employee_code", "employee_name", "gender", "nationality", "date_of_birth",
    "designation", "date_of_joining", "facility_code", "facility_name", "parent_department_name",
    "department", "work_center", "shift", "supervisor_name", "expat",
    "person_classification", "supervisor_code", "religion", "expatriate", "passport_number",
    "passport_issue_date", "passport_expiry_date", "labour_card", "lc_issue_date", "lc_expiry_date",
    "relieving_date", "approved_relieving", "labour_union", "separation_reason", "separation_mode",
    "person_category", "residence_card", "rc_issue", "rc_expiry"
]
VALID_EMP_TYPES = {"Permanent", "Contract", "Probation", "Temporary", "Intern"}


def _get_or_create(cur, table, id_col, code_col, name_col, name, code_prefix):
    """Match a lookup (department/designation) by name, creating it if absent."""
    if not name:
        return None
    cur.execute(f"SELECT {id_col} FROM {table} WHERE lower({name_col})=lower(%s)", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    code = (code_prefix + "-" + "".join(ch for ch in name.upper() if ch.isalnum())[:8])
    cur.execute(
        f"INSERT INTO {table} ({code_col}, {name_col}) VALUES (%s,%s) RETURNING {id_col}",
        (code[:20], name))
    return cur.fetchone()[0]


def _parse_num(val):
    if val in (None, ""):
        return Decimal("0")
    try:
        return q(val)
    except Exception:
        return Decimal("0")


def parse_date(val):
    if not val:
        return None
    import datetime as dt_module
    if isinstance(val, dt_module.datetime):
        return val.date()
    if isinstance(val, dt_module.date):
        return val
    val_str = str(val).strip()
    if not val_str or val_str.lower() in ("none", "null", "-", "—"):
        return None
    for fmt_str in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            return dt_module.datetime.strptime(val_str[:10], fmt_str).date()
        except ValueError:
            continue
    return None


@app.route("/api/employees/import", methods=["POST"])
def api_import():
    """Bulk create/update employees + salary structures from the Excel template."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    f = request.files["file"]
    if not f.filename.lower().endswith((".xlsx", ".xlsm")):
        return jsonify({"error": "Please upload a .xlsx file."}), 400

    try:
        wb = load_workbook(io.BytesIO(f.read()), data_only=True)
    except Exception:
        return jsonify({"error": "Could not read the workbook — is it a valid Excel file?"}), 400
    ws = wb["Employees"] if "Employees" in wb.sheetnames else wb.active

    # locate the header row (the one containing 'Personnel' or 'Employee Code')
    header_row = None
    for r in range(1, 8):
        values = [str(c.value).strip().lower() if c.value else "" for c in ws[r]]
        if any("personnel" in v or "employee code" in v or "employee_code" in v for v in values):
            header_row = r
            break
    if header_row is None:
        return jsonify({"error": "Header row not found. Use the provided template."}), 400

    conn = get_conn()
    created = updated = 0
    errors = []
    try:
        with conn.cursor() as cur:
            comp_ids = _component_ids(cur)  # ensures BASIC/HRA/TRANS/INCOMETAX exist

            for r in range(header_row + 1, ws.max_row + 1):
                cells = [ws.cell(row=r, column=i + 1).value for i in range(len(IMPORT_COLS))]
                rec = dict(zip(IMPORT_COLS, cells))
                code = (str(rec["employee_code"]).strip() if rec["employee_code"] else "")
                if not code:
                    continue  # skip blank rows

                # Name splitting
                full_name = str(rec["employee_name"] or "").strip()
                if not full_name:
                    errors.append(f"Row {r}: missing name for {code}")
                    continue
                parts = full_name.split()
                first_name = parts[0]
                last_name = " ".join(parts[1:]) if len(parts) > 1 else parts[0]

                # Date of joining
                doj = parse_date(rec["date_of_joining"])
                if not doj:
                    errors.append(f"Row {r}: missing Date of Joining for {code}")
                    continue

                # Designation
                desig_name = str(rec["designation"]).strip() if rec["designation"] else None
                desig_id = _get_or_create(cur, "designations", "designation_id",
                                          "designation_code", "designation_name",
                                          desig_name, "DES")

                # Parent Department & Department
                parent_dept_name = str(rec["parent_department_name"]).strip() if rec["parent_department_name"] else None
                parent_dept_id = None
                if parent_dept_name:
                    parent_dept_id = _get_or_create(cur, "departments", "department_id",
                                                    "department_code", "department_name",
                                                    parent_dept_name, "DEP")
                
                dept_name = str(rec["department"]).strip() if rec["department"] else None
                dept_id = None
                if dept_name:
                    dept_id = _get_or_create(cur, "departments", "department_id",
                                             "department_code", "department_name",
                                             dept_name, "DEP")
                    if parent_dept_id:
                        cur.execute("""
                            UPDATE departments SET parent_department_id = %s 
                            WHERE department_id = %s AND (parent_department_id IS NULL OR parent_department_id != %s)
                        """, (parent_dept_id, dept_id, parent_dept_id))

                # Facility / Location
                fac_code = str(rec["facility_code"]).strip() if rec["facility_code"] else None
                fac_name = str(rec["facility_name"]).strip() if rec["facility_name"] else None
                location_id = None
                if fac_code or fac_name:
                    if fac_code:
                        cur.execute("SELECT location_id FROM locations WHERE lower(location_code)=lower(%s)", (fac_code,))
                        row = cur.fetchone()
                        if row:
                            location_id = row[0]
                            if fac_name:
                                cur.execute("UPDATE locations SET location_name=%s WHERE location_id=%s", (fac_name, location_id))
                        else:
                            cur.execute("INSERT INTO locations (location_code, location_name) VALUES (%s, %s) RETURNING location_id", (fac_code, fac_name or fac_code))
                            location_id = cur.fetchone()[0]
                    elif fac_name:
                        cur.execute("SELECT location_id FROM locations WHERE lower(location_name)=lower(%s)", (fac_name,))
                        row = cur.fetchone()
                        if row:
                            location_id = row[0]
                        else:
                            cur.execute("INSERT INTO locations (location_code, location_name) VALUES (%s, %s) RETURNING location_id", 
                                        ("LOC-" + "".join(ch for ch in fac_name.upper() if ch.isalnum())[:8], fac_name))
                            location_id = cur.fetchone()[0]

                # Supervisor
                super_code = str(rec["supervisor_code"]).strip() if rec["supervisor_code"] else None
                manager_id = None
                if super_code:
                    cur.execute("SELECT employee_id FROM employees WHERE employee_code=%s", (super_code,))
                    row = cur.fetchone()
                    if row:
                        manager_id = row[0]

                # Parse rest of dates
                dob = parse_date(rec["date_of_birth"])
                passport_issue = parse_date(rec["passport_issue_date"])
                passport_expiry = parse_date(rec["passport_expiry_date"])
                lc_issue = parse_date(rec["lc_issue_date"])
                lc_expiry = parse_date(rec["lc_expiry_date"])
                relieving = parse_date(rec["relieving_date"])
                rc_issue = parse_date(rec["rc_issue"])
                rc_expiry = parse_date(rec["rc_expiry"])

                def clean_str(val, max_len=100):
                    if val is None:
                        return None
                    s = str(val).strip()
                    if s.lower() in ("none", "null", "-", "—"):
                        return None
                    return s[:max_len]

                gender_str = clean_str(rec["gender"], 15)
                if gender_str:
                    gender_str = gender_str.title()
                    if gender_str not in ("Male", "Female", "Other"):
                        gender_str = None
                
                work_center = clean_str(rec["work_center"], 100)
                shift = clean_str(rec["shift"], 100)
                supervisor_name = clean_str(rec["supervisor_name"], 150)
                expat = clean_str(rec["expat"], 20)
                person_classification = clean_str(rec["person_classification"], 100)
                religion = clean_str(rec["religion"], 50)
                expatriate = clean_str(rec["expatriate"], 20)
                passport_number = clean_str(rec["passport_number"], 50)
                labour_card = clean_str(rec["labour_card"], 50)
                approved_relieving = clean_str(rec["approved_relieving"], 20)
                labour_union = clean_str(rec["labour_union"], 100)
                separation_reason = clean_str(rec["separation_reason"], 255)
                separation_mode = clean_str(rec["separation_mode"], 100)
                person_category = clean_str(rec["person_category"], 100)
                residence_card = clean_str(rec["residence_card"], 50)

                # upsert employee by code
                cur.execute("SELECT employee_id FROM employees WHERE employee_code=%s", (code,))
                found = cur.fetchone()
                if found:
                    emp_id = found[0]
                    cur.execute("""
                        UPDATE employees SET
                            first_name=%s, last_name=%s, gender=%s, date_of_birth=%s, nationality=%s,
                            department_id=%s, designation_id=%s, date_of_joining=%s, location_id=%s, manager_id=%s,
                            facility_code=%s, facility_name=%s, parent_department_name=%s, work_center=%s, shift=%s,
                            supervisor_name=%s, expat=%s, person_classification=%s, supervisor_code=%s, religion=%s,
                            expatriate=%s, passport_number=%s, passport_issue_date=%s, passport_expiry_date=%s,
                            labour_card=%s, lc_issue_date=%s, lc_expiry_date=%s, relieving_date=%s, date_of_leaving=%s,
                            approved_relieving=%s, labour_union=%s, separation_reason=%s, separation_mode=%s,
                            person_category=%s, residence_card=%s, rc_issue=%s, rc_expiry=%s, updated_at=now()
                        WHERE employee_id=%s
                    """, (
                        first_name, last_name, gender_str, dob, clean_str(rec["nationality"], 60),
                        dept_id, desig_id, doj, location_id, manager_id,
                        fac_code, fac_name, parent_dept_name, work_center, shift,
                        supervisor_name, expat, person_classification, super_code, religion,
                        expatriate, passport_number, passport_issue, passport_expiry,
                        labour_card, lc_issue, lc_expiry, relieving, relieving,
                        approved_relieving, labour_union, separation_reason, separation_mode,
                        person_category, residence_card, rc_issue, rc_expiry,
                        emp_id
                    ))
                    updated += 1
                else:
                    cur.execute("""
                        INSERT INTO employees (
                            employee_code, first_name, last_name, gender, date_of_birth, nationality,
                            department_id, designation_id, date_of_joining, location_id, manager_id,
                            facility_code, facility_name, parent_department_name, work_center, shift,
                            supervisor_name, expat, person_classification, supervisor_code, religion,
                            expatriate, passport_number, passport_issue_date, passport_expiry_date,
                            labour_card, lc_issue_date, lc_expiry_date, relieving_date, date_of_leaving,
                            approved_relieving, labour_union, separation_reason, separation_mode,
                            person_category, residence_card, rc_issue, rc_expiry, status
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s, 'Active'
                        ) RETURNING employee_id
                    """, (
                        code, first_name, last_name, gender_str, dob, clean_str(rec["nationality"], 60),
                        dept_id, desig_id, doj, location_id, manager_id,
                        fac_code, fac_name, parent_dept_name, work_center, shift,
                        supervisor_name, expat, person_classification, super_code, religion,
                        expatriate, passport_number, passport_issue, passport_expiry,
                        labour_card, lc_issue, lc_expiry, relieving, relieving,
                        approved_relieving, labour_union, separation_reason, separation_mode,
                        person_category, residence_card, rc_issue, rc_expiry
                    ))
                    emp_id = cur.fetchone()[0]
                    created += 1

                # salary structure: reuse active one or create it, then upsert its 4 lines with defaults
                cur.execute("""SELECT structure_id FROM employee_salary_structures
                               WHERE employee_id=%s AND effective_to IS NULL
                               ORDER BY effective_from DESC LIMIT 1""", (emp_id,))
                srow = cur.fetchone()
                if srow:
                    structure_id = srow[0]
                else:
                    cur.execute("""INSERT INTO employee_salary_structures
                        (employee_id, effective_from, currency) VALUES (%s,%s,'JOD')
                        RETURNING structure_id""", (emp_id, doj))
                    structure_id = cur.fetchone()[0]

                line_map = {
                    "BASIC": Decimal("0"),
                    "HRA": Decimal("0"),
                    "TRANS": Decimal("0"),
                    "INCOMETAX": Decimal("0"),
                }
                for ccode, amt in line_map.items():
                    cur.execute("""
                        INSERT INTO salary_structure_lines (structure_id, component_id, amount)
                        VALUES (%s,%s,%s)
                        ON CONFLICT (structure_id, component_id)
                        DO UPDATE SET amount = EXCLUDED.amount
                    """, (structure_id, comp_ids[ccode], amt))
        conn.commit()
        return jsonify({"created": created, "updated": updated,
                        "errors": errors, "total": created + updated})
    except Exception as exc:
        conn.rollback()
        return jsonify({"error": str(exc)}), 500
    finally:
        conn.close()


@app.route("/api/periods/<int:period_id>/process", methods=["POST"])
def api_process(period_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE payroll_periods SET status='Approved' WHERE period_id=%s",
                        (period_id,))
            if cur.rowcount == 0:
                abort(404)
            cur.execute("UPDATE payslips SET status='Approved' WHERE period_id=%s",
                        (period_id,))
        conn.commit()
        return jsonify({"status": "approved"})
    except Exception as exc:
        conn.rollback()
        return jsonify({"error": str(exc)}), 500
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
#  Cab Management API
# --------------------------------------------------------------------------- #
@app.route("/api/cabs/dashboard_stats")
def api_cab_dashboard_stats():
    date_from = request.args.get("date_from") or None
    date_to = request.args.get("date_to") or None
    origin = request.args.get("origin") or None
    destination = request.args.get("destination") or None
    employee = request.args.get("employee") or None
    department = request.args.get("department") or None

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Build filter conditions for trips
            filter_sql = ""
            filter_params = []
            
            if date_from:
                filter_sql += " AND pickup_time >= %s"
                filter_params.append(date_from + " 00:00:00")
            if date_to:
                filter_sql += " AND pickup_time <= %s"
                filter_params.append(date_to + " 23:59:59")
            if origin:
                filter_sql += " AND origin ILIKE %s"
                filter_params.append(f"%{origin}%")
            if destination:
                filter_sql += " AND destination ILIKE %s"
                filter_params.append(f"%{destination}%")
            if employee:
                filter_sql += " AND employee_id IN (SELECT employee_id FROM employees WHERE first_name ILIKE %s OR last_name ILIKE %s OR employee_code ILIKE %s)"
                filter_params.extend([f"%{employee}%", f"%{employee}%", f"%{employee}%"])
            if department:
                filter_sql += " AND employee_id IN (SELECT e.employee_id FROM employees e JOIN departments d ON e.department_id = d.department_id WHERE d.department_name ILIKE %s)"
                filter_params.append(f"%{department}%")

            # KPIs
            cur.execute(f"""
                SELECT 
                    COUNT(*) as total_trips,
                    COUNT(*) FILTER (WHERE trip_status = 'Scheduled') as scheduled,
                    COUNT(*) FILTER (WHERE trip_status = 'Ongoing') as ongoing,
                    COUNT(*) FILTER (WHERE trip_status = 'Completed') as completed,
                    COUNT(*) FILTER (WHERE trip_status = 'Cancelled') as cancelled,
                    COUNT(DISTINCT employee_id) as total_employees
                FROM cab_trips WHERE 1=1 {filter_sql}
            """, filter_params)
            kpis = cur.fetchone()
            
            cur.execute("SELECT COUNT(*) FROM cab_drivers WHERE status = 'Active'")
            total_drivers = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM cab_vehicles WHERE status = 'Active'")
            total_vehicles = cur.fetchone()[0]

            # Chart Data: Trips by Destination
            cur.execute(f"""
                SELECT destination, COUNT(*) as count 
                FROM cab_trips WHERE 1=1 {filter_sql}
                GROUP BY destination 
                ORDER BY count DESC LIMIT 5
            """, filter_params)
            chart_dest = rows_to_dicts(cur)

            # Chart Data: Trips by Status
            cur.execute(f"""
                SELECT trip_status, COUNT(*) as count 
                FROM cab_trips WHERE 1=1 {filter_sql}
                GROUP BY trip_status
            """, filter_params)
            chart_status = rows_to_dicts(cur)

            stats = {
                "kpis": {
                    "total_trips": kpis[0],
                    "scheduled": kpis[1],
                    "ongoing": kpis[2],
                    "completed": kpis[3],
                    "cancelled": kpis[4],
                    "total_employees": kpis[5],
                    "total_drivers": total_drivers,
                    "total_vehicles": total_vehicles
                },
                "charts": {
                    "by_destination": chart_dest,
                    "by_status": chart_status
                }
            }
            return jsonify(stats)
    finally:
        conn.close()


@app.route("/api/cabs/trips")
def api_cab_trips():
    status = request.args.get("status") or None
    date_from = request.args.get("date_from") or None
    date_to = request.args.get("date_to") or None
    origin = request.args.get("origin") or None
    destination = request.args.get("destination") or None
    employee = request.args.get("employee") or None
    department = request.args.get("department") or None
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT 
                    t.trip_id as id, t.trip_no, t.pickup_time, t.origin, t.destination,
                    t.trip_distance_km, t.trip_status, t.booking_status, t.cab_type as trip_cab_type,
                    e.first_name||' '||e.last_name AS employee_name, e.employee_code,
                    dep.department_name,
                    d.driver_name, v.vehicle_number, v.cab_type
                FROM cab_trips t
                LEFT JOIN employees e ON e.employee_id = t.employee_id
                LEFT JOIN departments dep ON dep.department_id = e.department_id
                LEFT JOIN cab_drivers d ON d.driver_id = t.driver_id
                LEFT JOIN cab_vehicles v ON v.vehicle_id = t.vehicle_id
                WHERE 1=1
            """
            params = []
            
            if status:
                sql += " AND t.trip_status = %s"
                params.append(status)
            if date_from:
                sql += " AND t.pickup_time >= %s"
                params.append(date_from + " 00:00:00")
            if date_to:
                sql += " AND t.pickup_time <= %s"
                params.append(date_to + " 23:59:59")
            if origin:
                sql += " AND t.origin ILIKE %s"
                params.append(f"%{origin}%")
            if destination:
                sql += " AND t.destination ILIKE %s"
                params.append(f"%{destination}%")
            if employee:
                sql += " AND (e.first_name ILIKE %s OR e.last_name ILIKE %s OR e.employee_code ILIKE %s)"
                params.extend([f"%{employee}%", f"%{employee}%", f"%{employee}%"])
            if department:
                sql += " AND dep.department_name ILIKE %s"
                params.append(f"%{department}%")
                
            sql += " ORDER BY t.pickup_time DESC"
            
            cur.execute(sql, params)
            rows = rows_to_dicts(cur)
            
            return jsonify(rows)
    finally:
        conn.close()

# --------------------------------------------------------------------------- #
#  Salary Components API
# --------------------------------------------------------------------------- #
@app.route("/api/components", methods=["GET"])
def api_get_components():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM pay_components ORDER BY display_order ASC, component_id ASC")
            rows = rows_to_dicts(cur)
            return jsonify(rows)
    finally:
        conn.close()

@app.route("/api/components", methods=["POST"])
def api_create_component():
    data = request.json
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO pay_components (component_code, component_name, component_type, calc_type, is_taxable, is_active)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING component_id
            """, (
                data.get("component_code"), data.get("component_name"), data.get("component_type"),
                data.get("calc_type", "Fixed"), data.get("is_taxable", False), data.get("is_active", True)
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"success": True, "component_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/components/<int:comp_id>", methods=["PUT"])
def api_update_component(comp_id):
    data = request.json
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE pay_components SET
                    component_code = %s, component_name = %s, component_type = %s,
                    calc_type = %s, is_taxable = %s, is_active = %s
                WHERE component_id = %s
            """, (
                data.get("component_code"), data.get("component_name"), data.get("component_type"),
                data.get("calc_type", "Fixed"), data.get("is_taxable", False), data.get("is_active", True),
                comp_id
            ))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/components/<int:comp_id>", methods=["DELETE"])
def api_delete_component(comp_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM pay_components WHERE component_id = %s", (comp_id,))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": "Cannot delete component; it may be in use."}), 400
    finally:
        conn.close()

# --------------------------------------------------------------------------- #
#  Departments API
# --------------------------------------------------------------------------- #
@app.route("/api/departments", methods=["GET"])
def api_get_departments():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT d.department_id, d.department_code, d.department_name, 
                       d.parent_department_id, p.department_name as parent_department_name,
                       d.is_active
                FROM departments d
                LEFT JOIN departments p ON d.parent_department_id = p.department_id
                ORDER BY d.department_name ASC
            """)
            rows = rows_to_dicts(cur)
            return jsonify(rows)
    finally:
        conn.close()

@app.route("/api/departments", methods=["POST"])
def api_create_department():
    data = request.json
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO departments (department_code, department_name, parent_department_id, is_active)
                VALUES (%s, %s, %s, %s) RETURNING department_id
            """, (
                data.get("department_code"), data.get("department_name"),
                data.get("parent_department_id") or None, data.get("is_active", True)
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"success": True, "department_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/departments/<int:dept_id>", methods=["PUT"])
def api_update_department(dept_id):
    data = request.json
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE departments SET
                    department_code = %s, department_name = %s, 
                    parent_department_id = %s, is_active = %s
                WHERE department_id = %s
            """, (
                data.get("department_code"), data.get("department_name"),
                data.get("parent_department_id") or None, data.get("is_active", True),
                dept_id
            ))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/departments/<int:dept_id>", methods=["DELETE"])
def api_delete_department(dept_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM departments WHERE department_id = %s", (dept_id,))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": "Cannot delete department; it may have active employees or sub-departments."}), 400
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
#  Employee Master API
# --------------------------------------------------------------------------- #
@app.route("/api/settings/employees", methods=["GET"])
def api_settings_employees():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT e.employee_id, e.employee_code, e.first_name, e.last_name,
                       e.personal_email, e.gender, e.date_of_joining, e.status,
                       e.department_id, d.department_name
                FROM employees e
                LEFT JOIN departments d ON d.department_id = e.department_id
                ORDER BY e.employee_code ASC
            """)
            rows = rows_to_dicts(cur)
            # Format dates to string
            for r in rows:
                if r.get('date_of_joining'):
                    r['date_of_joining'] = r['date_of_joining'].strftime('%Y-%m-%d')
            return jsonify(rows)
    finally:
        conn.close()

@app.route("/api/settings/employees", methods=["POST"])
def api_create_settings_employee():
    data = request.json
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employees (
                    employee_code, first_name, last_name, personal_email, 
                    gender, date_of_joining, status, department_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING employee_id
            """, (
                data.get("employee_code"), data.get("first_name"), data.get("last_name"),
                data.get("personal_email") or None, data.get("gender") or None,
                data.get("date_of_joining"), data.get("status", "Active"),
                data.get("department_id") or None
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"success": True, "employee_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/settings/employees/<int:emp_id>", methods=["PUT"])
def api_update_settings_employee(emp_id):
    data = request.json
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE employees SET
                    employee_code = %s, first_name = %s, last_name = %s,
                    personal_email = %s, gender = %s, date_of_joining = %s,
                    status = %s, department_id = %s
                WHERE employee_id = %s
            """, (
                data.get("employee_code"), data.get("first_name"), data.get("last_name"),
                data.get("personal_email") or None, data.get("gender") or None,
                data.get("date_of_joining"), data.get("status", "Active"),
                data.get("department_id") or None,
                emp_id
            ))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route("/api/settings/employees/<int:emp_id>", methods=["DELETE"])
def api_delete_settings_employee(emp_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": "Cannot delete employee. They may have active payroll records or documents."}), 400
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
#  Reports API
# --------------------------------------------------------------------------- #
@app.route("/api/reports/register")
def api_reports_register():
    period_id = request.args.get("period_id")
    print("API /api/reports/register called with period_id:", period_id)
    if not period_id or period_id == "undefined":
        return jsonify([])
    try:
        period_id = int(period_id)
    except ValueError:
        return jsonify([])
    dept = request.args.get("department") or None
    search = request.args.get("search") or None
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT e.employee_code, e.first_name||' '||e.last_name AS name, d.department_name AS department,
                       p.gross_earnings AS gross, p.total_deductions AS deductions, p.net_pay AS net,
                       COALESCE(SUM(pl.amount) FILTER (WHERE c.component_code = 'BASIC'), 0) AS basic,
                       COALESCE(SUM(pl.amount) FILTER (WHERE c.component_code = 'HRA'), 0) AS housing,
                       COALESCE(SUM(pl.amount) FILTER (WHERE c.component_code = 'TRANS'), 0) AS transport,
                       COALESCE(SUM(pl.amount) FILTER (WHERE c.component_code = 'INCOMETAX'), 0) AS income_tax,
                       COALESCE(SUM(pl.amount) FILTER (WHERE c.component_code = 'SS'), 0) AS social_security
                FROM payslips p
                JOIN employees e ON e.employee_id = p.employee_id
                LEFT JOIN departments d ON d.department_id = e.department_id
                LEFT JOIN payslip_lines pl ON pl.payslip_id = p.payslip_id
                LEFT JOIN pay_components c ON c.component_id = pl.component_id
                WHERE p.period_id = %s
            """
            params = [period_id]
            if dept:
                sql += " AND d.department_name = %s"
                params.append(dept)
            if search:
                sql += " AND (e.first_name||' '||e.last_name ILIKE %s OR e.employee_code ILIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])
            sql += " GROUP BY e.employee_code, e.first_name, e.last_name, d.department_name, p.gross_earnings, p.total_deductions, p.net_pay"
            sql += " ORDER BY e.first_name, e.last_name"
            
            cur.execute(sql, tuple(params))
            return jsonify(rows_to_dicts(cur))
    finally:
        conn.close()

@app.route("/api/reports/bank")
def api_reports_bank():
    period_id = request.args.get("period_id")
    print("API /api/reports/bank called with period_id:", period_id)
    if not period_id or period_id == "undefined":
        return jsonify([])
    try:
        period_id = int(period_id)
    except ValueError:
        return jsonify([])
    dept = request.args.get("department") or None
    search = request.args.get("search") or None
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT e.employee_code, e.first_name||' '||e.last_name AS name, d.department_name AS department,
                       p.net_pay AS net,
                       b.bank_name, b.account_no, b.iban, b.branch
                FROM payslips p
                JOIN employees e ON e.employee_id = p.employee_id
                LEFT JOIN departments d ON d.department_id = e.department_id
                LEFT JOIN employee_bank_accounts b ON b.employee_id = e.employee_id AND b.is_primary = TRUE
                WHERE p.period_id = %s
            """
            params = [period_id]
            if dept:
                sql += " AND d.department_name = %s"
                params.append(dept)
            if search:
                sql += " AND (e.first_name||' '||e.last_name ILIKE %s OR e.employee_code ILIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])
            sql += " ORDER BY e.first_name, e.last_name"
            
            cur.execute(sql, tuple(params))
            return jsonify(rows_to_dicts(cur))
    finally:
        conn.close()

@app.route("/api/reports/ss")
def api_reports_ss():
    period_id = request.args.get("period_id")
    print("API /api/reports/ss called with period_id:", period_id)
    if not period_id or period_id == "undefined":
        return jsonify([])
    try:
        period_id = int(period_id)
    except ValueError:
        return jsonify([])
    dept = request.args.get("department") or None
    search = request.args.get("search") or None
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT e.employee_code, e.first_name||' '||e.last_name AS name, d.department_name AS department,
                       COALESCE(SUM(pl.amount), 0) AS ss_amount
                FROM payslips p
                JOIN employees e ON e.employee_id = p.employee_id
                LEFT JOIN departments d ON d.department_id = e.department_id
                JOIN payslip_lines pl ON pl.payslip_id = p.payslip_id
                JOIN pay_components c ON c.component_id = pl.component_id
                WHERE p.period_id = %s AND c.component_code = 'SS'
            """
            params = [period_id]
            if dept:
                sql += " AND d.department_name = %s"
                params.append(dept)
            if search:
                sql += " AND (e.first_name||' '||e.last_name ILIKE %s OR e.employee_code ILIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])
            sql += " GROUP BY e.employee_code, e.first_name, e.last_name, d.department_name"
            sql += " ORDER BY e.first_name, e.last_name"
            
            cur.execute(sql, tuple(params))
            return jsonify(rows_to_dicts(cur))
    finally:
        conn.close()

@app.route("/api/reports/tax")
def api_reports_tax():
    period_id = request.args.get("period_id")
    print("API /api/reports/tax called with period_id:", period_id)
    if not period_id or period_id == "undefined":
        return jsonify([])
    try:
        period_id = int(period_id)
    except ValueError:
        return jsonify([])
    dept = request.args.get("department") or None
    search = request.args.get("search") or None
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT e.employee_code, e.first_name||' '||e.last_name AS name, d.department_name AS department,
                       COALESCE(SUM(pl.amount), 0) AS tax_amount
                FROM payslips p
                JOIN employees e ON e.employee_id = p.employee_id
                LEFT JOIN departments d ON d.department_id = e.department_id
                JOIN payslip_lines pl ON pl.payslip_id = p.payslip_id
                JOIN pay_components c ON c.component_id = pl.component_id
                WHERE p.period_id = %s AND c.component_code = 'INCOMETAX'
            """
            params = [period_id]
            if dept:
                sql += " AND d.department_name = %s"
                params.append(dept)
            if search:
                sql += " AND (e.first_name||' '||e.last_name ILIKE %s OR e.employee_code ILIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])
            sql += " GROUP BY e.employee_code, e.first_name, e.last_name, d.department_name"
            sql += " ORDER BY e.first_name, e.last_name"
            
            cur.execute(sql, tuple(params))
            return jsonify(rows_to_dicts(cur))
    finally:
        conn.close()



# ==========================================
# ATTENDANCE / BIOMETRICS
# ==========================================

import csv
import io
from datetime import datetime

@app.route('/api/attendance/logs', methods=['GET'])
def api_get_attendance_logs():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT b.log_id, e.first_name, e.last_name, e.employee_code, b.device_name, b.punch_time, b.direction, b.method
                FROM biometric_logs b
                JOIN employees e ON b.employee_id = e.employee_id
                ORDER BY b.punch_time DESC
                LIMIT 100
            ''')
            rows = cur.fetchall()
            logs = []
            for r in rows:
                logs.append({
                    'id': r[0],
                    'name': f"{r[1]} {r[2]}" if r[2] else r[1],
                    'empCode': r[3],
                    'device': r[4],
                    'timestamp': r[5].strftime('%Y-%m-%d %H:%M:%S'),
                    'direction': r[6],
                    'method': r[7]
                })
            return jsonify(logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/attendance/dahua-webhook', methods=['POST'])
def api_dahua_webhook():
    # Security check if a token is configured in .env
    expected_token = os.environ.get('DAHUA_WEBHOOK_SECRET')
    if expected_token and expected_token != 'your_secret_token_here':
        provided_token = request.args.get('token') or request.headers.get('Authorization')
        if not provided_token or expected_token not in provided_token:
            return jsonify({'error': 'Unauthorized'}), 401

    # Expects JSON: {"employee_code": "E1001", "timestamp": "2026-07-16 09:00:00", "direction": "IN", "device": "Dahua Main", "method": "Face"}
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Find employee by code
            cur.execute("SELECT employee_id FROM employees WHERE employee_code = %s", (data.get('employee_code'),))
            emp = cur.fetchone()
            if not emp:
                return jsonify({'error': 'Employee not found'}), 404
            
            cur.execute('''
                INSERT INTO biometric_logs (employee_id, device_name, punch_time, direction, method)
                VALUES (%s, %s, %s, %s, %s)
            ''', (emp[0], data.get('device', 'Webhook Device'), data.get('timestamp'), data.get('direction'), data.get('method', 'Webhook')))
        conn.commit()
        return jsonify({'message': 'Log saved'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/attendance/upload-csv', methods=['POST'])
def api_upload_biometric_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            added = 0
            for row in csv_input:
                emp_code = row.get('EmployeeCode') or row.get('employee_code')
                punch_time_str = row.get('Timestamp') or row.get('timestamp')
                direction = row.get('Direction') or row.get('direction')
                device = row.get('Device') or row.get('device') or 'CSV Upload'
                method = row.get('Method') or row.get('method') or 'CSV'

                if not emp_code or not punch_time_str or not direction:
                    continue # Skip invalid rows
                
                cur.execute("SELECT employee_id FROM employees WHERE employee_code = %s", (emp_code,))
                emp = cur.fetchone()
                if emp:
                    cur.execute('''
                        INSERT INTO biometric_logs (employee_id, device_name, punch_time, direction, method)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (emp[0], device, punch_time_str, direction.upper(), method))
                    added += 1
        conn.commit()
        return jsonify({'message': f'Successfully uploaded {added} logs.'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()



# ==========================================
# EXPENSES MODULE
# ==========================================
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/expenses/list', methods=['GET'])
def api_get_expenses():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT x.claim_id, e.first_name, e.last_name, e.employee_code, x.category, x.expense_date, x.amount, x.currency, x.description, x.receipt_file_path, x.status
                FROM expense_claims x
                JOIN employees e ON x.employee_id = e.employee_id
                ORDER BY x.created_at DESC
            ''')
            rows = cur.fetchall()
            claims = []
            for r in rows:
                claims.append({
                    'id': r[0],
                    'name': f"{r[1]} {r[2]}" if r[2] else r[1],
                    'empCode': r[3],
                    'category': r[4],
                    'date': r[5].strftime('%Y-%m-%d'),
                    'amount': str(r[6]),
                    'currency': r[7],
                    'description': r[8],
                    'receipt': r[9],
                    'status': r[10]
                })
            return jsonify(claims)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/expenses/new', methods=['POST'])
def api_new_expense():
    emp_code = request.form.get('employee_code')
    category = request.form.get('category')
    date_str = request.form.get('date')
    amount = request.form.get('amount')
    currency = request.form.get('currency', 'USD')
    description = request.form.get('description')
    
    if not all([emp_code, category, date_str, amount]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    file_path = None
    if 'receipt' in request.files:
        file = request.files['receipt']
        if file.filename != '':
            filename = secure_filename(f"{emp_code}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            full_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(full_path)
            file_path = f"/static/uploads/{filename}"

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT employee_id FROM employees WHERE employee_code = %s", (emp_code,))
            emp = cur.fetchone()
            if not emp:
                return jsonify({'error': 'Employee not found'}), 404
            
            cur.execute('''
                INSERT INTO expense_claims (employee_id, category, expense_date, amount, currency, description, receipt_file_path, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')
            ''', (emp[0], category, date_str, amount, currency, description, file_path))
        conn.commit()
        return jsonify({'message': 'Expense claim submitted successfully.'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/expenses/<int:claim_id>/approve', methods=['POST'])
def api_approve_expense(claim_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE expense_claims SET status = 'Approved' WHERE claim_id = %s RETURNING claim_id", (claim_id,))
            if not cur.fetchone():
                return jsonify({'error': 'Claim not found'}), 404
        conn.commit()
        return jsonify({'message': 'Expense Approved'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/expenses/<int:claim_id>/reject', methods=['POST'])
def api_reject_expense(claim_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE expense_claims SET status = 'Rejected' WHERE claim_id = %s RETURNING claim_id", (claim_id,))
            if not cur.fetchone():
                return jsonify({'error': 'Claim not found'}), 404
        conn.commit()
        return jsonify({'message': 'Expense Rejected'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


# ==========================================
# PERFORMANCE MODULE APIs
# ==========================================

@app.route('/api/performance/goals', methods=['GET'])
def api_get_perf_goals():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, employee_code, title, description, 
                       TO_CHAR(target_date, 'YYYY-MM-DD') as target_date, 
                       progress_percent, status 
                FROM perf_goals 
                ORDER BY target_date ASC
            """)
            goals = cur.fetchall()
        return jsonify(goals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/performance/goals/new', methods=['POST'])
def api_new_perf_goal():
    conn = get_conn()
    try:
        data = request.form
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO perf_goals (employee_code, title, description, target_date, progress_percent, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data.get('employee_code'), data.get('title'), data.get('description'), 
                  data.get('target_date'), data.get('progress_percent', 0), data.get('status', 'In Progress')))
        conn.commit()
        return jsonify({'message': 'Goal created successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/performance/reviews', methods=['GET'])
def api_get_perf_reviews():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, employee_code, reviewer_code, review_cycle, rating, comments, status,
                       TO_CHAR(created_at, 'YYYY-MM-DD') as date
                FROM perf_reviews 
                ORDER BY created_at DESC
            """)
            reviews = cur.fetchall()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/performance/reviews/new', methods=['POST'])
def api_new_perf_review():
    conn = get_conn()
    try:
        data = request.form
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO perf_reviews (employee_code, reviewer_code, review_cycle, rating, comments, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data.get('employee_code'), data.get('reviewer_code'), data.get('review_cycle'), 
                  data.get('rating'), data.get('comments'), data.get('status', 'Completed')))
        conn.commit()
        return jsonify({'message': 'Review submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/performance/feedback', methods=['GET'])
def api_get_perf_feedback():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT id, employee_code, provider_code, feedback_text, is_anonymous,
                       TO_CHAR(created_at, 'YYYY-MM-DD') as date
                FROM perf_feedback 
                ORDER BY created_at DESC
            """)
            feedbacks = cur.fetchall()
        return jsonify(feedbacks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/performance/feedback/new', methods=['POST'])
def api_new_perf_feedback():
    conn = get_conn()
    try:
        data = request.form
        is_anonymous = data.get('is_anonymous') == 'true'
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO perf_feedback (employee_code, provider_code, feedback_text, is_anonymous) 
                VALUES (%s, %s, %s, %s)
            """, (data.get('employee_code'), data.get('provider_code'), data.get('feedback_text'), is_anonymous))
        conn.commit()
        return jsonify({'message': 'Feedback submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)


# ==========================================
# REPORTING APIs (NEW)
# ==========================================

@app.route('/api/reports/demographics', methods=['GET'])
def api_reports_demographics():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    department, 
                    gender,
                    COUNT(*) as count
                FROM employees
                WHERE status = 'Active'
                GROUP BY department, gender
                ORDER BY department
            """)
            demo_data = cur.fetchall()
            
            # Additional aggregate: Age brackets (we don't have DOB in employees table by default, so we mock age distribution, or we can just return dept/gender)
            # We'll just return the department/gender distribution.
        return jsonify(demo_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/reports/turnover', methods=['GET'])
def api_reports_turnover():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    reason, 
                    COUNT(*) as count
                FROM resignations
                WHERE status IN ('Approved', 'Completed')
                GROUP BY reason
                ORDER BY count DESC
            """)
            turnover_data = cur.fetchall()
        return jsonify(turnover_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/reports/leaves', methods=['GET'])
def api_reports_leaves():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    status,
                    COUNT(*) as count
                FROM leave_requests
                GROUP BY status
            """)
            leave_data = cur.fetchall()
        return jsonify(leave_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/reports/performance', methods=['GET'])
def api_reports_performance():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    rating,
                    COUNT(*) as count
                FROM perf_reviews
                GROUP BY rating
                ORDER BY rating ASC
            """)
            perf_data = cur.fetchall()
        return jsonify(perf_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ==========================================
# HR HELPDESK APIs
# ==========================================

@app.route('/api/helpdesk/tickets', methods=['GET'])
def api_helpdesk_tickets_get():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    t.id, t.subject, t.category, t.priority, t.status, 
                    TO_CHAR(t.updated_at, 'Mon DD, YYYY') as last_updated,
                    e1.first_name || ' ' || e1.last_name as requester_name
                FROM helpdesk_tickets t
                LEFT JOIN employees e1 ON t.requester_id = e1.id
                ORDER BY 
                    CASE t.status WHEN 'Open' THEN 1 WHEN 'In Progress' THEN 2 ELSE 3 END,
                    CASE t.priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
                    t.updated_at DESC
            """)
            tickets = cur.fetchall()
        return jsonify(tickets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/helpdesk/tickets/new', methods=['POST'])
def api_helpdesk_tickets_new():
    data = request.json
    subject = data.get('subject')
    category = data.get('category')
    priority = data.get('priority', 'Low')
    description = data.get('description')
    requester_id = 1  # Hardcoded admin ID for now
    
    if not subject or not category or not description:
        return jsonify({'error': 'Missing required fields'}), 400
        
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO helpdesk_tickets (subject, category, priority, description, requester_id, status)
                VALUES (%s, %s, %s, %s, %s, 'Open')
                RETURNING id
            """, (subject, category, priority, description, requester_id))
            conn.commit()
            new_id = cur.fetchone()[0]
        return jsonify({'success': True, 'ticket_id': new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/helpdesk/tickets/<int:id>/status', methods=['PUT'])
def api_helpdesk_tickets_update(id):
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Missing status'}), 400
        
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE helpdesk_tickets 
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (status, id))
            conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
