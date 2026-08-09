import json
import os

# ─────────────────────────────────────────────
# FINANCE & ACCOUNTING ERP NAVIGATION (44 SCREENS / 11 MODULES)
# ─────────────────────────────────────────────

GROUPS_NAV = {
    "Financial Setup": [
        {"id": "finance_coa", "title": "Chart of Accounts", "url": "/finance/coa"},
        {"id": "finance_fiscal_calendar", "title": "Fiscal Year / Period Calendar", "url": "/finance/fiscal-calendar"},
        {"id": "finance_entities", "title": "Company / Legal Entity Master", "url": "/finance/entities"},
        {"id": "finance_currency_exchange", "title": "Currency & Exchange Rate Master", "url": "/finance/currency-exchange"},
    ],
    "General Ledger": [
        {"id": "gl_journal_entries", "title": "Journal Entry List", "url": "/gl/journal-entries"},
        {"id": "gl_journal_entries_new", "title": "New Journal Entry", "url": "/gl/journal-entries/new"},
        {"id": "gl_ledger_inquiry", "title": "General Ledger Inquiry", "url": "/gl/ledger-inquiry"},
        {"id": "gl_trial_balance", "title": "Trial Balance", "url": "/gl/trial-balance"},
        {"id": "gl_recurring_entries", "title": "Recurring Journal Templates", "url": "/gl/recurring-entries"},
    ],
    "Accounts Payable": [
        {"id": "ap_invoices", "title": "Vendor Invoice List (AP)", "url": "/ap/invoices"},
        {"id": "ap_bill_entry", "title": "Bill / Invoice Entry", "url": "/ap/bill-entry"},
        {"id": "ap_payment_run", "title": "Payment Run / Batch Payments", "url": "/ap/payment-run"},
        {"id": "ap_aging", "title": "AP Aging Report", "url": "/ap/aging"},
        {"id": "ap_vendor_statements", "title": "Vendor Statement / Reconciliation", "url": "/ap/vendor-statements"},
    ],
    "Accounts Receivable": [
        {"id": "ar_customers", "title": "Customer Master", "url": "/ar/customers"},
        {"id": "ar_invoices_new", "title": "Sales / Customer Invoice", "url": "/ar/invoices/new"},
        {"id": "ar_receipts", "title": "Receive Payment / Cash Application", "url": "/ar/receipts"},
        {"id": "ar_aging", "title": "AR Aging Report", "url": "/ar/aging"},
        {"id": "ar_collections", "title": "Collections Workbench", "url": "/ar/collections"},
    ],
    "Cash & Banking": [
        {"id": "cash_bank_accounts", "title": "Bank Account Master", "url": "/cash/bank-accounts"},
        {"id": "cash_reconciliation", "title": "Bank Reconciliation", "url": "/cash/reconciliation"},
        {"id": "cash_flow_forecast", "title": "Cash Flow Forecast", "url": "/cash/flow-forecast"},
        {"id": "cash_petty_cash", "title": "Petty Cash Management", "url": "/cash/petty-cash"},
    ],
    "Fixed Assets": [
        {"id": "assets_register", "title": "Fixed Asset Register", "url": "/assets/register"},
        {"id": "assets_new", "title": "Asset Acquisition / Capitalization", "url": "/assets/new"},
        {"id": "assets_depreciation", "title": "Depreciation Schedule", "url": "/assets/depreciation"},
        {"id": "assets_disposal", "title": "Asset Transfer / Disposal", "url": "/assets/disposal"},
    ],
    "Tax & Compliance": [
        {"id": "tax_codes", "title": "Tax Code / Rate Master", "url": "/tax/codes"},
        {"id": "tax_vat_return", "title": "VAT / Tax Return Filing", "url": "/tax/vat-return"},
        {"id": "tax_withholding", "title": "Withholding Tax Report", "url": "/tax/withholding"},
    ],
    "Budgeting & Planning": [
        {"id": "budget_annual_plan", "title": "Annual Budget Planning", "url": "/budget/annual-plan"},
        {"id": "budget_vs_actual", "title": "Budget vs Actual Dashboard", "url": "/budget/vs-actual"},
        {"id": "budget_forecast", "title": "Rolling Forecast", "url": "/budget/forecast"},
    ],
    "Cost Accounting": [
        {"id": "costing_centers", "title": "Cost Center / Profit Center Master", "url": "/costing/centers"},
        {"id": "costing_allocation", "title": "Cost Allocation Rules", "url": "/costing/allocation"},
        {"id": "costing_profitability", "title": "Profitability Analysis", "url": "/costing/profitability"},
    ],
    "Financial Reporting": [
        {"id": "reports_income_statement", "title": "Income Statement (P&L)", "url": "/reports/income-statement"},
        {"id": "reports_balance_sheet", "title": "Balance Sheet", "url": "/reports/balance-sheet"},
        {"id": "reports_cash_flow_statement", "title": "Cash Flow Statement", "url": "/reports/cash-flow-statement"},
        {"id": "reports_executive_dashboard", "title": "Executive Financial Dashboard", "url": "/reports/executive-dashboard"},
    ],
    "Period Close & Admin": [
        {"id": "close_checklist", "title": "Month-End Close Checklist", "url": "/close/checklist"},
        {"id": "finance_approval_matrix", "title": "Finance Approval Matrix", "url": "/finance/approval-matrix"},
        {"id": "finance_user_roles", "title": "User Roles & Permissions", "url": "/finance/user-roles"},
        {"id": "finance_audit_log", "title": "Financial Audit Log", "url": "/finance/audit-log"},
    ]
}

# ─────────────────────────────────────────────
# PAGE CONFIGURATIONS & MOCK DATA
# ─────────────────────────────────────────────

