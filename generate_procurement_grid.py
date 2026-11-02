import json
import os

# ─────────────────────────────────────────────
# NAVIGATION STRUCTURE (41 SCREENS IN 10 MODULES)
# ─────────────────────────────────────────────

GROUPS_NAV = {
    "Master Data": [
        {"id": "procurement_vendors", "title": "Vendor / Supplier Master", "url": "/procurement/vendors"},
        {"id": "vendors_onboarding", "title": "Vendor Onboarding / KYC", "url": "/vendors/onboarding"},
        {"id": "catalog_items", "title": "Item / Catalog Master", "url": "/catalog/items"},
        {"id": "budget_cost_centers", "title": "Cost Center / Budget Master", "url": "/budget/cost-centers"},
        {"id": "settings_approval_matrix", "title": "Approval Matrix Configuration", "url": "/settings/approval-matrix"},
    ],
    "Planning & Requisition": [
        {"id": "requisitions", "title": "Purchase Requisition (PR) List", "url": "/requisitions"},
        {"id": "requisitions_new", "title": "New Requisition", "url": "/requisitions/new"},
        {"id": "planning_mrp", "title": "MRP / Reorder Alerts", "url": "/planning/mrp"},
        {"id": "requisitions_budget_check", "title": "Budget Availability Check", "url": "/requisitions/budget-check"},
    ],
    "Sourcing": [
        {"id": "rfq", "title": "RFQ List", "url": "/rfq"},
        {"id": "rfq_new", "title": "Create RFQ", "url": "/rfq/new"},
        {"id": "rfq_compare", "title": "Vendor Quotation Comparison", "url": "/rfq/compare"},
        {"id": "tenders", "title": "Tender / Bid Management", "url": "/tenders"},
    ],
    "Contracts": [
        {"id": "contracts", "title": "Contract / Agreement List", "url": "/contracts"},
        {"id": "contracts_detail", "title": "Contract Detail", "url": "/contracts/CTR-0091"},
        {"id": "contracts_renewals", "title": "Contract Renewal & Expiry Tracker", "url": "/contracts/renewals"},
    ],
    "Purchase Orders": [
        {"id": "po", "title": "Purchase Order List", "url": "/po"},
        {"id": "po_new", "title": "New Purchase Order", "url": "/po/new"},
        {"id": "po_detail", "title": "PO Detail View", "url": "/po/PO-2026-00847"},
        {"id": "po_approval_queue", "title": "PO Approval Queue", "url": "/po/approval-queue"},
        {"id": "po_blanket", "title": "Blanket PO / Release Orders", "url": "/po/blanket"},
        {"id": "po_import", "title": "Import PO (International)", "url": "/po/import"},
    ],
    "Receiving": [
        {"id": "grn", "title": "Goods Receipt (GRN) List", "url": "/grn"},
        {"id": "grn_new", "title": "New Goods Receipt", "url": "/grn/new"},
        {"id": "grn_qc_inspection", "title": "Quality Inspection / QC Check", "url": "/grn/qc-inspection"},
        {"id": "grn_return_to_vendor", "title": "Return to Vendor (Debit Note)", "url": "/grn/return-to-vendor"},
    ],
    "Invoice & Payment": [
        {"id": "invoices", "title": "Vendor Invoice List", "url": "/invoices"},
        {"id": "invoices_3_way_match", "title": "3-Way Match (PO–GRN–Invoice)", "url": "/invoices/3-way-match"},
        {"id": "invoices_approval_queue", "title": "Invoice Approval Queue", "url": "/invoices/approval-queue"},
        {"id": "payments_schedule", "title": "Payment Scheduling", "url": "/payments/schedule"},
        {"id": "vendors_ledger", "title": "Vendor Ledger / Statement", "url": "/vendors/V-00412/ledger"},
    ],
    "Approvals": [
        {"id": "approvals_inbox", "title": "My Approvals Inbox", "url": "/approvals/inbox"},
        {"id": "approvals_history", "title": "Approval History / Audit Trail", "url": "/approvals/history"},
    ],
    "Analytics & Reporting": [
        {"id": "analytics_spend", "title": "Spend Analytics Dashboard", "url": "/analytics/spend"},
        {"id": "analytics_budget_vs_actual", "title": "Budget vs Actual Report", "url": "/analytics/budget-vs-actual"},
        {"id": "analytics_vendor_performance", "title": "Vendor Performance Report", "url": "/analytics/vendor-performance"},
        {"id": "analytics_po_aging", "title": "PO Aging / Overdue Report", "url": "/analytics/po-aging"},
        {"id": "analytics_savings", "title": "Savings / Cost Reduction Report", "url": "/analytics/savings"},
    ],
    "Administration": [
        {"id": "admin_roles", "title": "User Roles & Permissions", "url": "/admin/roles"},
        {"id": "admin_workflow_builder", "title": "Approval Workflow Builder", "url": "/admin/workflow-builder"},
        {"id": "admin_notifications", "title": "Notification / Alert Settings", "url": "/admin/notifications"},
        {"id": "admin_audit_log", "title": "Audit Log", "url": "/admin/audit-log"},
    ]
}

