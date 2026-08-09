import json
import os

# ─────────────────────────────────────────────
# SERVICE DESK ERP NAVIGATION (34 SCREENS / 10 MODULES)
# ─────────────────────────────────────────────

GROUPS_NAV = {
    "Setup & Master Data": [
        {"id": "servicedesk_catalog", "title": "Service Catalog", "url": "/servicedesk/catalog"},
        {"id": "servicedesk_sla_policies", "title": "SLA Policy Master", "url": "/servicedesk/sla-policies"},
        {"id": "servicedesk_categories", "title": "Category / Priority Master", "url": "/servicedesk/categories"},
        {"id": "servicedesk_teams", "title": "Team / Group Master", "url": "/servicedesk/teams"},
        {"id": "servicedesk_customers", "title": "Customer / Contact Master", "url": "/servicedesk/customers"},
    ],
    "Ticket Management": [
        {"id": "servicedesk_tickets", "title": "Ticket List (All Tickets)", "url": "/servicedesk/tickets"},
        {"id": "servicedesk_tickets_new", "title": "New Ticket Form", "url": "/servicedesk/tickets/new"},
        {"id": "servicedesk_ticket_detail", "title": "Ticket Detail View", "url": "/servicedesk/tickets/TCK-88213"},
        {"id": "servicedesk_my_tickets", "title": "My Tickets (Agent View)", "url": "/servicedesk/my-tickets"},
        {"id": "servicedesk_triage_queue", "title": "Ticket Queue / Triage", "url": "/servicedesk/triage-queue"},
    ],
    "Self-Service Portal": [
        {"id": "portal_home", "title": "Customer Portal Home", "url": "/portal/home"},
        {"id": "portal_kb_article", "title": "Knowledge Base Article (Public)", "url": "/portal/kb/how-to-reset-password"},
        {"id": "portal_submit_request", "title": "Submit Request Form", "url": "/portal/submit-request"},
    ],
    "Knowledge Base": [
        {"id": "servicedesk_kb_articles", "title": "KB Article List", "url": "/servicedesk/kb/articles"},
        {"id": "servicedesk_kb_editor", "title": "New Article Editor", "url": "/servicedesk/kb/editor"},
        {"id": "servicedesk_kb_analytics", "title": "KB Analytics", "url": "/servicedesk/kb/analytics"},
    ],
    "SLA & Escalation": [
        {"id": "servicedesk_sla_compliance", "title": "SLA Compliance Dashboard", "url": "/servicedesk/sla-compliance"},
        {"id": "servicedesk_escalation_rules", "title": "Escalation Rules Configuration", "url": "/servicedesk/escalation-rules"},
        {"id": "servicedesk_breach_alerts", "title": "SLA Breach Alerts", "url": "/servicedesk/breach-alerts"},
    ],
    "Automation & Workflow": [
        {"id": "servicedesk_automation_builder", "title": "Workflow / Automation Builder", "url": "/servicedesk/automation-builder"},
        {"id": "servicedesk_canned_responses", "title": "Canned Responses / Macros", "url": "/servicedesk/canned-responses"},
        {"id": "servicedesk_routing_rules", "title": "Ticket Routing Rules", "url": "/servicedesk/routing-rules"},
    ],
    "Communication & Collaboration": [
        {"id": "servicedesk_live_chat", "title": "Live Chat Console", "url": "/servicedesk/live-chat"},
        {"id": "servicedesk_email_to_ticket", "title": "Email-to-Ticket Mapping", "url": "/servicedesk/email-to-ticket"},
        {"id": "servicedesk_internal_notes", "title": "Internal Notes / Collaboration", "url": "/servicedesk/tickets/TCK-88213/notes"},
    ],
    "Assets & Change Mgmt": [
        {"id": "servicedesk_linked_assets", "title": "Linked Assets (CMDB)", "url": "/servicedesk/linked-assets"},
        {"id": "servicedesk_change_requests", "title": "Change Management Requests", "url": "/servicedesk/change-requests"},
    ],
    "Reporting & Analytics": [
        {"id": "servicedesk_agent_performance", "title": "Agent Performance Dashboard", "url": "/servicedesk/agent-performance"},
        {"id": "servicedesk_ticket_volume", "title": "Ticket Volume Trends", "url": "/servicedesk/ticket-volume"},
        {"id": "servicedesk_csat", "title": "CSAT / Survey Results", "url": "/servicedesk/csat"},
        {"id": "servicedesk_response_time", "title": "First Response / Resolution Time", "url": "/servicedesk/response-time"},
        {"id": "servicedesk_executive_dashboard", "title": "Executive Service Dashboard", "url": "/servicedesk/executive-dashboard"},
    ],
    "Administration": [
        {"id": "servicedesk_roles", "title": "Roles & Permissions", "url": "/servicedesk/roles"},
        {"id": "servicedesk_audit_log", "title": "Service Desk Audit Log", "url": "/servicedesk/audit-log"},
    ]
}

# ─────────────────────────────────────────────
# PAGE CONFIGURATIONS & MOCK DATA (Fallback List Views)
# ─────────────────────────────────────────────

