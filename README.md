# Enterprise ERP & HRMS System

A comprehensive, enterprise-grade **Human Resource Management System (HRMS)** and **Manufacturing ERP Platform** built with Flask, PostgreSQL, and a highly responsive Vanilla JS/CSS Single Page Application (SPA) frontend.

---

## 📁 Required Core System Files

The following core files are required for operating the system:

| File Name | Purpose / Description |
|---|---|
| `app.py` | Main Flask web server exposing routes for HRMS (`/` redirects to login), Manufacturing ERP (`/manufacture`), Procurement ERP (`/procurement`), Service Desk ERP (`/desk`), Project Management ERP (`/project`), Inventory ERP (`/inventory`), Finance ERP (`/finance`), Asset ERP (`/asset`), CRM ERP (`/crm`), and Sales & Distribution ERP (`/sales`). |
| `generate_manufacture_grid.py` | Centralized generator script for all 119 Manufacturing ERP screens. |
| `generate_procurement_grid.py` | Centralized generator script for all 41 Procurement ERP screens. |
| `generate_desk_grid.py` | Centralized generator script for all 34 Service Desk ERP screens. |
| `generate_project_grid.py` | Centralized generator script for all 39 Project Management ERP screens. |
| `generate_inventory_grid.py` | Centralized generator script for all 44 Inventory Management ERP screens. |
| `generate_finance_grid.py` | Centralized generator script for all 44 Finance & Accounting ERP screens. |
| `generate_asset_grid.py` | Centralized generator script for all 36 Asset Management ERP screens. |
| `generate_crm_grid.py` | Centralized generator script for all 37 CRM Management ERP screens. |
| `generate_sales_grid.py` | Centralized generator script for all 38 Sales & Distribution ERP screens. |
| `output_data.json` | Master navigation schema for Manufacturing pages. |
| `procurement_output_data.json` | Master navigation schema for Procurement pages. |
| `desk_output_data.json` | Master navigation schema for Service Desk pages. |
| `project_output_data.json` | Master navigation schema for Project Management pages. |
| `inventory_output_data.json` | Master navigation schema for Inventory Management pages. |
| `finance_output_data.json` | Master navigation schema for Finance & Accounting pages. |
| `asset_output_data.json` | Master navigation schema for Asset Management pages. |
| `crm_output_data.json` | Master navigation schema for CRM Management pages. |
| `sales_output_data.json` | Master navigation schema for Sales & Distribution pages. |
| `templates/erpset.html` | Enterprise ERP Settings &amp; Super Admin System Administration Control Center. |
| `templates/manufacture.html` | Dynamic Single Page Application (SPA) container for Manufacturing ERP. |
| `templates/procurement.html` | Dynamic Single Page Application (SPA) container for Procurement ERP. |
| `templates/desk.html` | Dynamic Single Page Application (SPA) container for Service Desk ERP. |
| `templates/project.html` | Dynamic Single Page Application (SPA) container for Project Management ERP. |
| `templates/inventory.html` | Dynamic Single Page Application (SPA) container for Inventory Management ERP. |
| `templates/finance.html` | Dynamic Single Page Application (SPA) container for Finance & Accounting ERP. |
| `templates/asset.html` | Dynamic Single Page Application (SPA) container for Asset Management ERP. |
| `templates/crm.html` | Dynamic Single Page Application (SPA) container for CRM Management ERP. |
| `templates/sales.html` | Dynamic Single Page Application (SPA) container for Sales & Distribution ERP. |
| `templates/payroll.html` | Dynamic Single Page Application (SPA) container for HRMS & Payroll. |
| `hrms_schema.sql` | PostgreSQL database schema for tables, indexes, and relations. |
| `seed.sql` | Database seed file for initial master records and data. |
| `requirements.txt` | Python library dependencies (`flask`, `psycopg2-binary`, `openpyxl`). |
| `.env` | Environment configuration file containing database credentials (`DATABASE_URL`). |

---

## 🏭 Manufacturing ERP Modules & Complete Page List (119 Screens)