PAGE_CONFIGS = {
    # SETUP
    "finance_coa": {
        "type": "list",
        "columns": ["Account Code", "Account Name", "Account Type", "Currency", "Debit (SAR)", "Credit (SAR)", "Net Balance", "Status", "Actions"],
        "rows": [
            {"Account Code": "1010-01", "Account Name": "Al-Rajhi Operating Bank Account", "Account Type": "Asset (Cash)", "Currency": "SAR", "Debit (SAR)": "4,250,000 SAR", "Credit (SAR)": "1,120,000 SAR", "Net Balance": "3,130,000 SAR", "Status": "active"},
            {"Account Code": "1200-05", "Account Name": "Trade Accounts Receivable", "Account Type": "Asset (AR)", "Currency": "SAR", "Debit (SAR)": "1,890,000 SAR", "Credit (SAR)": "420,000 SAR", "Net Balance": "1,470,000 SAR", "Status": "active"},
            {"Account Code": "2100-01", "Account Name": "Trade Accounts Payable", "Account Type": "Liability (AP)", "Currency": "SAR", "Debit (SAR)": "650,000 SAR", "Credit (SAR)": "1,450,000 SAR", "Net Balance": "800,000 SAR", "Status": "active"},
            {"Account Code": "4010-10", "Account Name": "Sales Revenue - Manufacturing", "Account Type": "Revenue", "Currency": "SAR", "Debit (SAR)": "0 SAR", "Credit (SAR)": "8,920,000 SAR", "Net Balance": "8,920,000 SAR", "Status": "active"},
        ]
    },
    "gl_journal_entries": {
        "type": "list",
        "columns": ["Voucher #", "Posting Date", "Reference / Description", "Entity", "Total Debit (SAR)", "Total Credit (SAR)", "Prepared By", "Posting Status", "Actions"],
        "rows": [
            {"Voucher #": "JV-2026-0412", "Posting Date": "2026-07-22", "Reference / Description": "Monthly Depreciation Allocation - Q2 Equipment", "Entity": "Saudi Industrial Corp", "Total Debit (SAR)": "145,000 SAR", "Total Credit (SAR)": "145,000 SAR", "Prepared By": "Tariq Mansoor", "Posting Status": "approved"},
            {"Voucher #": "JV-2026-0409", "Posting Date": "2026-07-20", "Reference / Description": "Prepaid Office Lease Amortization July", "Entity": "Saudi Industrial Corp", "Total Debit (SAR)": "38,500 SAR", "Total Credit (SAR)": "38,500 SAR", "Prepared By": "Aisha Al-Harbi", "Posting Status": "approved"},
            {"Voucher #": "JV-2026-0405", "Posting Date": "2026-07-18", "Reference / Description": "Accrued VAT Output Adjustment", "Entity": "Saudi Industrial Corp", "Total Debit (SAR)": "62,400 SAR", "Total Credit (SAR)": "62,400 SAR", "Prepared By": "Tariq Mansoor", "Posting Status": "pending"},
        ]
    },
    "ap_invoices": {
        "type": "list",
        "columns": ["Invoice #", "Vendor Name", "Bill Date", "Due Date", "Amount (SAR)", "Tax (VAT 15%)", "Net Payable", "Payment Status", "Actions"],
        "rows": [
            {"Invoice #": "INV-SABIC-901", "Vendor Name": "SABIC Petrochemicals", "Bill Date": "2026-07-01", "Due Date": "2026-07-31", "Amount (SAR)": "450,000 SAR", "Tax (VAT 15%)": "67,500 SAR", "Net Payable": "517,500 SAR", "Payment Status": "pending"},
            {"Invoice #": "INV-ARAM-334", "Vendor Name": "Aramco Lubricants", "Bill Date": "2026-06-15", "Due Date": "2026-07-15", "Amount (SAR)": "120,000 SAR", "Tax (VAT 15%)": "18,000 SAR", "Net Payable": "138,000 SAR", "Payment Status": "approved"},
        ]
    },
    "reports_income_statement": {
        "type": "list",
        "columns": ["Financial Line Item", "Q1 Actual (SAR)", "Q2 Actual (SAR)", "YTD Total (SAR)", "Budget Target (SAR)", "Variance %", "Performance Status", "Actions"],
        "rows": [
            {"Financial Line Item": "Gross Revenue / Net Sales", "Q1 Actual (SAR)": "4,120,000 SAR", "Q2 Actual (SAR)": "4,800,000 SAR", "YTD Total (SAR)": "8,920,000 SAR", "Budget Target (SAR)": "8,500,000 SAR", "Variance %": "+4.9%", "Performance Status": "active"},
            {"Financial Line Item": "Cost of Goods Sold (COGS)", "Q1 Actual (SAR)": "2,450,000 SAR", "Q2 Actual (SAR)": "2,810,000 SAR", "YTD Total (SAR)": "5,260,000 SAR", "Budget Target (SAR)": "5,100,000 SAR", "Variance %": "-3.1%", "Performance Status": "expiring"},
            {"Financial Line Item": "Gross Profit Margin", "Q1 Actual (SAR)": "1,670,000 SAR", "Q2 Actual (SAR)": "1,990,000 SAR", "YTD Total (SAR)": "3,660,000 SAR", "Budget Target (SAR)": "3,400,000 SAR", "Variance %": "+7.6%", "Performance Status": "active"},
        ]
    }
}

# ─────────────────────────────────────────────
# BADGE & ROW RENDERERS
# ─────────────────────────────────────────────

STATUS_BADGES = {
    "active":           ("status-active",       "✔ Active / Normal"),
    "approved":         ("status-approved",     "✔ Posted / Paid"),
    "completed":        ("status-completed",    "Completed"),
    "open":             ("status-open",         "Open"),
    "closed":           ("status-closed",       "Closed"),
    "pending":          ("status-pending",      "Pending Approval"),
    "in_progress":      ("status-inprogress",   "In Progress"),
    "draft":            ("status-draft",        "Draft"),
    "expiring":         ("status-expiring",     "⚠ Over Budget"),
    "blocked":          ("status-blocked",      "✖ Overdue / Locked"),
    "overdue":          ("status-actionreq",    "⚡ Action Required"),
    "normal":           ("status-active",       "In Balance"),
}

def render_badge(val):
    key = str(val).lower().replace(" ", "_")
    if key in STATUS_BADGES:
        cls, label = STATUS_BADGES[key]
        return f'<span class="status-badge {cls}">{label}</span>'
    return val

def render_table_row(row, columns):
    cells = ""
    for col in columns:
        if col == "Actions":
            continue
        val = row.get(col, "—")
        if col.lower() in ("status", "posting status", "payment status", "performance status"):
            val = render_badge(val)
        cells += f"<td>{val}</td>"
    cells += """
    <td>
      <div class="action-icons">
        <svg title="View" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
        <svg title="Edit" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        <svg class="delete" title="Delete" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
      </div>
    </td>"""
    return f"<tr>{cells}</tr>"

def build_list_html(page_id, page_cfg, page_title):
    columns = page_cfg["columns"]
    rows_data = page_cfg["rows"]

    header_cells = "".join(f"<th>{c}</th>" for c in columns)
    body_rows = "".join(render_table_row(r, columns) for r in rows_data)

    return f"""
        <div class="card">
          <div class="toolbar">
            <div class="toolbar-left">
              <div class="search-box">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input type="text" placeholder="Search {page_title}..." oninput="const q=this.value.toLowerCase(); this.closest('.card').querySelectorAll('.data-table tbody tr').forEach(r => r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none');">
              </div>
              <button class="btn btn-outline">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                Filter
              </button>
              <button class="btn btn-outline">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                Columns
              </button>
            </div>
            <div class="toolbar-right">
              <button class="btn btn-outline">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 .49-3.5"></path></svg>
                Refresh
              </button>
              <button class="btn btn-outline">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                Export
              </button>
              <button class="btn btn-primary">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                Create New
              </button>
            </div>
          </div>
          <div class="table-responsive">
            <table class="data-table">
              <thead><tr>{header_cells}</tr></thead>
              <tbody>{body_rows}</tbody>
            </table>
          </div>
          <div class="pagination">
            <div>Showing 1 to {len(rows_data)} of {len(rows_data)} entries</div>
            <div class="pagination-controls">
              <button class="page-btn"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg></button>
              <button class="page-btn active">1</button>
              <button class="page-btn"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></button>
            </div>
          </div>
        </div>"""

# ─────────────────────────────────────────────
# BUILD CONTENT MAP FOR ALL 44 SCREENS
# ─────────────────────────────────────────────
content_map = {}

# Populate configured pages
for page_id, cfg in PAGE_CONFIGS.items():
    title = page_id.replace("_", " ").title()
    content_map[page_id] = build_list_html(page_id, cfg, title)

# Fallback populator for any remaining screens in GROUPS_NAV
for grp_name, page_list in GROUPS_NAV.items():
    for item in page_list:
        pid = item["id"]
        if pid not in content_map:
            t = item["title"]
            content_map[pid] = build_list_html(pid, {
                "type": "list",
                "columns": ["Ref #", "Financial Category", "Account Code", "Amount (SAR)", "Posting Date", "Status", "Actions"],
                "rows": [
                    {"Ref #": "FIN-2026-001", "Financial Category": grp_name, "Account Code": "1100-01", "Amount (SAR)": "250,000 SAR", "Posting Date": "2026-07-22", "Status": "active"},
                    {"Ref #": "FIN-2026-002", "Financial Category": grp_name, "Account Code": "2100-05", "Amount (SAR)": "180,000 SAR", "Posting Date": "2026-07-20", "Status": "approved"},
                    {"Ref #": "FIN-2026-003", "Financial Category": grp_name, "Account Code": "4010-02", "Amount (SAR)": "95,000 SAR", "Posting Date": "2026-07-18", "Status": "pending"},
                ]
            }, t)

content_map_js = json.dumps(content_map)
groups_json = json.dumps(GROUPS_NAV, indent=4)