PAGE_CONFIGS = {
    "servicedesk_catalog": {
        "type": "list",
        "columns": ["Service Code", "Service Name", "Category", "Fulfillment Team", "Default SLA", "User Visibility", "Status", "Actions"],
        "rows": [
            {"Service Code": "SVC-IT-001", "Service Name": "Hardware & Laptop Procurement", "Category": "IT Equipment", "Fulfillment Team": "IT Operations", "Default SLA": "SLA-STD-48H", "User Visibility": "All Employees", "Status": "active"},
            {"Service Code": "SVC-IT-002", "Service Name": "VPN & Remote Network Access", "Category": "Network & Security", "Fulfillment Team": "Cybersecurity Team", "Default SLA": "SLA-HIGH-4H", "User Visibility": "All Employees", "Status": "active"},
            {"Service Code": "SVC-HR-005", "Service Name": "Access Card & Employee Badge", "Category": "Facilities / HR", "Fulfillment Team": "HR Operations", "Default SLA": "SLA-STD-24H", "User Visibility": "All Employees", "Status": "active"},
            {"Service Code": "SVC-FIN-009", "Service Name": "ERP System Permission Change", "Category": "Business Systems", "Fulfillment Team": "ERP Admin Group", "Default SLA": "SLA-CRIT-1H", "User Visibility": "Department Heads", "Status": "active"},
        ]
    },
    "servicedesk_sla_policies": {
        "type": "list",
        "columns": ["SLA Code", "Policy Name", "Priority Target", "Response Target", "Resolution Target", "Business Hours", "Escalation Trigger", "Status", "Actions"],
        "rows": [
            {"SLA Code": "SLA-CRIT-01", "Policy Name": "Critical Production Incident SLA", "Priority Target": "P1 - Critical", "Response Target": "15 Mins", "Resolution Target": "1 Hour", "Business Hours": "24/7 Support", "Escalation Trigger": "Auto-SMS to CTO", "Status": "active"},
            {"SLA Code": "SLA-HIGH-02", "Policy Name": "High Priority Business Interruption", "Priority Target": "P2 - High", "Response Target": "30 Mins", "Resolution Target": "4 Hours", "Business Hours": "08:00 - 18:00 AST", "Escalation Trigger": "Notify Team Lead", "Status": "active"},
            {"SLA Code": "SLA-STD-03", "Policy Name": "Standard Request Fulfillment SLA", "Priority Target": "P3 - Medium", "Response Target": "2 Hours", "Resolution Target": "24 Hours", "Business Hours": "08:00 - 17:00 AST", "Escalation Trigger": "Standard Queue", "Status": "active"},
            {"SLA Code": "SLA-LOW-04", "Policy Name": "General Query & Feedback SLA", "Priority Target": "P4 - Low", "Response Target": "4 Hours", "Resolution Target": "48 Hours", "Business Hours": "08:00 - 17:00 AST", "Escalation Trigger": "None", "Status": "active"},
        ]
    },
    "servicedesk_categories": {
        "type": "list",
        "columns": ["Category Code", "Category Name", "Parent Category", "Assigned Lead", "Active Tickets", "Default Priority", "Status", "Actions"],
        "rows": [
            {"Category Code": "CAT-HW", "Category Name": "Hardware & Devices", "Parent Category": "IT Infrastructure", "Assigned Lead": "Bilal Mansoor", "Active Tickets": "18 Tickets", "Default Priority": "Medium", "Status": "active"},
            {"Category Code": "CAT-SW", "Category Name": "Software & Applications", "Parent Category": "IT Infrastructure", "Assigned Lead": "Sarah Otaibi", "Active Tickets": "32 Tickets", "Default Priority": "High", "Status": "active"},
            {"Category Code": "CAT-NET", "Category Name": "Network & Telecom", "Parent Category": "IT Infrastructure", "Assigned Lead": "Khaled Zahrani", "Active Tickets": "9 Tickets", "Default Priority": "Critical", "Status": "active"},
        ]
    },
    "servicedesk_tickets": {
        "type": "list",
        "columns": ["Ticket ID", "Subject / Summary", "Requester", "Assigned Agent", "Category", "Priority", "SLA Status", "Status", "Actions"],
        "rows": [
            {"Ticket ID": "TCK-88213", "Subject / Summary": "VPN Disconnecting Every 5 Minutes on Windows 11", "Requester": "Fahad Al-Sulaiman", "Assigned Agent": "Bilal Mansoor", "Category": "Network & Security", "Priority": "High", "SLA Status": "✔ 2h 15m Left", "Status": "in_progress"},
            {"Ticket ID": "TCK-88212", "Subject / Summary": "ERP Payroll Run Permission Elevation Request", "Requester": "Tariq Harbi", "Assigned Agent": "Sarah Otaibi", "Category": "Business Systems", "Priority": "Critical", "SLA Status": "⚠ 15m Left", "Status": "open"},
            {"Ticket ID": "TCK-88211", "Subject / Summary": "New Office Chair & Ergonomic Desk Assembly", "Requester": "Huda Otaibi", "Assigned Agent": "Facilities Team", "Category": "Facilities", "Priority": "Low", "SLA Status": "✔ 24h Left", "Status": "resolved"},
            {"Ticket ID": "TCK-88210", "Subject / Summary": "Outlook Email Auto-Forwarding Rules Not Applying", "Requester": "Youssef Nabil", "Assigned Agent": "Helpdesk Level 1", "Category": "Software", "Priority": "Medium", "SLA Status": "✔ 6h Left", "Status": "open"},
        ]
    },
    "servicedesk_my_tickets": {
        "type": "list",
        "columns": ["Ticket ID", "Subject", "Requester", "Priority", "SLA Due", "Last Updated", "Status", "Actions"],
        "rows": [
            {"Ticket ID": "TCK-88213", "Subject": "VPN Disconnecting Every 5 Minutes", "Requester": "Fahad Al-Sulaiman", "Priority": "High", "SLA Due": "Today 16:00", "Last Updated": "10 mins ago", "Status": "in_progress"},
            {"Ticket ID": "TCK-88208", "Subject": "Dual Monitor Setup in Conference Room B", "Requester": "Ahmad Ghamdi", "Priority": "Medium", "SLA Due": "Tomorrow 11:00", "Last Updated": "1 hour ago", "Status": "open"},
        ]
    },
    "servicedesk_breach_alerts": {
        "type": "list",
        "columns": ["Alert ID", "Ticket ID", "Subject", "Assigned Agent", "Target SLA", "Overdue By", "Escalation Status", "Actions"],
        "rows": [
            {"Alert ID": "ALT-9012", "Ticket ID": "TCK-88198", "Subject": "SAP Integration Service Connection Timed Out", "Assigned Agent": "DevOps Group", "Target SLA": "1 Hour Resolution", "Overdue By": "⚡ 45 Mins Overdue", "Escalation Status": "Escalated to VP", "Actions": "View"},
            {"Alert ID": "ALT-9011", "Ticket ID": "TCK-88201", "Subject": "Printer Jam on 4th Floor HP LaserJet", "Assigned Agent": "Facilities Support", "Target SLA": "4 Hours Resolution", "Overdue By": "⚡ 12 Mins Overdue", "Escalation Status": "Notified Supervisor", "Actions": "View"},
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
    "resolved":         ("status-completed",    "✔ Resolved"),
    "open":             ("status-open",         "Open"),
    "closed":           ("status-closed",       "Closed"),
    "pending":          ("status-pending",      "Pending"),
    "in_progress":      ("status-inprogress",   "In Progress"),
    "draft":            ("status-draft",        "Draft"),
    "published":        ("status-active",       "Published"),
    "blocked":          ("status-blocked",      "✖ Blocked"),
    "overdue":          ("status-actionreq",    "⚡ Overdue"),
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
        if col.lower() in ("status", "review status", "sla status", "escalation status"):
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

# ─────────────────────────────────────────────
# LAYOUT BUILDERS (CUSTOM PROFESSIONAL ERP VIEWS)
# ─────────────────────────────────────────────

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
              <button class="btn btn-primary" onclick="window.setPage('servicedesk_tickets_new')">
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

def build_form_html(form_type):
    if form_type == "new_ticket":
        return """
        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px; margin-top:10px; text-align:left;">
          <!-- Left: Form -->
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:20px; font-size:16px; font-weight:700; color:#0f172a; border-bottom:1px solid #f1f5f9; padding-bottom:12px;">Create New Service Desk Ticket</h3>
            <div style="display:grid; grid-template-columns:1fr; gap:16px;">
              <div>
                <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Subject / Short Summary <span style="color:#ef4444;">*</span></label>
                <input type="text" id="t_subject" placeholder="e.g. Printer offline on 3rd floor or SAP access card expired" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box;">
              </div>
              <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
                <div>
                  <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Service Category <span style="color:#ef4444;">*</span></label>
                  <select id="t_category" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box; background:#fff;">
                    <option value="">Select Category</option>
                    <option value="hardware">Hardware &amp; Devices</option>
                    <option value="software">Software &amp; Applications</option>
                    <option value="network">Network &amp; Security</option>
                    <option value="facilities">Facilities &amp; Operations</option>
                    <option value="erp">ERP &amp; Business Systems</option>
                  </select>
                </div>
                <div>
                  <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Urgency / Priority <span style="color:#ef4444;">*</span></label>
                  <select id="t_priority" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box; background:#fff;">
                    <option value="Low">Low - General Request</option>
                    <option value="Medium" selected>Medium - Normal SLA</option>
                    <option value="High">High - Urgent Business Impact</option>
                    <option value="Critical">Critical - Production Down</option>
                  </select>
                </div>
              </div>
              <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
                <div>
                  <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Requester Employee <span style="color:#ef4444;">*</span></label>
                  <select id="t_requester" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box; background:#fff;">
                    <option value="Fahad Al-Sulaiman">Fahad Al-Sulaiman (Senior Developer)</option>
                    <option value="Tariq Harbi">Tariq Harbi (HR Specialist)</option>
                    <option value="Youssef Nabil">Youssef Nabil (Financial Analyst)</option>
                    <option value="Huda Otaibi">Huda Otaibi (Facilities Lead)</option>
                  </select>
                </div>
                <div>
                  <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Assigned Group</label>
                  <select id="t_group" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box; background:#fff;">
                    <option value="it_support">IT Tier 1 Support</option>
                    <option value="facilities">Facilities Team</option>
                    <option value="erp_admin">ERP Admin Group</option>
                    <option value="networks">Network &amp; Security Group</option>
                  </select>
                </div>
              </div>
              <div>
                <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Detailed Description</label>
                <!-- Editor Toolbar -->
                <div style="background:#f8fafc; border:1px solid #cbd5e1; border-bottom:none; border-radius:6px 6px 0 0; padding:8px 12px; display:flex; gap:10px;">
                  <button type="button" style="background:none; border:none; font-weight:700; color:#475569; cursor:pointer; font-size:13px;">B</button>
                  <button type="button" style="background:none; border:none; font-style:italic; color:#475569; cursor:pointer; font-size:13px;">I</button>
                  <button type="button" style="background:none; border:none; text-decoration:underline; color:#475569; cursor:pointer; font-size:13px;">U</button>
                  <span style="color:#cbd5e1;">|</span>
                  <button type="button" style="background:none; border:none; color:#475569; cursor:pointer; font-size:13px;">🔗 Link</button>
                  <button type="button" style="background:none; border:none; color:#475569; cursor:pointer; font-size:13px;">📷 Image</button>
                  <button type="button" style="background:none; border:none; color:#475569; cursor:pointer; font-size:13px;">&lt;/&gt; Code</button>
                </div>
                <textarea id="t_description" rows="8" placeholder="Provide troubleshooting details, error messages, and step-by-step reproduction steps..." style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:0 0 6px 6px; font-size:13.5px; resize:vertical; outline:none; font-family:inherit; box-sizing:border-box;"></textarea>
              </div>
              <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:10px; border-top:1px solid #f1f5f9; padding-top:20px;">
                <button type="button" onclick="window.setPage('servicedesk_tickets')" class="btn btn-outline">Cancel</button>
                <button type="button" onclick="alert('Ticket created and auto-assigned successfully!')" class="btn btn-primary">Create Ticket &amp; Dispatch</button>
              </div>
            </div>
          </div>
          <!-- Right: Sidebar -->
          <div>
            <div class="card" style="padding:20px; margin-bottom:16px;">
              <h4 style="margin-top:0; margin-bottom:12px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px;">SLA Alert Indicator</h4>
              <div style="background:#fef3c7; border:1px solid #fde68a; border-radius:8px; padding:12px; display:flex; gap:10px;">
                <div style="font-size:20px;">⏱</div>
                <div>
                  <div style="font-size:12px; font-weight:700; color:#92400e;">Standard SLA (24h Target)</div>
                  <div style="font-size:11px; color:#b45309; margin-top:2px;">Based on Urgency: Medium. Resolution target will be automatically tracked in real-time.</div>
                </div>
              </div>
            </div>
            <div class="card" style="padding:20px;">
              <h4 style="margin-top:0; margin-bottom:12px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px;">Quick Templates</h4>
              <div style="display:grid; grid-template-columns:1fr; gap:8px;">
                <button type="button" onclick="applyTemplate('VPN Access Request', 'User requests VPN remote network connection setup for Windows 11 / macOS.')" style="text-align:left; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; cursor:pointer; font-size:12.5px; color:#334155; font-weight:500;">🌐 VPN Access Request</button>
                <button type="button" onclick="applyTemplate('ERP Access Elevation', 'Requesting role adjustment or permission expansion on ERP modules.')" style="text-align:left; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; cursor:pointer; font-size:12.5px; color:#334155; font-weight:500;">🔑 ERP Access Elevation</button>
                <button type="button" onclick="applyTemplate('Hardware Replacement', 'Employee requests upgrade or replacement of faulty workstation peripherals.')" style="text-align:left; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; cursor:pointer; font-size:12.5px; color:#334155; font-weight:500;">💻 Hardware Replacement / Fix</button>
              </div>
            </div>
          </div>
        </div>
        """
    elif form_type == "portal_request":
        return """
        <div style="max-width:800px; margin:0 auto; padding-top:10px; text-align:left;">
          <div class="card" style="padding:32px;">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:24px; border-bottom:1px solid #e2e8f0; padding-bottom:16px;">
              <div style="width:48px; height:48px; border-radius:12px; background:#e0e7ff; color:#3730a3; display:flex; align-items:center; justify-content:center; font-size:24px;">📝</div>
              <div>
                <h2 style="margin:0; font-size:20px; font-weight:700; color:#0f172a;">Submit Support Ticket / Inquiry</h2>
                <div style="font-size:13px; color:#64748b; margin-top:2px;">Our team typically responds to critical requests within 30 minutes.</div>
              </div>
            </div>
            <div style="display:grid; grid-template-columns:1fr; gap:18px;">
              <div>
                <label style="display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px;">Select the service you need assistance with <span style="color:#ef4444;">*</span></label>
                <select style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; background:#fff;">
                  <option>VPN Connection &amp; Remote Networks</option>
                  <option>ERP Financials &amp; HRMS Modules Access</option>
                  <option>Office Desktop Hardware &amp; Accessories</option>
                  <option>Company Email, Teams &amp; Office 365</option>
                  <option>Other / General Service Support Inquiry</option>
                </select>
              </div>
              <div>
                <label style="display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px;">Briefly summarize your request <span style="color:#ef4444;">*</span></label>
                <input type="text" placeholder="e.g. Outlook calendar sync errors or VPN token expiration" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box;">
              </div>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                <div>
                  <label style="display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px;">Preferred Contact Method</label>
                  <select style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; background:#fff;">
                    <option>Email &amp; System Notifications</option>
                    <option>Teams Chat Integration</option>
                    <option>Direct Phone Call (+966 55 987 6543)</option>
                  </select>
                </div>
                <div>
                  <label style="display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px;">Attachment / Screen Capture</label>
                  <input type="file" style="width:100%; font-size:13px; border:1px solid #cbd5e1; border-radius:6px; padding:6px 10px; background:#f8fafc;">
                </div>
              </div>
              <div>
                <label style="display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px;">Full Details of Issue</label>
                <textarea rows="6" placeholder="Provide as much detail as possible to help us resolve this quickly (e.g. error codes, steps you took before the issue started)..." style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; resize:vertical; font-family:inherit; box-sizing:border-box;"></textarea>
              </div>
              <div style="display:flex; justify-content:flex-end; gap:12px; border-top:1px solid #e2e8f0; padding-top:20px; margin-top:10px;">
                <button type="button" onclick="window.setPage('portal_home')" class="btn btn-outline">Cancel</button>
                <button type="button" onclick="alert('Your ticket was successfully submitted! Check the My Tickets dashboard for live updates.')" class="btn btn-primary" style="padding:10px 20px;">Submit Ticket Request</button>
              </div>
            </div>
          </div>
        </div>
        """

def build_detail_html():
    return """
    <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px; margin-top:10px; text-align:left;">
      <!-- Left Side: Conversation & Timeline -->
      <div>
        <div class="card" style="padding:24px; margin-bottom:20px;">
          <!-- Top Banner Info -->
          <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:1px solid #e2e8f0; padding-bottom:16px; margin-bottom:20px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span class="status-badge status-inprogress">In Progress</span>
                <span class="status-badge status-actionreq">High Priority</span>
                <span style="font-size:12.5px; color:#64748b; font-weight:500;">Ticket #TCK-88213</span>
              </div>
              <h2 style="margin:0; font-size:18px; font-weight:700; color:#0f172a;">VPN Disconnecting Every 5 Minutes on Windows 11</h2>
            </div>
            <div style="text-align:right;">
              <span style="font-size:12px; color:#64748b; display:block;">Assigned Agent</span>
              <strong style="font-size:13.5px; color:#334155; display:block; margin-top:2px;">Bilal Mansoor (IT Level 2)</strong>
            </div>
          </div>

          <!-- Timeline Grid -->
          <div style="display:flex; flex-direction:column; gap:20px;" id="detail-timeline-container">
            <!-- Customer Initial Message -->
            <div style="display:flex; gap:16px;">
              <div style="width:36px; height:36px; border-radius:50%; background:#c7d2fe; color:#3730a3; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">FA</div>
              <div style="flex:1;">
                <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
                  <strong style="font-size:13.5px; color:#0f172a;">Fahad Al-Sulaiman (Requester)</strong>
                  <span style="font-size:11px; color:#64748b;">Logged 2 hours ago</span>
                </div>
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px; font-size:13px; color:#334155; line-height:1.45;">
                  Hi support team, I recently upgraded my corporate laptop to Windows 11. Since the update, my Cisco AnyConnect VPN client keeps disconnecting exactly every 5 minutes. 
                  This is disrupting my database sessions. I have reinstalled the client twice, but the issue persists. Let me know what steps I should take.
                </div>
              </div>
            </div>

            <!-- System Event -->
            <div style="display:flex; justify-content:center; margin:10px 0;">
              <div style="background:#f1f5f9; padding:4px 12px; border-radius:12px; font-size:11px; color:#475569; font-weight:500; border:1px solid #cbd5e1;">
                ⚙ System assigned ticket to <strong>Bilal Mansoor</strong> · 1.8 hours ago
              </div>
            </div>

            <!-- Agent Internal Note -->
            <div style="display:flex; gap:16px;">
              <div style="width:36px; height:36px; border-radius:50%; background:#fde68a; color:#78350f; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">BM</div>
              <div style="flex:1;">
                <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
                  <strong style="font-size:13.5px; color:#78350f;">Bilal Mansoor (Internal Agent Note)</strong>
                  <span style="font-size:11px; color:#64748b;">1.5 hours ago</span>
                </div>
                <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:14px; font-size:13px; color:#78350f; line-height:1.45;">
                  Checked user's logs in CMDB. The DTLS handshake times out, forcing a fallback to TLS, which fails. This is a common issue with Windows 11 network driver adapters.
                  I will reply to the requester suggesting they turn off DTLS in the XML profile or adapter settings.
                </div>
              </div>
            </div>

            <!-- Agent Public Reply -->
            <div style="display:flex; gap:16px;">
              <div style="width:36px; height:36px; border-radius:50%; background:#2f5eff; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">BM</div>
              <div style="flex:1;">
                <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
                  <strong style="font-size:13.5px; color:#0f172a;">Bilal Mansoor (Support Engineer)</strong>
                  <span style="font-size:11px; color:#64748b;">1 hour ago</span>
                </div>
                <div style="background:#e0e7ff; border:1px solid #c7d2fe; border-radius:8px; padding:14px; font-size:13px; color:#1e1b4b; line-height:1.45;">
                  Hello Fahad, please follow these instructions:
                  <ol style="margin-top:6px; margin-bottom:0; padding-left:20px;">
                    <li>Open your Cisco AnyConnect client.</li>
                    <li>Go to Settings (Gear icon) -> VPN tab -> Preferences.</li>
                    <li>Uncheck the option <strong>"Allow DTLS (Datagram TLS)"</strong> if available.</li>
                    <li>Restart the VPN client and check if connection stays alive.</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Reply Editor Form -->
        <div class="card" style="padding:24px;">
          <div style="display:flex; gap:12px; margin-bottom:12px; border-bottom:1px solid #e2e8f0; padding-bottom:10px;">
            <button onclick="setReplyTab('reply')" id="tab-reply-btn" style="background:none; border:none; font-size:13.5px; font-weight:700; color:#2f5eff; cursor:pointer; padding-bottom:8px; border-bottom:2px solid #2f5eff;">Public Reply</button>
            <button onclick="setReplyTab('note')" id="tab-note-btn" style="background:none; border:none; font-size:13.5px; font-weight:600; color:#64748b; cursor:pointer; padding-bottom:8px;">Internal Agent Note</button>
          </div>
          <div>
            <textarea id="detail-reply-box" rows="5" placeholder="Write your response to the customer..." style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; resize:vertical; outline:none; font-family:inherit; box-sizing:border-box;"></textarea>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
              <span style="font-size:12px; color:#64748b;">Replying as <strong>Samir Al-Dawsari (Service Desk Manager)</strong></span>
              <button onclick="submitDetailTimeline()" class="btn btn-primary">Send Update</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: Properties & Metadata -->
      <div>
        <!-- SLA countdown -->
        <div class="card" style="padding:20px; margin-bottom:16px;">
          <h4 style="margin-top:0; margin-bottom:12px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px;">SLA Countdown</h4>
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
            <span style="font-size:12.5px; color:#475569;">Resolution Target:</span>
            <strong style="font-size:14px; color:#e11d48;" id="sla-countdown">✔ 2h 15m Left</strong>
          </div>
          <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;">
            <div style="width:65%; height:100%; background:#10b981; border-radius:4px;"></div>
          </div>
          <span style="font-size:11px; color:#64748b; margin-top:6px; display:block;">Breach Policy: Standard P2 SLA (4 Hours)</span>
        </div>

        <!-- Ticket Info -->
        <div class="card" style="padding:20px; margin-bottom:16px;">
          <h4 style="margin-top:0; margin-bottom:14px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">Properties</h4>
          <div style="display:grid; grid-template-columns:1fr; gap:12px; font-size:13px;">
            <div>
              <span style="color:#64748b; display:block; font-size:11.5px; font-weight:500; margin-bottom:2px;">Category</span>
              <span style="color:#334155; font-weight:600;">Network &amp; Security</span>
            </div>
            <div>
              <span style="color:#64748b; display:block; font-size:11.5px; font-weight:500; margin-bottom:2px;">Service Desk Team</span>
              <span style="color:#334155; font-weight:600;">IT Operations</span>
            </div>
            <div>
              <span style="color:#64748b; display:block; font-size:11.5px; font-weight:500; margin-bottom:2px;">Linked CMDB Asset</span>
              <span style="color:#2f5eff; font-weight:600; cursor:pointer;" onclick="alert('Viewing asset profile: VPN-CLI-PROD-092')">VPN-CLI-PROD-092 (Cisco AnyConnect)</span>
            </div>
          </div>
        </div>

        <!-- Requester Info -->
        <div class="card" style="padding:20px; margin-bottom:16px;">
          <h4 style="margin-top:0; margin-bottom:14px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">Requester Details</h4>
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:40px; height:40px; border-radius:50%; background:#e0e7ff; color:#3730a3; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:14px;">FA</div>
            <div>
              <strong style="font-size:13.5px; color:#0f172a; display:block;">Fahad Al-Sulaiman</strong>
              <span style="font-size:11px; color:#64748b;">Senior Developer</span>
            </div>
          </div>
          <div style="display:grid; grid-template-columns:1fr; gap:8px; font-size:12px; color:#475569;">
            <div>📧 fahad.sulaiman@company.com</div>
            <div>📞 +966 55 233 4455</div>
            <div>🏢 R&amp;D Division, Level 4</div>
          </div>
        </div>

        <!-- Actions Panel -->
        <div class="card" style="padding:20px;">
          <h4 style="margin-top:0; margin-bottom:12px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px;">Support Actions</h4>
          <div style="display:grid; grid-template-columns:1fr; gap:8px;">
            <button onclick="alert('Ticket escalated to IT Infrastructure Supervisor!')" class="btn btn-outline" style="width:100%; justify-content:center; border-color:#e11d48; color:#be123c; background:#fff;">Escalate Ticket</button>
            <button onclick="alert('Opening Change Management integration screen')" class="btn btn-outline" style="width:100%; justify-content:center; background:#fff;">Link Change Request</button>
            <button onclick="alert('Ticket status updated to Pending Vendor')" class="btn btn-outline" style="width:100%; justify-content:center; background:#fff;">Put on Hold</button>
            <button onclick="alert('Ticket successfully resolved!')" class="btn btn-primary" style="width:100%; justify-content:center;">✔ Resolve Ticket</button>
          </div>
        </div>
      </div>
    </div>
    """

def build_chat_html():
    return """
    <div style="display:grid; grid-template-columns: 260px 1fr 280px; height: calc(100vh - 140px); background:#fff; border:1px solid #e2e8f0; border-radius:8px; overflow:hidden; margin-top:10px; text-align:left;">
      <!-- Left Sidebar: Active Conversations -->
      <div style="border-right:1px solid #e2e8f0; display:flex; flex-direction:column; background:#f8fafc;">
        <div style="padding:16px 20px; border-bottom:1px solid #e2e8f0; font-weight:700; font-size:14px; color:#0f172a;">Active Conversations</div>
        <div style="flex:1; overflow-y:auto; padding:10px 0;" id="chat-queue-container">
          <div onclick="selectChat(this, 'Fahad Al-Sulaiman')" style="padding:12px 20px; display:flex; gap:12px; align-items:center; cursor:pointer; background:#e0e7ff; border-left:4px solid #2f5eff;">
            <div style="width:36px; height:36px; border-radius:50%; background:#2f5eff; color:#fff; font-weight:700; display:flex; align-items:center; justify-content:center; font-size:13px;">FA</div>
            <div style="flex:1; min-width:0;">
              <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <strong style="font-size:12.5px; color:#0f172a; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Fahad Al-Sulaiman</strong>
                <span style="font-size:10px; color:#64748b;">13:42</span>
              </div>
              <div style="font-size:11.5px; color:#475569; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Need help configuring Git settings</div>
            </div>
          </div>
          <div onclick="selectChat(this, 'Tariq Harbi')" style="padding:12px 20px; display:flex; gap:12px; align-items:center; cursor:pointer;">
            <div style="width:36px; height:36px; border-radius:50%; background:#94a3b8; color:#fff; font-weight:700; display:flex; align-items:center; justify-content:center; font-size:13px;">TH</div>
            <div style="flex:1; min-width:0;">
              <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <strong style="font-size:12.5px; color:#334155; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Tariq Harbi</strong>
                <span style="font-size:10px; color:#64748b;">13:10</span>
              </div>
              <div style="font-size:11.5px; color:#64748b; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Is the printing server back online?</div>
            </div>
          </div>
          <div onclick="selectChat(this, 'Youssef Nabil')" style="padding:12px 20px; display:flex; gap:12px; align-items:center; cursor:pointer;">
            <div style="width:36px; height:36px; border-radius:50%; background:#94a3b8; color:#fff; font-weight:700; display:flex; align-items:center; justify-content:center; font-size:13px;">YN</div>
            <div style="flex:1; min-width:0;">
              <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <strong style="font-size:12.5px; color:#334155; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Youssef Nabil</strong>
                <span style="font-size:10px; color:#64748b;">Yesterday</span>
              </div>
              <div style="font-size:11.5px; color:#64748b; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Thanks for resolving my login issue!</div>
            </div>
          </div>
        </div>
      </div>
      <!-- Center: Message Thread -->
      <div style="display:flex; flex-direction:column; background:#fff;">
        <div style="padding:14px 20px; border-bottom:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <h4 style="margin:0; font-size:14.5px; font-weight:700; color:#0f172a;" id="active-chat-name">Fahad Al-Sulaiman</h4>
            <div style="font-size:11px; color:#10b981; display:flex; align-items:center; gap:4px; margin-top:2px;">
              <span style="width:6px; height:6px; background:#10b981; border-radius:50%;"></span> Active in Support Portal
            </div>
          </div>
          <div>
            <button onclick="alert('Ticket TCK-88213 linked successfully!')" class="btn btn-outline" style="padding:6px 10px; font-size:12px; background:#fff;">Link to Ticket</button>
          </div>
        </div>
        <div style="flex:1; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:16px;" id="chat-thread-messages">
          <div style="align-self:flex-start; max-width:70%;">
            <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-left:4px;">Fahad · 13:40</div>
            <div style="background:#f1f5f9; color:#0f172a; padding:12px 16px; border-radius:0 12px 12px 12px; font-size:13px; line-height:1.4;">
              Hi, I'm setting up our corporate Git repo on my laptop but I'm getting a credential permission error. Can you help?
            </div>
          </div>
          <div style="align-self:flex-end; max-width:70%;">
            <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-right:4px; text-align:right;">Samir (You) · 13:41</div>
            <div style="background:#2f5eff; color:#fff; padding:12px 16px; border-radius:12px 0 12px 12px; font-size:13px; line-height:1.4;">
              Hi Fahad! Have you authenticated using your active directory token or SSH keys?
            </div>
          </div>
          <div style="align-self:flex-start; max-width:70%;">
            <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-left:4px;">Fahad · 13:42</div>
            <div style="background:#f1f5f9; color:#0f172a; padding:12px 16px; border-radius:0 12px 12px 12px; font-size:13px; line-height:1.4;">
              I'm trying to use SSH keys, but it keeps saying permission denied (publickey). Let me paste my config...
            </div>
          </div>
        </div>
        <div style="border-top:1px solid #e2e8f0; padding:16px; display:flex; gap:10px; align-items:center;">
          <input type="text" id="chat-input" placeholder="Type your message to Fahad..." onkeydown="if(event.key==='Enter') sendChatMessage()" style="flex:1; padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:13px; outline:none; box-sizing:border-box;">
          <button onclick="sendChatMessage()" class="btn btn-primary" style="padding:11px 20px;">Send</button>
        </div>
      </div>
      <!-- Right Pane: Visitor Profile Info -->
      <div style="border-left:1px solid #e2e8f0; padding:20px; display:flex; flex-direction:column; background:#f8fafc;">
        <h4 style="margin-top:0; margin-bottom:16px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; border-bottom:1px solid #e2e8f0; padding-bottom:8px;">Visitor Info</h4>
        <div style="text-align:center; margin-bottom:20px;">
          <div style="width:60px; height:60px; border-radius:50%; background:#cbd5e1; color:#334155; font-weight:700; display:flex; align-items:center; justify-content:center; font-size:20px; margin:0 auto 10px auto;">FA</div>
          <strong style="display:block; font-size:14px; color:#0f172a;">Fahad Al-Sulaiman</strong>
          <span style="font-size:11.5px; color:#64748b;">Software Engineer</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr; gap:12px; font-size:12px; color:#334155;">
          <div><span style="color:#64748b; font-weight:500;">Department:</span> Engineering / R&amp;D</div>
          <div><span style="color:#64748b; font-weight:500;">Location:</span> Riyadh HQ - Zone B</div>
          <div><span style="color:#64748b; font-weight:500;">Browser:</span> Chrome v114 (Windows 11)</div>
          <div><span style="color:#64748b; font-weight:500;">IP Address:</span> 10.15.22.88</div>
          <div><span style="color:#64748b; font-weight:500;">Connected Time:</span> 18 minutes ago</div>
        </div>
        <div style="margin-top:auto; border-top:1px solid #e2e8f0; padding-top:16px;">
          <strong style="display:block; font-size:12px; color:#0f172a; margin-bottom:8px;">Active SLA Status</strong>
          <div style="background:#e6f6ee; color:#1f8a56; border:1px solid #b7ebc6; padding:8px 10px; border-radius:6px; font-size:11.5px; font-weight:700; text-align:center;">
            ✔ SLA-GOLD (Response: 30m)
          </div>
        </div>
      </div>
    </div>
    """

def build_workflow_html():
    return """
    <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px; margin-top:10px; text-align:left;">
      <!-- Canvas -->
      <div class="card" style="padding:24px; background:#f8fafc; border:2px dashed #cbd5e1;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:12px; margin-bottom:20px; background:#fff; margin:-24px -24px 20px -24px; padding:16px 24px;">
          <h3 style="margin:0; font-size:15px; font-weight:700; color:#0f172a;">Workflow Canvas: Auto-Routing Rule</h3>
          <button onclick="alert('Workflow changes saved!')" class="btn btn-primary">Save Workflow</button>
        </div>

        <div style="display:flex; flex-direction:column; align-items:center; gap:20px;">
          <!-- Node 1: Trigger -->
          <div class="card" style="width:300px; padding:16px; border-left:4px solid #2f5eff; background:#fff; text-align:center;">
            <span style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">1. Trigger Event</span>
            <strong style="display:block; font-size:14px; color:#0f172a; margin-top:4px;">When Ticket is Created</strong>
            <span style="font-size:11.5px; color:#475569; display:block; margin-top:2px;">Applies to all incoming tickets</span>
          </div>

          <!-- Arrow -->
          <div style="font-size:20px; color:#94a3b8;">↓</div>

          <!-- Node 2: Condition -->
          <div class="card" style="width:300px; padding:16px; border-left:4px solid #f59e0b; background:#fff; text-align:center;">
            <span style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">2. Condition Criteria</span>
            <strong style="display:block; font-size:14px; color:#0f172a; margin-top:4px;">Priority == Critical</strong>
            <span style="font-size:11.5px; color:#475569; display:block; margin-top:2px;">AND Category == "Network &amp; Security"</span>
          </div>

          <!-- Arrow -->
          <div style="font-size:20px; color:#94a3b8;">↓</div>

          <!-- Node 3: Action -->
          <div class="card" style="width:300px; padding:16px; border-left:4px solid #10b981; background:#fff; text-align:center;">
            <span style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">3. Output Action</span>
            <strong style="display:block; font-size:14px; color:#0f172a; margin-top:4px;">Dispatch to Escalations Team</strong>
            <span style="font-size:11.5px; color:#475569; display:block; margin-top:2px;">AND Send SMS notification to CTO</span>
          </div>
        </div>
      </div>
      
      <!-- Toolbox Sidebar -->
      <div class="card" style="padding:20px;">
        <h4 style="margin-top:0; margin-bottom:12px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px;">Automation Toolbox</h4>
        <div style="display:grid; grid-template-columns:1fr; gap:10px;">
          <div onclick="alert('Added condition node')" style="padding:10px; border:1px solid #e2e8f0; border-radius:6px; cursor:pointer; background:#fff; hover:background:#f1f5f9;">
            <strong style="font-size:12.5px; color:#334155; display:block;">➕ Add Condition</strong>
            <span style="font-size:11px; color:#64748b;">Add checks for category, customer group, SLA breach window.</span>
          </div>
          <div onclick="alert('Added dispatch node')" style="padding:10px; border:1px solid #e2e8f0; border-radius:6px; cursor:pointer; background:#fff; hover:background:#f1f5f9;">
            <strong style="font-size:12.5px; color:#334155; display:block;">➕ Add Dispatch Action</strong>
            <span style="font-size:11px; color:#64748b;">Assign tickets to agents using round-robin or skill queues.</span>
          </div>
          <div onclick="alert('Added webhook node')" style="padding:10px; border:1px solid #e2e8f0; border-radius:6px; cursor:pointer; background:#fff; hover:background:#f1f5f9;">
            <strong style="font-size:12.5px; color:#334155; display:block;">➕ Add Webhook trigger</strong>
            <span style="font-size:11px; color:#64748b;">Trigger external APIs when tickets update.</span>
          </div>
        </div>
      </div>
    </div>
    """

def build_kb_articles_grid():
    return """
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin-top:10px; text-align:left;">
      <div class="card" style="padding:16px; text-align:center; border-bottom:3px solid #2f5eff;">
        <span style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase;">Total Articles</span>
        <div style="font-size:22px; font-weight:700; color:#0f172a; margin-top:4px;">24 Articles</div>
      </div>
      <div class="card" style="padding:16px; text-align:center; border-bottom:3px solid #10b981;">
        <span style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase;">Published Views</span>
        <div style="font-size:22px; font-weight:700; color:#0f172a; margin-top:4px;">12.4k Views</div>
      </div>
      <div class="card" style="padding:16px; text-align:center; border-bottom:3px solid #f59e0b;">
        <span style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase;">Draft Articles</span>
        <div style="font-size:22px; font-weight:700; color:#0f172a; margin-top:4px;">3 Drafts</div>
      </div>
    </div>

    <!-- Article Search & Action -->
    <div class="card" style="margin-top:20px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; text-align:left;">
      <div class="search-box">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="position:absolute; left:12px; top:50%; transform:translateY(-50%); color:#94a3b8;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" placeholder="Search KB database..." style="padding:8px 12px 8px 36px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; width:260px; box-sizing:border-box;" oninput="const q = this.value.toLowerCase(); this.closest('div').nextElementSibling.querySelectorAll('.card').forEach(c => c.style.display = c.textContent.toLowerCase().includes(q) ? '' : 'none');">
      </div>
      <button onclick="window.setPage('servicedesk_kb_editor')" class="btn btn-primary">+ Write New Article</button>
    </div>

    <!-- Articles Grid list -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:16px; text-align:left;">
      <div class="card" style="padding:20px; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="status-badge status-active">Published</span>
            <span style="font-size:11px; color:#64748b;">Views: 1,420</span>
          </div>
          <h4 style="margin:0; font-size:14.5px; font-weight:700; color:#0f172a;">How to Reset Cisco AnyConnect VPN Password</h4>
          <p style="font-size:12.5px; color:#475569; line-height:1.4; margin-top:6px; margin-bottom:12px;">Detailed step-by-step instructions on triggering password resets, handling MFA notifications, and connection verification.</p>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:12px;">
          <span style="font-size:11.5px; color:#64748b;">By: Khaled Zahrani</span>
          <div style="display:flex; gap:10px;">
            <button onclick="window.setPage('portal_kb_article')" class="btn btn-outline" style="padding:4px 8px; font-size:11.5px; background:#fff;">View Page</button>
            <button onclick="alert('Opening edit mode...')" class="btn btn-outline" style="padding:4px 8px; font-size:11.5px; background:#fff;">Edit</button>
          </div>
        </div>
      </div>

      <div class="card" style="padding:20px; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="status-badge status-active">Published</span>
            <span style="font-size:11px; color:#64748b;">Views: 890</span>
          </div>
          <h4 style="margin:0; font-size:14.5px; font-weight:700; color:#0f172a;">Setting Up Dual Monitors &amp; Docking Station</h4>
          <p style="font-size:12.5px; color:#475569; line-height:1.4; margin-top:6px; margin-bottom:12px;">Connecting display port peripherals and setting display refresh rates for dual screen configurations in office workstations.</p>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f5f9; padding-top:12px;">
          <span style="font-size:11.5px; color:#64748b;">By: Bilal Mansoor</span>
          <div style="display:flex; gap:10px;">
            <button onclick="alert('Viewing article details...')" class="btn btn-outline" style="padding:4px 8px; font-size:11.5px; background:#fff;">View Page</button>
            <button onclick="alert('Opening edit mode...')" class="btn btn-outline" style="padding:4px 8px; font-size:11.5px; background:#fff;">Edit</button>
          </div>
        </div>
      </div>
    </div>
    """

def build_kb_editor_html():
    return """
    <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px; margin-top:10px; text-align:left;">
      <!-- Left: Article Content Editor -->
      <div class="card" style="padding:24px;">
        <h3 style="margin-top:0; margin-bottom:20px; font-size:16px; font-weight:700; color:#0f172a; border-bottom:1px solid #f1f5f9; padding-bottom:12px;">New KB Article Draft</h3>
        <div style="display:grid; grid-template-columns:1fr; gap:16px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Article Title <span style="color:#ef4444;">*</span></label>
            <input type="text" placeholder="e.g. Cisco AnyConnect VPN Connection Guidelines" style="width:100%; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13.5px; box-sizing:border-box;">
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:#475569; margin-bottom:6px;">Body Content Editor</label>
            <!-- Mock rich toolbar -->
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-bottom:none; border-radius:6px 6px 0 0; padding:8px 12px; display:flex; gap:10px;">
              <button type="button" style="background:none; border:none; font-weight:700; color:#475569; cursor:pointer;">H1</button>
              <button type="button" style="background:none; border:none; font-weight:700; color:#475569; cursor:pointer;">H2</button>
              <span style="color:#cbd5e1;">|</span>
              <button type="button" style="background:none; border:none; font-weight:700; color:#475569; cursor:pointer;">B</button>
              <button type="button" style="background:none; border:none; font-style:italic; color:#475569; cursor:pointer;">I</button>
              <span style="color:#cbd5e1;">|</span>
              <button type="button" style="background:none; border:none; color:#475569; cursor:pointer;">🔢 List</button>
              <button type="button" style="background:none; border:none; color:#475569; cursor:pointer;">🔗 Link</button>
              <button type="button" style="background:none; border:none; color:#475569; cursor:pointer;">📷 Image</button>
            </div>
            <textarea rows="12" placeholder="Write step-by-step documentation instructions here..." style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:0 0 6px 6px; font-size:13.5px; resize:vertical; outline:none; font-family:inherit; box-sizing:border-box;"></textarea>
          </div>
          <div style="display:flex; justify-content:flex-end; gap:10px; border-top:1px solid #f1f5f9; padding-top:20px; margin-top:10px;">
            <button onclick="window.setPage('servicedesk_kb_articles')" class="btn btn-outline">Discard Draft</button>
            <button onclick="alert('Draft saved locally')" class="btn btn-outline">Save Draft</button>
            <button onclick="alert('Article published to portal successfully!')" class="btn btn-primary">Publish to Portal</button>
          </div>
        </div>
      </div>
      <!-- Right: Settings Sidebar -->
      <div class="card" style="padding:20px;">
        <h4 style="margin-top:0; margin-bottom:14px; font-size:13px; font-weight:700; color:#0f172a; text-transform:uppercase; letter-spacing:0.5px; border-bottom:1px solid #f1f5f9; padding-bottom:8px;">Article Properties</h4>
        <div style="display:grid; grid-template-columns:1fr; gap:14px; font-size:13px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Target Category</label>
            <select style="width:100%; padding:8px 10px; border:1px solid #cbd5e1; border-radius:6px; background:#fff;">
              <option>Network &amp; Security</option>
              <option>Hardware &amp; Workstations</option>
              <option>Finance &amp; ERP Access</option>
              <option>Software Tools</option>
            </select>
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Access Restrictions</label>
            <select style="width:100%; padding:8px 10px; border:1px solid #cbd5e1; border-radius:6px; background:#fff;">
              <option>Public (All Employees)</option>
              <option>Support Agents Only</option>
              <option>Internal IT Staff Only</option>
            </select>
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Keywords / Tags</label>
            <input type="text" placeholder="e.g. vpn, cisco, remote" style="width:100%; padding:8px 10px; border:1px solid #cbd5e1; border-radius:6px;">
          </div>
        </div>
      </div>
    </div>
    """

def build_portal_home_html():
    return """
    <div style="background: linear-gradient(135deg, #132238 0%, #1e2d42 100%); color:#fff; border-radius:12px; padding:40px; text-align:center; box-shadow:0 4px 20px rgba(0,0,0,0.15); margin-top:10px;">
      <h2 style="margin:0; font-size:24px; font-weight:700; letter-spacing:-0.5px;">Welcome to the Employee IT Help Center</h2>
      <p style="color:#94a3b8; font-size:14px; margin-top:8px; margin-bottom:24px;">Search our self-service knowledge base or submit a support ticket to our help desk technicians.</p>
      <div style="max-width:600px; margin:0 auto; position:relative;">
        <input type="text" placeholder="Search self-service solutions, documentation &amp; guides..." style="width:100%; padding:14px 20px; border:none; border-radius:30px; font-size:15px; box-shadow:0 10px 25px -5px rgba(0,0,0,0.3); outline:none; box-sizing:border-box;" oninput="const q = this.value.toLowerCase(); this.closest('div').parentElement.nextElementSibling.querySelectorAll('.card').forEach(c => c.style.display = c.textContent.toLowerCase().includes(q) ? '' : 'none');">
      </div>
    </div>

    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin-top:24px; text-align:center;">
      <div onclick="window.setPage('portal_submit_request')" class="card" style="padding:24px; cursor:pointer; hover:transform:translateY(-2px); transition:all 0.15s ease;">
        <div style="font-size:32px; margin-bottom:12px;">📝</div>
        <strong style="display:block; font-size:14.5px; color:#0f172a;">Submit Support Ticket</strong>
        <span style="font-size:12px; color:#64748b; display:block; margin-top:6px;">Raise an issue with IT, HR, or Facilities support.</span>
      </div>
      <div onclick="window.setPage('servicedesk_kb_articles')" class="card" style="padding:24px; cursor:pointer; hover:transform:translateY(-2px); transition:all 0.15s ease;">
        <div style="font-size:32px; margin-bottom:12px;">📚</div>
        <strong style="display:block; font-size:14.5px; color:#0f172a;">Knowledge Base</strong>
        <span style="font-size:12px; color:#64748b; display:block; margin-top:6px;">Browse setup tutorials and troubleshooting articles.</span>
      </div>
      <div onclick="window.setPage('servicedesk_my_tickets')" class="card" style="padding:24px; cursor:pointer; hover:transform:translateY(-2px); transition:all 0.15s ease;">
        <div style="font-size:32px; margin-bottom:12px;">🎫</div>
        <strong style="display:block; font-size:14.5px; color:#0f172a;">My Active Tickets</strong>
        <span style="font-size:12px; color:#64748b; display:block; margin-top:6px;">Check statuses and chat with assigned technical support.</span>
      </div>
      <div onclick="window.setPage('servicedesk_catalog')" class="card" style="padding:24px; cursor:pointer; hover:transform:translateY(-2px); transition:all 0.15s ease;">
        <div style="font-size:32px; margin-bottom:12px;">⚙</div>
        <strong style="display:block; font-size:14.5px; color:#0f172a;">Service Catalog</strong>
        <span style="font-size:12px; color:#64748b; display:block; margin-top:6px;">Request standard hardware upgrades or permissions.</span>
      </div>
    </div>

    <div class="card" style="padding:24px; margin-top:24px; text-align:left;">
      <h3 style="margin-top:0; margin-bottom:16px; font-size:16px; font-weight:700; color:#0f172a; border-bottom:1px solid #f1f5f9; padding-bottom:10px;">Featured Knowledge Base Guides</h3>
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
        <div onclick="window.setPage('portal_kb_article')" style="border:1px solid #e2e8f0; border-radius:8px; padding:16px; cursor:pointer; background:#f8fafc;">
          <strong style="font-size:14px; color:#2f5eff; display:block; margin-bottom:4px;">💻 Resetting Cisco AnyConnect VPN Passwords</strong>
          <span style="font-size:12px; color:#475569;">Step-by-step instructions on MFA verification and password rotation rules.</span>
        </div>
        <div onclick="alert('This guide is currently being updated.')" style="border:1px solid #e2e8f0; border-radius:8px; padding:16px; cursor:pointer; background:#f8fafc;">
          <strong style="font-size:14px; color:#2f5eff; display:block; margin-bottom:4px;">🖨 Office Multi-Function Printers User Guide</strong>
          <span style="font-size:12px; color:#475569;">How to map local workstations to the centralized printing server queue.</span>
        </div>
      </div>
    </div>
    """

def build_kb_article_html():
    return """
    <div style="max-width:850px; margin:0 auto; padding-top:10px; text-align:left;">
      <button onclick="window.setPage('portal_home')" class="btn btn-outline" style="margin-bottom:16px; gap:4px; padding:6px 12px; font-size:12.5px; background:#fff;">
        &larr; Back to Portal Home
      </button>
      
      <div class="card" style="padding:32px;">
        <h1 style="margin-top:0; margin-bottom:8px; font-size:22px; font-weight:700; color:#0f172a;">How to Reset Cisco AnyConnect VPN Password</h1>
        <div style="font-size:12px; color:#64748b; margin-bottom:24px; border-bottom:1px solid #e2e8f0; padding-bottom:12px;">
          Published by <strong>Khaled Zahrani (Network Team)</strong> · Updated 2 days ago · Category: <strong>Network &amp; Security</strong> · Views: <strong>1,420</strong>
        </div>

        <div style="font-size:14px; color:#334155; line-height:1.6; display:flex; flex-direction:column; gap:16px;">
          <p>This guide explains how to reset your corporate Cisco AnyConnect VPN password. Password resets are handled via our self-service directory portal to enforce multi-factor authentication (MFA).</p>
          
          <strong style="color:#0f172a; font-size:15px;">Prerequisites:</strong>
          <ul style="margin:0; padding-left:20px;">
            <li>Your active Employee ID card.</li>
            <li>Your mobile phone with Microsoft Authenticator app configured.</li>
          </ul>

          <strong style="color:#0f172a; font-size:15px; margin-top:8px;">Step-by-Step Instructions:</strong>
          <ol style="margin:0; padding-left:20px; display:flex; flex-direction:column; gap:10px;">
            <li>Go to the self-service reset link: <a href="#" onclick="alert('Opening portal reset console...')" style="color:#2f5eff; font-weight:600;">reset.company.com</a>.</li>
            <li>Enter your username (format: <code>firstname.lastname</code>) and select the domain name <code>CORP</code>.</li>
            <li>You will receive an MFA push notification on your registered phone. Approve the request.</li>
            <li>Once authenticated, enter your new strong password complying with character rules (min 12 chars, capital, number, special character).</li>
            <li>Open Cisco AnyConnect client on your workstation, type the new credentials, and connect.</li>
          </ol>

          <div style="background:#e0f2fe; border:1px solid #bae6fd; border-radius:8px; padding:12px 16px; margin-top:10px; font-size:13px; color:#0369a1;">
            <strong>💡 VPN Token Sync Duration:</strong> Please wait up to 2 minutes after resetting your password before logging into AnyConnect to allow active directories in other zones to synchronize.
          </div>
        </div>

        <div style="margin-top:32px; border-top:1px solid #e2e8f0; padding-top:20px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:13px; color:#64748b;" id="kb-vote-status">Was this article helpful?</span>
          <div style="display:flex; gap:8px;" id="kb-vote-buttons">
            <button onclick="voteArticle(true)" class="btn btn-outline" style="font-size:12.5px; padding:6px 12px; background:#fff;">👍 Yes, helpful</button>
            <button onclick="voteArticle(false)" class="btn btn-outline" style="font-size:12.5px; padding:6px 12px; background:#fff;">👎 No, unclear</button>
          </div>
        </div>
      </div>
    </div>
    """

def build_dashboard_html(dash_type):
    if dash_type == "sla":
        return """
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin-top:10px; text-align:left;">
          <div class="card" style="padding:20px; border-left:4px solid #10b981;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">SLA Compliance Rate</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">94.2%</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Above 92% SLA Target</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #2f5eff;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">First Response Target</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">15 Mins</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Average response: 12.5 Mins</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #f59e0b;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Near-Breach Queue</div>
            <div style="font-size:24px; font-weight:700; color:#f59e0b; margin-top:8px;">3 Tickets</div>
            <div style="font-size:11px; color:#d97706; margin-top:4px;">⚠ Actions required within 30m</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #ef4444;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Breached SLA (Today)</div>
            <div style="font-size:24px; font-weight:700; color:#ef4444; margin-top:8px;">1 Ticket</div>
            <div style="font-size:11px; color:#ef4444; margin-top:4px;">⚡ Logged as SLA exception</div>
          </div>
        </div>

        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:16px; margin-top:20px; text-align:left;">
          <!-- Compliance Trend -->
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:20px; font-size:15px; font-weight:700; color:#0f172a;">Weekly SLA Compliance Trend</h3>
            <!-- CSS Grid Chart -->
            <div style="display:flex; justify-content:space-between; align-items:flex-end; height:200px; padding:0 20px; border-bottom:1px solid #cbd5e1; border-left:1px solid #cbd5e1; margin-bottom:10px;">
              <div style="display:flex; flex-direction:column; align-items:center; gap:8px; width:45px;">
                <div style="width:28px; height:180px; background:#2f5eff; border-radius:4px 4px 0 0; display:flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700;">96%</div>
                <div style="font-size:11px; color:#64748b; font-weight:500;">Mon</div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:center; gap:8px; width:45px;">
                <div style="width:28px; height:160px; background:#2f5eff; border-radius:4px 4px 0 0; display:flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700;">91%</div>
                <div style="font-size:11px; color:#64748b; font-weight:500;">Tue</div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:center; gap:8px; width:45px;">
                <div style="width:28px; height:170px; background:#2f5eff; border-radius:4px 4px 0 0; display:flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700;">94%</div>
                <div style="font-size:11px; color:#64748b; font-weight:500;">Wed</div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:center; gap:8px; width:45px;">
                <div style="width:28px; height:175px; background:#2f5eff; border-radius:4px 4px 0 0; display:flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700;">95%</div>
                <div style="font-size:11px; color:#64748b; font-weight:500;">Thu</div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:center; gap:8px; width:45px;">
                <div style="width:28px; height:165px; background:#2f5eff; border-radius:4px 4px 0 0; display:flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700;">93%</div>
                <div style="font-size:11px; color:#64748b; font-weight:500;">Fri</div>
              </div>
            </div>
          </div>
          <!-- SLA By Priority -->
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:20px; font-size:15px; font-weight:700; color:#0f172a;">Compliance by Priority</h3>
            <div style="display:grid; grid-template-columns:1fr; gap:16px;">
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <strong style="color:#ef4444;">P1 - Critical (Target 1h)</strong>
                  <span style="font-weight:700;">100% compliant</span>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;">
                  <div style="width:100%; height:100%; background:#10b981;"></div>
                </div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <strong style="color:#f59e0b;">P2 - High (Target 4h)</strong>
                  <span style="font-weight:700;">92% compliant</span>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;">
                  <div style="width:92%; height:100%; background:#10b981;"></div>
                </div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <strong style="color:#2f5eff;">P3 - Medium (Target 24h)</strong>
                  <span style="font-weight:700;">95% compliant</span>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;">
                  <div style="width:95%; height:100%; background:#10b981;"></div>
                </div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <strong style="color:#64748b;">P4 - Low (Target 48h)</strong>
                  <span style="font-weight:700;">88% compliant</span>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;">
                  <div style="width:88%; height:100%; background:#f59e0b;"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        """
    elif dash_type == "agent":
        return """
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin-top:10px; text-align:left;">
          <div class="card" style="padding:20px; border-left:4px solid #2f5eff;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Active Helpdesk Agents</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">12 Agents</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">● 8 online right now</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #10b981;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Average Daily Closed</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">14.2 / day</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">▲ 5.4% increase from Q1</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #f59e0b;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Support Team Backlog</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">45 Tickets</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">Average load: 3.75/agent</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #8b5cf6;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Top Performer (This Week)</div>
            <div style="font-size:16px; font-weight:700; color:#8b5cf6; margin-top:14px;">Sarah Otaibi (32 Res)</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">With 100% SLA compliance</div>
          </div>
        </div>

        <!-- Leaderboard Table -->
        <div class="card" style="margin-top:20px; text-align:left;">
          <div style="padding:16px 20px; border-bottom:1px solid #cbd5e1; font-weight:700; font-size:15px; color:#0f172a;">Agent Operational Leaderboard</div>
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Agent Name</th>
                  <th>Assigned Group</th>
                  <th>Tickets Resolved</th>
                  <th>Avg Response Time</th>
                  <th>Avg Resolution Time</th>
                  <th>SLA Compliance</th>
                  <th>CSAT Rating</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Sarah Otaibi</strong></td>
                  <td>ERP Admin Group</td>
                  <td>32</td>
                  <td>8 Mins</td>
                  <td>1.5 Hours</td>
                  <td><span class="status-badge status-active">100%</span></td>
                  <td>★ 4.9 (48 ratings)</td>
                </tr>
                <tr>
                  <td><strong>Bilal Mansoor</strong></td>
                  <td>IT Level 2 Support</td>
                  <td>28</td>
                  <td>11 Mins</td>
                  <td>2.1 Hours</td>
                  <td><span class="status-badge status-active">96.4%</span></td>
                  <td>★ 4.8 (39 ratings)</td>
                </tr>
                <tr>
                  <td><strong>Khaled Zahrani</strong></td>
                  <td>Network &amp; Telecom</td>
                  <td>19</td>
                  <td>14 Mins</td>
                  <td>3.4 Hours</td>
                  <td><span class="status-badge status-pending">91.2%</span></td>
                  <td>★ 4.7 (24 ratings)</td>
                </tr>
                <tr>
                  <td><strong>Samir Al-Dawsari</strong></td>
                  <td>Manager Queue</td>
                  <td>11</td>
                  <td>18 Mins</td>
                  <td>4.2 Hours</td>
                  <td><span class="status-badge status-closed">89.0%</span></td>
                  <td>★ 4.6 (12 ratings)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        """
    elif dash_type == "csat":
        return """
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin-top:10px; text-align:left;">
          <div class="card" style="padding:20px; border-left:4px solid #10b981;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Average CSAT Rating</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">4.83 / 5.0</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Target CSAT: 4.50</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #2f5eff;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Survey Response Rate</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">68.4%</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">▲ Above industry standard (30%)</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #f59e0b;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Total Survey Invites</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">340 Sent</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">232 responses collected</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #ef4444;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Negative Reviews</div>
            <div style="font-size:24px; font-weight:700; color:#ef4444; margin-top:8px;">2 Feedback</div>
            <div style="font-size:11px; color:#ef4444; margin-top:4px;">Follow-up tickets automatically created</div>
          </div>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:20px; text-align:left;">
          <!-- Satisfaction Distribution -->
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:20px; font-size:15px; font-weight:700; color:#0f172a;">Satisfaction Rating Distribution</h3>
            <div style="display:grid; grid-template-columns:1fr; gap:12px; font-size:12.5px;">
              <div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                  <span>★★★★★ Excellent</span>
                  <strong>182 reviews (78%)</strong>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;"><div style="width:78%; height:100%; background:#10b981;"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                  <span>★★★★ Very Good</span>
                  <strong>36 reviews (15%)</strong>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;"><div style="width:15%; height:100%; background:#10b981;"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                  <span>★★★ Satisfactory</span>
                  <strong>12 reviews (5%)</strong>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;"><div style="width:5%; height:100%; background:#f59e0b;"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                  <span>★★ Poor / ★ Unsatisfactory</span>
                  <strong>2 reviews (2%)</strong>
                </div>
                <div style="width:100%; height:8px; background:#f1f5f9; border-radius:4px; overflow:hidden;"><div style="width:2%; height:100%; background:#ef4444;"></div></div>
              </div>
            </div>
          </div>
          
          <!-- Recent Comments -->
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:16px; font-size:15px; font-weight:700; color:#0f172a;">Recent Feedback Comments</h3>
            <div style="display:grid; grid-template-columns:1fr; gap:12px;">
              <div style="padding:10px 12px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; font-size:12.5px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#0f172a; margin-bottom:4px;">
                  <span>Fahad Al-Sulaiman · ★★★★★</span>
                  <span style="font-weight:400; color:#64748b; font-size:11px;">10m ago</span>
                </div>
                <div>"Bilal resolved my VPN issue very fast. He gave clear steps and followed up. Extremely satisfied!"</div>
              </div>
              <div style="padding:10px 12px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; font-size:12.5px;">
                <div style="display:flex; justify-content:space-between; font-weight:700; color:#0f172a; margin-bottom:4px;">
                  <span>Tariq Harbi · ★★★★★</span>
                  <span style="font-weight:400; color:#64748b; font-size:11px;">1h ago</span>
                </div>
                <div>"Permissions were elevated successfully. The support team is doing a great job!"</div>
              </div>
            </div>
          </div>
        </div>
        """
    elif dash_type == "volume":
        return """
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin-top:10px; text-align:left;">
          <div class="card" style="padding:20px; border-left:4px solid #2f5eff;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Total Tickets Logged</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">1,240 Tickets</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">In current fiscal period</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #10b981;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Total Tickets Resolved</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">1,195 Resolved</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ 96.3% overall resolution rate</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #ef4444;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Active Backlog</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">45 Open</div>
            <div style="font-size:11px; color:#cbd5e1; margin-top:4px;">● Standard queue</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #f59e0b;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Peak Traffic Time</div>
            <div style="font-size:18px; font-weight:700; color:#f59e0b; margin-top:14px;">10:00 AM - 12:00 PM</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">Based on historical telemetry</div>
          </div>
        </div>

        <div class="card" style="margin-top:20px; padding:24px; text-align:left;">
          <h3 style="margin-top:0; margin-bottom:20px; font-size:15px; font-weight:700; color:#0f172a;">Weekly Incoming vs Resolved Volume</h3>
          <div style="display:flex; justify-content:space-between; align-items:flex-end; height:180px; border-bottom:1px solid #cbd5e1; border-left:1px solid #cbd5e1; padding:0 30px; margin-bottom:10px;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:60px;">
              <div style="display:flex; gap:4px; align-items:flex-end;">
                <div style="width:14px; height:120px; background:#2f5eff; border-radius:2px 2px 0 0;"></div>
                <div style="width:14px; height:110px; background:#10b981; border-radius:2px 2px 0 0;"></div>
              </div>
              <div style="font-size:11px; color:#64748b; font-weight:500;">Week 26</div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:60px;">
              <div style="display:flex; gap:4px; align-items:flex-end;">
                <div style="width:14px; height:140px; background:#2f5eff; border-radius:2px 2px 0 0;"></div>
                <div style="width:14px; height:135px; background:#10b981; border-radius:2px 2px 0 0;"></div>
              </div>
              <div style="font-size:11px; color:#64748b; font-weight:500;">Week 27</div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:60px;">
              <div style="display:flex; gap:4px; align-items:flex-end;">
                <div style="width:14px; height:130px; background:#2f5eff; border-radius:2px 2px 0 0;"></div>
                <div style="width:14px; height:128px; background:#10b981; border-radius:2px 2px 0 0;"></div>
              </div>
              <div style="font-size:11px; color:#64748b; font-weight:500;">Week 28</div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:6px; width:60px;">
              <div style="display:flex; gap:4px; align-items:flex-end;">
                <div style="width:14px; height:150px; background:#2f5eff; border-radius:2px 2px 0 0;"></div>
                <div style="width:14px; height:142px; background:#10b981; border-radius:2px 2px 0 0;"></div>
              </div>
              <div style="font-size:11px; color:#64748b; font-weight:500;">Week 29</div>
            </div>
          </div>
          <div style="display:flex; gap:20px; justify-content:center; font-size:12px; margin-top:10px;">
            <div style="display:flex; align-items:center; gap:6px;"><span style="width:12px; height:12px; background:#2f5eff; display:inline-block; border-radius:2px;"></span> Incoming Tickets</div>
            <div style="display:flex; align-items:center; gap:6px;"><span style="width:12px; height:12px; background:#10b981; display:inline-block; border-radius:2px;"></span> Resolved Tickets</div>
          </div>
        </div>
        """
    elif dash_type == "response":
        return """
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin-top:10px; text-align:left;">
          <div class="card" style="padding:20px; border-left:4px solid #2f5eff;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Avg First Response Time</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">12.5 Mins</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Target is under 15 Mins</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #10b981;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Avg Resolution Time</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">3.4 Hours</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Target is under 4 Hours</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #f59e0b;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">SLA Met Percentage</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">97.2%</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Exceeding SLA contract threshold</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #ef4444;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Reopen Rate</div>
            <div style="font-size:24px; font-weight:700; color:#ef4444; margin-top:8px;">1.8%</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Under target limit (5%)</div>
          </div>
        </div>

        <div class="card" style="margin-top:20px; text-align:left;">
          <div style="padding:16px 20px; border-bottom:1px solid #cbd5e1; font-weight:700; font-size:15px; color:#0f172a;">Response Metrics By Priority Group</div>
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Priority Level</th>
                  <th>SLA Response Target</th>
                  <th>Actual Avg Response</th>
                  <th>SLA Resolution Target</th>
                  <th>Actual Avg Resolution</th>
                  <th>Compliance Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong style="color:#ef4444;">P1 - Critical</strong></td>
                  <td>15 Mins</td>
                  <td>6 Mins</td>
                  <td>1 Hour</td>
                  <td>48 Mins</td>
                  <td><span class="status-badge status-active">100% Met</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#f59e0b;">P2 - High</strong></td>
                  <td>30 Mins</td>
                  <td>14 Mins</td>
                  <td>4 Hours</td>
                  <td>2.8 Hours</td>
                  <td><span class="status-badge status-active">96.8% Met</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#2f5eff;">P3 - Medium</strong></td>
                  <td>2 Hours</td>
                  <td>45 Mins</td>
                  <td>24 Hours</td>
                  <td>12.5 Hours</td>
                  <td><span class="status-badge status-active">95.2% Met</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#64748b;">P4 - Low</strong></td>
                  <td>4 Hours</td>
                  <td>1.5 Hours</td>
                  <td>48 Hours</td>
                  <td>22.0 Hours</td>
                  <td><span class="status-badge status-pending">89.4% Met</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        """
    elif dash_type == "executive":
        return """
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin-top:10px; text-align:left;">
          <div class="card" style="padding:20px; border-left:4px solid #132238;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Operational Support Budget</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">85,000 SAR</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ 12% Cost savings achieved this month</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #2f5eff;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Centralized SLA Target Met</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">94.2%</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Above Corporate SLA Threshold (92%)</div>
          </div>
          <div class="card" style="padding:20px; border-left:4px solid #10b981;">
            <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">CSAT Average Satisfaction</div>
            <div style="font-size:24px; font-weight:700; color:#0f172a; margin-top:8px;">4.83 / 5.0</div>
            <div style="font-size:11px; color:#10b981; margin-top:4px;">✔ Target CSAT met (4.50)</div>
          </div>
        </div>

        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:16px; margin-top:20px; text-align:left;">
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:12px; font-size:15px; font-weight:700; color:#0f172a;">Executive Service Desk Performance</h3>
            <p style="font-size:13px; color:#475569; line-height:1.45;">Overall service delivery metrics show positive momentum. Automations run successfully, handling 24% of routing exceptions without human dispatch delay. Network &amp; Systems category remains the dominant origin of support requests, mainly driven by MFA authentication configuration adjustments.</p>
            <div style="margin-top:16px; border-top:1px solid #f1f5f9; padding-top:16px;">
              <strong style="font-size:13px; display:block; color:#0f172a; margin-bottom:10px;">Quarterly Strategic Focus</strong>
              <div style="font-size:12.5px; color:#334155; display:flex; flex-direction:column; gap:8px;">
                <div>☑ Implement self-service password reset scripts for all ERP sub-modules (Estimated: Aug 15)</div>
                <div>☑ Deprecate Legacy VPN protocols and switch 100% to Cisco AnyConnect (Completed)</div>
                <div>☐ Recruit 2 Level 2 technical analysts for Night Shifts (In Progress)</div>
              </div>
            </div>
          </div>
          <div class="card" style="padding:24px;">
            <h3 style="margin-top:0; margin-bottom:16px; font-size:15px; font-weight:700; color:#0f172a;">Category Breakdown</h3>
            <div style="display:grid; grid-template-columns:1fr; gap:14px;">
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <span>💻 Network &amp; Security</span>
                  <strong>48%</strong>
                </div>
                <div style="width:100%; height:6px; background:#f1f5f9; border-radius:3px; overflow:hidden;"><div style="width:48%; height:100%; background:#2f5eff;"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <span>⚙ Software / ERP</span>
                  <strong>32%</strong>
                </div>
                <div style="width:100%; height:6px; background:#f1f5f9; border-radius:3px; overflow:hidden;"><div style="width:32%; height:100%; background:#2f5eff;"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <span>🔌 Workstations Hardware</span>
                  <strong>12%</strong>
                </div>
                <div style="width:100%; height:6px; background:#f1f5f9; border-radius:3px; overflow:hidden;"><div style="width:12%; height:100%; background:#2f5eff;"></div></div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                  <span>🏢 Facilities Support</span>
                  <strong>8%</strong>
                </div>
                <div style="width:100%; height:6px; background:#f1f5f9; border-radius:3px; overflow:hidden;"><div style="width:8%; height:100%; background:#2f5eff;"></div></div>
              </div>
            </div>
          </div>
        </div>
        """

# ─────────────────────────────────────────────
# BUILD CONTENT MAP FOR ALL 34 SCREENS
# ─────────────────────────────────────────────
content_map = {}

# Custom pages mapping
content_map["servicedesk_tickets_new"] = build_form_html("new_ticket")
content_map["portal_submit_request"] = build_form_html("portal_request")
content_map["servicedesk_ticket_detail"] = build_detail_html()
content_map["portal_home"] = build_portal_home_html()
content_map["portal_kb_article"] = build_kb_article_html()
content_map["servicedesk_kb_editor"] = build_kb_editor_html()
content_map["servicedesk_kb_articles"] = build_kb_articles_grid()
content_map["servicedesk_live_chat"] = build_chat_html()
content_map["servicedesk_automation_builder"] = build_workflow_html()

# Dashboards mapping
content_map["servicedesk_sla_compliance"] = build_dashboard_html("sla")
content_map["servicedesk_agent_performance"] = build_dashboard_html("agent")
content_map["servicedesk_ticket_volume"] = build_dashboard_html("volume")
content_map["servicedesk_csat"] = build_dashboard_html("csat")
content_map["servicedesk_response_time"] = build_dashboard_html("response")
content_map["servicedesk_executive_dashboard"] = build_dashboard_html("executive")

# Fallback populator for any remaining screens in GROUPS_NAV
for grp_name, page_list in GROUPS_NAV.items():
    for item in page_list:
        pid = item["id"]
        if pid not in content_map:
            t = item["title"]
            if pid in PAGE_CONFIGS:
                content_map[pid] = build_list_html(pid, PAGE_CONFIGS[pid], t)
            else:
                content_map[pid] = build_list_html(pid, {
                    "type": "list",
                    "columns": ["Ticket / Ref Code", "Subject / Summary", "Category / Department", "Assigned Lead", "Date Logged", "Status", "Actions"],
                    "rows": [
                        {"Ticket / Ref Code": f"DSK-2026-001", "Subject / Summary": f"{t} System Entry", "Category / Department": grp_name, "Assigned Lead": "Helpdesk Support", "Date Logged": "2026-07-22", "Status": "active"},
                        {"Ticket / Ref Code": f"DSK-2026-002", "Subject / Summary": f"{t} Operational Task", "Category / Department": grp_name, "Assigned Lead": "IT Operations", "Date Logged": "2026-07-20", "Status": "resolved"},
                        {"Ticket / Ref Code": f"DSK-2026-003", "Subject / Summary": f"{t} Pending Queue Request", "Category / Department": grp_name, "Assigned Lead": "Level 2 Support", "Date Logged": "2026-07-18", "Status": "open"},
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

# Output desk_output_data.json
nav_output = {"config": config_obj}
with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\desk_output_data.json', 'w', encoding='utf-8') as f:
    json.dump(nav_output, f, indent=4)

# ─────────────────────────────────────────────
# CUSTOM JAVASCRIPT BLOCK FOR INTERACTIVITY
# ─────────────────────────────────────────────

CUSTOM_JS = """
    function applyTemplate(subject, desc) {
      const subInput = document.getElementById('t_subject');
      const descInput = document.getElementById('t_description');
      if (subInput) subInput.value = subject;
      if (descInput) descInput.value = desc;
    }

    let activeReplyTab = 'reply';
    function setReplyTab(tab) {
      activeReplyTab = tab;
      const replyBtn = document.getElementById('tab-reply-btn');
      const noteBtn = document.getElementById('tab-note-btn');
      const replyBox = document.getElementById('detail-reply-box');
      if (!replyBtn || !noteBtn || !replyBox) return;
      if (tab === 'reply') {
        replyBtn.style.color = '#2f5eff';
        replyBtn.style.borderBottom = '2px solid #2f5eff';
        replyBtn.style.fontWeight = '700';
        noteBtn.style.color = '#64748b';
        noteBtn.style.borderBottom = 'none';
        noteBtn.style.fontWeight = '600';
        replyBox.placeholder = 'Write your response to the customer...';
      } else {
        noteBtn.style.color = '#b45309';
        noteBtn.style.borderBottom = '2px solid #b45309';
        noteBtn.style.fontWeight = '700';
        replyBtn.style.color = '#64748b';
        replyBtn.style.borderBottom = 'none';
        replyBtn.style.fontWeight = '600';
        replyBox.placeholder = 'Write an internal note (only visible to support agents)...';
      }
    }

    function submitDetailTimeline() {
      const replyBox = document.getElementById('detail-reply-box');
      if (!replyBox || !replyBox.value.trim()) return;
      const text = replyBox.value.trim();
      const container = document.getElementById('detail-timeline-container');
      
      const newBlock = document.createElement('div');
      newBlock.style.display = 'flex';
      newBlock.style.gap = '16px';
      
      if (activeReplyTab === 'reply') {
        newBlock.innerHTML = `
          <div style="width:36px; height:36px; border-radius:50%; background:#2f5eff; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">SD</div>
          <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
              <strong style="font-size:13.5px; color:#0f172a;">Samir Al-Dawsari (Support Manager)</strong>
              <span style="font-size:11px; color:#64748b;">Just now</span>
            </div>
            <div style="background:#e0e7ff; border:1px solid #c7d2fe; border-radius:8px; padding:14px; font-size:13px; color:#1e1b4b; line-height:1.45;">
              ${text.replace(/\\n/g, '<br>')}
            </div>
          </div>
        `;
      } else {
        newBlock.innerHTML = `
          <div style="width:36px; height:36px; border-radius:50%; background:#fde68a; color:#78350f; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">SD</div>
          <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
              <strong style="font-size:13.5px; color:#78350f;">Samir Al-Dawsari (Internal Agent Note)</strong>
              <span style="font-size:11px; color:#64748b;">Just now</span>
            </div>
            <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:14px; font-size:13px; color:#78350f; line-height:1.45;">
              ${text.replace(/\\n/g, '<br>')}
            </div>
          </div>
        `;
      }
      container.appendChild(newBlock);
      replyBox.value = '';
    }

    function voteArticle(helpful) {
      const status = document.getElementById('kb-vote-status');
      const buttons = document.getElementById('kb-vote-buttons');
      if (status && buttons) {
        status.innerHTML = helpful ? '✔ Thank you! You voted this article as helpful.' : '❌ Thank you for your feedback. We will improve this article.';
        status.style.color = helpful ? '#10b981' : '#be123c';
        status.style.fontWeight = '700';
        buttons.style.display = 'none';
      }
    }

    function selectChat(el, name) {
      const container = document.getElementById('chat-queue-container');
      if (!container) return;
      const items = container.children;
      for (const item of items) {
        item.style.background = 'transparent';
        item.style.borderLeft = 'none';
      }
      el.style.background = '#e0e7ff';
      el.style.borderLeft = '4px solid #2f5eff';
      
      const activeName = document.getElementById('active-chat-name');
      if (activeName) activeName.innerText = name;
      
      const msgBox = document.getElementById('chat-thread-messages');
      if (msgBox) {
        msgBox.innerHTML = `
          <div style="align-self:flex-start; max-width:70%;">
            <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-left:4px;">${name} · 13:40</div>
            <div style="background:#f1f5f9; color:#0f172a; padding:12px 16px; border-radius:0 12px 12px 12px; font-size:13px; line-height:1.4;">
              Hi, I need assistance regarding active system configurations of my account.
            </div>
          </div>
        `;
      }
    }

    function sendChatMessage() {
      const input = document.getElementById('chat-input');
      const msgBox = document.getElementById('chat-thread-messages');
      if (!input || !input.value.trim() || !msgBox) return;
      const text = input.value.trim();
      
      const userBubble = document.createElement('div');
      userBubble.style.alignSelf = 'flex-end';
      userBubble.style.maxWidth = '70%';
      userBubble.innerHTML = `
        <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-right:4px; text-align:right;">Samir (You) · Just now</div>
        <div style="background:#2f5eff; color:#fff; padding:12px 16px; border-radius:12px 0 12px 12px; font-size:13px; line-height:1.4;">
          ${text}
        </div>
      `;
      msgBox.appendChild(userBubble);
      input.value = '';
      msgBox.scrollTop = msgBox.scrollHeight;
      
      const name = document.getElementById('active-chat-name').innerText;
      setTimeout(() => {
        const typing = document.createElement('div');
        typing.style.alignSelf = 'flex-start';
        typing.style.maxWidth = '70%';
        typing.id = 'chat-typing-indicator';
        typing.innerHTML = `
          <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-left:4px;">${name} · Typing...</div>
          <div style="background:#f1f5f9; color:#64748b; padding:10px 16px; border-radius:0 12px 12px 12px; font-size:12.5px; font-style:italic;">
            Typing message...
          </div>
        `;
        msgBox.appendChild(typing);
        msgBox.scrollTop = msgBox.scrollHeight;
        
        setTimeout(() => {
          const el = document.getElementById('chat-typing-indicator');
          if (el) el.remove();
          
          const reply = document.createElement('div');
          reply.style.alignSelf = 'flex-start';
          reply.style.maxWidth = '70%';
          reply.innerHTML = `
            <div style="font-size:11px; color:#64748b; margin-bottom:4px; margin-left:4px;">${name} · Just now</div>
            <div style="background:#f1f5f9; color:#0f172a; padding:12px 16px; border-radius:0 12px 12px 12px; font-size:13px; line-height:1.4;">
              Thanks for the update. I will try that configuration now and report back if any problems persist.
            </div>
          `;
          msgBox.appendChild(reply);
          msgBox.scrollTop = msgBox.scrollHeight;
        }, 1200);
      }, 600);
    }
"""

# ─────────────────────────────────────────────
# GENERATE SERVICE DESK SPA HTML FILE
# ─────────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AureliaHRMS · Enterprise Service Desk ERP</title>
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
    .status-actionreq {{ background:#fdeceb; color:#c0362c; }}
  </style>
</head>
<body>
  <div style="display:flex; width:100vw; height:100vh;">
    <!-- SIDEBAR -->
    <aside class="sidebar" style="width:200px; height:100vh; flex-shrink:0; display:flex; flex-direction:column; border-right:1px solid #1e2d42;">
      <div style="height:60px; padding:0 16px; display:flex; align-items:center; gap:8px; border-bottom:1px solid #1e2d42; box-sizing:border-box;">
        <div style="width:32px; height:32px; border-radius:8px; background:#2f5eff; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:16px;">SD</div>
        <div>
          <div style="font-size:15px; font-weight:700; color:#fff; letter-spacing:-0.2px;">ExeonDesk</div>
          <div style="font-size:11px; color:#94a3b8;">Service Desk ERP</div>
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
            <div class="user-avatar" id="profileAvatarBtn" onclick="toggleProfileMenu(event)">SD</div>
            <div class="profile-dropdown-card" id="profileDropdownCard">
              <div class="p-card-header">
                <div class="p-card-avatar">SD</div>
                <div class="p-card-info">
                  <div class="p-card-name">Samir Al-Dawsari</div>
                  <div class="p-card-role">Service Desk Manager</div>
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
          <span class="crumb" style="color:#64748b; font-weight:500;" id="breadcrumb-group">Setup &amp; Master Data</span>
          <span style="color:#94a3b8; margin:0 4px;">·</span>
          <span class="crumb" style="color:#2f5eff; font-weight:600;" id="breadcrumb-page">Service Catalog</span>
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
        const close  = (g === 'Setup & Master Data' || g === ALL_GROUPS[0]) ? '' : `<span class="close-btn" onclick="closeTab(event,'${{g}}')">&times;</span>`;
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
        const icon = `<svg style="width:16px; height:16px; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"></path><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path></svg>`;
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
      if (g === 'Setup & Master Data' || g === ALL_GROUPS[0]) return;
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
                <div style="width:52px; height:52px; border-radius:50%; background:#e0e7ff; color:#3730a3; font-weight:700; font-size:18px; display:flex; align-items:center; justify-content:center; border:2px solid #c7d2fe;">SD</div>
                <div>
                  <h2 style="margin:0; font-size:18px; font-weight:700; color:#0f172a;">Samir Al-Dawsari</h2>
                  <div style="font-size:13px; color:#64748b; font-weight:500;">Service Desk Manager · Employee ID: EMP-2041</div>
                </div>
              </div>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div class="form-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">First Name</label><input type="text" value="Samir" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Last Name</label><input type="text" value="Al-Dawsari" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Email Address</label><input type="email" value="samir.dawsari@company.com" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Phone Number</label><input type="text" value="+966 55 987 6543" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Department</label><input type="text" value="IT &amp; Technical Support" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Role Level</label><input type="text" value="Service Desk Manager (Level 4)" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
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
              <div style="font-size:14px; font-weight:700; color:#0f172a; margin-bottom:10px;">Service Desk Preferences</div>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Default Queue</label><select style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"><option>All Open Tickets</option><option>My Assigned Tickets</option><option>Unassigned Triage Queue</option></select></div>
                <div><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">SLA Breach Sound Alert</label><select style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"><option>Enabled (Chime)</option><option>Disabled</option></select></div>
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
              <h2 style="margin:0; font-size:17px; font-weight:700; color:#0f172a;">Service Desk Help &amp; ITKB</h2>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div style="margin-bottom:16px;">
              <input type="text" placeholder="Search Service Desk docs, SLA escalation &amp; ticket triage..." style="width:100%; padding:10px 14px; border:1px solid #cbd5e1; border-radius:8px; font-size:13.5px;" oninput="const q = this.value.toLowerCase(); this.parentElement.nextElementSibling.querySelectorAll('div').forEach(d => d.style.display = d.textContent.toLowerCase().includes(q) ? '' : 'none');">
            </div>
            <div style="display:grid; grid-template-columns:1fr; gap:10px;">
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">🎫 Managing Ticket Escalation &amp; SLA Breach Rules</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">How ticket priorities automatically adjust SLA response targets.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">🤖 Automation Builder &amp; Auto-Routing</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Setting up round-robin and skill-based assignment for incoming tickets.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📞 Contact Enterprise Support Administrator</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Submit a priority request or email servicedesk.admin@company.com</div></div>
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
      if (confirm('Are you sure you want to sign out of ExeonDesk ERP?')) {{
        window.location.href = 'login.html';
      }}
    }}

    // Dynamic helper scripts for interactive views
    {CUSTOM_JS}

    window.addEventListener('DOMContentLoaded', () => {{ handleUrlRoutingOnLoad(GROUPS); renderTopNav(); renderSidebar(); renderContent(); wireGlobalSearch('desk'); }} );
  </script>
</body>
</html>
"""

with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\templates\desk.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("desk.html generated successfully with professional custom ERP pages!")