### 1. Production Planning (11 Pages)
- **Production Planning Dashboard** (`/mfg/pp/production-planning-dashboard`)
- **Production Plan** (`/mfg/pp/production-plan`)
- **Master Production Schedule (MPS)** (`/mfg/pp/master-production-schedule-mps`)
- **Material Requirement Planning (MRP)** (`/mfg/pp/material-requirement-planning-mrp`)
- **Capacity Planning** (`/mfg/pp/capacity-planning`)
- **Demand Forecast** (`/mfg/pp/demand-forecast`)
- **Production Calendar** (`/mfg/pp/production-calendar`)
- **Resource Planning** (`/mfg/pp/resource-planning`)
- **Shift Planning** (`/mfg/pp/shift-planning`)
- **Production Plan Approval** (`/mfg/pp/production-plan-approval`)
- **Production Plan Reports** (`/mfg/pp/production-plan-reports`)

### 2. Work Orders (10 Pages)
- **Work Order Dashboard** (`/mfg/wo/work-order-dashboard`)
- **Work Order List** (`/mfg/wo/work-order-list`)
- **Create Work Order** (`/mfg/wo/create-work-order`)
- **Edit Work Order** (`/mfg/wo/edit-work-order`)
- **Work Order Details** (`/mfg/wo/work-order-details`)
- **Release Work Order** (`/mfg/wo/release-work-order`)
- **Work Order Tracking** (`/mfg/wo/work-order-tracking`)
- **Work Order Closure** (`/mfg/wo/work-order-closure`)
- **Work Order History** (`/mfg/wo/work-order-history`)
- **Work Order Reports** (`/mfg/wo/work-order-reports`)

### 3. Shop Floor Execution (12 Pages)
- **Shop Floor Dashboard** (`/mfg/sfe/shop-floor-dashboard`)
- **Production Monitoring** (`/mfg/sfe/production-monitoring`)
- **Operator Dashboard** (`/mfg/sfe/operator-dashboard`)
- **Machine Status** (`/mfg/sfe/machine-status`)
- **Job Assignment** (`/mfg/sfe/job-assignment`)
- **Production Entry** (`/mfg/sfe/production-entry`)
- **Downtime Recording** (`/mfg/sfe/downtime-recording`)
- **Labor Time Entry** (`/mfg/sfe/labor-time-entry`)
- **Shift Monitoring** (`/mfg/sfe/shift-monitoring`)
- **WIP Tracking** (`/mfg/sfe/wip-tracking`)
- **Production Completion** (`/mfg/sfe/production-completion`)
- **Shop Floor Reports** (`/mfg/sfe/shop-floor-reports`)

### 4. Material Management (15 Pages)
- **Material Management Dashboard** (`/mfg/mm/material-management-dashboard`)
- **Stock Availability** (`/mfg/mm/stock-availability`)
- **Item Master** (`/mfg/mm/item-master`)
- **Warehouse Master** (`/mfg/mm/warehouse-master`)
- **Bin Location Master** (`/mfg/mm/bin-location-master`)
- **Material Request** (`/mfg/mm/material-request`)
- **Material Issue** (`/mfg/mm/material-issue`)
- **Goods Receipt Note (GRN)** (`/mfg/mm/goods-receipt-note-grn`)
- **Material Transfer** (`/mfg/mm/material-transfer`)
- **Inventory Adjustment** (`/mfg/mm/inventory-adjustment`)
- **Cycle Count** (`/mfg/mm/cycle-count`)
- **Physical Inventory** (`/mfg/mm/physical-inventory`)
- **Batch Management** (`/mfg/mm/batch-management`)
- **Serial Number Tracking** (`/mfg/mm/serial-number-tracking`)
- **Inventory Reports** (`/mfg/mm/inventory-reports`)