# ─────────────────────────────────────────────
# PAGE CONFIGURATIONS & MOCK DATA
# ─────────────────────────────────────────────

PAGE_CONFIGS = {
    # MASTER DATA
    "procurement_vendors": {
        "type": "list",
        "columns": ["Vendor Code", "Company Name", "Category", "Contact Person", "Email / Phone", "Rating", "Payment Terms", "Status", "Actions"],
        "rows": [
            {"Vendor Code": "VEND-00101", "Company Name": "Saudi Industrial Steel Co.", "Category": "Raw Materials", "Contact Person": "Fahad Al-Sulaiman", "Email / Phone": "f.sulaiman@saudisteel.com", "Rating": "★ 4.8", "Payment Terms": "Net 60", "Status": "active"},
            {"Vendor Code": "VEND-00102", "Company Name": "Arabian Timber & Wood Ltd.", "Category": "Lumber / Wood", "Contact Person": "Youssef Nabil", "Email / Phone": "y.nabil@arabiantimber.sa", "Rating": "★ 4.6", "Payment Terms": "Net 45", "Status": "active"},
            {"Vendor Code": "VEND-00103", "Company Name": "Global Hardware Components", "Category": "Hardware / Fasteners", "Contact Person": "Robert Chen", "Email / Phone": "r.chen@globalhardware.com", "Rating": "★ 4.2", "Payment Terms": "Net 30", "Status": "pending"},
            {"Vendor Code": "VEND-00104", "Company Name": "Gulf Upholstery & Leather", "Category": "Textiles / Fabrics", "Contact Person": "Nasser Al-Ghamdi", "Email / Phone": "nasser@gulfuph.com", "Rating": "★ 3.9", "Payment Terms": "Net 30", "Status": "blocked"},
        ]
    },
    "catalog_items": {
        "type": "list",
        "columns": ["Item Code", "Item Description", "Category", "Preferred Vendor", "Standard Cost", "Unit of Measure", "Reorder Level", "Status", "Actions"],
        "rows": [
            {"Item Code": "RM-STL-001", "Item Description": "Cold Rolled Steel Sheet 2.0mm", "Category": "Raw Metal", "Preferred Vendor": "Saudi Industrial Steel Co.", "Standard Cost": "450 SAR", "Unit of Measure": "Sheet", "Reorder Level": "200 Sheets", "Status": "active"},
            {"Item Code": "RM-WD-003", "Item Description": "Premium Grade Oak Plank 2x4", "Category": "Timber", "Preferred Vendor": "Arabian Timber & Wood Ltd.", "Standard Cost": "120 SAR", "Unit of Measure": "Piece", "Reorder Level": "150 Pcs", "Status": "active"},
            {"Item Code": "CM-SCR-012", "Item Description": "M6 Hex Head Stainless Bolt", "Category": "Hardware", "Preferred Vendor": "Global Hardware Components", "Standard Cost": "2.5 SAR", "Unit of Measure": "Box (100)", "Reorder Level": "50 Boxes", "Status": "active"},
        ]
    },
    "budget_cost_centers": {
        "type": "list",
        "columns": ["Cost Center Code", "Cost Center Name", "Department", "Annual Budget", "Committed Spend", "Available Balance", "Utilization %", "Status", "Actions"],
        "rows": [
            {"Cost Center Code": "CC-1001", "Cost Center Name": "Manufacturing Raw Materials", "Department": "Production", "Annual Budget": "5,000,000 SAR", "Committed Spend": "3,400,000 SAR", "Available Balance": "1,600,000 SAR", "Utilization %": "68%", "Status": "normal"},
            {"Cost Center Code": "CC-1002", "Cost Center Name": "Factory Maintenance & MRO", "Department": "Maintenance", "Annual Budget": "1,200,000 SAR", "Committed Spend": "1,104,000 SAR", "Available Balance": "96,000 SAR", "Utilization %": "92%", "Status": "overloaded"},
            {"Cost Center Code": "CC-1003", "Cost Center Name": "Corporate IT & Software", "Department": "Information Technology", "Annual Budget": "800,000 SAR", "Committed Spend": "328,000 SAR", "Available Balance": "472,000 SAR", "Utilization %": "41%", "Status": "underutilized"},
        ]
    },
    "settings_approval_matrix": {
        "type": "list",
        "columns": ["Matrix Code", "Document Type", "Value Min (SAR)", "Value Max (SAR)", "Primary Approver", "Escalation Role", "Auto-Escalation", "Status", "Actions"],
        "rows": [
            {"Matrix Code": "MAT-PO-01", "Document Type": "Purchase Order", "Value Min (SAR)": "0 SAR", "Value Max (SAR)": "50,000 SAR", "Primary Approver": "Procurement Manager", "Escalation Role": "Procurement Director", "Auto-Escalation": "24 Hours", "Status": "active"},
            {"Matrix Code": "MAT-PO-02", "Document Type": "Purchase Order", "Value Min (SAR)": "50,001 SAR", "Value Max (SAR)": "250,000 SAR", "Primary Approver": "Procurement Director", "Escalation Role": "VP Operations", "Auto-Escalation": "48 Hours", "Status": "active"},
            {"Matrix Code": "MAT-PO-03", "Document Type": "Purchase Order", "Value Min (SAR)": "250,001 SAR", "Value Max (SAR)": "Unlimited", "Primary Approver": "CFO & CEO", "Escalation Role": "Board Chair", "Auto-Escalation": "72 Hours", "Status": "active"},
        ]
    },

    # PLANNING & REQUISITION
    "requisitions": {
        "type": "list",
        "columns": ["PR Number", "Requester", "Department", "Cost Center", "Total Amount", "Required Date", "Items Count", "Status", "Actions"],
        "rows": [
            {"PR Number": "PR-2026-0841", "Requester": "Tariq Al-Harbi", "Department": "Manufacturing", "Cost Center": "CC-1001", "Total Amount": "145,000 SAR", "Required Date": "2026-08-01", "Items Count": "4 Line Items", "Status": "pending"},
            {"PR Number": "PR-2026-0840", "Requester": "Sami Mansoor", "Department": "Maintenance", "Cost Center": "CC-1002", "Total Amount": "28,500 SAR", "Required Date": "2026-07-28", "Items Count": "2 Line Items", "Status": "approved"},
            {"PR Number": "PR-2026-0839", "Requester": "Huda Otaibi", "Department": "Quality Assurance", "Cost Center": "CC-1004", "Total Amount": "12,000 SAR", "Required Date": "2026-07-25", "Items Count": "1 Line Item", "Status": "converted"},
        ]
    },

    # SOURCING
    "rfq": {
        "type": "list",
        "columns": ["RFQ Number", "Title / Requirement", "PR Reference", "Invited Vendors", "Quotations Received", "Closing Date", "Status", "Actions"],
        "rows": [
            {"RFQ Number": "RFQ-2026-0192", "Title / Requirement": "Q3 Steel Sheet Bulk Procurement", "PR Reference": "PR-2026-0841", "Invited Vendors": "4 Vendors", "Quotations Received": "3 Bids", "Closing Date": "2026-07-30", "Status": "open"},
            {"RFQ Number": "RFQ-2026-0191", "Title / Requirement": "CNC Spare Tooling Kits", "PR Reference": "PR-2026-0838", "Invited Vendors": "3 Vendors", "Quotations Received": "3 Bids", "Closing Date": "2026-07-22", "Status": "closed"},
        ]
    },

    # CONTRACTS
    "contracts": {
        "type": "list",
        "columns": ["Contract Code", "Vendor Name", "Contract Title", "Start Date", "Expiry Date", "Total Value (SAR)", "Renewal Alert", "Status", "Actions"],
        "rows": [
            {"Contract Code": "CTR-2026-0091", "Vendor Name": "Saudi Industrial Steel Co.", "Contract Title": "Annual Steel Sheet Supply Agreement", "Start Date": "2026-01-01", "Expiry Date": "2026-12-31", "Total Value (SAR)": "2,500,000 SAR", "Renewal Alert": "160 Days Left", "Status": "active"},
            {"Contract Code": "CTR-2025-0044", "Vendor Name": "Arabian Timber & Wood Ltd.", "Contract Title": "Lumber Supply Framework", "Start Date": "2025-08-15", "Expiry Date": "2026-08-15", "Total Value (SAR)": "950,000 SAR", "Renewal Alert": "⚠ 23 Days Left", "Status": "expiring"},
        ]
    },

    # PURCHASE ORDERS
    "po": {
        "type": "list",
        "columns": ["PO Number", "Vendor Name", "PO Date", "Delivery Date", "Order Amount", "PR Ref", "Payment Status", "Fulfillment Status", "Actions"],
        "rows": [
            {"PO Number": "PO-2026-00847", "Vendor Name": "Saudi Industrial Steel Co.", "PO Date": "2026-07-20", "Delivery Date": "2026-08-05", "Order Amount": "184,500 SAR", "PR Ref": "PR-0835", "Payment Status": "Unpaid", "Fulfillment Status": "pending"},
            {"PO Number": "PO-2026-00846", "Vendor Name": "Arabian Timber & Wood Ltd.", "PO Date": "2026-07-18", "Delivery Date": "2026-07-24", "Order Amount": "62,000 SAR", "PR Ref": "PR-0833", "Payment Status": "Partial", "Fulfillment Status": "completed"},
        ]
    },

    # RECEIVING
    "grn": {
        "type": "list",
        "columns": ["GRN Number", "PO Ref", "Vendor Name", "Receipt Date", "Received Qty", "Inspected Qty", "Accepted Qty", "QC Status", "Actions"],
        "rows": [
            {"GRN Number": "GRN-2026-0412", "PO Ref": "PO-2026-00846", "Vendor Name": "Arabian Timber & Wood Ltd.", "Receipt Date": "2026-07-22", "Received Qty": "150 Pcs", "Inspected Qty": "150 Pcs", "Accepted Qty": "148 Pcs", "QC Status": "approved"},
            {"GRN Number": "GRN-2026-0411", "PO Ref": "PO-2026-00842", "Vendor Name": "Global Hardware Components", "Receipt Date": "2026-07-21", "Received Qty": "50 Boxes", "Inspected Qty": "50 Boxes", "Accepted Qty": "45 Boxes", "QC Status": "partial"},
        ]
    },

    # INVOICE & PAYMENT
    "invoices": {
        "type": "list",
        "columns": ["Invoice Number", "Vendor Name", "PO Ref", "Invoice Date", "Due Date", "Total Amount", "3-Way Match", "Status", "Actions"],
        "rows": [
            {"Invoice Number": "INV-V-9921", "Vendor Name": "Arabian Timber & Wood Ltd.", "PO Ref": "PO-2026-00846", "Invoice Date": "2026-07-22", "Due Date": "2026-09-05", "Total Amount": "62,000 SAR", "3-Way Match": "✔ Matched", "Status": "approved"},
            {"Invoice Number": "INV-V-9920", "Vendor Name": "Global Hardware Components", "PO Ref": "PO-2026-00842", "Invoice Date": "2026-07-21", "Due Date": "2026-08-20", "Total Amount": "12,500 SAR", "3-Way Match": "⚠ Price Mismatch", "Status": "pending"},
        ]
    },

    # APPROVALS
    "approvals_inbox": {
        "type": "approval",
        "columns": ["Item ID", "Document Type", "Vendor / Requester", "Amount", "Submitted Date", "My Pending Role", "Status", "Actions"],
        "rows": [
            {"Item ID": "PO-2026-00847", "Document Type": "Purchase Order", "Vendor / Requester": "Saudi Industrial Steel Co.", "Amount": "184,500 SAR", "Submitted Date": "2026-07-20", "My Pending Role": "Procurement Manager", "Status": "pending"},
            {"Item ID": "PR-2026-0841", "Document Type": "Purchase Requisition", "Vendor / Requester": "Tariq Al-Harbi", "Amount": "145,000 SAR", "Submitted Date": "2026-07-22", "My Pending Role": "Department Head", "Status": "pending"},
        ]
    }
}