# Create CONFIG object for JS
config_obj = {}
for grp_name, page_list in GROUPS_NAV.items():
    for item in page_list:
        config_obj[item["id"]] = {
            "group": grp_name,
            "title": item["title"],
            "url": item["url"]
        }

config_json = json.dumps(config_obj, indent=4)

# Output finance_output_data.json
nav_output = {"config": config_obj}
with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\finance_output_data.json', 'w', encoding='utf-8') as f:
    json.dump(nav_output, f, indent=4)

# ─────────────────────────────────────────────
# GENERATE FINANCE SPA HTML FILE
# ─────────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AureliaHRMS · Enterprise Finance & Accounting ERP</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{{{ url_for('static', filename='css/payroll.css') }}}}">
  <script src="{{{{ url_for('static', filename='js/global_search.js') }}}}"></script>
  <style>
    html, body {{ width:100vw; height:100vh; overflow:hidden; margin:0; padding:0; background:#f8fafc; }}
    
    .sidebar {{ background:#132238; color:#cbd5e1; }}
    .top-nav {{ background:#132238; border-bottom:1px solid #1e2d42; }}
    .top-nav .nav-tab {{ color:#94a3b8; font-weight:500; padding:8px 14px; border-radius:6px; text-decoration:none; font-size:13px; transition:all 0.15s; }}
    .top-nav .nav-tab:hover {{ background:rgba(255,255,255,0.08); color:#fff; }}
    .top-nav .nav-tab.active {{ background:#fff; color:#132238; font-weight:600; }}

    .main-wrapper {{ width:calc(100vw - 200px); height:100vh; display:flex; flex-direction:column; overflow:hidden; }}
    .content {{ height:calc(100vh - 60px); overflow-y:auto; padding:16px; }}

    /* ── Tabs ── */
    .nav-tab {{ display:flex; align-items:center; gap:8px; }}
    .nav-tab .close-btn {{ display:inline-flex; align-items:center; justify-content:center; width:16px; height:16px; border-radius:50%; background:transparent; color:inherit; opacity:.6; font-size:14px; transition:all .2s; }}
    .nav-tab .close-btn:hover {{ background:rgba(0,0,0,.1); opacity:1; }}
    .top-nav .nav-links {{ gap:8px; display:flex; align-items:center; }}

    /* ── Dropdown ── */
    .dropdown {{ position:relative; display:inline-block; margin-left:8px; }}
    .dropdown-content {{ display:none; position:absolute; background:#fff; min-width:220px; box-shadow:0 8px 16px rgba(0,0,0,.1); z-index:100; border:1px solid #e2e8f0; border-radius:6px; top:100%; left:0; padding:8px 0; max-height:400px; overflow-y:auto; }}
    .dropdown-content a {{ color:#334155; padding:10px 16px; text-decoration:none; display:block; font-size:13px; font-weight:500; }}
    .dropdown-content a:hover {{ background:#f8fafc; color:#0f172a !important; }}
    .dropdown:hover .dropdown-content {{ display:block; }}

    /* ── Profile Dropdown ── */
    .profile-menu-container {{ position:relative; display:inline-block; }}
    .user-avatar {{ width:34px; height:34px; background:#e0e7ff; color:#3730a3; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; cursor:pointer; border:2px solid #c7d2fe; user-select:none; transition:all 0.2s ease; }}
    .user-avatar:hover {{ transform:scale(1.05); box-shadow:0 0 0 3px rgba(99,102,241,0.4); }}
    .profile-dropdown-card {{ position:absolute; top:46px; right:0; width:260px; background:#ffffff; border-radius:14px; box-shadow:0 12px 30px -4px rgba(0,0,0,0.15), 0 4px 12px -2px rgba(0,0,0,0.08); border:1px solid #e2e8f0; z-index:1000; display:none; padding:10px 0; transform-origin:top right; }}
    .profile-dropdown-card.show {{ display:block; animation:profilePop 0.18s cubic-bezier(0.16,1,0.3,1); }}
    @keyframes profilePop {{ 0% {{ opacity:0; transform:scale(0.92) translateY(-8px); }} 100% {{ opacity:1; transform:scale(1) translateY(0); }} }}
    .p-card-header {{ display:flex; align-items:center; gap:12px; padding:6px 18px 12px 18px; }}
    .p-card-avatar {{ width:48px; height:48px; border-radius:50%; background:#e0e7ff; color:#3730a3; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; flex-shrink:0; border:2px solid #c7d2fe; }}
    .p-card-info {{ overflow:hidden; }}
    .p-card-name {{ font-size:15px; font-weight:700; color:#0f172a; line-height:1.25; margin-bottom:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .p-card-role {{ font-size:12.5px; color:#64748b; font-weight:500; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .p-card-divider {{ height:1px; background:#f1f5f9; margin:6px 0; }}
    .p-card-item {{ display:flex; align-items:center; gap:12px; padding:10px 18px; font-size:13.5px; font-weight:500; color:#334155; cursor:pointer; transition:background 0.15s ease, color 0.15s ease; text-decoration:none; }}
    .p-card-item:hover {{ background:#f8fafc; color:#0f172a; }}
    .p-card-item svg {{ width:16px; height:16px; color:#64748b; transition:color 0.15s ease; }}
    .p-card-item:hover svg {{ color:#0f172a; }}
    .p-card-item.danger {{ color:#e11d48; font-weight:600; }}
    .p-card-item.danger svg {{ color:#e11d48; }}
    .p-card-item.danger:hover {{ background:#fff1f2; color:#be123c; }}
    .p-card-item.danger:hover svg {{ color:#be123c; }}

    /* Modal Overlay */
    .erp-modal-overlay {{ position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(15,23,42,0.55); backdrop-filter:blur(3px); z-index:9999; display:flex; align-items:center; justify-content:center; }}
    .erp-modal-card {{ background:#ffffff; border-radius:14px; width:520px; max-width:92vw; max-height:88vh; overflow-y:auto; box-shadow:0 20px 40px rgba(0,0,0,0.2); border:1px solid #e2e8f0; animation:slideUp 0.18s cubic-bezier(0.16,1,0.3,1); }}
    @keyframes slideUp {{ 0% {{ opacity:0; transform:translateY(12px); }} 100% {{ opacity:1; transform:translateY(0); }} }}

    /* ── Top right ── */
    .top-right-icons {{ display:flex; align-items:center; gap:16px; color:#94a3b8; margin-right:16px; }}
    .top-right-icons svg {{ cursor:pointer; }}
    .bell-icon-container {{ position:relative; display:inline-flex; }}
    .bell-dot {{ position:absolute; top:0; right:2px; width:6px; height:6px; background:#ef4444; border-radius:50%; border:1px solid #132238; }}

    /* ── Data grid ── */
    .card {{ background:#fff; border:1px solid #e2e8f0; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,.05); margin-top:16px; }}
    .toolbar {{ display:flex; justify-content:space-between; align-items:center; padding:16px 20px; border-bottom:1px solid #e2e8f0; flex-wrap:wrap; gap:10px; }}
    .toolbar-left, .toolbar-right {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
    .search-box {{ position:relative; }}
    .search-box svg {{ position:absolute; left:10px; top:50%; transform:translateY(-50%); color:#94a3b8; }}
    .search-box input {{ padding:8px 12px 8px 32px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; width:220px; outline:none; transition:border-color .2s; }}
    .search-box input:focus {{ border-color:#2f5eff; }}
    .btn {{ display:inline-flex; align-items:center; gap:6px; padding:8px 14px; font-size:13px; font-weight:500; border-radius:6px; cursor:pointer; transition:all .2s; border:none; }}
    .btn-primary {{ background:#2f5eff; color:#fff; }}
    .btn-primary:hover {{ filter:brightness(1.08); }}
    .btn-outline {{ background:#fff; border:1px solid #cbd5e1; color:#475569; }}
    .btn-outline:hover {{ background:#f8fafc; border-color:#94a3b8; }}
    .data-table {{ width:100%; border-collapse:collapse; }}
    .data-table th {{ background:#f8fafc; text-align:left; padding:6px 8px; font-size:10px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:.5px; border-bottom:1px solid #e2e8f0; white-space:nowrap; }}
    .data-table td {{ padding:6px 8px; font-size:11px; color:#334155; border-bottom:1px solid #e2e8f0; }}
    .data-table tbody tr:hover {{ background:#f8fafc; }}
    .action-icons {{ display:flex; gap:12px; }}
    .action-icons svg {{ color:#94a3b8; cursor:pointer; transition:color .2s; }}
    .action-icons svg:hover {{ color:#0f172a; }}
    .action-icons svg.delete:hover {{ color:#ef4444; }}
    .pagination {{ display:flex; align-items:center; justify-content:space-between; padding:16px 20px; color:#64748b; font-size:13px; }}
    .pagination-controls {{ display:flex; gap:4px; }}
    .page-btn {{ width:32px; height:32px; display:flex; align-items:center; justify-content:center; border:1px solid #e2e8f0; background:#fff; border-radius:6px; cursor:pointer; color:#475569; }}
    .page-btn.active {{ background:#2f5eff; color:#fff; border-color:#2f5eff; }}

    /* Status Badges */
    .status-badge {{ display:inline-flex; align-items:center; gap:4px; padding:2px 6px; border-radius:10px; font-size:10px; font-weight:600; white-space:nowrap; }}
    .status-active {{ background:#e6f6ee; color:#1f8a56; }}
    .status-approved {{ background:#e6f6ee; color:#1f8a56; }}
    .status-completed {{ background:#f1f5f9; color:#475569; }}
    .status-open {{ background:#fdf3df; color:#b7791f; }}
    .status-closed {{ background:#f1f5f9; color:#64748b; }}
    .status-pending {{ background:#fdf3df; color:#b7791f; }}
    .status-inprogress {{ background:#eaefff; color:#1f42c9; }}
    .status-draft {{ background:#f1f5f9; color:#64748b; }}
    .status-blocked {{ background:#fdeceb; color:#c0362c; }}
    .status-expiring {{ background:#fdf3df; color:#b7791f; }}
    .status-actionreq {{ background:#fdeceb; color:#c0362c; }}
  </style>
</head>
<body>
  <div style="display:flex; width:100vw; height:100vh;">
    <!-- SIDEBAR -->
    <aside class="sidebar" style="width:200px; height:100vh; flex-shrink:0; display:flex; flex-direction:column; border-right:1px solid #1e2d42;">
      <div style="height:60px; padding:0 16px; display:flex; align-items:center; gap:8px; border-bottom:1px solid #1e2d42; box-sizing:border-box;">
        <div style="width:32px; height:32px; border-radius:8px; background:#2f5eff; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:16px;">FA</div>
        <div>
          <div style="font-size:15px; font-weight:700; color:#fff; letter-spacing:-0.2px;">ExeonFinance</div>
          <div style="font-size:11px; color:#94a3b8;">Finance &amp; Accounting ERP</div>
        </div>
      </div>
      <div class="sidebar-menu" id="sidebar-menu-container" style="flex:1; overflow-y:auto; padding:16px 0;"></div>
    </aside>

    <!-- MAIN WRAPPER -->
    <div class="main-wrapper">
      <header class="top-nav" style="height:60px; padding:0 16px; display:flex; align-items:center; justify-content:space-between;">
        <nav class="nav-links" id="top-nav-links"></nav>
        <div class="top-right" style="display:flex; align-items:center;">
          <div class="top-right-icons">
            <div class="bell-icon-container">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
              <div class="bell-dot"></div>
            </div>
            <div class="global-search" id="globalSearchContainer">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
            <input type="text" id="globalSearch" placeholder="Search pages... (Ctrl+K)" autocomplete="off">
            <div class="search-dropdown" id="searchDropdown"></div>
          </div>
          </div>
          <a href="login.html?view=portal" class="datetime" style="color:#94a3b8; text-decoration:none; margin-right:16px; font-weight:500; font-size:13px;">&larr; Back to Portal</a>
          
          <div class="profile-menu-container" id="profileMenuContainer">
            <div class="user-avatar" id="profileAvatarBtn" onclick="toggleProfileMenu(event)">FA</div>
            <div class="profile-dropdown-card" id="profileDropdownCard">
              <div class="p-card-header">
                <div class="p-card-avatar">FA</div>
                <div class="p-card-info">
                  <div class="p-card-name">Tariq Mansoor</div>
                  <div class="p-card-role">Chief Financial Officer (CFO)</div>
                </div>
              </div>
              <div class="p-card-divider"></div>
              <div class="p-card-item" onclick="openProfileModal()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                <span>My Profile</span>
              </div>
              <div class="p-card-item" onclick="openAccountSettingsModal()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                <span>Account Settings</span>
              </div>
              <div class="p-card-item" onclick="openHelpCenterModal()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                <span>Help Center</span>
              </div>
              <div class="p-card-divider"></div>
              <div class="p-card-item danger" onclick="handleSignOut()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                <span>Sign out</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main class="content">
        <div class="breadcrumbs" style="font-size:13px; margin-bottom:12px;">
          <span class="crumb" style="color:#64748b; font-weight:500;" id="breadcrumb-group">Financial Setup</span>
          <span style="color:#94a3b8; margin:0 4px;">·</span>
          <span class="crumb" style="color:#2f5eff; font-weight:600;" id="breadcrumb-page">Chart of Accounts</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:8px;">
          <h1 class="page-title" id="page-title" style="margin:0; font-size:24px; font-weight:700; color:#0f172a;">Loading...</h1>
        </div>
        <div id="page-content"></div>
      </main>
    </div>
  </div>
  <div id="globalModalContainer"></div>

  <script>
    const GROUPS  = {groups_json};
    const CONFIG  = {config_json};
    const CONTENT = {content_map_js};
    const ALL_GROUPS = Object.keys(GROUPS);

    let openTabs   = [ALL_GROUPS[0]];
    let activeGroup = ALL_GROUPS[0];
    let activePage  = GROUPS[activeGroup][0].id;

    function renderTopNav() {{
      const nav = document.getElementById('top-nav-links');
      let html = '';
      for (const g of openTabs) {{
        const active = g === activeGroup ? 'active' : '';
        const close  = (g === 'Financial Setup' || g === ALL_GROUPS[0]) ? '' : `<span class="close-btn" onclick="closeTab(event,'${{g}}')">&times;</span>`;
        html += `<a href="#" class="nav-tab ${{active}}" onclick="setGroup('${{g}}');return false;">${{g}}${{close}}</a>`;
      }}
      const closed = ALL_GROUPS.filter(g => !openTabs.includes(g));
      if (closed.length > 0) {{
        html += `<div class="dropdown"><a href="#" class="nav-tab" style="padding:8px 14px;">Other <svg style="width:14px;height:14px;vertical-align:middle;margin-left:2px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></a><div class="dropdown-content">`;
        for (const g of closed) html += `<a href="#" onclick="addTab('${{g}}');return false;">+ ${{g}}</a>`;
        html += `</div></div>`;
      }}
      nav.innerHTML = html;
    }}

    function renderSidebar() {{
      const sb = document.getElementById('sidebar-menu-container');
      const pages = GROUPS[activeGroup] || [];
      let html = `<div style="font-size:10px; font-weight:700; letter-spacing:0.5px; color:#64748b; padding:0 16px 8px 16px; text-transform:uppercase;">${{activeGroup}}</div>`;
      for (const p of pages) {{
        const active = p.id === activePage ? 'background:#1e2d42; color:#fff; font-weight:600; border-left:3px solid #2f5eff;' : 'color:#cbd5e1;';
        const icon = `<svg style="width:16px; height:16px; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>`;
        html += `<a href="#" style="display:flex; align-items:center; gap:8px; padding:6px 16px; font-size:12px; text-decoration:none; transition:all 0.15s; ${{active}}" onclick="setPage('${{p.id}}');return false;">${{icon}}<span>${{p.title}}</span></a>`;
      }}
      sb.innerHTML = html;
    }}


    function initERPGrid(cardEl) {{
    function generateAutoKey(header) {{
      const rand = Math.floor(1000 + Math.random() * 9000);
      const clean = header.toLowerCase().replace(/[^a-z0-9#]/g, '');
      if (clean.includes('tag')) return `AST-2026-${{rand}}`;
      if (clean.includes('wo') || clean.includes('workorder')) return `WO-2026-${{rand}}`;
      if (clean.includes('tracking') || clean.includes('ref')) return `TRK-2026-${{rand}}`;
      if (clean.includes('location') && clean.includes('id')) return `LOC-2026-${{rand}}`;
      if (clean.includes('category') && clean.includes('id')) return `CAT-2026-${{rand}}`;
      if (clean.includes('vendor') && clean.includes('id')) return `VND-2026-${{rand}}`;
      if (clean.includes('method') && clean.includes('id')) return `DEP-2026-${{rand}}`;
      if (clean.includes('lead') && clean.includes('id')) return `LD-2026-${{rand}}`;
      if (clean.includes('opp') && clean.includes('id')) return `OPP-2026-${{rand}}`;
      if (clean.includes('inv') || clean.includes('invoice')) return `INV-2026-${{rand}}`;
      if (clean.includes('po#') || clean.includes('purchaseorder')) return `PO-2026-${{rand}}`;
      if (clean.includes('so#') || clean.includes('salesorder')) return `SO-2026-${{rand}}`;
      if (clean.includes('project') && clean.includes('id')) return `PRJ-2026-${{rand}}`;
      if (clean.includes('task') && clean.includes('id')) return `TSK-2026-${{rand}}`;
      if (clean.includes('bom') && clean.includes('id')) return `BOM-2026-${{rand}}`;
      if (clean.includes('item') && clean.includes('code')) return `ITM-2026-${{rand}}`;
      return null;
    }}

    const table = cardEl.querySelector('.data-table');
      if (!table) return;
      
      const tbody = table.querySelector('tbody');
      if (!tbody) return;
      
      const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
      const allRows = Array.from(tbody.querySelectorAll('tr')).map(tr => {{
        return {{
          element: tr,
          cells: Array.from(tr.querySelectorAll('td')).map(td => td.innerHTML)
        }};
      }});
      
      let filteredRows = [...allRows];
      let currentPage = 1;
      const itemsPerPage = 15;
      
      const searchInput = cardEl.querySelector('.search-box input');
      const filterBtn = cardEl.querySelector('.toolbar-left button:nth-of-type(1)');
      const columnsBtn = cardEl.querySelector('.toolbar-left button:nth-of-type(2)');
      const refreshBtn = cardEl.querySelector('.toolbar-right button:nth-of-type(1)');
      const exportBtn = cardEl.querySelector('.toolbar-right button:nth-of-type(2)');
      const createBtn = cardEl.querySelector('.toolbar-right button:nth-of-type(3)');
      const paginationDiv = cardEl.querySelector('.pagination');
      
      // Columns toggle menu
      if (columnsBtn) {{
        columnsBtn.style.position = 'relative';
        columnsBtn.addEventListener('click', (e) => {{
          e.stopPropagation();
          let dropdown = cardEl.querySelector('.columns-dropdown');
          if (dropdown) {{
            dropdown.remove();
            return;
          }}
          
          dropdown = document.createElement('div');
          dropdown.className = 'columns-dropdown';
          dropdown.style.cssText = 'position:absolute; top:100%; left:0; background:#fff; border:1px solid #cbd5e1; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.1); z-index:1000; padding:8px; min-width:180px; margin-top:4px; text-align:left;';
          dropdown.addEventListener('click', (e) => e.stopPropagation());
          
          headers.forEach((h, idx) => {{
            if (h === 'Actions') return;
            const item = document.createElement('label');
            item.style.cssText = 'display:flex; align-items:center; gap:8px; padding:6px 8px; cursor:pointer; font-size:12px; color:#334155; font-weight:500;';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            const th = table.querySelector(`thead th:nth-child(${{idx + 1}})`);
            const isVisible = th.style.display !== 'none';
            checkbox.checked = isVisible;
            checkbox.addEventListener('change', () => {{
              th.style.display = checkbox.checked ? '' : 'none';
              table.querySelectorAll(`tbody tr`).forEach(tr => {{
                const td = tr.cells[idx];
                if (td) td.style.display = checkbox.checked ? '' : 'none';
              }});
            }});
            item.appendChild(checkbox);
            item.appendChild(document.createTextNode(h));
            dropdown.appendChild(item);
          }});
          
          columnsBtn.appendChild(dropdown);
        }});
        
        document.addEventListener('click', () => {{
          const dropdown = cardEl.querySelector('.columns-dropdown');
          if (dropdown) dropdown.remove();
        }});
      }}
      
      // Filter functionality
      let activeFilterCol = null;
      let activeFilterVal = null;
      
      if (filterBtn) {{
        filterBtn.style.position = 'relative';
        filterBtn.addEventListener('click', (e) => {{
          e.stopPropagation();
          let dropdown = cardEl.querySelector('.filter-dropdown');
          if (dropdown) {{
            dropdown.remove();
            return;
          }}
          
          dropdown = document.createElement('div');
          dropdown.className = 'filter-dropdown';
          dropdown.style.cssText = 'position:absolute; top:100%; left:0; background:#fff; border:1px solid #cbd5e1; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.1); z-index:1000; padding:8px; min-width:200px; margin-top:4px; text-align:left;';
          dropdown.addEventListener('click', (e) => e.stopPropagation());
          
          const filterableCols = [];
          headers.forEach((h, idx) => {{
            if (['Category', 'Location', 'Health / Condition', 'Priority', 'Status'].includes(h)) {{
              filterableCols.push({{ name: h, index: idx }});
            }}
          }});
          
          if (filterableCols.length === 0) {{
            dropdown.innerHTML = '<div style="font-size:12px; padding:6px; color:#64748b;">No filterable columns</div>';
          }} else {{
            const selectCol = document.createElement('select');
            selectCol.style.cssText = 'width:100%; padding:6px; border:1px solid #cbd5e1; border-radius:4px; font-size:12px; margin-bottom:8px; outline:none; background:#fff;';
            filterableCols.forEach(col => {{
              const opt = document.createElement('option');
              opt.value = col.index;
              opt.textContent = col.name;
              selectCol.appendChild(opt);
            }});
            
            const valContainer = document.createElement('div');
            valContainer.style.cssText = 'max-height:150px; overflow-y:auto;';
            
            function updateFilterVals() {{
              valContainer.innerHTML = '';
              const colIdx = parseInt(selectCol.value);
              const uniqueVals = new Set();
              allRows.forEach(row => {{
                const text = row.element.cells[colIdx].textContent.replace(/<[^>]*>/g, '').trim();
                if (text) uniqueVals.add(text);
              }});
              
              const clearItem = document.createElement('div');
              clearItem.style.cssText = 'padding:6px 8px; font-size:12px; cursor:pointer; color:#ef4444; font-weight:600;';
              clearItem.textContent = '✖ Clear Filter';
              clearItem.addEventListener('click', () => {{
                activeFilterCol = null;
                activeFilterVal = null;
                filterBtn.style.background = '';
                filterBtn.style.color = '';
                dropdown.remove();
                applyAllFilters();
              }});
              valContainer.appendChild(clearItem);
              
              uniqueVals.forEach(val => {{
                const item = document.createElement('div');
                item.style.cssText = 'padding:6px 8px; font-size:12px; cursor:pointer; color:#334155; border-radius:4px;';
                if (activeFilterCol === colIdx && activeFilterVal === val) {{
                  item.style.background = '#2f5eff';
                  item.style.color = '#fff';
                }}
                item.textContent = val;
                item.addEventListener('mouseenter', () => {{
                  if (!(activeFilterCol === colIdx && activeFilterVal === val)) {{
                    item.style.background = '#f1f5f9';
                  }}
                }});
                item.addEventListener('mouseleave', () => {{
                  if (!(activeFilterCol === colIdx && activeFilterVal === val)) {{
                    item.style.background = '';
                  }}
                }});
                item.addEventListener('click', () => {{
                  activeFilterCol = colIdx;
                  activeFilterVal = val;
                  filterBtn.style.background = '#2f5eff';
                  filterBtn.style.color = '#fff';
                  dropdown.remove();
                  applyAllFilters();
                }});
                valContainer.appendChild(item);
              }});
            }}
            
            selectCol.addEventListener('change', updateFilterVals);
            dropdown.appendChild(selectCol);
            dropdown.appendChild(valContainer);
            updateFilterVals();
          }}
          
          filterBtn.appendChild(dropdown);
        }});
        
        document.addEventListener('click', () => {{
          const dropdown = cardEl.querySelector('.filter-dropdown');
          if (dropdown) dropdown.remove();
        }});
      }}
      
      // Search Box Event
      if (searchInput) {{
        searchInput.removeAttribute('oninput');
        searchInput.addEventListener('input', () => {{
          applyAllFilters();
        }});
      }}
      
      // Global Apply Filter
      function applyAllFilters() {{
        const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
        
        filteredRows = allRows.filter(row => {{
          if (activeFilterCol !== null && activeFilterVal !== null) {{
            const cellText = row.element.cells[activeFilterCol].textContent.trim();
            if (cellText !== activeFilterVal) return false;
          }}
          
          if (q !== '') {{
            const match = row.cells.some(cellText => {{
              const plain = cellText.replace(/<[^>]*>/g, '').toLowerCase();
              return plain.includes(q);
            }});
            if (!match) return false;
          }}
          
          return true;
        }});
        
        showPage(1);
      }}
      
      // Refresh Functionality
      if (refreshBtn) {{
        refreshBtn.addEventListener('click', () => {{
          const overlay = document.createElement('div');
          overlay.style.cssText = 'position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(255,255,255,0.7); display:flex; align-items:center; justify-content:center; z-index:100;';
          overlay.innerHTML = '<div style="width:24px; height:24px; border:3px solid #cbd5e1; border-top-color:#2f5eff; border-radius:50%; animation:spin 0.6s linear infinite;"></div>';
          
          const style = document.createElement('style');
          style.innerHTML = '@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}';
          document.head.appendChild(style);
          
          table.style.position = 'relative';
          table.appendChild(overlay);
          
          setTimeout(() => {{
            overlay.remove();
            if (searchInput) searchInput.value = '';
            activeFilterCol = null;
            activeFilterVal = null;
            if (filterBtn) {{
              filterBtn.style.background = '';
              filterBtn.style.color = '';
            }}
            applyAllFilters();
          }}, 400);
        }});
      }}
      
      // Export Functionality
      if (exportBtn) {{
        exportBtn.addEventListener('click', () => {{
          const csvHeaders = headers.filter((h, idx) => {{
            const th = table.querySelector(`thead th:nth-child(${{idx + 1}})`);
            return th && th.style.display !== 'none' && h !== 'Actions';
          }}).map(h => `"${{h.replace(/"/g, '""')}}"`).join(',');
          
          const csvRows = filteredRows.map(row => {{
            return headers.map((h, idx) => {{
              const th = table.querySelector(`thead th:nth-child(${{idx + 1}})`);
              if (!th || th.style.display === 'none' || h === 'Actions') return null;
              const cellText = row.element.cells[idx].textContent.trim();
              return `"${{cellText.replace(/"/g, '""')}}"`;
            }}).filter(val => val !== null).join(',');
          }}).join('\\n');
          
          const csvContent = "data:text/csv;charset=utf-8," + csvHeaders + "\\n" + csvRows;
          const encodedUri = encodeURI(csvContent);
          const link = document.createElement("a");
          link.setAttribute("href", encodedUri);
          link.setAttribute("download", `export.csv`);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }});
      }}
      
      // View Item Modal
      function openViewModal(row) {{
        let modal = document.getElementById('erpViewModal');
        if (modal) modal.remove();
        
        modal = document.createElement('div');
        modal.id = 'erpViewModal';
        modal.className = 'erp-modal-overlay';
        
        let detailsFields = '';
        headers.forEach((h, idx) => {{
          if (h === 'Actions') return;
          const val = row.element.cells[idx].innerHTML;
          detailsFields += `
            <div style="margin-bottom:14px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">
              <span style="display:block; font-size:11px; font-weight:600; color:#64748b; text-transform:uppercase; margin-bottom:2px;">${{h}}</span>
              <span style="font-size:13px; color:#1e293b; font-weight:500;">${{val}}</span>
            </div>
          `;
        }});
        
        modal.innerHTML = `
          <div class="erp-modal-card" style="width:400px; padding:20px; box-sizing:border-box; background:#fff; border-radius:12px; box-shadow:0 20px 25px -5px rgba(0,0,0,0.1);">
            <h3 style="margin:0 0 16px 0; font-size:16px; font-weight:700; color:#0f172a; border-bottom:2px solid #2f5eff; padding-bottom:8px;">Record Details</h3>
            <div style="max-height:400px; overflow-y:auto; margin-bottom:20px; padding-right:4px;">
              ${{detailsFields}}
            </div>
            <div style="display:flex; justify-content:flex-end;">
              <button onclick="document.getElementById('erpViewModal').remove()" class="btn btn-primary" style="padding:6px 16px; font-size:12px;">Close</button>
            </div>
          </div>
        `;
        
        document.body.appendChild(modal);
      }}

      // Edit Item Modal
      function openEditModal(row) {{
        let modal = document.getElementById('erpEditModal');
        if (modal) modal.remove();
        
        modal = document.createElement('div');
        modal.id = 'erpEditModal';
        modal.className = 'erp-modal-overlay';
        
        let formFields = '';
        headers.forEach((h, idx) => {{
          if (['Actions', 'Tag ID', 'WO #', 'Tracking Ref', 'Status', 'Alert Status'].includes(h)) return;
          const currentVal = row.element.cells[idx].textContent.trim();
          formFields += `
            <div style="margin-bottom:12px;">
              <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:4px;">${{h}}</label>
              <input type="text" name="col_${{idx}}" value="${{currentVal.replace(/"/g, '&quot;')}}" style="width:100%; padding:8px 10px; border:1px solid #cbd5e1; border-radius:6px; font-size:12px; outline:none; box-sizing:border-box;">
            </div>
          `;
        }});
        
        modal.innerHTML = `
          <div class="erp-modal-card" style="width:400px; padding:20px; box-sizing:border-box; background:#fff; border-radius:12px;">
            <h3 style="margin:0 0 16px 0; font-size:16px; font-weight:700; color:#0f172a;">Edit ${{CONFIG[activePage].title}}</h3>
            <form id="erpEditForm">
              \FormFields
              <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:20px;">
                <button type="button" class="btn btn-outline" onclick="document.getElementById('erpEditModal').remove()" style="padding:6px 12px; font-size:12px;">Cancel</button>
                <button type="submit" class="btn btn-primary" style="padding:6px 12px; font-size:12px;">Save Changes</button>
              </div>
            </form>
          </div>
        `.replace('\\FormFields', formFields);
        
        document.body.appendChild(modal);
        
        modal.querySelector('#erpEditForm').addEventListener('submit', (e) => {{
          e.preventDefault();
          
          headers.forEach((h, idx) => {{
            if (['Actions', 'Tag ID', 'WO #', 'Tracking Ref', 'Status', 'Alert Status'].includes(h)) return;
            const newVal = modal.querySelector(`input[name="col_${{idx}}"]`).value || '—';
            row.element.cells[idx].textContent = newVal;
          }});
          
          row.cells = Array.from(row.element.querySelectorAll('td')).map(td => td.innerHTML);
          
          modal.remove();
          applyAllFilters();
        }});
      }}

      // Create New Item Modal
      if (createBtn) {{
        createBtn.addEventListener('click', () => {{
          let modal = document.getElementById('erpCreateModal');
          if (modal) modal.remove();
          
          modal = document.createElement('div');
          modal.id = 'erpCreateModal';
          modal.className = 'erp-modal-overlay';
          
          let formFields = '';
          headers.forEach((h, idx) => {{
            if (['Actions', 'Tag ID', 'WO #', 'Tracking Ref', 'Status', 'Alert Status'].includes(h)) return;
            formFields += `
              <div style="margin-bottom:12px;">
                <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:4px;">${{h}}</label>
                <input type="text" name="col_${{idx}}" style="width:100%; padding:8px 10px; border:1px solid #cbd5e1; border-radius:6px; font-size:12px; outline:none; box-sizing:border-box;">
              </div>
            `;
          }});
          
          modal.innerHTML = `
            <div class="erp-modal-card" style="width:400px; padding:20px; box-sizing:border-box; background:#fff;">
              <h3 style="margin:0 0 16px 0; font-size:16px; font-weight:700; color:#0f172a;">Create New ${{CONFIG[activePage].title}}</h3>
              <form id="erpCreateForm">
                \FormFields
                <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:20px;">
                  <button type="button" class="btn btn-outline" onclick="document.getElementById('erpCreateModal').remove()" style="padding:6px 12px; font-size:12px;">Cancel</button>
                  <button type="submit" class="btn btn-primary" style="padding:6px 12px; font-size:12px;">Save Record</button>
                </div>
              </form>
            </div>
          `.replace('\\FormFields', formFields);
          
          document.body.appendChild(modal);
          
          modal.querySelector('#erpCreateForm').addEventListener('submit', (e) => {{
            e.preventDefault();
            const newTr = document.createElement('tr');
            
            headers.forEach((h, idx) => {{
              const td = document.createElement('td');
              const th = table.querySelector(`thead th:nth-child(${{idx + 1}})`);
              if (th && th.style.display === 'none') {{
                td.style.display = 'none';
              }}
              
              if (h === 'Actions') {{
                td.innerHTML = `
                  <div class="action-icons">
                    <svg title="View" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                    <svg title="Edit" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 2 2h14a2 2 0 0 2 2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    <svg class="delete" title="Delete" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                  </div>
                `;
              }} else if (['Tag ID', 'WO #', 'Tracking Ref'].includes(h)) {{
                const randNum = Math.floor(1000 + Math.random() * 9000);
                td.textContent = h === 'Tag ID' ? `AST-2026-${{randNum}}` : (h === 'WO #' ? `WO-2026-${{randNum}}` : `TRK-${{randNum}}`);
              }} else if (['Status', 'Alert Status'].includes(h)) {{
                td.innerHTML = '<span class="status-badge status-active">✔ In Use / Normal</span>';
              }} else {{
                const inputVal = modal.querySelector(`input[name="col_${{idx}}"]`).value || '—';
                td.textContent = inputVal;
              }}
              newTr.appendChild(td);
            }});
            
            tbody.appendChild(newTr);
            allRows.push({{
              element: newTr,
              cells: Array.from(newTr.querySelectorAll('td')).map(td => td.innerHTML)
            }});
            
            modal.remove();
            applyAllFilters();
            
            const newTotalPages = Math.ceil(filteredRows.length / itemsPerPage);
            showPage(newTotalPages);
          }});
        }});
      }}
      
      // Page Renderer
      function showPage(page) {{
        currentPage = page;
        const totalRows = filteredRows.length;
        const totalPages = Math.ceil(totalRows / itemsPerPage);
        const start = (page - 1) * itemsPerPage;
        const end = Math.min(start + itemsPerPage, totalRows);
        
        allRows.forEach(row => {{
          row.element.style.display = 'none';
        }});
        
        filteredRows.forEach((row, idx) => {{
          if (idx >= start && idx < end) {{
            row.element.style.display = '';
            headers.forEach((h, colIdx) => {{
              const th = table.querySelector(`thead th:nth-child(${{colIdx + 1}})`);
              const td = row.element.cells[colIdx];
              if (td && th) {{
                td.style.display = th.style.display;
              }}
            }});
          }}
        }});
        
        // Wire row actions directly
        filteredRows.forEach(row => {{
          const viewBtn = row.element.querySelector('.action-icons svg:nth-of-type(1)');
          if (viewBtn && !viewBtn.dataset.wired) {{
            viewBtn.dataset.wired = 'true';
            viewBtn.addEventListener('click', (e) => {{
              e.stopPropagation();
              openViewModal(row);
            }});
          }}
          
          const editBtn = row.element.querySelector('.action-icons svg:nth-of-type(2)');
          if (editBtn && !editBtn.dataset.wired) {{
            editBtn.dataset.wired = 'true';
            editBtn.addEventListener('click', (e) => {{
              e.stopPropagation();
              openEditModal(row);
            }});
          }}
          
          const delBtn = row.element.querySelector('.action-icons svg.delete');
          if (delBtn && !delBtn.dataset.wired) {{
            delBtn.dataset.wired = 'true';
            delBtn.addEventListener('click', (e) => {{
              e.stopPropagation();
              if (confirm('Are you sure you want to delete this record?')) {{
                row.element.remove();
                const indexAll = allRows.indexOf(row);
                if (indexAll > -1) allRows.splice(indexAll, 1);
                const indexFilter = filteredRows.indexOf(row);
                if (indexFilter > -1) filteredRows.splice(indexFilter, 1);
                applyAllFilters();
              }}
            }});
          }}
        }});
        
        const infoDiv = paginationDiv.firstElementChild;
        if (infoDiv) {{
          if (totalRows === 0) {{
            infoDiv.textContent = 'Showing 0 to 0 of 0 entries';
          }} else {{
            infoDiv.textContent = `Showing ${{start + 1}} to ${{end}} of ${{totalRows}} entries`;
          }}
        }}
        
        const controlsDiv = paginationDiv.querySelector('.pagination-controls');
        if (controlsDiv) {{
          let controlsHtml = '';
          controlsHtml += `<button class="page-btn prev-btn" ${{page === 1 ? 'disabled style="opacity:0.5; cursor:default;"' : ''}}><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg></button>`;
          
          const maxVisiblePages = 5;
          let startPage = Math.max(1, page - Math.floor(maxVisiblePages / 2));
          let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
          if (endPage - startPage + 1 < maxVisiblePages) {{
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
          }}
          
          for (let i = startPage; i <= endPage; i++) {{
            controlsHtml += `<button class="page-btn num-btn ${{i === page ? 'active' : ''}}">${{i}}</button>`;
          }}
          
          controlsHtml += `<button class="page-btn next-btn" ${{page === totalPages || totalPages === 0 ? 'disabled style="opacity:0.5; cursor:default;"' : ''}}><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></button>`;
          
          controlsDiv.innerHTML = controlsHtml;
          
          controlsDiv.querySelectorAll('.num-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
              const p = parseInt(btn.textContent);
              showPage(p);
            }});
          }});
          
          const prevBtn = controlsDiv.querySelector('.prev-btn');
          if (prevBtn && page > 1) {{
            prevBtn.addEventListener('click', () => showPage(page - 1));
          }}
          
          const nextBtn = controlsDiv.querySelector('.next-btn');
          if (nextBtn && page < totalPages) {{
            nextBtn.addEventListener('click', () => showPage(page + 1));
          }}
        }}
      }}
      
      showPage(1);
    }}

    function renderContent() {{
      const info = CONFIG[activePage];
      if (!info) return;
      document.getElementById('breadcrumb-group').innerText = info.group;
      document.getElementById('breadcrumb-page').innerText  = info.title;
      document.getElementById('page-title').innerText       = info.title;
      const el = document.getElementById('page-content');
      if (CONTENT[activePage]) {{
        el.innerHTML = CONTENT[activePage];
        el.querySelectorAll('.card').forEach(card => {{
          initERPGrid(card);
        }});
      }} else {{
        el.innerHTML = `<div class="card" style="padding:40px; text-align:center; color:#94a3b8;">
          <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:12px;"><rect x="3" y="3" width="18" height="18" rx="2"></rect><path d="M3 9h18M9 21V9"></path></svg>
          <div style="font-size:16px; font-weight:600; color:#475569; margin-bottom:6px;">${{info.title}}</div>
          <div style="font-size:13px;">This screen is being built. Route: ${{info.url}}</div>
        </div>`;
      }}
    }}

    function setGroup(g) {{ activeGroup = g; activePage = GROUPS[g][0].id; renderTopNav(); renderSidebar(); renderContent(); }}
    function addTab(g)   {{ if (!openTabs.includes(g)) openTabs.push(g); setGroup(g); }}
    function closeTab(e, g) {{
      e.stopPropagation();
      if (g === 'Financial Setup' || g === ALL_GROUPS[0]) return;
      if (openTabs.length <= 1) return;
      openTabs = openTabs.filter(x => x !== g);
      if (activeGroup === g) {{ activeGroup = openTabs[openTabs.length-1]; activePage = GROUPS[activeGroup][0].id; }}
      renderTopNav(); renderSidebar(); renderContent();
    }}
    function setPage(id) {{ activePage = id; renderSidebar(); renderContent(); }}

    function toggleProfileMenu(e) {{
      e.stopPropagation();
      const card = document.getElementById('profileDropdownCard');
      if (card) card.classList.toggle('show');
    }}

    document.addEventListener('click', (e) => {{
      const container = document.getElementById('profileMenuContainer');
      const card = document.getElementById('profileDropdownCard');
      if (container && card && !container.contains(e.target)) {{
        card.classList.remove('show');
      }}
    }});

    function openProfileModal() {{
      const card = document.getElementById('profileDropdownCard');
      if (card) card.classList.remove('show');
      const container = document.getElementById('globalModalContainer');
      container.innerHTML = `
        <div class="erp-modal-overlay" onclick="closeGlobalModal(event)">
          <div class="erp-modal-card" onclick="event.stopPropagation()" style="padding:28px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid #e2e8f0; padding-bottom:14px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div style="width:52px; height:52px; border-radius:50%; background:#e0e7ff; color:#3730a3; font-weight:700; font-size:18px; display:flex; align-items:center; justify-content:center; border:2px solid #c7d2fe;">FA</div>
                <div>
                  <h2 style="margin:0; font-size:18px; font-weight:700; color:#0f172a;">Tariq Mansoor</h2>
                  <div style="font-size:13px; color:#64748b; font-weight:500;">Chief Financial Officer (CFO) · Employee ID: EMP-1002</div>
                </div>
              </div>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div class="form-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">First Name</label><input type="text" value="Tariq" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Last Name</label><input type="text" value="Mansoor" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Email Address</label><input type="email" value="tariq.mansoor@company.com" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Phone Number</label><input type="text" value="+966 50 112 3344" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Department</label><input type="text" value="Corporate Finance &amp; Treasury" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Role Level</label><input type="text" value="CFO / Executive Admin (Level 6)" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
            </div>
            <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:24px;">
              <button onclick="closeGlobalModal()" class="btn btn-outline">Cancel</button>
              <button onclick="saveProfileData()" class="btn btn-primary">Save Profile Changes</button>
            </div>
          </div>
        </div>
      `;
    }}

    function openAccountSettingsModal() {{
      const card = document.getElementById('profileDropdownCard');
      if (card) card.classList.remove('show');
      const container = document.getElementById('globalModalContainer');
      container.innerHTML = `
        <div class="erp-modal-overlay" onclick="closeGlobalModal(event)">
          <div class="erp-modal-card" onclick="event.stopPropagation()" style="padding:28px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; border-bottom:1px solid #e2e8f0; padding-bottom:12px;">
              <h2 style="margin:0; font-size:17px; font-weight:700; color:#0f172a;">Account &amp; Security Settings</h2>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div style="margin-bottom:20px;">
              <div style="font-size:14px; font-weight:700; color:#0f172a; margin-bottom:10px;">Security &amp; Password</div>
              <div style="display:grid; grid-template-columns:1fr; gap:10px;">
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Current Password</label><input type="password" value="••••••••••••" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">New Password</label><input type="password" placeholder="Enter new strong password" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              </div>
            </div>
            <div style="border-top:1px solid #f1f5f9; padding-top:16px;">
              <div style="font-size:14px; font-weight:700; color:#0f172a;">Financial Preferences</div>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:8px;">
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Base Accounting Currency</label><select style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"><option>SAR - Saudi Riyal</option><option>USD - US Dollar</option><option>EUR - Euro</option></select></div>
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Posting Approval Workflow</label><select style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"><option>Two-Step Senior Approval</option><option>Direct Posting</option></select></div>
              </div>
            </div>
            <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:24px;">
              <button onclick="closeGlobalModal()" class="btn btn-outline">Cancel</button>
              <button onclick="saveAccountSettings()" class="btn btn-primary">Update Settings</button>
            </div>
          </div>
        </div>
      `;
    }}

    function openHelpCenterModal() {{
      const card = document.getElementById('profileDropdownCard');
      if (card) card.classList.remove('show');
      const container = document.getElementById('globalModalContainer');
      container.innerHTML = `
        <div class="erp-modal-overlay" onclick="closeGlobalModal(event)">
          <div class="erp-modal-card" onclick="event.stopPropagation()" style="padding:28px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; border-bottom:1px solid #e2e8f0; padding-bottom:12px;">
              <h2 style="margin:0; font-size:17px; font-weight:700; color:#0f172a;">Finance &amp; Accounting Help Center</h2>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div style="margin-bottom:16px;">
              <input type="text" placeholder="Search VAT return guidelines, COA rules, AP aging reports..." style="width:100%; padding:10px 14px; border:1px solid #cbd5e1; border-radius:8px; font-size:13.5px;">
            </div>
            <div style="display:grid; grid-template-columns:1fr; gap:10px;">
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📑 ZATCA E-Invoicing &amp; VAT Tax Return Guide</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Filing quarterly tax returns and QR-code compliant XML formatting.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">💼 Month-End &amp; Year-End Closing Procedures</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Executing trial balance reconciliation, FX revaluation, and period locking.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📞 Contact Financial Systems Administrator</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Submit an urgent request or email finance.admin@company.com</div></div>
            </div>
            <div style="display:flex; justify-content:flex-end; margin-top:20px;">
              <button onclick="closeGlobalModal()" class="btn btn-primary">Close Help Center</button>
            </div>
          </div>
        </div>
      `;
    }}

    function closeGlobalModal(e) {{
      const container = document.getElementById('globalModalContainer');
      if (container) container.innerHTML = '';
    }}

    function saveProfileData() {{
      alert('Profile details updated successfully!');
      closeGlobalModal();
    }}

    function saveAccountSettings() {{
      alert('Account & Security settings saved!');
      closeGlobalModal();
    }}

    function handleSignOut() {{
      if (confirm('Are you sure you want to sign out of ExeonFinance ERP?')) {{
        window.location.href = 'login.html';
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{ handleUrlRoutingOnLoad(GROUPS); renderTopNav(); renderSidebar(); renderContent(); wireGlobalSearch('finance'); }});
  </script>
</body>
</html>
"""

with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\templates\finance.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("finance.html generated successfully!")