### 5. Quality Management (11 Pages)
- **Quality Dashboard** (`/mfg/qm/quality-dashboard`)
- **Inspection Plan** (`/mfg/qm/inspection-plan`)
- **Inspection Lot** (`/mfg/qm/inspection-lot`)
- **Incoming Quality Inspection (IQC)** (`/mfg/qm/incoming-quality-inspection`)
- **In-Process Inspection (IPQC)** (`/mfg/qm/in-process-inspection`)
- **Final Inspection (OQC)** (`/mfg/qm/final-inspection`)
- **Non-Conformance Report (NCR)** (`/mfg/qm/non-conformance-report-ncr`)
- **CAPA** (`/mfg/qm/capa`)
- **Defect Recording** (`/mfg/qm/defect-recording`)
- **Quality Certificates** (`/mfg/qm/quality-certificates`)
- **Quality Reports** (`/mfg/qm/quality-reports`)

### 6. Maintenance Management (12 Pages)
- **Maintenance Dashboard** (`/mfg/mnt/maintenance-dashboard`)
- **Asset Master** (`/mfg/mnt/asset-master`)
- **Equipment Master** (`/mfg/mnt/equipment-master`)
- **Preventive Maintenance** (`/mfg/mnt/preventive-maintenance`)
- **Breakdown Maintenance** (`/mfg/mnt/breakdown-maintenance`)
- **Maintenance Work Orders** (`/mfg/mnt/maintenance-work-orders`)
- **Maintenance Schedule** (`/mfg/mnt/maintenance-schedule`)
- **Spare Parts Management** (`/mfg/mnt/spare-parts-management`)
- **Technician Assignment** (`/mfg/mnt/technician-assignment`)
- **Maintenance History** (`/mfg/mnt/maintenance-history`)
- **Calibration Schedule** (`/mfg/mnt/calibration-schedule`)
- **Maintenance Reports** (`/mfg/mnt/maintenance-reports`)

### 7. Subcontracting (9 Pages)
- **Subcontract Dashboard** (`/mfg/sub/subcontract-dashboard`)
- **Vendor Assignment** (`/mfg/sub/vendor-assignment`)
- **Subcontract Order** (`/mfg/sub/subcontract-order`)
- **Material Issue to Vendor** (`/mfg/sub/material-issue-to-vendor`)
- **Material Receipt from Vendor** (`/mfg/sub/material-receipt-from-vendor`)
- **Vendor Performance** (`/mfg/sub/vendor-performance`)
- **Job Tracking** (`/mfg/sub/job-tracking`)
- **Cost Analysis** (`/mfg/sub/cost-analysis`)
- **Subcontract Reports** (`/mfg/sub/subcontract-reports`)

### 8. Production Costing (11 Pages)
- **Costing Dashboard** (`/mfg/pc/costing-dashboard`)
- **BOM Costing** (`/mfg/pc/bom-costing`)
- **Routing Cost** (`/mfg/pc/routing-cost`)
- **Standard Cost** (`/mfg/pc/standard-cost`)
- **Actual Cost** (`/mfg/pc/actual-cost`)
- **Variance Analysis** (`/mfg/pc/variance-analysis`)
- **Labor Cost** (`/mfg/pc/labor-cost`)
- **Machine Cost** (`/mfg/pc/machine-cost`)
- **Overhead Cost** (`/mfg/pc/overhead-cost`)
- **Cost Rollup** (`/mfg/pc/cost-rollup`)
- **Cost Reports** (`/mfg/pc/cost-reports`)

### 9. Analytics & Reporting (10 Pages)
- **Executive Dashboard** (`/mfg/ar/executive-dashboard`)
- **Production KPI Dashboard** (`/mfg/ar/production-kpi-dashboard`)
- **Inventory Dashboard** (`/mfg/ar/inventory-dashboard`)
- **OEE Dashboard** (`/mfg/ar/oee-dashboard`)
- **Quality Dashboard** (`/mfg/ar/quality-dashboard`)
- **Maintenance Dashboard** (`/mfg/ar/maintenance-dashboard`)
- **Cost Dashboard** (`/mfg/ar/cost-dashboard`)
- **Custom Reports** (`/mfg/ar/custom-reports`)
- **Scheduled Reports** (`/mfg/ar/scheduled-reports`)
- **Export Center** (`/mfg/ar/export-center`)