# ─────────────────────────────────────────────
# BADGE & ROW RENDERERS
# ─────────────────────────────────────────────
STATUS_BADGES = {
    "active":           ("status-active",       "Active"),
    "approved":         ("status-approved",     "✔ Approved"),
    "completed":        ("status-completed",    "Completed"),
    "converted":        ("status-converted",    "Converted"),
    "open":             ("status-open",         "Open"),
    "closed":           ("status-closed",       "Closed"),
    "pending":          ("status-pending",      "Pending"),
    "in_progress":      ("status-inprogress",   "In Progress"),
    "draft":            ("status-draft",        "Draft"),
    "blocked":          ("status-blocked",      "✖ Blocked"),
    "expiring":         ("status-expiring",     "⚠ Expiring"),
    "action_required":  ("status-actionreq",    "⚡ Action Required"),
    "overloaded":       ("status-overloaded",   "⚠ Overloaded"),
    "underutilized":    ("status-underutil",    "↓ Underutilized"),
    "normal":           ("status-active",       "Normal"),
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
        if col.lower() in ("status", "review status", "qc status", "fulfillment status"):
            val = render_badge(val)
        cells += f"<td>{val}</td>"
    cells += """
    <td>
      <div class="action-icons">
        <svg title="View" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
        <svg title="Edit" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        <svg class="delete" title="Delete" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
      </div>
    </td>"""
    return f"<tr>{cells}</tr>"

def render_approval_row(row, columns):
    cells = ""
    for col in columns:
        if col == "Actions":
            continue
        val = row.get(col, "—")
        if col.lower() in ("status", "review status"):
            val = render_badge(val)
        cells += f"<td>{val}</td>"
    cells += """
    <td>
      <div class="action-icons">
        <svg title="Approve" style="color:#22c55e;" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <svg title="Reject" style="color:#ef4444;" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        <svg title="View" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
      </div>
    </td>"""
    return f"<tr>{cells}</tr>"

def build_list_html(page_id, page_cfg, page_title):
    columns = page_cfg["columns"]
    rows_data = page_cfg["rows"]
    page_type = page_cfg.get("type", "list")

    header_cells = "".join(f"<th>{c}</th>" for c in columns)
    body_rows = ""
    for r in rows_data:
        if page_type == "approval":
            body_rows += render_approval_row(r, columns)
        else:
            body_rows += render_table_row(r, columns)

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
# BUILD CONTENT MAP FOR ALL 41 SCREENS
# ─────────────────────────────────────────────
content_map = {}

# Populate customized pages from PAGE_CONFIGS
for page_id, cfg in PAGE_CONFIGS.items():
    ptype = cfg.get("type", "list")
    title = page_id.replace("_", " ").title()
    if ptype == "list" or ptype == "approval":
        content_map[page_id] = build_list_html(page_id, cfg, title)

# Fallback populator for any remaining screens in GROUPS_NAV
for grp_name, page_list in GROUPS_NAV.items():
    for item in page_list:
        pid = item["id"]
        if pid not in content_map:
            t = item["title"]
            content_map[pid] = build_list_html(pid, {
                "type": "list",
                "columns": ["Record Code", "Title / Description", "Category", "Reference Code", "Date Created", "Status", "Actions"],
                "rows": [
                    {"Record Code": f"PRC-2026-001", "Title / Description": f"{t} Primary Entry", "Category": grp_name, "Reference Code": "REF-9901", "Date Created": "2026-07-22", "Status": "active"},
                    {"Record Code": f"PRC-2026-002", "Title / Description": f"{t} Operational Record", "Category": grp_name, "Reference Code": "REF-9902", "Date Created": "2026-07-20", "Status": "completed"},
                    {"Record Code": f"PRC-2026-003", "Title / Description": f"{t} Review Pending", "Category": grp_name, "Reference Code": "REF-9903", "Date Created": "2026-07-18", "Status": "pending"},
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

# Output procurement_output_data.json
nav_output = {"config": config_obj}
with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\procurement_output_data.json', 'w', encoding='utf-8') as f:
    json.dump(nav_output, f, indent=4)

# ─────────────────────────────────────────────
# GENERATE PROCUREMENT SPA HTML FILE
# ─────────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AureliaHRMS · Enterprise Procurement ERP</title>
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
    .user-avatar {{ width:34px; height:34px; background:#fef08a; color:#854d0e; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; cursor:pointer; border:2px solid #fef9c3; user-select:none; transition:all 0.2s ease; }}
    .user-avatar:hover {{ transform:scale(1.05); box-shadow:0 0 0 3px rgba(250,204,21,0.4); }}
    .profile-dropdown-card {{ position:absolute; top:46px; right:0; width:260px; background:#ffffff; border-radius:14px; box-shadow:0 12px 30px -4px rgba(0,0,0,0.15), 0 4px 12px -2px rgba(0,0,0,0.08); border:1px solid #e2e8f0; z-index:1000; display:none; padding:10px 0; transform-origin:top right; }}
    .profile-dropdown-card.show {{ display:block; animation:profilePop 0.18s cubic-bezier(0.16,1,0.3,1); }}
    @keyframes profilePop {{ 0% {{ opacity:0; transform:scale(0.92) translateY(-8px); }} 100% {{ opacity:1; transform:scale(1) translateY(0); }} }}
    .p-card-header {{ display:flex; align-items:center; gap:12px; padding:6px 18px 12px 18px; }}
    .p-card-avatar {{ width:48px; height:48px; border-radius:50%; background:#fef08a; color:#854d0e; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; flex-shrink:0; border:2px solid #fef9c3; }}
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
    .status-converted {{ background:#eaefff; color:#1f42c9; }}
    .status-open {{ background:#fdf3df; color:#b7791f; }}
    .status-closed {{ background:#f1f5f9; color:#64748b; }}
    .status-pending {{ background:#fdf3df; color:#b7791f; }}
    .status-inprogress {{ background:#eaefff; color:#1f42c9; }}
    .status-draft {{ background:#f1f5f9; color:#64748b; }}
    .status-blocked {{ background:#fdeceb; color:#c0362c; }}
    .status-expiring {{ background:#fdf3df; color:#b7791f; }}
    .status-actionreq {{ background:#fdeceb; color:#c0362c; }}
    .status-overloaded {{ background:#fdeceb; color:#c0362c; }}
    .status-underutil {{ background:#f1f5f9; color:#475569; }}
  </style>
</head>
<body>
  <div style="display:flex; width:100vw; height:100vh;">
    <!-- SIDEBAR -->
    <aside class="sidebar" style="width:200px; height:100vh; flex-shrink:0; display:flex; flex-direction:column; border-right:1px solid #1e2d42;">
      <div style="height:60px; padding:0 16px; display:flex; align-items:center; gap:8px; border-bottom:1px solid #1e2d42; box-sizing:border-box;">
        <div style="width:32px; height:32px; border-radius:8px; background:#2f5eff; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:16px;">P</div>
        <div>
          <div style="font-size:15px; font-weight:700; color:#fff; letter-spacing:-0.2px;">ExeonProcure</div>
          <div style="font-size:11px; color:#94a3b8;">Enterprise Procurement</div>
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
            <div class="user-avatar" id="profileAvatarBtn" onclick="toggleProfileMenu(event)">SR</div>
            <div class="profile-dropdown-card" id="profileDropdownCard">
              <div class="p-card-header">
                <div class="p-card-avatar">SR</div>
                <div class="p-card-info">
                  <div class="p-card-name">Salim Rahal</div>
                  <div class="p-card-role">Procurement Director</div>
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
          <span class="crumb" style="color:#64748b; font-weight:500;" id="breadcrumb-group">Procurement</span>
          <span style="color:#94a3b8; margin:0 4px;">·</span>
          <span class="crumb" style="color:#2f5eff; font-weight:600;" id="breadcrumb-page">Overview</span>
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
        const close  = (g === 'Master Data' || g === ALL_GROUPS[0]) ? '' : `<span class="close-btn" onclick="closeTab(event,'${{g}}')">&times;</span>`;
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
        const icon = `<svg style="width:16px; height:16px; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>`;
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
      if (g === 'Master Data' || g === ALL_GROUPS[0]) return;
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
                <div style="width:52px; height:52px; border-radius:50%; background:#fef08a; color:#854d0e; font-weight:700; font-size:18px; display:flex; align-items:center; justify-content:center; border:2px solid #fef9c3;">SR</div>
                <div>
                  <h2 style="margin:0; font-size:18px; font-weight:700; color:#0f172a;">Salim Rahal</h2>
                  <div style="font-size:13px; color:#64748b; font-weight:500;">Procurement Director · Employee ID: EMP-1002</div>
                </div>
              </div>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div class="form-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">First Name</label><input type="text" value="Salim" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Last Name</label><input type="text" value="Rahal" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Email Address</label><input type="email" value="salim.rahal@company.com" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Phone Number</label><input type="text" value="+966 50 123 4567" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Department</label><input type="text" value="Procurement &amp; Sourcing" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Role Level</label><input type="text" value="Procurement Director (Level 5)" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
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
              <div style="font-size:14px; font-weight:700; color:#0f172a; margin-bottom:10px;">System Preferences</div>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Interface Language</label><select style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"><option>English (US)</option><option>Arabic (العربية)</option></select></div>
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Email Alerts</label><select style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"><option>Enabled (Immediate)</option><option>Daily Digest</option></select></div>
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
              <h2 style="margin:0; font-size:17px; font-weight:700; color:#0f172a;">Procurement Help Center &amp; Support</h2>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div style="margin-bottom:16px;">
              <input type="text" placeholder="Search Procurement FAQs, 3-Way Match &amp; PO guides..." style="width:100%; padding:10px 14px; border:1px solid #cbd5e1; border-radius:8px; font-size:13.5px;">
            </div>
            <div style="display:grid; grid-template-columns:1fr; gap:10px;">
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📦 Requisition to Purchase Order Workflow</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">How to convert approved Purchase Requisitions into Purchase Orders.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">🔍 3-Way Matching &amp; Invoice Clearance</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Resolving quantity &amp; price variances between PO, GRN, and Vendor Invoice.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📞 Contact Enterprise Procurement Helpdesk</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Submit a support ticket or contact procurement.support@company.com</div></div>
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
      if (confirm('Are you sure you want to sign out of ExeonProcure ERP?')) {{
        window.location.href = 'login.html';
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{ handleUrlRoutingOnLoad(GROUPS); renderTopNav(); renderSidebar(); renderContent(); wireGlobalSearch('procurement'); }});
  </script>
</body>
</html>
"""

with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\templates\procurement.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("procurement.html generated successfully!")