### 10. Administration (18 Pages)
- **User Management** (`/mfg/admin/user-management`)
- **Role Management** (`/mfg/admin/role-management`)
- **Permission Management** (`/mfg/admin/permission-management`)
- **Company Setup** (`/mfg/admin/company-setup`)
- **Plant Setup** (`/mfg/admin/plant-setup`)
- **Department Master** (`/mfg/admin/department-master`)
- **Work Center Master** (`/mfg/admin/work-center-master`)
- **Machine Master** (`/mfg/admin/machine-master`)
- **Shift Master** (`/mfg/admin/shift-master`)
- **Calendar Master** (`/mfg/admin/calendar-master`)
- **Number Series** (`/mfg/admin/number-series`)
- **Workflow Setup** (`/mfg/admin/workflow-setup`)
- **Approval Setup** (`/mfg/admin/approval-setup`)
- **Notification Setup** (`/mfg/admin/notification-setup`)
- **Audit Log** (`/mfg/admin/audit-log`)
- **System Configuration** (`/mfg/admin/system-configuration`)
- **Backup & Restore** (`/mfg/admin/backup-restore`)
- **Integration Settings** (`/mfg/admin/integration-settings`)

---

## 🚀 How to Run the Application

### 1. Start the Flask Web Server
```bash
python app.py
```

### 2. Access the Application Links
- **ERP Portal Login Page (HRMS Entrance)**: `http://127.0.0.1:5000/` (redirects to `/login.html`, navigate to `/payroll.html` after logging in)
- **Manufacturing ERP Platform**: `http://127.0.0.1:5000/manufacture`

### 3. Regenerating Manufacturing UI (Optional)
If you update `output_data.json` or `generate_manufacture_grid.py`, regenerate the frontend html template with:
```bash
python generate_manufacture_grid.py
```

## 🛠️ HRMS & Payroll Customizations

The HRMS & Payroll module has been customized with the following production-grade features:

### 1. Expanded Employee Database Schema (34 Custom Fields)
The database has been migrated to support detailed profiles with fields including:
- **Core Info**: Personnel code, job title, expatriate flag, religion, labor union membership.
- **Organization & Shift**: Facility, work center, shift designation, supervisor code, parent department, and leaf sub-department.
- **Identification & Labor**: Passport details, labour card info (issue/expiry), residence card credentials.
- **Separation**: Relieving dates, separation reasons, and mode of separation.

These details are permanently documented in the [hrms_schema.sql](file:///c:/Users/Arfath.khan/Downloads/HRM2/hrms_payroll/hrms_schema.sql) file.

### 2. Custom Excel Import Template
- Generated a styled, structured spreadsheet at [employee_upload_template.xlsx](file:///c:/Users/Arfath.khan/Downloads/HRM2/hrms_payroll/employee_upload_template.xlsx) mapped directly to the 34 fields.
- Implemented robust error handling, flexible header identification, dynamic creation of missing structural lines (e.g. `BASIC`), and manager mapping in `/api/employees/import`.

### 3. Hierarchical Department & Sub-Department Filtering
- Refactored the backend department endpoints to resolve hierarchical parent-child relationships.
- Wired the **Sub Department** filter in the Employee Dashboard to populate dynamically depending on the selected parent department.

### 4. Paginated Data Grids (15 Entries/Page)
Added client-side pagination to the following screens:
- **Employee Dashboard Grid**
- **Headcount Analytics Employee Roster Grid**
- **Shift Roster Grid**
- **Employee Master Settings Grid**
- **Document Expiry Grid**

### 5. Document Expiry Refresh Button
- Integrated a live **Refresh** button next to Excel and PDF exports, pulling the latest document status changes directly from the database asynchronously.

### 6. Root URL Login Landing Page
- Configured the root path (`/`) to redirect users directly to the login panel (`login.html`), transitioning to the ERP portal upon successful authentication.