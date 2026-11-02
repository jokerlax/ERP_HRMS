import json
import os

# ─────────────────────────────────────────────
# PAGE CONFIGURATION: columns + mock data per page
# ─────────────────────────────────────────────
PAGE_CONFIGS = {

    # ═══════════════════════════════════════
    # PRODUCTION PLANNING
    # ═══════════════════════════════════════
    "pp_production_planning_dashboard": {"type": "dashboard"},

    "pp_production_plan": {
        "type": "list",
        "columns": ["Plan Code", "Plan Name", "Planning Horizon", "Target Output Qty", "Allocated Work Centers", "Start Date", "End Date", "Planner", "Status", "Actions"],
        "rows": [
            {"Plan Code": "PP-2026-Q3-01", "Plan Name": "Q3 High-Demand Furniture Build", "Planning Horizon": "3 Months", "Target Output Qty": "4,500 units", "Allocated Work Centers": "CNC, Assembly 1 & 2", "Start Date": "2026-07-01", "End Date": "2026-09-30", "Planner": "A. Al-Mansoor", "Status": "active"},
            {"Plan Code": "PP-2026-Q3-02", "Plan Name": "Metal Desk & Cabinet Line", "Planning Horizon": "1 Month", "Target Output Qty": "1,200 units", "Allocated Work Centers": "Welding Bay, Paint Shop", "Start Date": "2026-07-15", "End Date": "2026-08-15", "Planner": "S. Rahal", "Status": "active"},
            {"Plan Code": "PP-2026-Q3-03", "Plan Name": "Upholstery & Fabric Production", "Planning Horizon": "2 Months", "Target Output Qty": "800 units", "Allocated Work Centers": "Upholstery Stn 1", "Start Date": "2026-08-01", "End Date": "2026-09-30", "Planner": "M. Farooq", "Status": "draft"},
            {"Plan Code": "PP-2026-Q2-04", "Plan Name": "Q2 Export Order Fulfillment", "Planning Horizon": "3 Months", "Target Output Qty": "6,000 units", "Allocated Work Centers": "All Plants", "Start Date": "2026-04-01", "End Date": "2026-06-30", "Planner": "A. Al-Mansoor", "Status": "completed"},
        ]
    },

    "pp_master_production_schedule_mps": {
        "type": "list",
        "columns": ["MPS Code", "Item Code & Description", "Plant", "Total Demand", "Week 1 (Jul 21)", "Week 2 (Jul 28)", "Week 3 (Aug 04)", "Week 4 (Aug 11)", "Total Build Qty", "Stock On Hand", "Net Available", "Status", "Actions"],
        "rows": [
            {"MPS Code": "MPS-2026-001", "Item Code & Description": "FG-WOOD-001 (Wooden Ergonomic Chair)", "Plant": "Riyadh Main", "Total Demand": "500 units", "Week 1 (Jul 21)": "150", "Week 2 (Jul 28)": "150", "Week 3 (Aug 04)": "100", "Week 4 (Aug 11)": "100", "Total Build Qty": "500", "Stock On Hand": "85", "Net Available": "585", "Status": "active"},
            {"MPS Code": "MPS-2026-002", "Item Code & Description": "FG-MET-004 (Metal Executive Desk Frame)", "Plant": "Dammam Plant", "Total Demand": "350 units", "Week 1 (Jul 21)": "100", "Week 2 (Jul 28)": "100", "Week 3 (Aug 04)": "100", "Week 4 (Aug 11)": "50", "Total Build Qty": "350", "Stock On Hand": "40", "Net Available": "390", "Status": "active"},
            {"MPS Code": "MPS-2026-003", "Item Code & Description": "FG-UPH-008 (Leather Sofa Cover Set)", "Plant": "Jeddah Plant", "Total Demand": "200 units", "Week 1 (Jul 21)": "50", "Week 2 (Jul 28)": "50", "Week 3 (Aug 04)": "50", "Week 4 (Aug 11)": "50", "Total Build Qty": "200", "Stock On Hand": "15", "Net Available": "215", "Status": "pending"},
            {"MPS Code": "MPS-2026-004", "Item Code & Description": "FG-CAB-012 (Cabinet Hardware Modular Kit)", "Plant": "Riyadh Main", "Total Demand": "1,200 units", "Week 1 (Jul 21)": "300", "Week 2 (Jul 28)": "300", "Week 3 (Aug 04)": "300", "Week 4 (Aug 11)": "300", "Total Build Qty": "1,200", "Stock On Hand": "250", "Net Available": "1,450", "Status": "active"},
            {"MPS Code": "MPS-2026-005", "Item Code & Description": "FG-STL-006 (Heavy Duty Steel Storage Shelf)", "Plant": "Riyadh Main", "Total Demand": "800 units", "Week 1 (Jul 21)": "200", "Week 2 (Jul 28)": "200", "Week 3 (Aug 04)": "200", "Week 4 (Aug 11)": "200", "Total Build Qty": "800", "Stock On Hand": "120", "Net Available": "920", "Status": "in_review"},
        ]
    },

    "pp_material_requirement_planning_mrp": {
        "type": "list",
        "columns": ["MRP Run ID", "Item Code & Description", "Gross Req", "Scheduled Rec", "Projected Avail", "Net Req", "Planned Order Release", "Action Recommended", "Status", "Actions"],
        "rows": [
            {"MRP Run ID": "MRP-2026-089", "Item Code & Description": "RM-TIMBER-001 (Oak Wood Plank 2x4)", "Gross Req": "1,200 pcs", "Scheduled Rec": "300 pcs", "Projected Avail": "150 pcs", "Net Req": "750 pcs", "Planned Order Release": "PO-2026-091 (Jul 24)", "Action Recommended": "Issue PO immediately", "Status": "action_required"},
            {"MRP Run ID": "MRP-2026-089", "Item Code & Description": "RM-STEEL-004 (Cold Rolled Steel Sheet)", "Gross Req": "850 sheets", "Scheduled Rec": "500 sheets", "Projected Avail": "400 sheets", "Net Req": "0 sheets", "Planned Order Release": "—", "Action Recommended": "Stock sufficient", "Status": "normal"},
            {"MRP Run ID": "MRP-2026-089", "Item Code & Description": "RM-LEATH-002 (Premium Brown Leather)", "Gross Req": "450 sqm", "Scheduled Rec": "0 sqm", "Projected Avail": "80 sqm", "Net Req": "370 sqm", "Planned Order Release": "PO-2026-094 (Jul 25)", "Action Recommended": "Expedite delivery", "Status": "action_required"},
            {"MRP Run ID": "MRP-2026-088", "Item Code & Description": "CM-SCREW-012 (M6 Stainless Screws)", "Gross Req": "15,000 pcs", "Scheduled Rec": "10,000 pcs", "Projected Avail": "8,000 pcs", "Net Req": "0 pcs", "Planned Order Release": "—", "Action Recommended": "Stock sufficient", "Status": "normal"},
        ]
    },

    "pp_capacity_planning": {
        "type": "list",
        "columns": ["Work Center Code", "Work Center Name", "Department", "Available Capacity", "Required Load", "Utilization %", "Capacity Load Status", "Shift Model", "Actions"],
        "rows": [
            {"Work Center Code": "WC-CNC-01", "Work Center Name": "CNC Cutting & Milling Bay", "Department": "Machining", "Available Capacity": "160 hrs/wk", "Required Load": "184 hrs/wk", "Utilization %": "115%", "Capacity Load Status": "overloaded", "Shift Model": "2 Shifts (16 hrs/day)"},
            {"Work Center Code": "WC-ASM-01", "Work Center Name": "Main Furniture Assembly", "Department": "Assembly", "Available Capacity": "240 hrs/wk", "Required Load": "210 hrs/wk", "Utilization %": "87.5%", "Capacity Load Status": "normal", "Shift Model": "3 Shifts (24 hrs/day)"},
            {"Work Center Code": "WC-WLD-02", "Work Center Name": "Robotic Welding Bay", "Department": "Metal Work", "Available Capacity": "120 hrs/wk", "Required Load": "118 hrs/wk", "Utilization %": "98.3%", "Capacity Load Status": "normal", "Shift Model": "2 Shifts (16 hrs/day)"},
            {"Work Center Code": "WC-PNT-01", "Work Center Name": "Powder Coating Booth", "Department": "Finishing", "Available Capacity": "160 hrs/wk", "Required Load": "95 hrs/wk", "Utilization %": "59.3%", "Capacity Load Status": "underutilized", "Shift Model": "2 Shifts (16 hrs/day)"},
        ]
    },

    "pp_demand_forecast": {
        "type": "list",
        "columns": ["Forecast Code", "Product Line", "Period", "Historical Base", "AI Forecast Model", "Predicted Demand", "Planner Adjustment", "Final Approved Forecast", "Status", "Actions"],
        "rows": [
            {"Forecast Code": "FC-2026-Q3-W", "Product Line": "Wooden Office Chairs", "Period": "Q3 2026", "Historical Base": "1,200 units", "AI Forecast Model": "Holt-Winters Seasonal", "Predicted Demand": "1,450 units", "Planner Adjustment": "+50 units", "Final Approved Forecast": "1,500 units", "Status": "active"},
            {"Forecast Code": "FC-2026-Q3-M", "Product Line": "Metal Executive Desks", "Period": "Q3 2026", "Historical Base": "800 units", "AI Forecast Model": "ARIMA Linear Trend", "Predicted Demand": "920 units", "Planner Adjustment": "0 units", "Final Approved Forecast": "920 units", "Status": "active"},
            {"Forecast Code": "FC-2026-Q3-S", "Product Line": "Modular Storage Systems", "Period": "Q3 2026", "Historical Base": "2,100 units", "AI Forecast Model": "Moving Average", "Predicted Demand": "2,350 units", "Planner Adjustment": "+100 units", "Final Approved Forecast": "2,450 units", "Status": "pending"},
        ]
    },

    "pp_production_calendar": {
        "type": "list",
        "columns": ["Calendar Ref", "Plant Location", "Date", "Day of Week", "Shift Assignment", "Working Status", "Available Hours", "Planner Note", "Actions"],
        "rows": [
            {"Calendar Ref": "CAL-2026-0723", "Plant Location": "Riyadh Main", "Date": "2026-07-23", "Day of Week": "Thursday", "Shift Assignment": "Morning + Evening", "Working Status": "normal", "Available Hours": "16 hrs", "Planner Note": "Regular production run"},
            {"Calendar Ref": "CAL-2026-0724", "Plant Location": "Riyadh Main", "Date": "2026-07-24", "Day of Week": "Friday", "Shift Assignment": "Maintenance Shift Only", "Working Status": "inactive", "Available Hours": "0 hrs", "Planner Note": "Scheduled factory shutdown for PM"},
            {"Calendar Ref": "CAL-2026-0725", "Plant Location": "Riyadh Main", "Date": "2026-07-25", "Day of Week": "Saturday", "Shift Assignment": "Full 3 Shifts", "Working Status": "normal", "Available Hours": "24 hrs", "Planner Note": "Catch-up shift for WO-0412"},
        ]
    },

    "pp_resource_planning": {
        "type": "list",
        "columns": ["Resource ID", "Resource Name", "Type", "Primary Work Center", "Daily Max Capacity", "Allocated Plans", "Efficiency Rating", "Status", "Actions"],
        "rows": [
            {"Resource ID": "RES-CNC-001", "Resource Name": "5-Axis CNC Milling Machine", "Type": "Machine", "Primary Work Center": "CNC Machining", "Daily Max Capacity": "20 hrs/day", "Allocated Plans": "PP-2026-Q3-01", "Efficiency Rating": "96.5%", "Status": "active"},
            {"Resource ID": "RES-LBR-004", "Resource Name": "Senior CNC Technicians Team", "Type": "Labor", "Primary Work Center": "CNC Machining", "Daily Max Capacity": "40 man-hrs/day", "Allocated Plans": "PP-2026-Q3-01", "Efficiency Rating": "98.0%", "Status": "active"},
            {"Resource ID": "RES-ROB-002", "Resource Name": "KUKA Robotic Welding Arm", "Type": "Automation", "Primary Work Center": "Welding Bay", "Daily Max Capacity": "22 hrs/day", "Allocated Plans": "PP-2026-Q3-02", "Efficiency Rating": "99.2%", "Status": "active"},
        ]
    },

    "pp_shift_planning": {
        "type": "list",
        "columns": ["Shift Code", "Shift Name", "Start Time", "End Time", "Break Time", "Assigned Operators", "Target Output Rate", "Supervisor", "Actions"],
        "rows": [
            {"Shift Code": "SFT-M1", "Shift Name": "Morning Production Shift", "Start Time": "07:00 AM", "End Time": "03:30 PM", "Break Time": "60 mins", "Assigned Operators": "24 Operators", "Target Output Rate": "40 units/hr", "Supervisor": "Tariq Al-Harbi"},
            {"Shift Code": "SFT-E1", "Shift Name": "Evening Assembly Shift", "Start Time": "03:30 PM", "End Time": "12:00 AM", "Break Time": "60 mins", "Assigned Operators": "20 Operators", "Target Output Rate": "35 units/hr", "Supervisor": "Faisal Otaibi"},
            {"Shift Code": "SFT-N1", "Shift Name": "Night Overtime Shift", "Start Time": "12:00 AM", "End Time": "07:00 AM", "Break Time": "45 mins", "Assigned Operators": "10 Operators", "Target Output Rate": "20 units/hr", "Supervisor": "Khaled Zahrani"},
        ]
    },

    "pp_production_plan_approval": {
        "type": "approval",
        "columns": ["Plan Ref", "Plan Name", "Planning Period", "Est Cost (SAR)", "Capacity Check", "Material Availability", "Submitted By", "Status", "Actions"],
        "rows": [
            {"Plan Ref": "PP-2026-Q3-03", "Plan Name": "Upholstery & Fabric Production", "Planning Period": "Q3 2026", "Est Cost (SAR)": "450,000 SAR", "Capacity Check": "✔ 100% OK", "Material Availability": "✔ 95% OK", "Submitted By": "M. Farooq", "Status": "pending"},
            {"Plan Ref": "PP-2026-Q3-05", "Plan Name": "Special Heavy Machinery Parts", "Planning Period": "Aug - Sep 2026", "Est Cost (SAR)": "1,200,000 SAR", "Capacity Check": "⚠ Overload Risk", "Material Availability": "✖ Material Deficit", "Submitted By": "A. Al-Mansoor", "Status": "rejected"},
        ]
    },

    "pp_production_plan_reports": {
        "type": "reports",
        "columns": ["Report Code", "Report Title", "Category", "Period", "Generated On", "By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Code": "RPT-PP-001", "Report Title": "Master Production Schedule (MPS) Execution Report", "Category": "Production", "Period": "July 2026", "Generated On": "2026-07-22", "By": "Salim Rahal", "Format": "PDF", "Size": "1.4 MB"},
            {"Report Code": "RPT-PP-002", "Report Title": "MRP Material Shortage & Action Exception Log", "Category": "Material", "Period": "Q3 2026", "Generated On": "2026-07-21", "By": "Planner AI", "Format": "XLSX", "Size": "850 KB"},
            {"Report Code": "RPT-PP-003", "Report Title": "Work Center Capacity Load & Bottleneck Analysis", "Category": "Capacity", "Period": "Q3 2026", "Generated On": "2026-07-20", "By": "Admin", "Format": "PDF", "Size": "2.1 MB"},
        ]
    },

    # ═══════════════════════════════════════
    # WORK ORDERS
    # ═══════════════════════════════════════
    "wo_work_order_dashboard": {"type": "wo_dashboard"},

    "wo_work_order_list": {
        "type": "list",
        "columns": ["WO Number", "Finished Good", "BOM Ref", "Qty Ordered", "Qty Completed", "Work Center", "Start Date", "Due Date", "Priority", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0412", "Finished Good": "Wooden Chair", "BOM Ref": "BOM-001", "Qty Ordered": "200", "Qty Completed": "142", "Work Center": "Assembly Line 1", "Start Date": "2026-07-18", "Due Date": "2026-07-25", "Priority": "High", "Status": "in_progress"},
            {"WO Number": "WO-2026-0411", "Finished Good": "Metal Desk Frame", "BOM Ref": "BOM-002", "Qty Ordered": "80", "Qty Completed": "80", "Work Center": "CNC Machining", "Start Date": "2026-07-15", "Due Date": "2026-07-22", "Priority": "Medium", "Status": "completed"},
            {"WO Number": "WO-2026-0410", "Finished Good": "Leather Sofa Cover", "BOM Ref": "BOM-003", "Qty Ordered": "60", "Qty Completed": "0", "Work Center": "Upholstery Stn", "Start Date": "2026-07-20", "Due Date": "2026-07-30", "Priority": "Low", "Status": "draft"},
            {"WO Number": "WO-2026-0409", "Finished Good": "Cabinet Hardware Kit", "BOM Ref": "BOM-004", "Qty Ordered": "500", "Qty Completed": "500", "Work Center": "Assembly Line 2", "Start Date": "2026-07-10", "Due Date": "2026-07-18", "Priority": "High", "Status": "completed"},
            {"WO Number": "WO-2026-0408", "Finished Good": "Steel Shelf Unit", "BOM Ref": "BOM-006", "Qty Ordered": "150", "Qty Completed": "0", "Work Center": "Welding Bay", "Start Date": "2026-07-22", "Due Date": "2026-07-28", "Priority": "High", "Status": "released"},
        ]
    },

    "wo_create_work_order": {"type": "wo_form", "mode": "create"},
    "wo_edit_work_order":   {"type": "wo_form", "mode": "edit"},

    "wo_work_order_details": {"type": "wo_detail"},

    "wo_release_work_order": {
        "type": "approval",
        "columns": ["WO Number", "Finished Good", "Qty Ordered", "Planned Start", "Work Center", "BOM Verified", "Material Available", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0413", "Finished Good": "Powder Coated Frame", "Qty Ordered": "300", "Planned Start": "2026-07-23", "Work Center": "Painting Booth", "BOM Verified": "✔ Yes", "Material Available": "✔ Yes", "Status": "pending"},
            {"WO Number": "WO-2026-0414", "Finished Good": "Steel Shelf Unit", "Qty Ordered": "150", "Planned Start": "2026-07-22", "Work Center": "Welding Bay", "BOM Verified": "✔ Yes", "Material Available": "⚠ Partial", "Status": "pending"},
            {"WO Number": "WO-2026-0415", "Finished Good": "Oak Wood Panel", "Qty Ordered": "240", "Planned Start": "2026-07-24", "Work Center": "CNC Machining", "BOM Verified": "✖ No", "Material Available": "✖ No", "Status": "rejected"},
        ]
    },

    "wo_work_order_tracking": {
        "type": "list",
        "columns": ["WO Number", "Operation", "Work Center", "Operator", "Start Time", "End Time", "Qty Confirmed", "Progress", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0412", "Operation": "Cutting", "Work Center": "CNC Machining", "Operator": "Ahmed K.", "Start Time": "07:00 AM", "End Time": "09:30 AM", "Qty Confirmed": "200", "Progress": "100%", "Status": "completed"},
            {"WO Number": "WO-2026-0412", "Operation": "Assembly", "Work Center": "Assembly Line 1", "Operator": "Khalid M.", "Start Time": "10:00 AM", "End Time": "—", "Qty Confirmed": "142", "Progress": "71%", "Status": "in_progress"},
            {"WO Number": "WO-2026-0412", "Operation": "Painting", "Work Center": "Painting Booth", "Operator": "—", "Start Time": "—", "End Time": "—", "Qty Confirmed": "0", "Progress": "0%", "Status": "draft"},
            {"WO Number": "WO-2026-0408", "Operation": "Welding", "Work Center": "Welding Bay", "Operator": "Sara M.", "Start Time": "08:00 AM", "End Time": "—", "Qty Confirmed": "45", "Progress": "30%", "Status": "in_progress"},
        ]
    },

    "wo_work_order_closure": {
        "type": "list",
        "columns": ["WO Number", "Finished Good", "Qty Ordered", "Qty Produced", "Qty Rejected", "Variance", "Completed On", "Closed By", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0411", "Finished Good": "Metal Desk Frame", "Qty Ordered": "80", "Qty Produced": "80", "Qty Rejected": "2", "Variance": "−2.5%", "Completed On": "2026-07-22", "Closed By": "—", "Status": "pending"},
            {"WO Number": "WO-2026-0409", "Finished Good": "Cabinet Hardware Kit", "Qty Ordered": "500", "Qty Produced": "498", "Qty Rejected": "4", "Variance": "−0.4%", "Completed On": "2026-07-18", "Closed By": "Admin", "Status": "completed"},
        ]
    },

    "wo_work_order_history": {
        "type": "list",
        "columns": ["WO Number", "Finished Good", "Qty Ordered", "Qty Produced", "Start Date", "End Date", "Duration (Days)", "Work Center", "Closed By", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0409", "Finished Good": "Cabinet Hardware Kit", "Qty Ordered": "500", "Qty Produced": "498", "Start Date": "2026-07-10", "End Date": "2026-07-18", "Duration (Days)": "8", "Work Center": "Assembly Line 2", "Closed By": "Admin", "Status": "completed"},
            {"WO Number": "WO-2026-0405", "Finished Good": "Plywood Sheet Set", "Qty Ordered": "1000", "Qty Produced": "995", "Start Date": "2026-07-01", "End Date": "2026-07-09", "Duration (Days)": "9", "Work Center": "CNC Machining", "Closed By": "Admin", "Status": "completed"},
            {"WO Number": "WO-2026-0401", "Finished Good": "Foam Cushion Pack", "Qty Ordered": "200", "Qty Produced": "200", "Start Date": "2026-06-20", "End Date": "2026-06-28", "Duration (Days)": "8", "Work Center": "Upholstery Stn", "Closed By": "Admin", "Status": "completed"},
        ]
    },

    "wo_work_order_reports": {
        "type": "reports",
        "columns": ["Report Name", "Report Type", "WO Range", "Generated On", "Generated By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "WO Completion Summary", "Report Type": "Summary", "WO Range": "WO-2026-0400 to 0412", "Generated On": "2026-07-22", "Generated By": "System", "Format": "XLSX", "Size": "185 KB"},
            {"Report Name": "Variance & Rejection Report", "Report Type": "Exception", "WO Range": "Jul 2026", "Generated On": "2026-07-22", "Generated By": "Admin", "Format": "PDF", "Size": "102 KB"},
            {"Report Name": "WO Aging Report", "Report Type": "Analytics", "WO Range": "Q2-Q3 2026", "Generated On": "2026-07-20", "Generated By": "System", "Format": "XLSX", "Size": "298 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # SHOP FLOOR EXECUTION
    # ═══════════════════════════════════════
    "sfe_shop_floor_dashboard":   {"type": "sfe_dashboard"},
    "sfe_production_monitoring":  {"type": "sfe_monitoring"},
    "sfe_operator_dashboard":     {"type": "sfe_operator"},
    "sfe_machine_status":         {"type": "sfe_machines"},
    "sfe_job_assignment":         {"type": "sfe_job_assign_form"},
    "sfe_production_entry":       {"type": "sfe_production_form"},
    "sfe_downtime_recording":     {"type": "sfe_downtime_form"},
    "sfe_labor_time_entry":       {"type": "sfe_labor_form"},

    "sfe_shift_monitoring": {
        "type": "list",
        "columns": ["Shift", "Date", "Supervisor", "Headcount Planned", "Headcount Present", "Output Target", "Output Achieved", "Efficiency %", "Downtime Events", "Status", "Actions"],
        "rows": [
            {"Shift": "Morning (06–14)", "Date": "2026-07-22", "Supervisor": "Ahmed Al-Rashid", "Headcount Planned": "24", "Headcount Present": "22", "Output Target": "480 Pcs", "Output Achieved": "412 Pcs", "Efficiency %": "85.8%", "Downtime Events": "2", "Status": "in_progress"},
            {"Shift": "Evening (14–22)", "Date": "2026-07-22", "Supervisor": "Sara Mohammed", "Headcount Planned": "18", "Headcount Present": "18", "Output Target": "360 Pcs", "Output Achieved": "0 Pcs", "Efficiency %": "—", "Downtime Events": "0", "Status": "draft"},
            {"Shift": "Morning (06–14)", "Date": "2026-07-21", "Supervisor": "Ahmed Al-Rashid", "Headcount Planned": "24", "Headcount Present": "24", "Output Target": "480 Pcs", "Output Achieved": "475 Pcs", "Efficiency %": "99.0%", "Downtime Events": "1", "Status": "completed"},
            {"Shift": "Evening (14–22)", "Date": "2026-07-21", "Supervisor": "Khalid Nasser", "Headcount Planned": "18", "Headcount Present": "16", "Output Target": "360 Pcs", "Output Achieved": "322 Pcs", "Efficiency %": "89.4%", "Downtime Events": "3", "Status": "completed"},
        ]
    },

    "sfe_wip_tracking": {
        "type": "list",
        "columns": ["WO Number", "Item", "Operation (From)", "Operation (To)", "WIP Location", "WIP Qty", "Waiting Since", "Age (Hrs)", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0412", "Item": "Wooden Chair", "Operation (From)": "Cutting", "Operation (To)": "Assembly", "WIP Location": "Staging Area A", "WIP Qty": "200 Pcs", "Waiting Since": "09:30 AM", "Age (Hrs)": "2.5", "Status": "active"},
            {"WO Number": "WO-2026-0408", "Item": "Steel Shelf", "Operation (From)": "Welding", "Operation (To)": "Painting", "WIP Location": "Staging Area B", "WIP Qty": "45 Pcs", "Waiting Since": "11:00 AM", "Age (Hrs)": "1.0", "Status": "active"},
            {"WO Number": "WO-2026-0411", "Item": "Metal Desk Frame", "Operation (From)": "Painting", "Operation (To)": "QC Inspection", "WIP Location": "QC Queue", "WIP Qty": "80 Pcs", "Waiting Since": "08:00 AM", "Age (Hrs)": "4.0", "Status": "overloaded"},
            {"WO Number": "WO-2026-0405", "Item": "Plywood Sheet", "Operation (From)": "CNC Cut", "Operation (To)": "Sanding", "WIP Location": "Staging Area C", "WIP Qty": "150 Pcs", "Waiting Since": "07:00 AM", "Age (Hrs)": "5.5", "Status": "overloaded"},
        ]
    },

    "sfe_production_completion": {
        "type": "list",
        "columns": ["WO Number", "Operation", "Work Center", "Planned Qty", "Produced Qty", "Scrap Qty", "Operator", "Completed On", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0412", "Operation": "Cutting", "Work Center": "CNC Machining", "Planned Qty": "200", "Produced Qty": "200", "Scrap Qty": "0", "Operator": "Ahmed K.", "Completed On": "2026-07-22 09:30", "Status": "completed"},
            {"WO Number": "WO-2026-0411", "Operation": "Painting", "Work Center": "Painting Booth", "Planned Qty": "80", "Produced Qty": "78", "Scrap Qty": "2", "Operator": "Khalid M.", "Completed On": "2026-07-22 11:00", "Status": "completed"},
            {"WO Number": "WO-2026-0408", "Operation": "Welding", "Work Center": "Welding Bay", "Planned Qty": "150", "Produced Qty": "45", "Scrap Qty": "0", "Operator": "Sara M.", "Completed On": "—", "Status": "in_progress"},
        ]
    },

    "sfe_shop_floor_reports": {
        "type": "reports",
        "columns": ["Report Name", "Report Type", "Period", "Generated On", "Generated By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "Daily Production Summary", "Report Type": "Summary", "Period": "2026-07-22", "Generated On": "2026-07-22", "Generated By": "System", "Format": "XLSX", "Size": "128 KB"},
            {"Report Name": "Operator Efficiency Report", "Report Type": "Analytics", "Period": "Jul Wk 3", "Generated On": "2026-07-22", "Generated By": "Admin", "Format": "PDF", "Size": "88 KB"},
            {"Report Name": "Downtime Analysis", "Report Type": "Exception", "Period": "Jul 2026", "Generated On": "2026-07-21", "Generated By": "System", "Format": "XLSX", "Size": "210 KB"},
            {"Report Name": "OEE Report by Work Center", "Report Type": "Analytics", "Period": "Q3 2026", "Generated On": "2026-07-20", "Generated By": "Admin", "Format": "PDF", "Size": "315 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # MATERIAL MANAGEMENT
    # ═══════════════════════════════════════
    "mm_material_dashboard":    {"type": "mm_dashboard"},
    "mm_stock_availability":    {"type": "mm_stock_view"},
    "mm_material_request":      {"type": "mm_mr_form"},
    "mm_material_issue":        {"type": "mm_mi_form"},
    "mm_material_receipt":      {"type": "mm_grn_form"},
    "mm_material_transfer":     {"type": "mm_mt_form"},
    "mm_inventory_adjustment":  {"type": "mm_adj_form"},
    "mm_cycle_count":           {"type": "mm_cc_form"},
    "mm_physical_inventory":    {"type": "mm_pi_form"},

    "mm_item_master": {
        "type": "list",
        "columns": ["Item Code", "Item Name", "Item Group", "UoM", "Valuation", "Reorder Lvl", "Safety Stock", "Current Stock", "Status", "Actions"],
        "rows": [
            {"Item Code": "RM-WD-003",  "Item Name": "Teak Wood Board",      "Item Group": "Raw Material", "UoM": "Pcs",  "Valuation": "FIFO",  "Reorder Lvl": "50",  "Safety Stock": "20",  "Current Stock": "12",  "Status": "active"},
            {"Item Code": "RM-STL-001", "Item Name": "Steel Sheet 2mm",       "Item Group": "Raw Material", "UoM": "Kg",   "Valuation": "Avg",   "Reorder Lvl": "200", "Safety Stock": "80",  "Current Stock": "145", "Status": "active"},
            {"Item Code": "RM-LTH-007", "Item Name": "Leather Hide Grade A",  "Item Group": "Raw Material", "UoM": "m²",   "Valuation": "FIFO",  "Reorder Lvl": "30",  "Safety Stock": "10",  "Current Stock": "8",   "Status": "active"},
            {"Item Code": "FG-CH-001",  "Item Name": "Wooden Chair (Finished)","Item Group": "Finished Good","UoM": "Pcs",  "Valuation": "Std",   "Reorder Lvl": "100", "Safety Stock": "30",  "Current Stock": "0",   "Status": "active"},
            {"Item Code": "RM-PNT-002", "Item Name": "Primer Coat Paint",     "Item Group": "Consumable",   "UoM": "Ltr",  "Valuation": "Avg",   "Reorder Lvl": "20",  "Safety Stock": "5",   "Current Stock": "2",   "Status": "active"},
            {"Item Code": "RM-SCR-010", "Item Name": "Hex Screw M8",          "Item Group": "Spare Parts",  "UoM": "Pcs",  "Valuation": "Avg",   "Reorder Lvl": "1000","Safety Stock": "500", "Current Stock": "320", "Status": "inactive"},
        ]
    },

    "mm_warehouse_master": {
        "type": "list",
        "columns": ["Warehouse Code", "Warehouse Name", "Type", "Location", "Total Capacity", "Manager", "Status", "Actions"],
        "rows": [
            {"Warehouse Code": "WH-01", "Warehouse Name": "Main Raw Material Store",   "Type": "Raw Material",  "Location": "Plant 1 — Block A", "Total Capacity": "5000 m²", "Manager": "Ahmed K.",  "Status": "active"},
            {"Warehouse Code": "WH-02", "Warehouse Name": "Finished Goods Warehouse",  "Type": "Finished Good", "Location": "Plant 1 — Block B", "Total Capacity": "3000 m²", "Manager": "Sara M.",   "Status": "active"},
            {"Warehouse Code": "WH-03", "Warehouse Name": "WIP Staging Area",          "Type": "WIP",           "Location": "Plant 1 — Shop Floor","Total Capacity": "800 m²","Manager": "Khalid M.", "Status": "active"},
            {"Warehouse Code": "WH-04", "Warehouse Name": "Spare Parts Store",         "Type": "Spare Parts",   "Location": "Maintenance Bldg",  "Total Capacity": "500 m²",  "Manager": "Rami H.",   "Status": "active"},
            {"Warehouse Code": "WH-05", "Warehouse Name": "Consumables Store",         "Type": "Consumable",    "Location": "Plant 1 — Block A", "Total Capacity": "200 m²",  "Manager": "Ahmed K.",  "Status": "inactive"},
        ]
    },

    "mm_bin_location_master": {
        "type": "list",
        "columns": ["Bin Code", "Warehouse", "Rack", "Row", "Level", "Max Capacity", "Current Usage", "Status", "Actions"],
        "rows": [
            {"Bin Code": "WH01-R01-A1", "Warehouse": "WH-01 Raw Material", "Rack": "R01", "Row": "A", "Level": "1", "Max Capacity": "500 kg", "Current Usage": "72%", "Status": "active"},
            {"Bin Code": "WH01-R01-A2", "Warehouse": "WH-01 Raw Material", "Rack": "R01", "Row": "A", "Level": "2", "Max Capacity": "500 kg", "Current Usage": "45%", "Status": "active"},
            {"Bin Code": "WH01-R02-B1", "Warehouse": "WH-01 Raw Material", "Rack": "R02", "Row": "B", "Level": "1", "Max Capacity": "800 kg", "Current Usage": "90%", "Status": "active"},
            {"Bin Code": "WH02-R01-A1", "Warehouse": "WH-02 Finished Goods","Rack": "R01", "Row": "A", "Level": "1", "Max Capacity": "200 Pcs","Current Usage": "0%",  "Status": "active"},
            {"Bin Code": "WH04-S01-A1", "Warehouse": "WH-04 Spare Parts",   "Rack": "S01", "Row": "A", "Level": "1", "Max Capacity": "1000 Pcs","Current Usage":"32%", "Status": "active"},
        ]
    },

    "mm_batch_management": {
        "type": "list",
        "columns": ["Batch No", "Item Code", "Item Name", "Warehouse", "Qty on Hand", "Mfg Date", "Expiry Date", "Age (Days)", "Status", "Actions"],
        "rows": [
            {"Batch No": "BTH-2026-0041", "Item Code": "RM-LTH-007", "Item Name": "Leather Hide Grade A",  "Warehouse": "WH-01", "Qty on Hand": "8 m²",   "Mfg Date": "2026-06-01", "Expiry Date": "2028-06-01", "Age (Days)": "51",  "Status": "active"},
            {"Batch No": "BTH-2026-0038", "Item Code": "RM-PNT-002", "Item Name": "Primer Coat Paint",     "Warehouse": "WH-01", "Qty on Hand": "2 Ltr",  "Mfg Date": "2026-05-15", "Expiry Date": "2026-11-15", "Age (Days)": "68",  "Status": "active"},
            {"Batch No": "BTH-2026-0035", "Item Code": "RM-WD-003",  "Item Name": "Teak Wood Board",       "Warehouse": "WH-01", "Qty on Hand": "12 Pcs", "Mfg Date": "2026-04-10", "Expiry Date": "—",          "Age (Days)": "103", "Status": "active"},
            {"Batch No": "BTH-2026-0020", "Item Code": "RM-PNT-002", "Item Name": "Primer Coat Paint",     "Warehouse": "WH-01", "Qty on Hand": "0 Ltr",  "Mfg Date": "2025-12-01", "Expiry Date": "2026-06-01", "Age (Days)": "233", "Status": "inactive"},
        ]
    },

    "mm_serial_number_tracking": {
        "type": "list",
        "columns": ["Serial No", "Item Code", "Item Name", "Warehouse / Location", "WO Reference", "GRN Reference", "Received On", "Status", "Actions"],
        "rows": [
            {"Serial No": "SN-FG-0001", "Item Code": "FG-CH-001", "Item Name": "Wooden Chair",     "Warehouse / Location": "WH-02 FG",    "WO Reference": "WO-2026-0409", "GRN Reference": "—",          "Received On": "2026-07-18", "Status": "active"},
            {"Serial No": "SN-FG-0002", "Item Code": "FG-CH-001", "Item Name": "Wooden Chair",     "Warehouse / Location": "WH-02 FG",    "WO Reference": "WO-2026-0409", "GRN Reference": "—",          "Received On": "2026-07-18", "Status": "active"},
            {"Serial No": "SN-EQ-1045", "Item Code": "EQ-CNC-002", "Item Name": "CNC Spindle Unit","Warehouse / Location": "WH-04 Spare", "WO Reference": "—",            "GRN Reference": "GRN-2026-042","Received On": "2026-06-20","Status": "active"},
            {"Serial No": "SN-EQ-1044", "Item Code": "EQ-CNC-002", "Item Name": "CNC Spindle Unit","Warehouse / Location": "In Use — CNC1","WO Reference": "—",           "GRN Reference": "GRN-2026-042","Received On": "2026-06-20","Status": "in_progress"},
        ]
    },

    "mm_inventory_reports": {
        "type": "reports",
        "columns": ["Report Name", "Category", "Period", "Generated On", "By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "Stock Valuation Report",       "Category": "Valuation",   "Period": "Jul 2026",    "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "420 KB"},
            {"Report Name": "Slow-Moving Inventory",        "Category": "Analytics",   "Period": "Q2 2026",     "Generated On": "2026-07-21", "By": "Admin",  "Format": "PDF",  "Size": "188 KB"},
            {"Report Name": "Stock Aging Report",           "Category": "Analytics",   "Period": "Jul 2026",    "Generated On": "2026-07-20", "By": "System", "Format": "XLSX", "Size": "310 KB"},
            {"Report Name": "GRN Summary",                  "Category": "Transaction", "Period": "Jul Wk 3",   "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "95 KB"},
            {"Report Name": "Material Issue vs WO Report",  "Category": "Transaction", "Period": "Jul 2026",    "Generated On": "2026-07-21", "By": "Admin",  "Format": "PDF",  "Size": "142 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # QUALITY MANAGEMENT
    # ═══════════════════════════════════════
    "qm_quality_dashboard":             {"type": "qm_dashboard"},
    "qm_incoming_quality_inspection":   {"type": "qm_iqc_form"},
    "qm_in_process_inspection":          {"type": "qm_ipqc_form"},
    "qm_final_inspection":              {"type": "qm_oqc_form"},
    "qm_non_conformance_report_ncr":    {"type": "qm_ncr_form"},
    "qm_capa":                          {"type": "qm_capa_form"},

    "qm_inspection_lot": {
        "type": "list",
        "columns": ["Lot No", "Item Code", "Item Name", "Inspection Type", "Lot Qty", "Sample Size", "Reference Doc", "Inspector", "Created Date", "Status", "Actions"],
        "rows": [
            {"Lot No": "IL-2026-055", "Item Code": "RM-WD-003",  "Item Name": "Teak Wood Board",    "Inspection Type": "Incoming (IQC)", "Lot Qty": "98 Pcs",  "Sample Size": "13 Pcs", "Reference Doc": "GRN-2026-055", "Inspector": "Ahmed K.",  "Created Date": "2026-07-22", "Status": "in_progress"},
            {"Lot No": "IL-2026-054", "Item Code": "FG-CH-001",  "Item Name": "Wooden Chair",        "Inspection Type": "In-Process (IPQC)", "Lot Qty": "200 Pcs", "Sample Size": "20 Pcs", "Reference Doc": "WO-2026-0412",  "Inspector": "Sara M.",   "Created Date": "2026-07-22", "Status": "in_progress"},
            {"Lot No": "IL-2026-053", "Item Code": "FG-CH-001",  "Item Name": "Wooden Chair",        "Inspection Type": "Final (OQC)",    "Lot Qty": "100 Pcs", "Sample Size": "20 Pcs", "Reference Doc": "WO-2026-0409",  "Inspector": "Ahmed K.",  "Created Date": "2026-07-21", "Status": "approved"},
            {"Lot No": "IL-2026-052", "Item Code": "RM-STL-001", "Item Name": "Steel Sheet 2mm",     "Inspection Type": "Incoming (IQC)", "Lot Qty": "200 Kg",  "Sample Size": "20 Kg",  "Reference Doc": "GRN-2026-052", "Inspector": "Khalid M.", "Created Date": "2026-07-20", "Status": "rejected"},
        ]
    },

    "qm_defect_recording": {
        "type": "list",
        "columns": ["Defect ID", "Work Order / Lot", "Item Code", "Defect Category", "Defect Description", "Severity", "Defect Qty", "Reported By", "Date", "Status", "Actions"],
        "rows": [
            {"Defect ID": "DEF-2026-031", "Work Order / Lot": "WO-2026-0412", "Item Code": "FG-CH-001",  "Defect Category": "Process Defect", "Defect Description": "Adhesive Joint Weakness", "Severity": "Major",    "Defect Qty": "3 Pcs", "Reported By": "Sara M.",  "Date": "2026-07-22", "Status": "active"},
            {"Defect ID": "DEF-2026-030", "Work Order / Lot": "IL-2026-055",   "Item Code": "RM-WD-003",  "Defect Category": "Material Defect","Defect Description": "Grain Direction Deviation","Severity": "Minor",    "Defect Qty": "1 Pc",  "Reported By": "Ahmed K.", "Date": "2026-07-22", "Status": "active"},
            {"Defect ID": "DEF-2026-029", "Work Order / Lot": "GRN-2026-052",  "Item Code": "RM-STL-001", "Defect Category": "Dimensional",    "Defect Description": "Thickness 1.7mm vs 2mm Spec","Severity":"Critical", "Defect Qty": "5 Kg",  "Reported By": "Khalid M.","Date": "2026-07-20", "Status": "completed"},
        ]
    },

    "qm_quality_certificates": {
        "type": "list",
        "columns": ["Certificate No", "Item Code", "Item Name", "Batch / Lot No", "Customer", "Inspection Ref", "Issue Date", "Issued By", "Status", "Actions"],
        "rows": [
            {"Certificate No": "COA-2026-088", "Item Code": "FG-CH-001", "Item Name": "Wooden Chair", "Batch / Lot No": "WO-2026-0409-FG", "Customer": "Al-Madar Furniture", "Inspection Ref": "OQC-2026-031", "Issue Date": "2026-07-22", "Issued By": "Ahmed K.", "Status": "approved"},
            {"Certificate No": "COA-2026-087", "Item Code": "FG-CH-001", "Item Name": "Wooden Chair", "Batch / Lot No": "WO-2026-0405-FG", "Customer": "Riyadh Trade Co.",   "Inspection Ref": "OQC-2026-029", "Issue Date": "2026-07-18", "Issued By": "Sara M.",  "Status": "approved"},
        ]
    },

    "qm_inspection_plan": {
        "type": "list",
        "columns": ["Plan Code", "Item Code", "Item Name", "Inspection Type", "Frequency", "Sampling Method", "Parameters Count", "Responsible", "Status", "Actions"],
        "rows": [
            {"Plan Code": "QP-001", "Item Code": "RM-WD-003",  "Item Name": "Teak Wood Board",       "Inspection Type": "Incoming",    "Frequency": "Every GRN", "Sampling Method": "AQL 2.5",  "Parameters Count": "5",  "Responsible": "QC Team A", "Status": "active"},
            {"Plan Code": "QP-002", "Item Code": "RM-STL-001", "Item Name": "Steel Sheet 2mm",        "Inspection Type": "Incoming",    "Frequency": "Every GRN", "Sampling Method": "100%",     "Parameters Count": "8",  "Responsible": "QC Team B", "Status": "active"},
            {"Plan Code": "QP-003", "Item Code": "FG-CH-001",  "Item Name": "Wooden Chair",           "Inspection Type": "In-Process",  "Frequency": "Per Batch", "Sampling Method": "AQL 1.0",  "Parameters Count": "12", "Responsible": "QC Team A", "Status": "active"},
            {"Plan Code": "QP-004", "Item Code": "FG-CH-001",  "Item Name": "Wooden Chair",           "Inspection Type": "Outgoing",    "Frequency": "Per WO",    "Sampling Method": "AQL 0.65", "Parameters Count": "15", "Responsible": "QC Team B", "Status": "active"},
            {"Plan Code": "QP-005", "Item Code": "RM-PNT-002", "Item Name": "Primer Coat Paint",      "Inspection Type": "Incoming",    "Frequency": "Random",    "Sampling Method": "AQL 4.0",  "Parameters Count": "3",  "Responsible": "QC Team A", "Status": "active"},
        ]
    },

    "qm_quality_hold": {
        "type": "list",
        "columns": ["Hold No", "Item Code", "Item Name", "Batch / Lot", "Warehouse", "Hold Qty", "Reason", "Raised By", "Hold Since", "Status", "Actions"],
        "rows": [
            {"Hold No": "QH-2026-012", "Item Code": "RM-STL-001", "Item Name": "Steel Sheet 2mm",   "Batch / Lot": "BTH-2026-0044", "Warehouse": "WH-01", "Hold Qty": "5 Kg",   "Reason": "Thickness Variance",   "Raised By": "Ahmed K.", "Hold Since": "2026-07-21", "Status": "active"},
            {"Hold No": "QH-2026-011", "Item Code": "RM-LTH-007", "Item Name": "Leather Hide",      "Batch / Lot": "BTH-2026-0041", "Warehouse": "WH-01", "Hold Qty": "1 m²",   "Reason": "Surface Defect",       "Raised By": "Sara M.",  "Hold Since": "2026-07-20", "Status": "active"},
            {"Hold No": "QH-2026-010", "Item Code": "FG-CH-001",  "Item Name": "Wooden Chair",      "Batch / Lot": "WO-2026-0409",  "Warehouse": "WH-02", "Hold Qty": "3 Pcs",  "Reason": "Finish Defect",        "Raised By": "Ahmed K.", "Hold Since": "2026-07-19", "Status": "completed"},
            {"Hold No": "QH-2026-009", "Item Code": "RM-PNT-002", "Item Name": "Primer Coat Paint", "Batch / Lot": "BTH-2026-0038", "Warehouse": "WH-01", "Hold Qty": "2 Ltr",  "Reason": "Viscosity Out of Spec","Raised By": "Sara M.",  "Hold Since": "2026-07-15", "Status": "rejected"},
        ]
    },

    "qm_supplier_quality_management": {
        "type": "list",
        "columns": ["Supplier Code", "Supplier Name", "Items Inspected", "Lots Accepted", "Lots Rejected", "Rejection Rate", "Avg Quality Score", "Last Audit", "Rating", "Status", "Actions"],
        "rows": [
            {"Supplier Code": "SUP-001", "Supplier Name": "Al-Rashid Timber Co.",  "Items Inspected": "12", "Lots Accepted": "11", "Lots Rejected": "1", "Rejection Rate": "8.3%",  "Avg Quality Score": "88/100", "Last Audit": "2026-05-15", "Rating": "B+", "Status": "active"},
            {"Supplier Code": "SUP-002", "Supplier Name": "Gulf Steel Trading",     "Items Inspected": "18", "Lots Accepted": "16", "Lots Rejected": "2", "Rejection Rate": "11.1%", "Avg Quality Score": "82/100", "Last Audit": "2026-04-10", "Rating": "B",  "Status": "active"},
            {"Supplier Code": "SUP-003", "Supplier Name": "Delta Paints LLC",       "Items Inspected": "6",  "Lots Accepted": "6",  "Lots Rejected": "0", "Rejection Rate": "0%",    "Avg Quality Score": "95/100", "Last Audit": "2026-06-01", "Rating": "A",  "Status": "active"},
            {"Supplier Code": "SUP-004", "Supplier Name": "Premium Leather Ltd",    "Items Inspected": "8",  "Lots Accepted": "7",  "Lots Rejected": "1", "Rejection Rate": "12.5%", "Avg Quality Score": "79/100", "Last Audit": "2026-03-20", "Rating": "C+", "Status": "active"},
        ]
    },

    "qm_quality_audit": {
        "type": "list",
        "columns": ["Audit No", "Audit Type", "Area / Dept", "Auditor", "Scheduled Date", "Completed Date", "Findings", "Critical", "Score", "Status", "Actions"],
        "rows": [
            {"Audit No": "QA-2026-005", "Audit Type": "Internal",  "Area / Dept": "Production Floor",      "Auditor": "Ahmed K.",  "Scheduled Date": "2026-07-20", "Completed Date": "2026-07-21", "Findings": "4", "Critical": "1", "Score": "84%", "Status": "completed"},
            {"Audit No": "QA-2026-004", "Audit Type": "Supplier",  "Area / Dept": "Al-Rashid Timber",      "Auditor": "Sara M.",   "Scheduled Date": "2026-07-15", "Completed Date": "2026-07-15", "Findings": "2", "Critical": "0", "Score": "91%", "Status": "completed"},
            {"Audit No": "QA-2026-006", "Audit Type": "Internal",  "Area / Dept": "Warehouse WH-01",       "Auditor": "Khalid M.", "Scheduled Date": "2026-08-01", "Completed Date": "—",          "Findings": "—", "Critical": "—", "Score": "—",   "Status": "draft"},
            {"Audit No": "QA-2026-007", "Audit Type": "Regulatory","Area / Dept": "Full Plant ISO 9001",   "Auditor": "External",  "Scheduled Date": "2026-09-10", "Completed Date": "—",          "Findings": "—", "Critical": "—", "Score": "—",   "Status": "draft"},
        ]
    },

    "qm_quality_reports": {
        "type": "reports",
        "columns": ["Report Name", "Category", "Period", "Generated On", "By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "Inspection Summary Report",      "Category": "Inspection",   "Period": "Jul 2026",   "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "210 KB"},
            {"Report Name": "NCR Trend Analysis",            "Category": "NCR/CAPA",     "Period": "Q2-Q3 2026", "Generated On": "2026-07-21", "By": "Admin",  "Format": "PDF",  "Size": "155 KB"},
            {"Report Name": "Supplier Quality Scorecard",    "Category": "Supplier",     "Period": "H1 2026",    "Generated On": "2026-07-20", "By": "System", "Format": "XLSX", "Size": "98 KB"},
            {"Report Name": "First Pass Yield (FPY) Report", "Category": "Production",   "Period": "Jul 2026",   "Generated On": "2026-07-22", "By": "System", "Format": "PDF",  "Size": "88 KB"},
            {"Report Name": "CAPA Closure Report",           "Category": "NCR/CAPA",     "Period": "Q3 2026",    "Generated On": "2026-07-18", "By": "Admin",  "Format": "PDF",  "Size": "72 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # MAINTENANCE MANAGEMENT
    # ═══════════════════════════════════════
    "mnt_maintenance_dashboard":    {"type": "mnt_dashboard"},

    "mnt_breakdown_maintenance": {
        "type": "list",
        "columns": ["Breakdown ID", "Equipment", "Asset Tag", "Failure Description", "Reported By", "Reported Time", "Downtime (Hrs)", "Assigned Tech", "Status", "Actions"],
        "rows": [
            {"Breakdown ID": "BD-2026-018", "Equipment": "Painting Booth", "Asset Tag": "AST-PNT-001", "Failure Description": "Nozzle Blockage & Pressure Drop", "Reported By": "Ahmed K.",  "Reported Time": "2026-07-22 10:15", "Downtime (Hrs)": "2.2h", "Assigned Tech": "Rami Hassan", "Status": "in_progress"},
            {"Breakdown ID": "BD-2026-017", "Equipment": "Assembly Line 1","Asset Tag": "AST-ASM-001", "Failure Description": "Conveyor Belt Tension Release",  "Reported By": "Ahmed K.",  "Reported Time": "2026-07-19 14:00", "Downtime (Hrs)": "2.5h", "Assigned Tech": "Rami Hassan", "Status": "completed"},
            {"Breakdown ID": "BD-2026-016", "Equipment": "CNC Mach #2",    "Asset Tag": "AST-CNC-002", "Failure Description": "Coolant Pump Pressure Loss",     "Reported By": "Khalid M.", "Reported Time": "2026-07-10 09:30", "Downtime (Hrs)": "1.2h", "Assigned Tech": "Khalid M.",   "Status": "completed"},
        ]
    },

    "mnt_asset_master": {
        "type": "list",
        "columns": ["Asset Tag", "Asset Name", "Category", "Location", "Purchase Date", "Cost (SAR)", "Warranty Exp", "Criticality", "Status", "Actions"],
        "rows": [
            {"Asset Tag": "AST-CNC-001", "Asset Name": "CNC Machining Center #1", "Category": "Production Machinery", "Location": "Plant 1 — Shop Floor", "Purchase Date": "2022-03-15", "Cost (SAR)": "450,000", "Warranty Exp": "2025-03-15", "Criticality": "High",   "Status": "active"},
            {"Asset Tag": "AST-CNC-002", "Asset Name": "CNC Machining Center #2", "Category": "Production Machinery", "Location": "Plant 1 — Shop Floor", "Purchase Date": "2023-01-10", "Cost (SAR)": "480,000", "Warranty Exp": "2026-01-10", "Criticality": "High",   "Status": "active"},
            {"Asset Tag": "AST-PNT-001", "Asset Name": "Automated Spray Paint Booth","Category": "Finishing Equipment",   "Location": "Plant 1 — Block B",   "Purchase Date": "2021-08-20", "Cost (SAR)": "220,000", "Warranty Exp": "2024-08-20", "Criticality": "Medium", "Status": "active"},
            {"Asset Tag": "AST-WLD-003", "Asset Name": "Robotic Welding Cell #1",  "Category": "Fabrication",           "Location": "Plant 1 — Shop Floor", "Purchase Date": "2024-05-01", "Cost (SAR)": "310,000", "Warranty Exp": "2027-05-01", "Criticality": "High",   "Status": "active"},
            {"Asset Tag": "AST-CMP-004", "Asset Name": "Air Compressor 50HP",      "Category": "Facility / Utility",    "Location": "Utility Building",    "Purchase Date": "2020-11-12", "Cost (SAR)": "85,000",  "Warranty Exp": "2023-11-12", "Criticality": "High",   "Status": "active"},
        ]
    },

    "mnt_equipment_master": {
        "type": "list",
        "columns": ["Equipment Code", "Equipment Name", "Asset Ref", "Model / Serial", "Manufacturer", "Operating Hrs", "MTBF (Hrs)", "MTTR (Hrs)", "Status", "Actions"],
        "rows": [
            {"Equipment Code": "EQ-CNC-01", "Equipment Name": "CNC Spindle Head Assembly", "Asset Ref": "AST-CNC-001", "Model / Serial": "HSD-ES951 / SN-4421", "Manufacturer": "HSD Italy",     "Operating Hrs": "4,250", "MTBF (Hrs)": "620", "MTTR (Hrs)": "3.5", "Status": "active"},
            {"Equipment Code": "EQ-PNT-02", "Equipment Name": "Paint Spray Nozzle Pump",   "Asset Ref": "AST-PNT-001", "Model / Serial": "GRACO-G40 / SN-9910", "Manufacturer": "Graco USA",    "Operating Hrs": "2,890", "MTBF (Hrs)": "310", "MTTR (Hrs)": "1.8", "Status": "inactive"},
            {"Equipment Code": "EQ-WLD-01", "Equipment Name": "MIG Welding Torch Arm",     "Asset Ref": "AST-WLD-003", "Model / Serial": "ABB-IRB2600 / SN-104", "Manufacturer": "ABB Robotics", "Operating Hrs": "1,600", "MTBF (Hrs)": "850", "MTTR (Hrs)": "2.1", "Status": "active"},
            {"Equipment Code": "EQ-CMP-01", "Equipment Name": "Rotary Screw Element",      "Asset Ref": "AST-CMP-004", "Model / Serial": "ATLAS-GA37 / SN-7721", "Manufacturer": "Atlas Copco", "Operating Hrs": "12,400","MTBF (Hrs)": "1200","MTTR (Hrs)": "6.0", "Status": "active"},
        ]
    },

    "mnt_preventive_maintenance": {
        "type": "list",
        "columns": ["PM Plan Code", "Plan Name", "Equipment / Asset", "Frequency", "Task Count", "Estimated Hours", "Next Due Date", "Assigned Team", "Status", "Actions"],
        "rows": [
            {"PM Plan Code": "PM-CNC-M", "Plan Name": "Monthly CNC Spindle Lubrication & Alignment", "Equipment / Asset": "CNC Mach #1", "Frequency": "Monthly",   "Task Count": "8",  "Estimated Hours": "2.0h", "Next Due Date": "2026-08-01", "Assigned Team": "Mech Team A", "Status": "active"},
            {"PM Plan Code": "PM-PNT-W", "Plan Name": "Weekly Paint Booth Nozzle Cleaning",         "Equipment / Asset": "Painting Booth", "Frequency": "Weekly",    "Task Count": "5",  "Estimated Hours": "1.0h", "Next Due Date": "2026-07-25", "Assigned Team": "Paint Tech",   "Status": "active"},
            {"PM Plan Code": "PM-CMP-Q", "Plan Name": "Quarterly Compressor Filter Replacement",    "Equipment / Asset": "Air Compressor", "Frequency": "Quarterly", "Task Count": "12", "Estimated Hours": "4.0h", "Next Due Date": "2026-09-15", "Assigned Team": "Utility Team",  "Status": "active"},
            {"PM Plan Code": "PM-WLD-A", "Plan Name": "Annual Welding Robot Calibration",           "Equipment / Asset": "Welding Cell",  "Frequency": "Annually",  "Task Count": "24", "Estimated Hours": "8.0h", "Next Due Date": "2026-11-20", "Assigned Team": "External ABB", "Status": "active"},
        ]
    },

    "mnt_maintenance_work_orders": {
        "type": "list",
        "columns": ["MWO Number", "Type", "Asset / Equipment", "Issue / Task Description", "Priority", "Requested By", "Technician", "Due Date", "Status", "Actions"],
        "rows": [
            {"MWO Number": "MWO-2026-088", "Type": "Breakdown",   "Asset / Equipment": "Painting Booth", "Issue / Task Description": "Nozzle Blockage & Pressure Drop", "Priority": "High",   "Requested By": "Ahmed K.",  "Technician": "Rami Hassan",  "Due Date": "2026-07-22", "Status": "in_progress"},
            {"MWO Number": "MWO-2026-087", "Type": "Preventive",  "Asset / Equipment": "CNC Mach #1",    "Issue / Task Description": "Monthly Spindle Maintenance",     "Priority": "Medium", "Requested By": "System PM", "Technician": "Khalid M.",   "Due Date": "2026-07-25", "Status": "approved"},
            {"MWO Number": "MWO-2026-086", "Type": "Calibration", "Asset / Equipment": "QC Micrometer",  "Issue / Task Description": "Bi-Annual Calibration Check",     "Priority": "Low",    "Requested By": "Sara M.",   "Technician": "External Lab", "Due Date": "2026-07-20", "Status": "completed"},
            {"MWO Number": "MWO-2026-085", "Type": "Breakdown",   "Asset / Equipment": "Assembly Line 1","Issue / Task Description": "Conveyor Belt Tension Release",  "Priority": "High",   "Requested By": "Ahmed K.",  "Technician": "Rami Hassan",  "Due Date": "2026-07-19", "Status": "completed"},
        ]
    },

    "mnt_maintenance_schedule": {
        "type": "list",
        "columns": ["Schedule ID", "MWO Ref", "Asset / Equipment", "Maintenance Type", "Scheduled Start", "Scheduled End", "Assigned Tech", "Shift", "Status", "Actions"],
        "rows": [
            {"Schedule ID": "SCH-2026-042", "MWO Ref": "MWO-2026-088", "Asset / Equipment": "Painting Booth", "Maintenance Type": "Breakdown Repair",   "Scheduled Start": "2026-07-22 10:30", "Scheduled End": "2026-07-22 13:00", "Assigned Tech": "Rami Hassan", "Shift": "Morning", "Status": "in_progress"},
            {"Schedule ID": "SCH-2026-041", "MWO Ref": "MWO-2026-087", "Asset / Equipment": "CNC Mach #1",    "Maintenance Type": "Preventive (Monthly)", "Scheduled Start": "2026-07-25 08:00", "Scheduled End": "2026-07-25 10:00", "Assigned Tech": "Khalid M.",  "Shift": "Morning", "Status": "draft"},
            {"Schedule ID": "SCH-2026-040", "MWO Ref": "MWO-2026-085", "Asset / Equipment": "Assembly Line 1","Maintenance Type": "Breakdown Repair",   "Scheduled Start": "2026-07-19 14:00", "Scheduled End": "2026-07-19 16:30", "Assigned Tech": "Rami Hassan", "Shift": "Evening", "Status": "completed"},
        ]
    },

    "mnt_spare_parts_management": {
        "type": "list",
        "columns": ["Part Code", "Part Name", "Compatible Equipment", "Bin Location", "Stock Qty", "Min Reorder", "Unit Cost (SAR)", "Supplier", "Status", "Actions"],
        "rows": [
            {"Part Code": "SP-NOZ-001", "Part Name": "Spray Nozzle 0.4mm",   "Compatible Equipment": "Painting Booth", "Bin Location": "WH04-S01-A1", "Stock Qty": "4 Pcs",   "Min Reorder": "10 Pcs", "Unit Cost (SAR)": "120",   "Supplier": "Graco Trading",  "Status": "active"},
            {"Part Code": "SP-BLT-012", "Part Name": "V-Belt 1200mm",        "Compatible Equipment": "Assembly Line 1","Bin Location": "WH04-S02-B1", "Stock Qty": "15 Pcs",  "Min Reorder": "5 Pcs",  "Unit Cost (SAR)": "45",    "Supplier": "Saudi Belting Co","Status": "active"},
            {"Part Code": "SP-FLT-005", "Part Name": "Air Filter Cartridge",  "Compatible Equipment": "Air Compressor", "Bin Location": "WH04-S03-C2", "Stock Qty": "2 Pcs",   "Min Reorder": "4 Pcs",  "Unit Cost (SAR)": "350",   "Supplier": "Atlas Copco KSA","Status": "active"},
            {"Part Code": "SP-SPD-009", "Part Name": "CNC Spindle Bearing Set","Compatible Equipment": "CNC Mach #1/2", "Bin Location": "WH04-S01-A3", "Stock Qty": "1 Set",  "Min Reorder": "1 Set",  "Unit Cost (SAR)": "2,400", "Supplier": "SKF Bearings",   "Status": "active"},
        ]
    },

    "mnt_technician_assignment": {
        "type": "list",
        "columns": ["Tech Code", "Technician Name", "Specialization", "Active Work Orders", "Shift", "Status Today", "Completed MWO (Month)", "Efficiency %", "Actions"],
        "rows": [
            {"Tech Code": "TECH-001", "Technician Name": "Rami Hassan",    "Specialization": "Mechanical & Hydraulics", "Active Work Orders": "1 (MWO-088)", "Shift": "Morning (06–14)", "Status Today": "Busy",  "Completed MWO (Month)": "14", "Efficiency %": "92%"},
            {"Tech Code": "TECH-002", "Technician Name": "Khalid Mohammed","Specialization": "Electrical & Automation", "Active Work Orders": "0",           "Shift": "Morning (06–14)", "Status Today": "Available","Completed MWO (Month)": "18", "Efficiency %": "96%"},
            {"Tech Code": "TECH-003", "Technician Name": "Ahmed Al-Rashid","Specialization": "Pneumatics & Controls",   "Active Work Orders": "1 (MWO-087)", "Shift": "Evening (14–22)", "Status Today": "Off Duty",  "Completed MWO (Month)": "11", "Efficiency %": "88%"},
            {"Tech Code": "TECH-004", "Technician Name": "External Contractor","Specialization":"HVAC & Utility",        "Active Work Orders": "0",           "Shift": "On-Call",         "Status Today": "Available","Completed MWO (Month)": "4",  "Efficiency %": "95%"},
        ]
    },

    "mnt_maintenance_history": {
        "type": "list",
        "columns": ["MWO Number", "Asset / Equipment", "Type", "Problem", "Resolution", "Downtime (Hrs)", "Parts Used", "Cost (SAR)", "Completed On", "Technician", "Status"],
        "rows": [
            {"MWO Number": "MWO-2026-085", "Asset / Equipment": "Assembly Line 1","Type": "Breakdown",  "Problem": "Conveyor Belt Tension Release",  "Resolution": "Replaced V-Belt & recalibrated tension", "Downtime (Hrs)": "2.5h", "Parts Used": "SP-BLT-012 (1 Pc)", "Cost (SAR)": "145",   "Completed On": "2026-07-19", "Technician": "Rami Hassan", "Status": "completed"},
            {"MWO Number": "MWO-2026-080", "Asset / Equipment": "Air Compressor", "Type": "Preventive", "Problem": "Quarterly PM Service",             "Resolution": "Filter replacement, oil change, full check","Downtime (Hrs)": "4.0h", "Parts Used": "SP-FLT-005 (2 Pcs)","Cost (SAR)": "1,100", "Completed On": "2026-07-15", "Technician": "Rami Hassan", "Status": "completed"},
            {"MWO Number": "MWO-2026-074", "Asset / Equipment": "CNC Mach #2",    "Type": "Breakdown",  "Problem": "Coolant Pump Pressure Loss",     "Resolution": "Cleared blockage in return line",          "Downtime (Hrs)": "1.2h", "Parts Used": "None",              "Cost (SAR)": "60",    "Completed On": "2026-07-10", "Technician": "Khalid M.",   "Status": "completed"},
        ]
    },

    "mnt_calibration_schedule": {
        "type": "list",
        "columns": ["Equipment / Instrument", "Tag No", "Calibration Range", "Standard Spec", "Frequency", "Last Calibrated", "Next Due Date", "Calibrated By", "Certificate", "Status", "Actions"],
        "rows": [
            {"Equipment / Instrument": "Digital Micrometer 0-25mm",  "Tag No": "CAL-MIC-01", "Calibration Range": "0 – 25 mm",   "Standard Spec": "ISO 3611",   "Frequency": "Bi-Annual", "Last Calibrated": "2026-01-20", "Next Due Date": "2026-07-20", "Calibrated By": "Saudi Calibration Lab","Certificate": "CAL-2026-0114", "Status": "pending"},
            {"Equipment / Instrument": "Temperature Transmitter",    "Tag No": "CAL-TMP-04", "Calibration Range": "0 – 300 °C",  "Standard Spec": "IEC 60751",  "Frequency": "Annually",  "Last Calibrated": "2025-11-10", "Next Due Date": "2026-11-10", "Calibrated By": "Internal Quality Tech",  "Certificate": "CAL-2025-0899", "Status": "active"},
            {"Equipment / Instrument": "Pressure Gauge 0-10 Bar",    "Tag No": "CAL-PRS-08", "Calibration Range": "0 – 10 Bar",   "Standard Spec": "EN 837-1",   "Frequency": "Annual",    "Last Calibrated": "2026-03-05", "Next Due Date": "2027-03-05", "Calibrated By": "Internal Quality Tech",  "Certificate": "CAL-2026-0320", "Status": "active"},
            {"Equipment / Instrument": "Vernier Height Gauge 600mm", "Tag No": "CAL-HGT-02", "Calibration Range": "0 – 600 mm",  "Standard Spec": "DIN 862",    "Frequency": "Bi-Annual", "Last Calibrated": "2026-02-14", "Next Due Date": "2026-08-14", "Calibrated By": "Saudi Calibration Lab","Certificate": "CAL-2026-0210", "Status": "active"},
        ]
    },

    "mnt_maintenance_reports": {
        "type": "reports",
        "columns": ["Report Name", "Category", "Period", "Generated On", "By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "MTBF & MTTR Analysis",            "Category": "Reliability", "Period": "Q2 2026",     "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "280 KB"},
            {"Report Name": "Equipment Downtime Log",           "Category": "Downtime",    "Period": "Jul 2026",    "Generated On": "2026-07-21", "By": "Admin",  "Format": "PDF",  "Size": "140 KB"},
            {"Report Name": "Spare Parts Consumption & Cost",  "Category": "Costing",     "Period": "H1 2026",    "Generated On": "2026-07-20", "By": "System", "Format": "XLSX", "Size": "310 KB"},
            {"Report Name": "Preventive Compliance Rate",      "Category": "Compliance",  "Period": "Jul 2026",    "Generated On": "2026-07-22", "By": "System", "Format": "PDF",  "Size": "95 KB"},
            {"Report Name": "Asset Lifecycle & Depreciation",   "Category": "Asset",       "Period": "2026 YTD",   "Generated On": "2026-07-15", "By": "Admin",  "Format": "XLSX", "Size": "450 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # SUBCONTRACTING
    # ═══════════════════════════════════════
    "sub_subcontract_dashboard":        {"type": "sub_dashboard"},
    "sub_subcontract_order":            {"type": "sub_order_form"},
    "sub_material_issue_to_vendor":     {"type": "sub_issue_form"},
    "sub_material_receipt_from_vendor": {"type": "sub_receipt_form"},

    "sub_vendor_assignment": {
        "type": "list",
        "columns": ["Vendor Code", "Vendor Name", "Outsourced Process", "Capacity (Pcs/Mo)", "Assigned Orders", "Avg Lead Time", "Quality Score", "Status", "Actions"],
        "rows": [
            {"Vendor Code": "SUB-V-001", "Vendor Name": "Gulf Electroplating Ltd",  "Outsourced Process": "Anodizing & Electroplating", "Capacity (Pcs/Mo)": "5,000", "Assigned Orders": "3", "Avg Lead Time": "4 Days", "Quality Score": "96%", "Status": "active"},
            {"Vendor Code": "SUB-V-002", "Vendor Name": "Riyadh Heat Treatment Co.","Outsourced Process": "Hardening & Tempering",     "Capacity (Pcs/Mo)": "2,500", "Assigned Orders": "1", "Avg Lead Time": "3 Days", "Quality Score": "98%", "Status": "active"},
            {"Vendor Code": "SUB-V-003", "Vendor Name": "Advanced Powder Coating",  "Outsourced Process": "Powder Coating",             "Capacity (Pcs/Mo)": "10,000","Assigned Orders": "4", "Avg Lead Time": "5 Days", "Quality Score": "91%", "Status": "active"},
            {"Vendor Code": "SUB-V-004", "Vendor Name": "Precision Laser Cutters",  "Outsourced Process": "Laser Cutting & Profiling",  "Capacity (Pcs/Mo)": "8,000", "Assigned Orders": "2", "Avg Lead Time": "2 Days", "Quality Score": "99%", "Status": "active"},
        ]
    },

    "sub_vendor_performance": {
        "type": "list",
        "columns": ["Vendor Code", "Vendor Name", "Orders Completed", "On-Time Delivery %", "Rejection Rate %", "Cost Variance", "Rating Grade", "Status", "Actions"],
        "rows": [
            {"Vendor Code": "SUB-V-001", "Vendor Name": "Gulf Electroplating Ltd",  "Orders Completed": "24", "On-Time Delivery %": "95.8%", "Rejection Rate %": "1.2%", "Cost Variance": "0.0%",  "Rating Grade": "A",  "Status": "active"},
            {"Vendor Code": "SUB-V-002", "Vendor Name": "Riyadh Heat Treatment Co.","Orders Completed": "12", "On-Time Delivery %": "100%",   "Rejection Rate %": "0.5%", "Cost Variance": "−1.5%", "Rating Grade": "A+", "Status": "active"},
            {"Vendor Code": "SUB-V-003", "Vendor Name": "Advanced Powder Coating",  "Orders Completed": "30", "On-Time Delivery %": "86.7%", "Rejection Rate %": "3.8%", "Cost Variance": "+2.4%","Rating Grade": "B",  "Status": "active"},
            {"Vendor Code": "SUB-V-004", "Vendor Name": "Precision Laser Cutters",  "Orders Completed": "18", "On-Time Delivery %": "98.2%", "Rejection Rate %": "0.2%", "Cost Variance": "0.0%",  "Rating Grade": "A+", "Status": "active"},
        ]
    },

    "sub_job_tracking": {
        "type": "list",
        "columns": ["Job Card No", "SCO Ref", "Vendor Name", "Operation", "Qty Dispatched", "Qty Received", "Dispatch Date", "Expected Return", "Delay (Days)", "Status", "Actions"],
        "rows": [
            {"Job Card No": "JC-2026-088", "SCO Ref": "SCO-2026-042", "Vendor Name": "Advanced Powder Coating",  "Operation": "Powder Coating",    "Qty Dispatched": "300 Pcs", "Qty Received": "285 Pcs", "Dispatch Date": "2026-07-18", "Expected Return": "2026-07-23", "Delay (Days)": "0", "Status": "in_progress"},
            {"Job Card No": "JC-2026-087", "SCO Ref": "SCO-2026-041", "Vendor Name": "Gulf Electroplating Ltd",  "Operation": "Chrome Plating",    "Qty Dispatched": "150 Pcs", "Qty Received": "150 Pcs", "Dispatch Date": "2026-07-15", "Expected Return": "2026-07-19", "Delay (Days)": "0", "Status": "completed"},
            {"Job Card No": "JC-2026-086", "SCO Ref": "SCO-2026-040", "Vendor Name": "Riyadh Heat Treatment Co.","Operation": "Hardening & Temper", "Qty Dispatched": "80 Pcs",  "Qty Received": "0 Pcs",   "Dispatch Date": "2026-07-10", "Expected Return": "2026-07-15", "Delay (Days)": "+7 ⚠", "Status": "overloaded"},
        ]
    },

    "sub_cost_analysis": {
        "type": "list",
        "columns": ["SCO Ref", "Vendor Name", "Operation", "Order Qty", "In-House Cost (SAR)", "Vendor Cost (SAR)", "Transport Cost (SAR)", "Total Cost (SAR)", "Savings / Variance", "Status", "Actions"],
        "rows": [
            {"SCO Ref": "SCO-2026-042", "Vendor Name": "Advanced Powder Coating",  "Operation": "Powder Coating", "Order Qty": "300 Pcs", "In-House Cost (SAR)": "4,500", "Vendor Cost (SAR)": "3,200", "Transport Cost (SAR)": "300", "Total Cost (SAR)": "3,500", "Savings / Variance": "+1,000 (22%)", "Status": "completed"},
            {"SCO Ref": "SCO-2026-041", "Vendor Name": "Gulf Electroplating Ltd",  "Operation": "Chrome Plating", "Order Qty": "150 Pcs", "In-House Cost (SAR)": "3,000", "Vendor Cost (SAR)": "2,400", "Transport Cost (SAR)": "200", "Total Cost (SAR)": "2,600", "Savings / Variance": "+400 (13%)",   "Status": "completed"},
            {"SCO Ref": "SCO-2026-040", "Vendor Name": "Riyadh Heat Treatment Co.","Operation": "Heat Treatment", "Order Qty": "80 Pcs",  "In-House Cost (SAR)": "1,800", "Vendor Cost (SAR)": "1,950", "Transport Cost (SAR)": "150", "Total Cost (SAR)": "2,100", "Savings / Variance": "−300 (−16%)",  "Status": "in_progress"},
        ]
    },

    "sub_subcontract_reports": {
        "type": "reports",
        "columns": ["Report Name", "Category", "Period", "Generated On", "By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "Subcontract Order Summary",       "Category": "Orders",      "Period": "Jul 2026",    "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "190 KB"},
            {"Report Name": "Vendor Performance Scorecard",   "Category": "Vendor",      "Period": "H1 2026",     "Generated On": "2026-07-21", "By": "Admin",  "Format": "PDF",  "Size": "165 KB"},
            {"Report Name": "Material at Vendor Reconciliation","Category": "Inventory",  "Period": "Jul Wk 3",    "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "210 KB"},
            {"Report Name": "Outsourcing Cost vs In-House",   "Category": "Costing",     "Period": "Q2 2026",     "Generated On": "2026-07-20", "By": "Admin",  "Format": "PDF",  "Size": "115 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # PRODUCTION COSTING
    # ═══════════════════════════════════════
    "pc_costing_dashboard":     {"type": "pc_dashboard"},
    "pc_cost_rollup":           {"type": "pc_rollup_form"},

    "pc_bom_costing": {
        "type": "list",
        "columns": ["BOM Code", "Finished Product", "Direct Material Cost (SAR)", "Sub-Assemblies Cost (SAR)", "Scrap Recovery (SAR)", "Total BOM Cost (SAR)", "Last Updated", "Status", "Actions"],
        "rows": [
            {"BOM Code": "BOM-CH-001", "Finished Product": "Wooden Chair Assembly", "Direct Material Cost (SAR)": "145.50", "Sub-Assemblies Cost (SAR)": "32.00", "Scrap Recovery (SAR)": "−5.00", "Total BOM Cost (SAR)": "172.50", "Last Updated": "2026-07-20", "Status": "approved"},
            {"BOM Code": "BOM-DK-002", "Finished Product": "Metal Desk Frame",      "Direct Material Cost (SAR)": "280.00", "Sub-Assemblies Cost (SAR)": "65.00", "Scrap Recovery (SAR)": "−12.00","Total BOM Cost (SAR)": "333.00", "Last Updated": "2026-07-18", "Status": "approved"},
            {"BOM Code": "BOM-SF-003", "Finished Product": "Leather Sofa Cover",    "Direct Material Cost (SAR)": "420.00", "Sub-Assemblies Cost (SAR)": "110.00","Scrap Recovery (SAR)": "−8.00", "Total BOM Cost (SAR)": "522.00", "Last Updated": "2026-07-15", "Status": "draft"},
        ]
    },

    "pc_routing_cost": {
        "type": "list",
        "columns": ["Routing Code", "Product", "Operations Count", "Labor Cost / Unit (SAR)", "Machine Cost / Unit (SAR)", "Setup Cost / Unit (SAR)", "Total Operations Cost (SAR)", "Status", "Actions"],
        "rows": [
            {"Routing Code": "ROUT-CH-01", "Product": "Wooden Chair Assembly", "Operations Count": "4", "Labor Cost / Unit (SAR)": "28.50", "Machine Cost / Unit (SAR)": "42.00", "Setup Cost / Unit (SAR)": "5.00", "Total Operations Cost (SAR)": "75.50", "Status": "active"},
            {"Routing Code": "ROUT-DK-02", "Product": "Metal Desk Frame",      "Operations Count": "5", "Labor Cost / Unit (SAR)": "45.00", "Machine Cost / Unit (SAR)": "78.00", "Setup Cost / Unit (SAR)": "12.00","Total Operations Cost (SAR)": "135.00","Status": "active"},
            {"Routing Code": "ROUT-SF-03", "Product": "Leather Sofa Cover",    "Operations Count": "3", "Labor Cost / Unit (SAR)": "38.00", "Machine Cost / Unit (SAR)": "22.00", "Setup Cost / Unit (SAR)": "8.00", "Total Operations Cost (SAR)": "68.00", "Status": "active"},
        ]
    },

    "pc_standard_cost": {
        "type": "list",
        "columns": ["Product Code", "Product Name", "Direct Material (SAR)", "Direct Labor (SAR)", "Machine Overhead (SAR)", "Factory Overhead (SAR)", "Standard Unit Cost (SAR)", "Valid From", "Status", "Actions"],
        "rows": [
            {"Product Code": "FG-CH-001", "Product Name": "Wooden Chair Assembly", "Direct Material (SAR)": "172.50", "Direct Labor (SAR)": "28.50", "Machine Overhead (SAR)": "42.00", "Factory Overhead (SAR)": "15.00", "Standard Unit Cost (SAR)": "258.00", "Valid From": "2026-01-01", "Status": "active"},
            {"Product Code": "FG-DK-002", "Product Name": "Metal Desk Frame",      "Direct Material (SAR)": "333.00", "Direct Labor (SAR)": "45.00", "Machine Overhead (SAR)": "78.00", "Factory Overhead (SAR)": "24.00", "Standard Unit Cost (SAR)": "480.00", "Valid From": "2026-01-01", "Status": "active"},
            {"Product Code": "FG-SF-003", "Product Name": "Leather Sofa Cover",    "Direct Material (SAR)": "522.00", "Direct Labor (SAR)": "38.00", "Machine Overhead (SAR)": "22.00", "Factory Overhead (SAR)": "30.00", "Standard Unit Cost (SAR)": "612.00", "Valid From": "2026-01-01", "Status": "active"},
        ]
    },

    "pc_actual_cost": {
        "type": "list",
        "columns": ["WO Number", "Product Name", "Order Qty", "Actual Material (SAR)", "Actual Labor (SAR)", "Actual Machine (SAR)", "Actual Total (SAR)", "Actual Unit Cost (SAR)", "Variance %", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0412", "Product Name": "Wooden Chair", "Order Qty": "200", "Actual Material (SAR)": "35,100", "Actual Labor (SAR)": "5,900", "Actual Machine (SAR)": "8,600", "Actual Total (SAR)": "49,600", "Actual Unit Cost (SAR)": "248.00", "Variance %": "−3.88% (Savings)", "Status": "completed"},
            {"WO Number": "WO-2026-0408", "Product Name": "Steel Shelf",  "Order Qty": "150", "Actual Material (SAR)": "51,200", "Actual Labor (SAR)": "7,100", "Actual Machine (SAR)": "12,300","Actual Total (SAR)": "70,600", "Actual Unit Cost (SAR)": "470.67", "Variance %": "−1.94% (Savings)", "Status": "completed"},
            {"WO Number": "WO-2026-0411", "Product Name": "Desk Frame",   "Order Qty": "80",  "Actual Material (SAR)": "27,400", "Actual Labor (SAR)": "4,100", "Actual Machine (SAR)": "6,800", "Actual Total (SAR)": "38,300", "Actual Unit Cost (SAR)": "478.75", "Variance %": "−0.26% (Savings)", "Status": "in_progress"},
        ]
    },

    "pc_variance_analysis": {
        "type": "list",
        "columns": ["WO Number", "Product Name", "Std Unit Cost (SAR)", "Act Unit Cost (SAR)", "Material Var (SAR)", "Labor Var (SAR)", "Overhead Var (SAR)", "Total Variance (SAR)", "Variance Type", "Status", "Actions"],
        "rows": [
            {"WO Number": "WO-2026-0412", "Product Name": "Wooden Chair", "Std Unit Cost (SAR)": "258.00", "Act Unit Cost (SAR)": "248.00", "Material Var (SAR)": "−1,200 (Fav)", "Labor Var (SAR)": "−300 (Fav)", "Overhead Var (SAR)": "+500 (Unfav)", "Total Variance (SAR)": "−1,000", "Variance Type": "Favorable",   "Status": "approved"},
            {"WO Number": "WO-2026-0408", "Product Name": "Steel Shelf",  "Std Unit Cost (SAR)": "480.00", "Act Unit Cost (SAR)": "470.67", "Material Var (SAR)": "−1,800 (Fav)", "Labor Var (SAR)": "+600 (Unfav)","Overhead Var (SAR)": "−200 (Fav)",   "Total Variance (SAR)": "−1,400", "Variance Type": "Favorable",   "Status": "approved"},
            {"WO Number": "WO-2026-0405", "Product Name": "Leather Sofa", "Std Unit Cost (SAR)": "612.00", "Act Unit Cost (SAR)": "645.00", "Material Var (SAR)": "+2,500 (Unfav)","Labor Var (SAR)": "+800 (Unfav)","Overhead Var (SAR)": "0",          "Total Variance (SAR)": "+3,300", "Variance Type": "Unfavorable", "Status": "pending"},
        ]
    },

    "pc_labor_cost": {
        "type": "list",
        "columns": ["Work Center", "Labor Rate / Hr (SAR)", "Setup Rate / Hr (SAR)", "Overtime Multiplier", "Efficiency Factor", "Total Labor Hours (Jul)", "Total Labor Cost (SAR)", "Status", "Actions"],
        "rows": [
            {"Work Center": "Assembly Line 2", "Labor Rate / Hr (SAR)": "45.00", "Setup Rate / Hr (SAR)": "60.00", "Overtime Multiplier": "1.5x", "Efficiency Factor": "92%", "Total Labor Hours (Jul)": "420h", "Total Labor Cost (SAR)": "18,900", "Status": "active"},
            {"Work Center": "CNC Machining",   "Labor Rate / Hr (SAR)": "55.00", "Setup Rate / Hr (SAR)": "75.00", "Overtime Multiplier": "1.5x", "Efficiency Factor": "96%", "Total Labor Hours (Jul)": "380h", "Total Labor Cost (SAR)": "20,900", "Status": "active"},
            {"Work Center": "Welding Bay",     "Labor Rate / Hr (SAR)": "50.00", "Setup Rate / Hr (SAR)": "70.00", "Overtime Multiplier": "1.5x", "Efficiency Factor": "88%", "Total Labor Hours (Jul)": "290h", "Total Labor Cost (SAR)": "14,500", "Status": "active"},
        ]
    },

    "pc_machine_cost": {
        "type": "list",
        "columns": ["Machine Name", "Work Center", "Power Cost / Hr (SAR)", "Depreciation / Hr (SAR)", "Maintenance / Hr (SAR)", "Total Machine Rate / Hr (SAR)", "Hours Run (Jul)", "Total Machine Cost (SAR)", "Status", "Actions"],
        "rows": [
            {"Machine Name": "CNC Machine #1", "Work Center": "CNC Machining", "Power Cost / Hr (SAR)": "18.00", "Depreciation / Hr (SAR)": "45.00", "Maintenance / Hr (SAR)": "12.00", "Total Machine Rate / Hr (SAR)": "75.00", "Hours Run (Jul)": "210h", "Total Machine Cost (SAR)": "15,750", "Status": "active"},
            {"Machine Name": "Painting Booth", "Work Center": "Painting Booth","Power Cost / Hr (SAR)": "24.00", "Depreciation / Hr (SAR)": "30.00", "Maintenance / Hr (SAR)": "16.00", "Total Machine Rate / Hr (SAR)": "70.00", "Hours Run (Jul)": "180h", "Total Machine Cost (SAR)": "12,600", "Status": "active"},
            {"Machine Name": "Welding Robot",  "Work Center": "Welding Bay",   "Power Cost / Hr (SAR)": "15.00", "Depreciation / Hr (SAR)": "38.00", "Maintenance / Hr (SAR)": "10.00", "Total Machine Rate / Hr (SAR)": "63.00", "Hours Run (Jul)": "140h", "Total Machine Cost (SAR)": "8,820",  "Status": "active"},
        ]
    },

    "pc_overhead_cost": {
        "type": "list",
        "columns": ["Cost Pool Code", "Cost Pool Name", "Allocation Base", "Budgeted Overhead (SAR)", "Actual Overhead (SAR)", "Allocation Rate / Unit", "Absorbed Overhead (SAR)", "Variance (SAR)", "Status", "Actions"],
        "rows": [
            {"Cost Pool Code": "OH-FAC-01", "Cost Pool Name": "Plant Electricity & Utilities", "Allocation Base": "Machine Hours", "Budgeted Overhead (SAR)": "45,000", "Actual Overhead (SAR)": "43,200", "Allocation Rate / Unit": "SAR 22.50 / MH", "Absorbed Overhead (SAR)": "44,100", "Variance (SAR)": "−900 (Fav)",   "Status": "active"},
            {"Cost Pool Code": "OH-SUP-02", "Cost Pool Name": "Factory Supervision & Mgmt",    "Allocation Base": "Direct Labor Hrs","Budgeted Overhead (SAR)": "60,000", "Actual Overhead (SAR)": "61,500", "Allocation Rate / Unit": "SAR 18.00 / DLH", "Absorbed Overhead (SAR)": "60,800", "Variance (SAR)": "+700 (Unfav)", "Status": "active"},
            {"Cost Pool Code": "OH-MNT-03", "Cost Pool Name": "Plant Maintenance Overhead",    "Allocation Base": "Machine Hours", "Budgeted Overhead (SAR)": "25,000", "Actual Overhead (SAR)": "23,800", "Allocation Rate / Unit": "SAR 12.00 / MH", "Absorbed Overhead (SAR)": "24,400", "Variance (SAR)": "−600 (Fav)",   "Status": "active"},
        ]
    },

    "pc_cost_reports": {
        "type": "reports",
        "columns": ["Report Name", "Category", "Period", "Generated On", "By", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "Standard vs Actual Cost Variance Report", "Category": "Variance",   "Period": "Jul 2026",    "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "340 KB"},
            {"Report Name": "BOM Cost Breakdown Analysis",            "Category": "BOM Cost",   "Period": "Q3 2026",     "Generated On": "2026-07-21", "By": "Admin",  "Format": "PDF",  "Size": "210 KB"},
            {"Report Name": "Work Center Rate & Overhead Absorbed",   "Category": "Overhead",   "Period": "Jul 2026",    "Generated On": "2026-07-22", "By": "System", "Format": "XLSX", "Size": "180 KB"},
            {"Report Name": "Work Order Profitability & Margin",       "Category": "Margin",     "Period": "H1 2026",     "Generated On": "2026-07-15", "By": "Admin",  "Format": "PDF",  "Size": "290 KB"},
        ]
    },

    # ═══════════════════════════════════════
    # ANALYTICS & REPORTING
    # ═══════════════════════════════════════
    "ar_executive_dashboard":       {"type": "ar_exec_dashboard"},
    "ar_production_kpi_dashboard":  {"type": "ar_prod_kpi"},
    "ar_inventory_dashboard":       {"type": "ar_inv_dash"},
    "ar_oee_dashboard":             {"type": "ar_oee_dash"},
    "ar_quality_dashboard":         {"type": "ar_qm_dash"},
    "ar_maintenance_dashboard":     {"type": "ar_mnt_dash"},
    "ar_cost_dashboard":            {"type": "ar_cost_dash"},

    "ar_custom_reports": {
        "type": "reports",
        "columns": ["Report Name", "Module / Area", "Frequency", "Created By", "Last Run Date", "Status", "Actions"],
        "rows": [
            {"Report Name": "Daily Production Output vs Target", "Module / Area": "Production", "Frequency": "Daily",   "Created By": "Ahmed K.",  "Last Run Date": "2026-07-22", "Status": "active"},
            {"Report Name": "Raw Material Stock Out Warning",   "Module / Area": "Inventory",  "Frequency": "Realtime", "Created By": "Khalid M.","Last Run Date": "2026-07-22", "Status": "active"},
            {"Report Name": "Subcontract Loss & Scrap Reconciliation", "Module / Area": "Subcontract", "Frequency": "Weekly","Created By": "Sara M.",  "Last Run Date": "2026-07-20", "Status": "active"},
        ]
    },

    "ar_scheduled_reports": {
        "type": "list",
        "columns": ["Schedule Ref", "Report Name", "Recipients", "Cron Frequency", "Format", "Next Scheduled Run", "Status", "Actions"],
        "rows": [
            {"Schedule Ref": "SCH-REP-01", "Report Name": "Executive Monthly Summary", "Recipients": "gm@company.com, plant.head@company.com", "Cron Frequency": "Monthly (1st at 06:00)", "Format": "PDF",  "Next Scheduled Run": "2026-08-01 06:00", "Status": "active"},
            {"Schedule Ref": "SCH-REP-02", "Report Name": "Weekly OEE & Downtime Log", "Recipients": "maint.mgr@company.com",                  "Cron Frequency": "Weekly (Mon at 07:00)",  "Format": "XLSX", "Next Scheduled Run": "2026-07-27 07:00", "Status": "active"},
            {"Schedule Ref": "SCH-REP-03", "Report Name": "Daily Quality NCR Summary", "Recipients": "qc.team@company.com",                   "Cron Frequency": "Daily at 18:00",         "Format": "PDF",  "Next Scheduled Run": "2026-07-22 18:00", "Status": "active"},
        ]
    },

    "ar_export_center": {
        "type": "list",
        "columns": ["Export ID", "Dataset Name", "Records Count", "Export Format", "Requested By", "Requested On", "File Size", "Download Link", "Status"],
        "rows": [
            {"Export ID": "EXP-2026-088", "Dataset Name": "Full Item Stock Master Dump",     "Records Count": "428",  "Export Format": "XLSX", "Requested By": "Ahmed K.",  "Requested On": "2026-07-22 11:20", "File Size": "410 KB", "Download Link": "[Download XLSX]", "Status": "completed"},
            {"Export ID": "EXP-2026-087", "Dataset Name": "WO Execution History (2026 YTD)", "Records Count": "1,240","Export Format": "CSV",  "Requested By": "Admin",     "Requested On": "2026-07-21 16:45", "File Size": "820 KB", "Download Link": "[Download CSV]",  "Status": "completed"},
            {"Export ID": "EXP-2026-086", "Dataset Name": "Quality Inspection Ledger",       "Records Count": "890",  "Export Format": "JSON", "Requested By": "Sara M.",   "Requested On": "2026-07-20 09:15", "File Size": "1.2 MB", "Download Link": "[Download JSON]", "Status": "completed"},
        ]
    },

    # ═══════════════════════════════════════
    # ADMINISTRATION
    # ═══════════════════════════════════════
    "admin_user_management": {
        "type": "list",
        "columns": ["User ID", "Full Name", "Email", "Role", "Department", "Plant Access", "Last Login", "Status", "Actions"],
        "rows": [
            {"User ID": "USR-001", "Full Name": "Ahmed Al-Rashid", "Email": "ahmed.r@company.com", "Role": "Plant Manager",   "Department": "Production",  "Plant Access": "Plant 1 & 2", "Last Login": "2026-07-22 08:30", "Status": "active"},
            {"User ID": "USR-002", "Full Name": "Khalid Mohammed", "Email": "khalid.m@company.com", "Role": "Store Manager",   "Department": "Materials",   "Plant Access": "Plant 1",     "Last Login": "2026-07-22 09:12", "Status": "active"},
            {"User ID": "USR-003", "Full Name": "Sara Mohammed",   "Email": "sara.m@company.com",   "Role": "QC Inspector",    "Department": "Quality",     "Plant Access": "Plant 1",     "Last Login": "2026-07-21 17:05", "Status": "active"},
            {"User ID": "USR-004", "Full Name": "Rami Hassan",     "Email": "rami.h@company.com",   "Role": "Maint Technician","Department": "Maintenance", "Plant Access": "Plant 1 & 2", "Last Login": "2026-07-22 10:00", "Status": "active"},
        ]
    },

    "admin_role_management": {
        "type": "list",
        "columns": ["Role Code", "Role Name", "Description", "Users Count", "Permissions Count", "Access Level", "Status", "Actions"],
        "rows": [
            {"Role Code": "ROLE-ADMIN", "Role Name": "System Administrator", "Description": "Full ERP administrative & configuration access", "Users Count": "2", "Permissions Count": "120", "Access Level": "Full System", "Status": "active"},
            {"Role Code": "ROLE-PLANT", "Role Name": "Plant Manager",        "Description": "Production, WO, MRP, and Analytics access",      "Users Count": "4", "Permissions Count": "85",  "Access Level": "Plant Wide",  "Status": "active"},
            {"Role Code": "ROLE-STORE", "Role Name": "Store / Inventory Mgr", "Description": "Stock, GRN, Material Issue, Transfers",         "Users Count": "6", "Permissions Count": "42",  "Access Level": "Warehouse",   "Status": "active"},
            {"Role Code": "ROLE-QC",    "Role Name": "Quality Inspector",     "Description": "IQC, IPQC, OQC, NCR, CAPA, Certificates",        "Users Count": "5", "Permissions Count": "38",  "Access Level": "Quality Dept", "Status": "active"},
        ]
    },

    "admin_permission_management": {
        "type": "list",
        "columns": ["Permission Code", "Module", "Resource", "Action", "Description", "Assigned Roles", "Status", "Actions"],
        "rows": [
            {"Permission Code": "PERM-WO-CREATE",  "Module": "Work Orders", "Resource": "Work Order",     "Action": "Create / Edit", "Description": "Create and modify work order records", "Assigned Roles": "Plant Mgr, Production Sup", "Status": "active"},
            {"Permission Code": "PERM-GRN-POST",   "Module": "Materials",   "Resource": "Goods Receipt",  "Action": "Post Stock",    "Description": "Post inventory receipt to ledger",     "Assigned Roles": "Store Mgr, Inventory Tech",  "Status": "active"},
            {"Permission Code": "PERM-NCR-APPROVE","Module": "Quality",     "Resource": "NCR / CAPA",     "Action": "Approve",       "Description": "Approve disposition decision and CAPA","Assigned Roles": "QC Manager, Plant Mgr",     "Status": "active"},
        ]
    },

    "admin_company_setup": {
        "type": "list",
        "columns": ["Company Code", "Company Name", "CR Number", "VAT Number", "Base Currency", "Fiscal Year", "Country", "Status", "Actions"],
        "rows": [
            {"Company Code": "CMP-001", "Company Name": "Saudi Modern Industrial Co.", "CR Number": "1010892241", "VAT Number": "300451299800003", "Base Currency": "SAR (SR)", "Fiscal Year": "Jan – Dec", "Country": "Saudi Arabia", "Status": "active"},
        ]
    },

    "admin_plant_setup": {
        "type": "list",
        "columns": ["Plant Code", "Plant Name", "Location / City", "Company Ref", "Plant Manager", "Timezone", "Status", "Actions"],
        "rows": [
            {"Plant Code": "PLT-01", "Plant Name": "Riyadh Main Manufacturing Facility", "Location / City": "Riyadh 2nd Industrial Zone", "Company Ref": "CMP-001", "Plant Manager": "Ahmed Al-Rashid", "Timezone": "Asia/Riyadh (GMT+3)", "Status": "active"},
            {"Plant Code": "PLT-02", "Plant Name": "Jeddah Assembly & Warehouse Hub",    "Location / City": "Jeddah Industrial City",     "Company Ref": "CMP-001", "Plant Manager": "Faisal Al-Otaibi", "Timezone": "Asia/Riyadh (GMT+3)", "Status": "active"},
        ]
    },

    "admin_department_master": {
        "type": "list",
        "columns": ["Dept Code", "Department Name", "Plant Ref", "Head of Dept", "Cost Center", "Employees Count", "Status", "Actions"],
        "rows": [
            {"Dept Code": "DEPT-PROD", "Department Name": "Production & Assembly",   "Plant Ref": "PLT-01", "Head of Dept": "Ahmed Al-Rashid", "Cost Center": "CC-101-PROD", "Employees Count": "45", "Status": "active"},
            {"Dept Code": "DEPT-MAT",  "Department Name": "Materials & Warehouse",    "Plant Ref": "PLT-01", "Head of Dept": "Khalid Mohammed", "Cost Center": "CC-102-MAT",  "Employees Count": "18", "Status": "active"},
            {"Dept Code": "DEPT-QC",   "Department Name": "Quality Control & Assurance","Plant Ref":"PLT-01", "Head of Dept": "Sara Mohammed",   "Cost Center": "CC-103-QC",   "Employees Count": "12", "Status": "active"},
            {"Dept Code": "DEPT-MNT",  "Department Name": "Plant Maintenance",        "Plant Ref": "PLT-01", "Head of Dept": "Rami Hassan",     "Cost Center": "CC-104-MNT",  "Employees Count": "10", "Status": "active"},
        ]
    },

    "admin_work_center_master": {
        "type": "list",
        "columns": ["WC Code", "Work Center Name", "Department", "Capacity (Hrs/Day)", "Labor Rate (SAR)", "Machine Rate (SAR)", "Status", "Actions"],
        "rows": [
            {"WC Code": "WC-CNC-01", "Work Center Name": "CNC Machining Shop",  "Department": "Production", "Capacity (Hrs/Day)": "16h", "Labor Rate (SAR)": "55.00", "Machine Rate (SAR)": "75.00", "Status": "active"},
            {"WC Code": "WC-ASM-02", "Work Center Name": "Assembly Line 2",     "Department": "Production", "Capacity (Hrs/Day)": "16h", "Labor Rate (SAR)": "45.00", "Machine Rate (SAR)": "25.00", "Status": "active"},
            {"WC Code": "WC-PNT-01", "Work Center Name": "Spray Paint Booth",   "Department": "Production", "Capacity (Hrs/Day)": "8h",  "Labor Rate (SAR)": "40.00", "Machine Rate (SAR)": "70.00", "Status": "active"},
            {"WC Code": "WC-WLD-03", "Work Center Name": "Robotic Welding Bay", "Department": "Production", "Capacity (Hrs/Day)": "16h", "Labor Rate (SAR)": "50.00", "Machine Rate (SAR)": "63.00", "Status": "active"},
        ]
    },

    "admin_machine_master": {
        "type": "list",
        "columns": ["Machine Code", "Machine Name", "Work Center", "Serial No", "Power (kW)", "Mfg Year", "Status", "Actions"],
        "rows": [
            {"Machine Code": "MCH-CNC-001", "Machine Name": "5-Axis CNC Milling Unit #1", "Work Center": "WC-CNC-01", "Serial No": "HSD-99124", "Power (kW)": "35 kW", "Mfg Year": "2022", "Status": "active"},
            {"Machine Code": "MCH-PNT-001", "Machine Name": "Automated Spray Painter",     "Work Center": "WC-PNT-01", "Serial No": "GRC-44120", "Power (kW)": "22 kW", "Mfg Year": "2021", "Status": "active"},
            {"Machine Code": "MCH-WLD-001", "Machine Name": "ABB Robotic Welder Cell",     "Work Center": "WC-WLD-03", "Serial No": "ABB-88102", "Power (kW)": "18 kW", "Mfg Year": "2024", "Status": "active"},
        ]
    },

    "admin_shift_master": {
        "type": "list",
        "columns": ["Shift Code", "Shift Name", "Start Time", "End Time", "Break Duration", "Working Hours", "Status", "Actions"],
        "rows": [
            {"Shift Code": "SHIFT-A", "Shift Name": "Morning Shift", "Start Time": "06:00 AM", "End Time": "02:30 PM", "Break Duration": "30 mins", "Working Hours": "8.0h", "Status": "active"},
            {"Shift Code": "SHIFT-B", "Shift Name": "Evening Shift", "Start Time": "02:30 PM", "End Time": "11:00 PM", "Break Duration": "30 mins", "Working Hours": "8.0h", "Status": "active"},
            {"Shift Code": "SHIFT-C", "Shift Name": "Night Shift",   "Start Time": "11:00 PM", "End Time": "06:00 AM", "Break Duration": "30 mins", "Working Hours": "6.5h", "Status": "active"},
        ]
    },

    "admin_calendar_master": {
        "type": "list",
        "columns": ["Calendar Year", "Holiday Name", "Date", "Day of Week", "Category", "Factory Working?", "Status", "Actions"],
        "rows": [
            {"Calendar Year": "2026", "Holiday Name": "Founding Day",        "Date": "2026-02-22", "Day of Week": "Sunday",   "Category": "National Holiday", "Factory Working?": "Closed", "Status": "active"},
            {"Calendar Year": "2026", "Holiday Name": "Eid Al-Fitr Holiday", "Date": "2026-03-20", "Day of Week": "Friday",   "Category": "Religious Holiday","Factory Working?": "Closed", "Status": "active"},
            {"Calendar Year": "2026", "Holiday Name": "Saudi National Day",  "Date": "2026-09-23", "Day of Week": "Wednesday","Category": "National Holiday", "Factory Working?": "Closed", "Status": "active"},
        ]
    },

    "admin_number_series": {
        "type": "list",
        "columns": ["Series Code", "Document Type", "Prefix", "Current Number", "Suffix", "Format Pattern", "Status", "Actions"],
        "rows": [
            {"Series Code": "NS-WO",  "Document Type": "Work Order",       "Prefix": "WO-2026-",  "Current Number": "0415", "Suffix": "", "Format Pattern": "{PREFIX}{NUM:4}", "Status": "active"},
            {"Series Code": "NS-GRN", "Document Type": "Goods Receipt",    "Prefix": "GRN-2026-", "Current Number": "0056", "Suffix": "", "Format Pattern": "{PREFIX}{NUM:3}", "Status": "active"},
            {"Series Code": "NS-NCR", "Document Type": "Quality NCR",      "Prefix": "NCR-2026-", "Current Number": "0019", "Suffix": "", "Format Pattern": "{PREFIX}{NUM:3}", "Status": "active"},
            {"Series Code": "NS-MWO", "Document Type": "Maintenance WO",   "Prefix": "MWO-2026-", "Current Number": "0089", "Suffix": "", "Format Pattern": "{PREFIX}{NUM:3}", "Status": "active"},
        ]
    },

    "admin_workflow_setup": {
        "type": "list",
        "columns": ["Workflow Code", "Workflow Name", "Trigger Entity", "Steps Count", "Auto-Escalation (Hrs)", "Status", "Actions"],
        "rows": [
            {"Workflow Code": "WF-WO-APP",  "Workflow Name": "Work Order Release Approval",    "Trigger Entity": "Work Order",     "Steps Count": "2 Steps", "Auto-Escalation (Hrs)": "24h", "Status": "active"},
            {"Workflow Code": "WF-NCR-CAPA","Workflow Name": "Critical NCR Escalation",        "Trigger Entity": "Quality NCR",    "Steps Count": "3 Steps", "Auto-Escalation (Hrs)": "12h", "Status": "active"},
            {"Workflow Code": "WF-PO-APP",  "Workflow Name": "Purchase Order Value Approval",  "Trigger Entity": "Purchase Order", "Steps Count": "2 Steps", "Auto-Escalation (Hrs)": "48h", "Status": "active"},
        ]
    },

    "admin_approval_setup": {
        "type": "list",
        "columns": ["Approval Matrix", "Document Type", "Min Value (SAR)", "Max Value (SAR)", "Approver Role", "Substitute Role", "Status", "Actions"],
        "rows": [
            {"Approval Matrix": "MAT-PO-1", "Document Type": "Subcontract PO", "Min Value (SAR)": "0.00",      "Max Value (SAR)": "50,000.00", "Approver Role": "Plant Manager",   "Substitute Role": "Operations Head", "Status": "active"},
            {"Approval Matrix": "MAT-PO-2", "Document Type": "Subcontract PO", "Min Value (SAR)": "50,000.00", "Max Value (SAR)": "Un-limited",  "Approver Role": "General Manager", "Substitute Role": "VP Operations",   "Status": "active"},
        ]
    },

    "admin_notification_setup": {
        "type": "list",
        "columns": ["Event Code", "Event Name", "Channel", "Recipients", "Template Code", "Status", "Actions"],
        "rows": [
            {"Event Code": "EVT-LOW-STOCK","Event Name": "Reorder Level Breach Alert","Channel": "Email & SMS", "Recipients": "Store Manager, Buyer", "Template Code": "TMPL-STOCK-ALERT", "Status": "active"},
            {"Event Code": "EVT-MACHINE-DT","Event Name": "Machine Breakdown Alert",  "Channel": "System & SMS", "Recipients": "Maintenance Tech",  "Template Code": "TMPL-DT-ALERT",    "Status": "active"},
            {"Event Code": "EVT-NCR-HIGH", "Event Name": "Critical NCR Raised",       "Channel": "Email",        "Recipients": "QC Lead, Plant Mgr",  "Template Code": "TMPL-NCR-ALERT",   "Status": "active"},
        ]
    },

    "admin_audit_log": {
        "type": "list",
        "columns": ["Log ID", "Timestamp", "User Name", "Action Performed", "Module", "Record Ref", "IP Address", "Status"],
        "rows": [
            {"Log ID": "LOG-88120", "Timestamp": "2026-07-22 11:45:02", "User Name": "Ahmed Al-Rashid", "Action Performed": "Approved Work Order",     "Module": "Work Orders", "Record Ref": "WO-2026-0412", "IP Address": "192.168.1.45", "Status": "success"},
            {"Log ID": "LOG-88119", "Timestamp": "2026-07-22 10:15:30", "User Name": "Khalid Mohammed", "Action Performed": "Posted Inventory Issue",  "Module": "Materials",   "Record Ref": "MI-2026-038",  "IP Address": "192.168.1.88", "Status": "success"},
            {"Log ID": "LOG-88118", "Timestamp": "2026-07-22 09:30:11", "User Name": "Sara Mohammed",   "Action Performed": "Created Inspection Lot",  "Module": "Quality",     "Record Ref": "IL-2026-055",  "IP Address": "192.168.1.92", "Status": "success"},
        ]
    },

    "admin_system_configuration": {
        "type": "list",
        "columns": ["Config Key", "Parameter Description", "Module Scope", "Current Value", "Default Value", "Modified Date", "Status", "Actions"],
        "rows": [
            {"Config Key": "CFG-WO-AUTO-RELEASE", "Parameter Description": "Auto-release WO when materials available", "Module Scope": "Work Orders", "Current Value": "TRUE",        "Default Value": "FALSE", "Modified Date": "2026-06-01", "Status": "active"},
            {"Config Key": "CFG-QC-AQL-DEFAULT",  "Parameter Description": "Default AQL Sampling Level for IQC",        "Module Scope": "Quality",     "Current Value": "AQL 2.5 Normal","Default Value": "AQL 2.5","Modified Date": "2026-05-15", "Status": "active"},
            {"Config Key": "CFG-MNT-EMERGENCY",   "Parameter Description": "Auto-notify maintenance on breakdown",      "Module Scope": "Maintenance", "Current Value": "TRUE",        "Default Value": "TRUE",  "Modified Date": "2026-04-10", "Status": "active"},
        ]
    },

    "admin_backup_restore": {
        "type": "list",
        "columns": ["Backup ID", "Backup Type", "Created Date / Time", "File Size", "Storage Location", "Auto Schedule", "Status", "Actions"],
        "rows": [
            {"Backup ID": "BAK-2026-0722", "Backup Type": "Automated Full System", "Created Date / Time": "2026-07-22 02:00", "File Size": "1.45 GB", "Storage Location": "Cloud Storage (KSA-Riyadh)", "Auto Schedule": "Daily 02:00 AM", "Status": "completed"},
            {"Backup ID": "BAK-2026-0721", "Backup Type": "Automated Full System", "Created Date / Time": "2026-07-21 02:00", "File Size": "1.42 GB", "Storage Location": "Cloud Storage (KSA-Riyadh)", "Auto Schedule": "Daily 02:00 AM", "Status": "completed"},
            {"Backup ID": "BAK-2026-0720", "Backup Type": "Manual Ad-Hoc Pre-Patch","Created Date / Time": "2026-07-20 22:30", "File Size": "1.40 GB", "Storage Location": "Local On-Prem Vault",      "Auto Schedule": "Manual",        "Status": "completed"},
        ]
    },

    "admin_integration_settings": {
        "type": "list",
        "columns": ["Integration ID", "System Name", "Integration Type", "Endpoint URL", "Auth Mode", "Last Sync", "Sync Status", "Actions"],
        "rows": [
            {"Integration ID": "INT-HRMS-01",  "System Name": "HRMS & Payroll System",     "Integration Type": "REST API / Bi-Directional", "Endpoint URL": "https://hrms.company.com/api/v2/", "Auth Mode": "OAuth2 Bearer", "Last Sync": "2026-07-22 11:30", "Sync Status": "active"},
            {"Integration ID": "INT-FIN-02",   "System Name": "Finance & General Ledger",   "Integration Type": "REST API / Event Driven",  "Endpoint URL": "https://fin.company.com/api/v1/",  "Auth Mode": "API Key / TLS",  "Last Sync": "2026-07-22 11:45", "Sync Status": "active"},
            {"Integration ID": "INT-SCADA-03", "System Name": "Shop Floor SCADA / IoT Hub", "Integration Type": "MQTT / OPC-UA Broker",   "Endpoint URL": "opc.tcp://192.168.10.50:4840",      "Auth Mode": "X.509 Cert",    "Last Sync": "2026-07-22 11:54", "Sync Status": "active"},
        ]
    },

    "pp_production_plan": {
        "type": "list",
        "columns": ["Plan ID", "Target Product", "Quantity", "Start Date", "End Date", "Priority", "Status", "Actions"],
        "rows": [
            {"Plan ID": "PP-2026-001", "Target Product": "Wooden Chair Assembly", "Quantity": "500 Pcs", "Start Date": "2026-07-01", "End Date": "2026-07-31", "Priority": "High", "Status": "approved"},
            {"Plan ID": "PP-2026-002", "Target Product": "Metal Desk Frame", "Quantity": "200 Pcs", "Start Date": "2026-07-05", "End Date": "2026-07-25", "Priority": "Medium", "Status": "in_progress"},
            {"Plan ID": "PP-2026-003", "Target Product": "Leather Sofa Cover", "Quantity": "150 Pcs", "Start Date": "2026-07-10", "End Date": "2026-08-10", "Priority": "Low", "Status": "draft"},
            {"Plan ID": "PP-2026-004", "Target Product": "Cabinet Hardware Kit", "Quantity": "1000 Pcs", "Start Date": "2026-08-01", "End Date": "2026-08-20", "Priority": "High", "Status": "approved"},
        ]
    },

    "pp_master_production_schedule__mps_": {
        "type": "list",
        "columns": ["Item Code", "Item Name", "Planning Period", "Projected Demand", "Scheduled Receipts", "On-Hand Balance", "Net Requirement", "Actions"],
        "rows": [
            {"Item Code": "FG-CH-001", "Item Name": "Wooden Chair", "Planning Period": "Jul 2026 Wk 3", "Projected Demand": "200", "Scheduled Receipts": "150", "On-Hand Balance": "80", "Net Requirement": "−30"},
            {"Item Code": "FG-DK-002", "Item Name": "Metal Desk", "Planning Period": "Jul 2026 Wk 3", "Projected Demand": "100", "Scheduled Receipts": "0", "On-Hand Balance": "20", "Net Requirement": "80"},
            {"Item Code": "FG-SF-003", "Item Name": "Leather Sofa", "Planning Period": "Jul 2026 Wk 4", "Projected Demand": "60", "Scheduled Receipts": "60", "On-Hand Balance": "15", "Net Requirement": "−15"},
            {"Item Code": "FG-CB-004", "Item Name": "Cabinet Unit", "Planning Period": "Aug 2026 Wk 1", "Projected Demand": "350", "Scheduled Receipts": "200", "On-Hand Balance": "40", "Net Requirement": "110"},
        ]
    },

    "pp_material_requirement_planning__mrp_": {
        "type": "list",
        "columns": ["MRP Run ID", "Run Date & Time", "Items Evaluated", "Planned Orders", "Shortages Found", "Triggered By", "Status", "Actions"],
        "rows": [
            {"MRP Run ID": "MRP-2026-0042", "Run Date & Time": "2026-07-22 08:00 AM", "Items Evaluated": "342", "Planned Orders": "28", "Shortages Found": "5", "Triggered By": "Auto Scheduler", "Status": "completed"},
            {"MRP Run ID": "MRP-2026-0041", "Run Date & Time": "2026-07-21 06:00 AM", "Items Evaluated": "342", "Planned Orders": "15", "Shortages Found": "2", "Triggered By": "Admin", "Status": "completed"},
            {"MRP Run ID": "MRP-2026-0040", "Run Date & Time": "2026-07-18 08:00 AM", "Items Evaluated": "338", "Planned Orders": "31", "Shortages Found": "8", "Triggered By": "Auto Scheduler", "Status": "completed"},
        ]
    },

    "pp_capacity_planning": {
        "type": "list",
        "columns": ["Work Center", "Shift", "Total Capacity (Hrs)", "Utilized (Hrs)", "Utilization %", "Status", "Actions"],
        "rows": [
            {"Work Center": "Assembly Line 1", "Shift": "Morning", "Total Capacity (Hrs)": "8.0", "Utilized (Hrs)": "7.2", "Utilization %": "90%", "Status": "overloaded"},
            {"Work Center": "Painting Booth", "Shift": "Morning", "Total Capacity (Hrs)": "8.0", "Utilized (Hrs)": "5.5", "Utilization %": "69%", "Status": "normal"},
            {"Work Center": "Packaging Station", "Shift": "Evening", "Total Capacity (Hrs)": "8.0", "Utilized (Hrs)": "2.0", "Utilization %": "25%", "Status": "underutilized"},
            {"Work Center": "CNC Machining", "Shift": "Morning", "Total Capacity (Hrs)": "8.0", "Utilized (Hrs)": "8.0", "Utilization %": "100%", "Status": "overloaded"},
        ]
    },

    "pp_demand_forecast": {
        "type": "list",
        "columns": ["Item Group", "Item Name", "Forecast Period", "Forecasted Qty", "Actual Qty", "Variance", "Confidence %", "Actions"],
        "rows": [
            {"Item Group": "Furniture", "Item Name": "Wooden Chair", "Forecast Period": "Aug 2026", "Forecasted Qty": "250", "Actual Qty": "—", "Variance": "—", "Confidence %": "85%"},
            {"Item Group": "Furniture", "Item Name": "Metal Desk", "Forecast Period": "Aug 2026", "Forecasted Qty": "120", "Actual Qty": "—", "Variance": "—", "Confidence %": "78%"},
            {"Item Group": "Upholstery", "Item Name": "Leather Sofa", "Forecast Period": "Jul 2026", "Forecasted Qty": "60", "Actual Qty": "58", "Variance": "−3.3%", "Confidence %": "92%"},
            {"Item Group": "Storage", "Item Name": "Cabinet Unit", "Forecast Period": "Aug 2026", "Forecasted Qty": "400", "Actual Qty": "—", "Variance": "—", "Confidence %": "70%"},
        ]
    },

    "pp_production_calendar": {
        "type": "list",
        "columns": ["Date", "Day", "Plant", "Shift Pattern", "Working Hours", "Type", "Status", "Actions"],
        "rows": [
            {"Date": "2026-07-21", "Day": "Monday", "Plant": "Plant 1", "Shift Pattern": "2-Shift", "Working Hours": "16 hrs", "Type": "Regular", "Status": "active"},
            {"Date": "2026-07-22", "Day": "Tuesday", "Plant": "Plant 1", "Shift Pattern": "2-Shift", "Working Hours": "16 hrs", "Type": "Regular", "Status": "active"},
            {"Date": "2026-07-25", "Day": "Friday", "Plant": "Plant 1", "Shift Pattern": "1-Shift", "Working Hours": "8 hrs", "Type": "Regular", "Status": "active"},
            {"Date": "2026-07-26", "Day": "Saturday", "Plant": "Plant 1", "Shift Pattern": "Off", "Working Hours": "0 hrs", "Type": "Holiday", "Status": "inactive"},
            {"Date": "2026-07-27", "Day": "Sunday", "Plant": "Plant 1", "Shift Pattern": "Off", "Working Hours": "0 hrs", "Type": "Weekend", "Status": "inactive"},
        ]
    },

    "pp_resource_planning": {
        "type": "list",
        "columns": ["Resource Name", "Category", "Department", "Assigned Tasks", "Available From", "Utilization %", "Status", "Actions"],
        "rows": [
            {"Resource Name": "Ahmed Al-Rashid", "Category": "Operator", "Department": "Assembly", "Assigned Tasks": "3", "Available From": "08:00 AM", "Utilization %": "87%", "Status": "active"},
            {"Resource Name": "CNC Machine #2", "Category": "Machine", "Department": "Machining", "Assigned Tasks": "2", "Available From": "06:00 AM", "Utilization %": "100%", "Status": "overloaded"},
            {"Resource Name": "Paint Spray Unit A", "Category": "Equipment", "Department": "Finishing", "Assigned Tasks": "1", "Available From": "09:00 AM", "Utilization %": "60%", "Status": "active"},
            {"Resource Name": "Sara Mohammed", "Category": "Supervisor", "Department": "QC", "Assigned Tasks": "5", "Available From": "07:00 AM", "Utilization %": "75%", "Status": "active"},
        ]
    },

    "pp_shift_planning": {
        "type": "list",
        "columns": ["Shift Code", "Shift Name", "Start Time", "End Time", "Break Duration", "Supervisor", "Headcount", "Status", "Actions"],
        "rows": [
            {"Shift Code": "SH-01", "Shift Name": "Morning Shift", "Start Time": "06:00 AM", "End Time": "02:00 PM", "Break Duration": "30 min", "Supervisor": "Ahmed Al-Rashid", "Headcount": "24", "Status": "active"},
            {"Shift Code": "SH-02", "Shift Name": "Evening Shift", "Start Time": "02:00 PM", "End Time": "10:00 PM", "Break Duration": "30 min", "Supervisor": "Sara Mohammed", "Headcount": "18", "Status": "active"},
            {"Shift Code": "SH-03", "Shift Name": "Night Shift", "Start Time": "10:00 PM", "End Time": "06:00 AM", "Break Duration": "30 min", "Supervisor": "Khalid Nasser", "Headcount": "10", "Status": "inactive"},
        ]
    },

    "pp_production_plan_approval": {
        "type": "list",
        "columns": ["Plan ID", "Product", "Quantity", "Requested By", "Submitted On", "Approver", "Review Status", "Actions"],
        "rows": [
            {"Plan ID": "PP-2026-005", "Product": "Steel Cabinet Frame", "Quantity": "300 Pcs", "Requested By": "Ahmed Al-Rashid", "Submitted On": "2026-07-20", "Approver": "Sara Mohammed", "Review Status": "pending"},
            {"Plan ID": "PP-2026-006", "Product": "Powder Coated Sheet", "Quantity": "600 Pcs", "Requested By": "Khalid Nasser", "Submitted On": "2026-07-21", "Approver": "Sara Mohammed", "Review Status": "pending"},
            {"Plan ID": "PP-2026-003", "Product": "Leather Sofa Cover", "Quantity": "150 Pcs", "Requested By": "Admin", "Submitted On": "2026-07-18", "Approver": "Sara Mohammed", "Review Status": "rejected"},
        ]
    },

    "pp_production_plan_reports": {
        "type": "reports",
        "columns": ["Report Name", "Report Type", "Generated On", "Generated By", "Period", "Format", "Size", "Actions"],
        "rows": [
            {"Report Name": "Weekly Production Summary", "Report Type": "Summary", "Generated On": "2026-07-22", "Generated By": "System", "Period": "Jul Wk 3", "Format": "XLSX", "Size": "142 KB"},
            {"Report Name": "MRP Shortage Analysis", "Report Type": "Exception", "Generated On": "2026-07-22", "Generated By": "Admin", "Period": "Jul 2026", "Format": "PDF", "Size": "98 KB"},
            {"Report Name": "Capacity Utilization Report", "Report Type": "Analytics", "Generated On": "2026-07-21", "Generated By": "System", "Period": "Jul 2026", "Format": "XLSX", "Size": "215 KB"},
            {"Report Name": "Demand vs Actual Report", "Report Type": "Comparison", "Generated On": "2026-07-20", "Generated By": "Admin", "Period": "Q2 2026", "Format": "PDF", "Size": "340 KB"},
        ]
    },
}

# ─────────────────────────────────────────────
# STATUS BADGE LOGIC
# ─────────────────────────────────────────────
STATUS_BADGES = {
    "approved":       ("status-approved",     "Approved"),
    "in_progress":    ("status-inprogress",   "In Progress"),
    "draft":          ("status-draft",        "Draft"),
    "completed":      ("status-completed",    "Completed"),
    "pending":        ("status-pending",      "Pending Approval"),
    "rejected":       ("status-rejected",     "Rejected"),
    "active":         ("status-active",       "Active"),
    "inactive":       ("status-inactive",     "Inactive"),
    "overloaded":     ("status-overloaded",   "⚠ Overloaded"),
    "underutilized":  ("status-underutil",    "↓ Underutilized"),
    "normal":         ("status-active",       "Normal"),
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
        # Auto-badge status fields
        if col.lower() in ("status", "review status"):
            val = render_badge(val)
        # Highlight negative values
        if isinstance(val, str) and val.startswith("−"):
            val = f'<span style="color:#ef4444; font-weight:600;">{val}</span>'
        # Highlight 100% utilization
        if col == "Utilization %" and val == "100%":
            val = f'<span style="color:#ef4444; font-weight:600;">{val}</span>'
        cells += f"<td>{val}</td>"
    # Actions column
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

def render_reports_row(row, columns):
    cells = ""
    for col in columns:
        if col == "Actions":
            continue
        val = row.get(col, "—")
        cells += f"<td>{val}</td>"
    cells += """
    <td>
      <div class="action-icons">
        <svg title="Download" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        <svg title="Preview" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
        <svg class="delete" title="Delete" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
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
        elif page_type == "reports":
            body_rows += render_reports_row(r, columns)
        else:
            body_rows += render_table_row(r, columns)

    create_btn_label = "Generate Report" if page_type == "reports" else "+ Create New"
    export_label = "Export" if page_type != "reports" else "Schedule Report"

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
                {export_label}
              </button>
              <button class="btn btn-primary">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                {create_btn_label}
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

DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
    </div>
    <div class="kpi-body">
      <div class="kpi-value">12</div>
      <div class="kpi-label">Active Production Plans</div>
    </div>
    <div class="kpi-trend up">↑ 3 this week</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
    </div>
    <div class="kpi-body">
      <div class="kpi-value">78%</div>
      <div class="kpi-label">Avg. Capacity Utilization</div>
    </div>
    <div class="kpi-trend down">↓ 4% vs last week</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
    </div>
    <div class="kpi-body">
      <div class="kpi-value">5</div>
      <div class="kpi-label">Material Shortages (MRP)</div>
    </div>
    <div class="kpi-trend down">↑ 2 since yesterday</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body">
      <div class="kpi-value">3</div>
      <div class="kpi-label">Plans Awaiting Approval</div>
    </div>
    <div class="kpi-trend neutral">→ Same as yesterday</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:2;">
    <div class="dash-card-header">
      <span class="dash-card-title">Weekly Production vs Plan</span>
      <span class="dash-card-badge">Jul 2026 — Week 3</span>
    </div>
    <div class="chart-placeholder">
      <div class="chart-bars">
        <div class="chart-bar-group"><div class="chart-bar planned" style="height:80px;"></div><div class="chart-bar actual" style="height:72px;"></div><div class="bar-label">Mon</div></div>
        <div class="chart-bar-group"><div class="chart-bar planned" style="height:95px;"></div><div class="chart-bar actual" style="height:90px;"></div><div class="bar-label">Tue</div></div>
        <div class="chart-bar-group"><div class="chart-bar planned" style="height:85px;"></div><div class="chart-bar actual" style="height:60px;"></div><div class="bar-label">Wed</div></div>
        <div class="chart-bar-group"><div class="chart-bar planned" style="height:90px;"></div><div class="chart-bar actual" style="height:85px;"></div><div class="bar-label">Thu</div></div>
        <div class="chart-bar-group"><div class="chart-bar planned" style="height:75px;"></div><div class="chart-bar actual" style="height:78px;"></div><div class="bar-label">Fri</div></div>
      </div>
      <div class="chart-legend">
        <span class="legend-dot planned-dot"></span> Planned
        <span class="legend-dot actual-dot" style="margin-left:16px;"></span> Actual
      </div>
    </div>
  </div>

  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header">
      <span class="dash-card-title">Capacity Utilization by Work Center</span>
    </div>
    <div class="capacity-list">
      <div class="cap-row"><span>Assembly Line 1</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:90%; background:#ef4444;"></div></div><span class="cap-pct" style="color:#ef4444;">90%</span></div>
      <div class="cap-row"><span>CNC Machining</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:100%; background:#ef4444;"></div></div><span class="cap-pct" style="color:#ef4444;">100%</span></div>
      <div class="cap-row"><span>Painting Booth</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:69%; background:#f59e0b;"></div></div><span class="cap-pct">69%</span></div>
      <div class="cap-row"><span>Packaging</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:25%; background:#22c55e;"></div></div><span class="cap-pct">25%</span></div>
    </div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header">
      <span class="dash-card-title">Pending Approvals</span>
      <a href="#" style="font-size:12px; color:var(--brand-yellow); text-decoration:none;">View All</a>
    </div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Plan ID</th><th>Product</th><th>Requested By</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>PP-2026-005</td><td>Steel Cabinet Frame</td><td>Ahmed</td><td><span class="status-badge status-pending">Pending</span></td></tr>
          <tr><td>PP-2026-006</td><td>Powder Coated Sheet</td><td>Khalid</td><td><span class="status-badge status-pending">Pending</span></td></tr>
          <tr><td>PP-2026-003</td><td>Leather Sofa Cover</td><td>Admin</td><td><span class="status-badge status-rejected">Rejected</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header">
      <span class="dash-card-title">Top 5 MRP Shortages</span>
      <a href="#" style="font-size:12px; color:var(--brand-yellow); text-decoration:none;">Run MRP</a>
    </div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Item Code</th><th>Description</th><th>Shortage Qty</th></tr></thead>
        <tbody>
          <tr><td>RM-STL-001</td><td>Steel Sheet 2mm</td><td><span style="color:#ef4444; font-weight:600;">−250 kg</span></td></tr>
          <tr><td>RM-WD-003</td><td>Teak Wood Board</td><td><span style="color:#ef4444; font-weight:600;">−80 Pcs</span></td></tr>
          <tr><td>RM-LTH-007</td><td>Leather Hide Grade A</td><td><span style="color:#ef4444; font-weight:600;">−30 m²</span></td></tr>
          <tr><td>RM-PNT-002</td><td>Primer Coat Paint</td><td><span style="color:#f59e0b; font-weight:600;">−12 L</span></td></tr>
          <tr><td>RM-SCR-010</td><td>Hex Screw M8</td><td><span style="color:#f59e0b; font-weight:600;">−500 Pcs</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>"""


# ─────────────────────────────────────────────
# WORK ORDER DASHBOARD HTML
# ─────────────────────────────────────────────
WO_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">24</div><div class="kpi-label">Open Work Orders</div></div>
    <div class="kpi-trend up">↑ 4 since yesterday</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">8</div><div class="kpi-label">Completed Today</div></div>
    <div class="kpi-trend up">↑ 2 vs yesterday</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">3</div><div class="kpi-label">Overdue Work Orders</div></div>
    <div class="kpi-trend down">↑ 1 since last check</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">91%</div><div class="kpi-label">On-Time Completion Rate</div></div>
    <div class="kpi-trend up">↑ 3% vs last month</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header">
      <span class="dash-card-title">Work Orders by Status</span>
      <span class="dash-card-badge">Today</span>
    </div>
    <div style="display:flex; gap:24px; align-items:center; padding: 8px 0 16px;">
      <div style="flex:1;">
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div class="cap-row"><span style="width:120px;">In Progress</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:60%; background:#f59e0b;"></div></div><span class="cap-pct">14</span></div>
          <div class="cap-row"><span style="width:120px;">Released</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:20%; background:#3b82f6;"></div></div><span class="cap-pct">5</span></div>
          <div class="cap-row"><span style="width:120px;">Draft</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:20%; background:#94a3b8;"></div></div><span class="cap-pct">5</span></div>
          <div class="cap-row"><span style="width:120px;">Completed</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:35%; background:#22c55e;"></div></div><span class="cap-pct">8</span></div>
          <div class="cap-row"><span style="width:120px;">Overdue</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:12%; background:#ef4444;"></div></div><span class="cap-pct">3</span></div>
        </div>
      </div>
    </div>
  </div>

  <div class="card dash-card" style="flex:2;">
    <div class="dash-card-header">
      <span class="dash-card-title">Active Work Orders</span>
      <a href="#" style="font-size:12px; color:var(--brand-yellow); text-decoration:none;">View All</a>
    </div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>WO Number</th><th>Finished Good</th><th>Qty / Completed</th><th>Due Date</th><th>Status</th></tr></thead>
        <tbody>
          <tr>
            <td style="font-weight:600;">WO-2026-0412</td><td>Wooden Chair</td>
            <td><span style="font-weight:600;">142</span> / 200</td>
            <td>2026-07-25</td>
            <td><span class="status-badge status-inprogress">In Progress</span></td>
          </tr>
          <tr>
            <td style="font-weight:600;">WO-2026-0408</td><td>Steel Shelf Unit</td>
            <td><span style="font-weight:600;">45</span> / 150</td>
            <td style="color:#ef4444; font-weight:600;">2026-07-22 ⚠</td>
            <td><span class="status-badge status-overloaded">Overdue</span></td>
          </tr>
          <tr>
            <td style="font-weight:600;">WO-2026-0413</td><td>Powder Coated Frame</td>
            <td>0 / 300</td>
            <td>2026-07-28</td>
            <td><span class="status-badge status-approved">Released</span></td>
          </tr>
          <tr>
            <td style="font-weight:600;">WO-2026-0410</td><td>Leather Sofa Cover</td>
            <td>0 / 60</td>
            <td>2026-07-30</td>
            <td><span class="status-badge status-draft">Draft</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header">
      <span class="dash-card-title">Pending Release Queue</span>
      <a href="#" style="font-size:12px; color:var(--brand-yellow); text-decoration:none;">Release All</a>
    </div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>WO Number</th><th>Product</th><th>BOM</th><th>Material</th></tr></thead>
        <tbody>
          <tr><td>WO-2026-0413</td><td>Powder Coated Frame</td><td style="color:#22c55e;">✔</td><td style="color:#22c55e;">✔</td></tr>
          <tr><td>WO-2026-0414</td><td>Steel Shelf Unit</td><td style="color:#22c55e;">✔</td><td style="color:#f59e0b;">⚠ Partial</td></tr>
          <tr><td>WO-2026-0415</td><td>Oak Wood Panel</td><td style="color:#ef4444;">✖</td><td style="color:#ef4444;">✖</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header">
      <span class="dash-card-title">Output by Work Center (Today)</span>
    </div>
    <div style="display:flex; flex-direction:column; gap:12px;">
      <div class="cap-row"><span>Assembly Line 1</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:85%; background:#f59e0b;"></div></div><span class="cap-pct">142</span></div>
      <div class="cap-row"><span>CNC Machining</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:100%; background:#3b82f6;"></div></div><span class="cap-pct">200</span></div>
      <div class="cap-row"><span>Welding Bay</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:30%; background:#f59e0b;"></div></div><span class="cap-pct">45</span></div>
      <div class="cap-row"><span>Painting Booth</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:0%; background:#94a3b8;"></div></div><span class="cap-pct">0</span></div>
    </div>
  </div>
</div>
"""

# ─────────────────────────────────────────────
# WORK ORDER FORM HTML (Create / Edit)
# ─────────────────────────────────────────────
def build_wo_form_html(mode="create"):
    title = "Create New Work Order" if mode == "create" else "Edit Work Order — WO-2026-0412"
    header_note = "" if mode == "create" else '<span class="status-badge status-inprogress" style="margin-left:12px;">In Progress</span>'
    pre = {
        "wo_no":     "" if mode == "create" else "WO-2026-0412",
        "product":   "" if mode == "create" else "Wooden Chair",
        "bom":       "" if mode == "create" else "BOM-001",
        "routing":   "" if mode == "create" else "RT-CHAIR-001",
        "qty":       "" if mode == "create" else "200",
        "start":     "" if mode == "create" else "2026-07-18",
        "due":       "" if mode == "create" else "2026-07-25",
        "wc":        "" if mode == "create" else "Assembly Line 1",
        "priority":  "High",
        "notes":     "" if mode == "create" else "Expedite – customer PO pending.",
    }
    return f"""
<div class="wo-form-wrapper">
  <!-- Form Header -->
  <div class="form-header-bar">
    <div>
      <h2 style="margin:0; font-size:16px; font-weight:700; color:#0f172a;">{title} {header_note}</h2>
      <div class="breadcrumbs" style="margin-top:4px; padding:0;">
        <span style="color:#94a3b8; font-size:12px;">Work Orders &rsaquo; Work Order List &rsaquo; {"New" if mode=="create" else "WO-2026-0412"}</span>
      </div>
    </div>
    <div style="display:flex; gap:10px;">
      <button class="btn btn-outline">Cancel</button>
      <button class="btn btn-outline">Save as Draft</button>
      <button class="btn btn-primary">{"Create &amp; Release" if mode=="create" else "Save Changes"}</button>
    </div>
  </div>

  <!-- Section 1: General Information -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
      General Information
    </div>
    <div class="form-grid">
      <div class="form-group">
        <label>Work Order #</label>
        <input type="text" value="{pre['wo_no']}" placeholder="Auto-generated" {"readonly" if mode=="edit" else ""}>
      </div>
      <div class="form-group">
        <label>Finished Good <span class="req">*</span></label>
        <input type="text" value="{pre['product']}" placeholder="Select item...">
      </div>
      <div class="form-group">
        <label>BOM Reference <span class="req">*</span></label>
        <input type="text" value="{pre['bom']}" placeholder="Select BOM...">
      </div>
      <div class="form-group">
        <label>Routing</label>
        <input type="text" value="{pre['routing']}" placeholder="Select routing...">
      </div>
      <div class="form-group">
        <label>Order Quantity <span class="req">*</span></label>
        <input type="number" value="{pre['qty']}" placeholder="0">
      </div>
      <div class="form-group">
        <label>Unit of Measure</label>
        <select><option selected>Pcs</option><option>Kg</option><option>Ltr</option><option>Set</option></select>
      </div>
      <div class="form-group">
        <label>Planned Start Date <span class="req">*</span></label>
        <input type="date" value="{pre['start']}">
      </div>
      <div class="form-group">
        <label>Due Date <span class="req">*</span></label>
        <input type="date" value="{pre['due']}">
      </div>
      <div class="form-group">
        <label>Work Center <span class="req">*</span></label>
        <input type="text" value="{pre['wc']}" placeholder="Select work center...">
      </div>
      <div class="form-group">
        <label>Priority</label>
        <select>
          <option {"selected" if pre['priority']=="High" else ""}>High</option>
          <option {"selected" if pre['priority']=="Medium" else ""}>Medium</option>
          <option {"selected" if pre['priority']=="Low" else ""}>Low</option>
        </select>
      </div>
      <div class="form-group">
        <label>Production Plan Reference</label>
        <input type="text" value="" placeholder="Link to plan...">
      </div>
      <div class="form-group">
        <label>Sales Order Reference</label>
        <input type="text" value="" placeholder="SO-2026-...">
      </div>
    </div>
  </div>

  <!-- Section 2: BOM Components (Readonly Preview) -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"></path></svg>
      Bill of Materials — Components
    </div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Component Code</th><th>Description</th><th>Required Qty</th><th>UoM</th><th>On-Hand Stock</th><th>Availability</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>RM-WD-003</td><td>Teak Wood Board</td><td>4.0</td><td>Pcs</td><td>12</td><td><span class="status-badge status-active">✔ Available</span></td></tr>
          <tr><td>2</td><td>RM-STL-001</td><td>Steel Bracket Set</td><td>1.0</td><td>Set</td><td>8</td><td><span class="status-badge status-active">✔ Available</span></td></tr>
          <tr><td>3</td><td>RM-SCR-010</td><td>Hex Screw M8</td><td>16.0</td><td>Pcs</td><td>50</td><td><span class="status-badge status-active">✔ Available</span></td></tr>
          <tr><td>4</td><td>RM-PNT-002</td><td>Primer Coat Paint</td><td>0.5</td><td>Ltr</td><td>2</td><td><span class="status-badge status-pending">⚠ Partial</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Section 3: Routing / Operations -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
      Routing — Operations Sequence
    </div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Seq</th><th>Operation</th><th>Work Center</th><th>Setup Time</th><th>Machine Time</th><th>Labor Time</th></tr></thead>
        <tbody>
          <tr><td>10</td><td>Cutting</td><td>CNC Machining</td><td>15 min</td><td>30 min</td><td>20 min</td></tr>
          <tr><td>20</td><td>Assembly</td><td>Assembly Line 1</td><td>10 min</td><td>45 min</td><td>45 min</td></tr>
          <tr><td>30</td><td>Painting</td><td>Painting Booth</td><td>20 min</td><td>60 min</td><td>30 min</td></tr>
          <tr><td>40</td><td>QC Inspection</td><td>QC Station</td><td>5 min</td><td>—</td><td>15 min</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Section 4: Notes & Attachments -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
      Notes &amp; Attachments
    </div>
    <div class="form-grid" style="grid-template-columns:1fr;">
      <div class="form-group">
        <label>Internal Notes</label>
        <textarea rows="3" placeholder="Add production notes...">{pre['notes']}</textarea>
      </div>
    </div>
    <div class="attachment-zone">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" style="color:#94a3b8;"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
      <span style="color:#64748b; font-size:13px;">Drop files here or <a href="#" style="color:var(--brand-yellow);">Browse</a></span>
    </div>
  </div>

  <!-- Form Footer -->
  <div class="form-footer">
    <div style="font-size:12px; color:#94a3b8;">
      {"" if mode=="create" else "Created by <b>Admin</b> on 2026-07-18 &nbsp;|&nbsp; Modified by <b>Admin</b> on 2026-07-22"}
    </div>
    <div style="display:flex; gap:10px;">
      <button class="btn btn-outline">Cancel</button>
      <button class="btn btn-outline">Save as Draft</button>
      <button class="btn btn-primary">{"Create &amp; Release" if mode=="create" else "Save Changes"}</button>
    </div>
  </div>
</div>
"""

# ─────────────────────────────────────────────
# WORK ORDER DETAIL VIEW HTML
# ─────────────────────────────────────────────
WO_DETAIL_HTML = """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div>
      <h2 style="margin:0; font-size:16px; font-weight:700; color:#0f172a;">
        Work Order — WO-2026-0412
        <span class="status-badge status-inprogress" style="margin-left:12px; font-size:12px;">In Progress</span>
      </h2>
      <div style="color:#94a3b8; font-size:12px; margin-top:4px;">Work Orders &rsaquo; Work Order List &rsaquo; WO-2026-0412</div>
    </div>
    <div style="display:flex; gap:10px;">
      <button class="btn btn-outline">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        Edit
      </button>
      <button class="btn btn-outline">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        Print
      </button>
      <button class="btn btn-primary">Close Work Order</button>
    </div>
  </div>

  <!-- Header Summary Cards -->
  <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:16px;">
    <div class="card" style="padding:16px;">
      <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px;">Finished Good</div>
      <div style="font-size:15px; font-weight:700; color:#0f172a;">Wooden Chair</div>
      <div style="font-size:12px; color:#94a3b8; margin-top:2px;">BOM-001 | RT-CHAIR-001</div>
    </div>
    <div class="card" style="padding:16px;">
      <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px;">Quantity Progress</div>
      <div style="font-size:15px; font-weight:700; color:#0f172a;">142 <span style="color:#94a3b8; font-weight:400;">/ 200 Pcs</span></div>
      <div style="background:#f1f5f9; border-radius:999px; height:6px; margin-top:8px;"><div style="width:71%; background:var(--brand-yellow); height:100%; border-radius:999px;"></div></div>
    </div>
    <div class="card" style="padding:16px;">
      <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px;">Timeline</div>
      <div style="font-size:13px; font-weight:600; color:#0f172a;">2026-07-18 → 2026-07-25</div>
      <div style="font-size:12px; color:#f59e0b; margin-top:2px;">⚠ 3 days remaining</div>
    </div>
    <div class="card" style="padding:16px;">
      <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px;">Work Center</div>
      <div style="font-size:15px; font-weight:700; color:#0f172a;">Assembly Line 1</div>
      <div style="font-size:12px; color:#94a3b8; margin-top:2px;">Priority: <span style="color:#ef4444; font-weight:600;">High</span></div>
    </div>
  </div>

  <!-- Operation Progress -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
      Operation Progress
    </div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Seq</th><th>Operation</th><th>Work Center</th><th>Operator</th><th>Start</th><th>End</th><th>Qty Confirmed</th><th>Progress</th><th>Status</th></tr></thead>
        <tbody>
          <tr>
            <td>10</td><td>Cutting</td><td>CNC Machining</td><td>Ahmed K.</td><td>07:00 AM</td><td>09:30 AM</td><td>200</td>
            <td><div style="display:flex; align-items:center; gap:6px;"><div style="width:60px; background:#f1f5f9; border-radius:999px; height:6px;"><div style="width:100%; background:#22c55e; height:100%; border-radius:999px;"></div></div><span>100%</span></div></td>
            <td><span class="status-badge status-completed">Completed</span></td>
          </tr>
          <tr>
            <td>20</td><td>Assembly</td><td>Assembly Line 1</td><td>Khalid M.</td><td>10:00 AM</td><td>—</td><td>142</td>
            <td><div style="display:flex; align-items:center; gap:6px;"><div style="width:60px; background:#f1f5f9; border-radius:999px; height:6px;"><div style="width:71%; background:#f59e0b; height:100%; border-radius:999px;"></div></div><span>71%</span></div></td>
            <td><span class="status-badge status-inprogress">In Progress</span></td>
          </tr>
          <tr>
            <td>30</td><td>Painting</td><td>Painting Booth</td><td>—</td><td>—</td><td>—</td><td>0</td>
            <td><div style="display:flex; align-items:center; gap:6px;"><div style="width:60px; background:#f1f5f9; border-radius:999px; height:6px;"><div style="width:0%; background:#94a3b8; height:100%; border-radius:999px;"></div></div><span>0%</span></div></td>
            <td><span class="status-badge status-draft">Pending</span></td>
          </tr>
          <tr>
            <td>40</td><td>QC Inspection</td><td>QC Station</td><td>—</td><td>—</td><td>—</td><td>0</td>
            <td><div style="display:flex; align-items:center; gap:6px;"><div style="width:60px; background:#f1f5f9; border-radius:999px; height:6px;"><div style="width:0%; background:#94a3b8; height:100%; border-radius:999px;"></div></div><span>0%</span></div></td>
            <td><span class="status-badge status-draft">Pending</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Material Consumption -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"></path></svg>
      Material Consumption
    </div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Component</th><th>Required Qty</th><th>Issued Qty</th><th>Consumed Qty</th><th>Balance</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>Teak Wood Board</td><td>800 Pcs</td><td>800</td><td>568</td><td>232</td><td><span class="status-badge status-inprogress">Partial</span></td></tr>
          <tr><td>Steel Bracket Set</td><td>200 Set</td><td>200</td><td>142</td><td>58</td><td><span class="status-badge status-inprogress">Partial</span></td></tr>
          <tr><td>Hex Screw M8</td><td>3200 Pcs</td><td>3200</td><td>2272</td><td>928</td><td><span class="status-badge status-inprogress">Partial</span></td></tr>
          <tr><td>Primer Coat Paint</td><td>100 Ltr</td><td>0</td><td>0</td><td>—</td><td><span class="status-badge status-draft">Not Issued</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Audit Trail -->
  <div class="form-section card">
    <div class="form-section-title">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
      Activity Log
    </div>
    <div style="display:flex; flex-direction:column; gap:12px; padding:4px 0;">
      <div style="display:flex; gap:12px; align-items:flex-start;">
        <div style="width:36px; height:36px; border-radius:50%; background:#dbeafe; color:#2563eb; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">AK</div>
        <div><div style="font-size:13px; font-weight:600; color:#0f172a;">Work Order Released</div><div style="font-size:12px; color:#64748b;">Released by <b>Admin</b> on 2026-07-18 08:00 AM</div></div>
      </div>
      <div style="display:flex; gap:12px; align-items:flex-start;">
        <div style="width:36px; height:36px; border-radius:50%; background:#dcfce7; color:#16a34a; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">AH</div>
        <div><div style="font-size:13px; font-weight:600; color:#0f172a;">Operation 10 Completed</div><div style="font-size:12px; color:#64748b;">Confirmed by <b>Ahmed K.</b> on 2026-07-18 09:30 AM — 200 Pcs</div></div>
      </div>
      <div style="display:flex; gap:12px; align-items:flex-start;">
        <div style="width:36px; height:36px; border-radius:50%; background:#fff7ed; color:#ea580c; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">KM</div>
        <div><div style="font-size:13px; font-weight:600; color:#0f172a;">Operation 20 Started</div><div style="font-size:12px; color:#64748b;">Started by <b>Khalid M.</b> on 2026-07-18 10:00 AM</div></div>
      </div>
    </div>
  </div>

  <div class="form-footer">
    <div style="font-size:12px; color:#94a3b8;">Created by <b>Admin</b> on 2026-07-17 &nbsp;|&nbsp; Modified by <b>Ahmed K.</b> on 2026-07-22 09:30 AM</div>
    <div style="display:flex; gap:10px;">
      <button class="btn btn-outline">Print Work Order</button>
      <button class="btn btn-primary">Close Work Order</button>
    </div>
  </div>
</div>
"""




# ═══════════════════════════════════════════════════════════
# ANALYTICS & REPORTING HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

AR_EXEC_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">SAR 4.2M</div><div class="kpi-label">Monthly Plant Output Value</div></div>
    <div class="kpi-trend up">↑ 6.4% vs target</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 7 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 7 22 7 22 12"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">84.2%</div><div class="kpi-label">Overall Plant OEE</div></div>
    <div class="kpi-trend up">↑ 1.8% vs last month</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">94.7%</div><div class="kpi-label">First Pass Quality Yield</div></div>
    <div class="kpi-trend up">↑ 0.5% vs target</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">98.1%</div><div class="kpi-label">On-Time Order Delivery</div></div>
    <div class="kpi-trend up">↑ 98% SLA met</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Plant Performance Summary by Department</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Department / Area</th><th>Plan Target</th><th>Actual Output</th><th>OEE %</th><th>Scrap %</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">Wood Machining &amp; CNC</td><td>1,200 Pcs</td><td style="color:#22c55e;font-weight:600;">1,240 Pcs</td><td>88.5%</td><td>1.2%</td><td><span class="status-badge status-active">On Track</span></td></tr>
          <tr><td style="font-weight:600;">Metal Assembly &amp; Welding</td><td>800 Pcs</td><td style="color:#22c55e;font-weight:600;">815 Pcs</td><td>82.1%</td><td>0.8%</td><td><span class="status-badge status-active">On Track</span></td></tr>
          <tr><td style="font-weight:600;">Automated Paint Line</td><td>1,500 Pcs</td><td style="color:#ef4444;font-weight:600;">1,380 Pcs</td><td>76.4%</td><td>2.4%</td><td><span class="status-badge status-pending">Attention</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Cost Breakdown Overview</span></div>
    <div class="capacity-list" style="margin-top:8px;">
      <div class="cap-row"><span style="width:130px;">Raw Materials</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:60%;background:#3b82f6;"></div></div><span class="cap-pct">60%</span></div>
      <div class="cap-row"><span style="width:130px;">Direct Labor</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:22%;background:#22c55e;"></div></div><span class="cap-pct">22%</span></div>
      <div class="cap-row"><span style="width:130px;">Machinery &amp; Power</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:12%;background:#f59e0b;"></div></div><span class="cap-pct">12%</span></div>
      <div class="cap-row"><span style="width:130px;">Factory Overheads</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:6%;background:#8b5cf6;"></div></div><span class="cap-pct">6%</span></div>
    </div>
  </div>
</div>
"""


# ═══════════════════════════════════════════════════════════
# PRODUCTION COSTING HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

PC_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">SAR 1.84M</div><div class="kpi-label">Total Production Cost (Jul)</div></div>
    <div class="kpi-trend up">↓ 2.4% below standard budget</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">62%</div><div class="kpi-label">Material Cost Share</div></div>
    <div class="kpi-trend neutral">→ SAR 1.14M direct materials</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">21%</div><div class="kpi-label">Direct Labor Share</div></div>
    <div class="kpi-trend up">↑ Efficiency factor 94%</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">−SAR 42.5K</div><div class="kpi-label">Net Cost Variance (Favorable)</div></div>
    <div class="kpi-trend up">↑ Savings across 14 Work Orders</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Standard vs Actual Unit Cost Comparison</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Product Name</th><th>Standard Cost (SAR)</th><th>Actual Cost (SAR)</th><th>Variance / Unit</th><th>Total Production</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">Wooden Chair Assembly</td><td>SAR 258.00</td><td style="color:#22c55e;font-weight:600;">SAR 248.00</td><td style="color:#22c55e;font-weight:700;">−SAR 10.00 (−3.9%)</td><td>500 Pcs</td><td><span class="status-badge status-active">Favorable</span></td></tr>
          <tr><td style="font-weight:600;">Metal Desk Frame</td><td>SAR 480.00</td><td style="color:#22c55e;font-weight:600;">SAR 470.67</td><td style="color:#22c55e;font-weight:700;">−SAR 9.33 (−1.9%)</td><td>200 Pcs</td><td><span class="status-badge status-active">Favorable</span></td></tr>
          <tr><td style="font-weight:600;">Leather Sofa Cover</td><td>SAR 612.00</td><td style="color:#ef4444;font-weight:600;">SAR 645.00</td><td style="color:#ef4444;font-weight:700;">+SAR 33.00 (+5.4%)</td><td>150 Pcs</td><td><span class="status-badge status-rejected">Unfavorable</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Cost Element Distribution</span></div>
    <div class="capacity-list" style="margin-top:8px;">
      <div class="cap-row"><span style="width:130px;">Direct Material</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:62%;background:#3b82f6;"></div></div><span class="cap-pct">62%</span></div>
      <div class="cap-row"><span style="width:130px;">Direct Labor</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:21%;background:#22c55e;"></div></div><span class="cap-pct">21%</span></div>
      <div class="cap-row"><span style="width:130px;">Machine Overhead</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:11%;background:#f59e0b;"></div></div><span class="cap-pct">11%</span></div>
      <div class="cap-row"><span style="width:130px;">Factory Overhead</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:6%;background:#8b5cf6;"></div></div><span class="cap-pct">6%</span></div>
    </div>
  </div>
</div>
"""

def build_pc_form(form_type):
    if form_type == "rollup":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Standard Cost Rollup Run — CR-2026-Q3</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Production Costing &rsaquo; Cost Rollup</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Execute Cost Rollup</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Cost Rollup Parameters</div>
    <div class="form-grid">
      <div class="form-group"><label>Run Reference</label><input type="text" value="CR-2026-Q3" readonly></div>
      <div class="form-group"><label>Costing Version <span class="req">*</span></label><select><option>Standard Cost 2026 Q3</option><option>Budget Cost 2026</option></select></div>
      <div class="form-group"><label>Plant / Valuation Area <span class="req">*</span></label><select><option>Plant 1 — Main Facility</option></select></div>
      <div class="form-group"><label>Effective From Date <span class="req">*</span></label><input type="date" value="2026-07-01"></div>
      <div class="form-group"><label>Include Sub-Assemblies?</label><select><option>Yes — Multi-Level Rollup</option><option>Single Level Only</option></select></div>
      <div class="form-group"><label>Overhead Rate Master</label><select><option>Standard Overhead Rates 2026</option></select></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Products Included in Rollup</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Item Code</th><th>Item Name</th><th>Current Std Cost (SAR)</th><th>Calculated Rollup Cost (SAR)</th><th>Delta (SAR)</th><th>Delta %</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>FG-CH-001</td><td>Wooden Chair Assembly</td><td>262.00</td><td><b style="color:#22c55e;">258.00</b></td><td>−4.00</td><td>−1.5%</td><td><span class="status-badge status-active">Ready</span></td></tr>
          <tr><td>FG-DK-002</td><td>Metal Desk Frame</td><td>472.00</td><td><b style="color:#ef4444;">480.00</b></td><td>+8.00</td><td>+1.7%</td><td><span class="status-badge status-active">Ready</span></td></tr>
          <tr><td>FG-SF-003</td><td>Leather Sofa Cover</td><td>600.00</td><td><b style="color:#ef4444;">612.00</b></td><td>+12.00</td><td>+2.0%</td><td><span class="status-badge status-active">Ready</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Executing cost rollup will update standard prices in Item Master and BOM Costing tables.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Execute Cost Rollup</button></div>
  </div>
</div>"""
    return ""


# ═══════════════════════════════════════════════════════════
# SUBCONTRACTING HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

SUB_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">4</div><div class="kpi-label">Active Subcontract Vendors</div></div>
    <div class="kpi-trend up">↑ All qualified</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">6</div><div class="kpi-label">Orders at Vendor</div></div>
    <div class="kpi-trend neutral">→ 530 Pcs total in transit/process</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">SAR 18.5K</div><div class="kpi-label">Subcontract Spend (Jul)</div></div>
    <div class="kpi-trend up">↓ 14% lower than budget</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">95.4%</div><div class="kpi-label">Vendor Quality Score</div></div>
    <div class="kpi-trend up">↑ 2.1% improvement</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Active Subcontract Orders (SCO)</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>SCO Number</th><th>Vendor</th><th>Operation</th><th>Dispatched Qty</th><th>Returned Qty</th><th>Target Date</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">SCO-2026-042</td><td>Advanced Powder Coating</td><td>Powder Coating</td><td>300 Pcs</td><td>285 Pcs</td><td>2026-07-23</td><td><span class="status-badge status-inprogress">In Progress</span></td></tr>
          <tr><td style="font-weight:600;">SCO-2026-041</td><td>Gulf Electroplating Ltd</td><td>Chrome Plating</td><td>150 Pcs</td><td>150 Pcs</td><td>2026-07-19</td><td><span class="status-badge status-completed">Completed</span></td></tr>
          <tr><td style="font-weight:600;">SCO-2026-040</td><td>Riyadh Heat Treatment Co.</td><td>Heat Treatment</td><td>80 Pcs</td><td>0 Pcs</td><td>2026-07-15</td><td><span class="status-badge status-overloaded">Delayed (+7d)</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Outsourced Operations Breakdown</span></div>
    <div class="capacity-list" style="margin-top:8px;">
      <div class="cap-row"><span style="width:130px;">Powder Coating</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:55%;background:#3b82f6;"></div></div><span class="cap-pct">55%</span></div>
      <div class="cap-row"><span style="width:130px;">Plating / Anodizing</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:25%;background:#22c55e;"></div></div><span class="cap-pct">25%</span></div>
      <div class="cap-row"><span style="width:130px;">Heat Treatment</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:15%;background:#f59e0b;"></div></div><span class="cap-pct">15%</span></div>
      <div class="cap-row"><span style="width:130px;">Laser Cutting</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:5%;background:#8b5cf6;"></div></div><span class="cap-pct">5%</span></div>
    </div>
  </div>
</div>
"""

def build_sub_form(form_type):
    if form_type == "order":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Create Subcontract Order — SCO-2026-043</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Subcontracting &rsaquo; Subcontract Order</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Create Order</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Order Details</div>
    <div class="form-grid">
      <div class="form-group"><label>SCO Reference</label><input type="text" value="SCO-2026-043" readonly></div>
      <div class="form-group"><label>Subcontract Vendor <span class="req">*</span></label><select><option>Advanced Powder Coating</option><option>Gulf Electroplating Ltd</option><option>Riyadh Heat Treatment Co.</option></select></div>
      <div class="form-group"><label>Linked Work Order</label><input type="text" value="WO-2026-0412"></div>
      <div class="form-group"><label>Outsourced Operation <span class="req">*</span></label><select><option>Powder Coating</option><option>Chrome Plating</option><option>Heat Treatment</option><option>Laser Cutting</option></select></div>
      <div class="form-group"><label>Order Date</label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Expected Return Date <span class="req">*</span></label><input type="date" value="2026-07-27"></div>
      <div class="form-group"><label>Unit Service Cost (SAR) <span class="req">*</span></label><input type="number" value="15.00"></div>
      <div class="form-group"><label>Total Service Value (SAR)</label><input type="text" value="SAR 3,000.00" readonly style="background:#f8fafc;font-weight:700;"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Components / Raw Materials Supplied to Vendor</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th>Required Qty</th><th>Dispatched Qty</th><th>UoM</th><th>Source Warehouse</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>FG-CH-001-RAW</td><td>Wooden Chair Unfinished Frame</td><td>200</td><td><input type="number" value="200" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Pcs</td><td>WH-03 WIP Staging</td></tr>
          <tr><td>2</td><td>RM-PNT-002</td><td>Primer Coat Paint (Consumable)</td><td>10</td><td><input type="number" value="10" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Ltr</td><td>WH-01 Raw Material</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Subcontract Order will issue material to Vendor Stock Location upon dispatch.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Create Order</button></div>
  </div>
</div>"""
    elif form_type == "issue":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Material Issue to Vendor — MIV-2026-022</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Subcontracting &rsaquo; Material Issue to Vendor</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Dispatch</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Dispatch Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Dispatch Reference</label><input type="text" value="MIV-2026-022" readonly></div>
      <div class="form-group"><label>SCO Reference <span class="req">*</span></label><input type="text" value="SCO-2026-043"></div>
      <div class="form-group"><label>Vendor</label><input type="text" value="Advanced Powder Coating" readonly></div>
      <div class="form-group"><label>Dispatch Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Transporter / Driver</label><input type="text" value="Saudi Logistics Co. / Driver Ali"></div>
      <div class="form-group"><label>Vehicle / Gate Pass No</label><input type="text" value="GP-2026-9901"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Dispatched Items</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Item Code</th><th>Item Name</th><th>Order Qty</th><th>Dispatch Qty</th><th>UoM</th><th>Source Location</th><th>Target Vendor Stock</th></tr></thead>
        <tbody>
          <tr><td>FG-CH-001-RAW</td><td>Wooden Chair Unfinished Frame</td><td>200</td><td><input type="number" value="200" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Pcs</td><td>WH-03 WIP Staging</td><td>VND-LOC-APC</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Inventory will be moved to Vendor Subcontract Location.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Dispatch</button></div>
  </div>
</div>"""
    elif form_type == "receipt":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Material Receipt from Vendor — MRV-2026-019</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Subcontracting &rsaquo; Material Receipt from Vendor</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Accept &amp; Receive</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Receipt Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Receipt Reference</label><input type="text" value="MRV-2026-019" readonly></div>
      <div class="form-group"><label>SCO Reference <span class="req">*</span></label><input type="text" value="SCO-2026-042"></div>
      <div class="form-group"><label>Vendor</label><input type="text" value="Advanced Powder Coating" readonly></div>
      <div class="form-group"><label>Receipt Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Delivery Note No</label><input type="text" value="DN-APC-4412"></div>
      <div class="form-group"><label>Target Warehouse <span class="req">*</span></label><select><option>WH-02 Finished Goods</option><option>WH-03 WIP Staging</option></select></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Received Items &amp; QC Check</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Item Code</th><th>Item Name</th><th>Dispatched Qty</th><th>Received Qty</th><th>Accepted Qty</th><th>Rejected Qty</th><th>Scrap / Loss Qty</th><th>QC Status</th></tr></thead>
        <tbody>
          <tr><td>FG-CH-001</td><td>Wooden Chair Powder Coated</td><td>300 Pcs</td><td><input type="number" value="300" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="number" value="285" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td style="color:#ef4444;font-weight:600;">10</td><td style="color:#f59e0b;font-weight:600;">5</td><td><span class="status-badge status-active">QC Passed (285)</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Receipt will update inventory, post vendor service cost, and clear vendor stock ledger.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Accept &amp; Receive</button></div>
  </div>
</div>"""
    return ""


# ═══════════════════════════════════════════════════════════
# MAINTENANCE MANAGEMENT HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

MNT_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">12</div><div class="kpi-label">Active Work Orders</div></div>
    <div class="kpi-trend up">↑ 3 new today</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">96.4%</div><div class="kpi-label">PM Compliance Rate</div></div>
    <div class="kpi-trend up">↑ 2.1% vs last month</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">2.4h</div><div class="kpi-label">Mean Time to Repair (MTTR)</div></div>
    <div class="kpi-trend up">↓ 0.5h faster than target</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">740h</div><div class="kpi-label">Mean Time Between Failures</div></div>
    <div class="kpi-trend up">↑ 45h improvement</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Live Equipment Status</span><span class="dash-card-badge">8 Machinery Units</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Equipment Name</th><th>Asset Tag</th><th>Location</th><th>Operating Hrs</th><th>Health Score</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">CNC Machining Center #1</td><td>AST-CNC-001</td><td>Plant 1 — Shop Floor</td><td>4,250h</td><td><b style="color:#22c55e;">94%</b></td><td><span class="status-badge status-active">Running</span></td></tr>
          <tr><td style="font-weight:600;">Automated Spray Paint Booth</td><td>AST-PNT-001</td><td>Plant 1 — Block B</td><td>2,890h</td><td><b style="color:#ef4444;">48%</b></td><td><span class="status-badge status-rejected">Breakdown</span></td></tr>
          <tr><td style="font-weight:600;">Robotic Welding Cell #1</td><td>AST-WLD-003</td><td>Plant 1 — Shop Floor</td><td>1,600h</td><td><b style="color:#22c55e;">98%</b></td><td><span class="status-badge status-active">Running</span></td></tr>
          <tr><td style="font-weight:600;">Air Compressor 50HP</td><td>AST-CMP-004</td><td>Utility Building</td><td>12,400h</td><td><b style="color:#f59e0b;">81%</b></td><td><span class="status-badge status-inprogress">PM Scheduled</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Maintenance Work Orders</span><span class="dash-card-badge">Current Week</span></div>
    <div class="capacity-list" style="margin-top:8px;">
      <div class="cap-row"><span style="width:110px;">Preventive (PM)</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:65%;background:#3b82f6;"></div></div><span class="cap-pct">18</span></div>
      <div class="cap-row"><span style="width:110px;">Breakdown</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:25%;background:#ef4444;"></div></div><span class="cap-pct">7</span></div>
      <div class="cap-row"><span style="width:110px;">Calibration</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:10%;background:#f59e0b;"></div></div><span class="cap-pct">3</span></div>
    </div>
  </div>
</div>
"""


# ═══════════════════════════════════════════════════════════
# QUALITY MANAGEMENT HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

QM_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">38</div><div class="kpi-label">Inspections Today</div></div>
    <div class="kpi-trend up">↑ 6 vs yesterday</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">94.2%</div><div class="kpi-label">First Pass Yield (FPY)</div></div>
    <div class="kpi-trend up">↑ 1.8% vs last week</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">7</div><div class="kpi-label">Open NCRs</div></div>
    <div class="kpi-trend down">↑ 2 since last week</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">4</div><div class="kpi-label">CAPAs In Progress</div></div>
    <div class="kpi-trend neutral">→ No change</div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Inspection Results — Last 7 Days</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Date</th><th>Type</th><th>Inspected</th><th>Passed</th><th>Failed</th><th>FPY %</th><th>NCRs Raised</th></tr></thead>
        <tbody>
          <tr><td>2026-07-22</td><td>IQC / IPQC / OQC</td><td>38</td><td style="color:#22c55e;font-weight:600;">36</td><td style="color:#ef4444;font-weight:600;">2</td><td><b>94.7%</b></td><td>2</td></tr>
          <tr><td>2026-07-21</td><td>IQC / IPQC</td><td>24</td><td style="color:#22c55e;font-weight:600;">22</td><td style="color:#ef4444;font-weight:600;">2</td><td><b>91.7%</b></td><td>2</td></tr>
          <tr><td>2026-07-20</td><td>OQC</td><td>15</td><td style="color:#22c55e;font-weight:600;">15</td><td style="color:#ef4444;font-weight:600;">0</td><td><b>100%</b></td><td>0</td></tr>
          <tr><td>2026-07-19</td><td>IQC</td><td>10</td><td style="color:#22c55e;font-weight:600;">9</td><td style="color:#ef4444;font-weight:600;">1</td><td><b>90.0%</b></td><td>1</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Quality by Inspection Type</span></div>
    <div class="capacity-list" style="margin-top:8px;">
      <div class="cap-row"><span style="width:80px;">IQC</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:88%;background:#3b82f6;"></div></div><span class="cap-pct">88%</span></div>
      <div class="cap-row"><span style="width:80px;">IPQC</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:94%;background:#22c55e;"></div></div><span class="cap-pct">94%</span></div>
      <div class="cap-row"><span style="width:80px;">OQC</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:98%;background:#f59e0b;"></div></div><span class="cap-pct">98%</span></div>
    </div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Open NCRs</span><span class="dash-card-badge" style="background:#fee2e2;color:#991b1b;">7 Open</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>NCR No</th><th>Item</th><th>Defect Type</th><th>Severity</th><th>Raised On</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">NCR-2026-018</td><td>Steel Sheet 2mm</td><td>Thickness Variance</td><td><span style="color:#ef4444;font-weight:600;">Critical</span></td><td>2026-07-22</td><td><span class="status-badge status-pending">Under Review</span></td></tr>
          <tr><td style="font-weight:600;">NCR-2026-017</td><td>Leather Hide</td><td>Surface Defect</td><td><span style="color:#f59e0b;font-weight:600;">Major</span></td><td>2026-07-21</td><td><span class="status-badge status-inprogress">CAPA Raised</span></td></tr>
          <tr><td style="font-weight:600;">NCR-2026-016</td><td>Primer Coat Paint</td><td>Viscosity OOS</td><td><span style="color:#f59e0b;font-weight:600;">Major</span></td><td>2026-07-20</td><td><span class="status-badge status-inprogress">CAPA Raised</span></td></tr>
          <tr><td style="font-weight:600;">NCR-2026-015</td><td>Wooden Chair</td><td>Finish Defect</td><td><span style="color:#94a3b8;font-weight:600;">Minor</span></td><td>2026-07-19</td><td><span class="status-badge status-draft">Pending Decision</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">CAPA Status</span></div>
    <div style="display:flex;flex-direction:column;gap:10px;margin-top:8px;">
      <div style="display:flex;justify-content:space-between;align-items:center;background:#f0fdf4;border-radius:8px;padding:10px 14px;">
        <span style="font-size:13px;color:#166534;font-weight:600;">Closed on Time</span><span style="font-size:20px;font-weight:700;color:#22c55e;">12</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;background:#fef9c3;border-radius:8px;padding:10px 14px;">
        <span style="font-size:13px;color:#854d0e;font-weight:600;">In Progress</span><span style="font-size:20px;font-weight:700;color:#f59e0b;">4</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;background:#fff1f2;border-radius:8px;padding:10px 14px;">
        <span style="font-size:13px;color:#991b1b;font-weight:600;">Overdue</span><span style="font-size:20px;font-weight:700;color:#ef4444;">2</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;background:#f8fafc;border-radius:8px;padding:10px 14px;">
        <span style="font-size:13px;color:#64748b;font-weight:600;">Pending Root Cause</span><span style="font-size:20px;font-weight:700;color:#94a3b8;">3</span>
      </div>
    </div>
  </div>
</div>
"""

def build_qm_form(form_type):
    if form_type == "iqc":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Incoming Quality Control — IQC-2026-055 <span class="status-badge status-inprogress" style="margin-left:8px;">In Inspection</span></h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Quality Management &rsaquo; Incoming QC (IQC)</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline" style="border-color:#ef4444;color:#ef4444;">Reject Lot</button><button class="btn btn-outline">Put on Hold</button><button class="btn btn-primary">Accept Lot</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>Inspection Header</div>
    <div class="form-grid">
      <div class="form-group"><label>IQC Reference</label><input type="text" value="IQC-2026-055" readonly></div>
      <div class="form-group"><label>GRN Reference</label><input type="text" value="GRN-2026-055" readonly></div>
      <div class="form-group"><label>Supplier</label><input type="text" value="Al-Rashid Timber Co." readonly></div>
      <div class="form-group"><label>Item Code / Name</label><input type="text" value="RM-WD-003 — Teak Wood Board" readonly></div>
      <div class="form-group"><label>Batch No</label><input type="text" value="BTH-2026-0045" readonly></div>
      <div class="form-group"><label>Lot Size</label><input type="text" value="98 Pcs" readonly></div>
      <div class="form-group"><label>Sample Size (AQL 2.5)</label><input type="text" value="13 Pcs" readonly></div>
      <div class="form-group"><label>Inspector</label><input type="text" value="Ahmed Khalid"></div>
      <div class="form-group"><label>Inspection Date</label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Inspection Plan</label><input type="text" value="QP-001" readonly></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>Inspection Parameters</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Parameter</th><th>Specification</th><th>Method</th><th>Sample 1</th><th>Sample 2</th><th>Sample 3</th><th>Result</th><th>Verdict</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>Moisture Content</td><td>≤ 12%</td><td>Moisture Meter</td><td><input type="text" value="10.2%" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="10.8%" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="11.1%" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>10.7% Avg</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>2</td><td>Thickness</td><td>25mm ± 0.5mm</td><td>Vernier Caliper</td><td><input type="text" value="25.1mm" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="24.8mm" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="25.3mm" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>25.1mm Avg</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>3</td><td>Surface Defects</td><td>0 Critical, ≤2 Minor</td><td>Visual</td><td><input type="text" value="0 def." style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="1 minor" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="0 def." style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>0 Critical</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>4</td><td>Grain Direction</td><td>Straight Grain</td><td>Visual</td><td><input type="text" value="OK" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="OK" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="Deviated" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;border-color:#ef4444;color:#ef4444;"></td><td>1 of 3 Fail</td><td><span class="status-badge status-rejected">FAIL</span></td></tr>
          <tr><td>5</td><td>Density</td><td>650–750 kg/m³</td><td>Weight/Volume</td><td><input type="text" value="680" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="710" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="text" value="695" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>695 Avg</td><td><span class="status-badge status-active">PASS</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Overall Result</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:14px;">
      <div style="background:#f0fdf4;border-radius:8px;padding:14px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:4px;">PARAMETERS</div><div style="font-size:22px;font-weight:700;color:#0f172a;">5</div></div>
      <div style="background:#f0fdf4;border-radius:8px;padding:14px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:4px;">PASSED</div><div style="font-size:22px;font-weight:700;color:#22c55e;">4</div></div>
      <div style="background:#fff1f2;border-radius:8px;padding:14px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:4px;">FAILED</div><div style="font-size:22px;font-weight:700;color:#ef4444;">1</div></div>
      <div style="background:#fef9c3;border-radius:8px;padding:14px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:4px;">OVERALL</div><div style="font-size:22px;font-weight:700;color:#f59e0b;">Conditional</div></div>
    </div>
    <div class="form-grid" style="grid-template-columns:1fr;"><div class="form-group"><label>Inspector Remarks</label><textarea rows="2" placeholder="Remarks...">1 sample showed grain deviation. Recommend usage with orientation check during production.</textarea></div></div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Acceptance will update GRN status and release stock to warehouse.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline" style="border-color:#ef4444;color:#ef4444;">Reject Lot</button><button class="btn btn-outline">Put on Hold</button><button class="btn btn-primary">Accept Lot</button></div>
  </div>
</div>"""

    elif form_type == "ipqc":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">In-Process Quality Control — IPQC-2026-088</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Quality Management &rsaquo; In-Process QC (IPQC)</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline" style="border-color:#ef4444;color:#ef4444;">Raise NCR</button><button class="btn btn-primary">Submit Result</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Production Reference</div>
    <div class="form-grid">
      <div class="form-group"><label>IPQC Reference</label><input type="text" value="IPQC-2026-088" readonly></div>
      <div class="form-group"><label>Work Order</label><input type="text" value="WO-2026-0412" readonly></div>
      <div class="form-group"><label>Item</label><input type="text" value="FG-CH-001 — Wooden Chair" readonly></div>
      <div class="form-group"><label>Operation</label><input type="text" value="Assembly" readonly></div>
      <div class="form-group"><label>Work Center</label><input type="text" value="Assembly Line 2" readonly></div>
      <div class="form-group"><label>Batch Size</label><input type="text" value="200 Pcs" readonly></div>
      <div class="form-group"><label>Sample Size (AQL 1.0)</label><input type="text" value="20 Pcs" readonly></div>
      <div class="form-group"><label>Inspector</label><input type="text" value="Sara Mohammed"></div>
      <div class="form-group"><label>Inspection Date/Time</label><input type="datetime-local" value="2026-07-22T11:30"></div>
      <div class="form-group"><label>Inspection Plan</label><input type="text" value="QP-003" readonly></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">In-Process Parameters</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Parameter</th><th>Specification</th><th>Measured Value</th><th>Min</th><th>Max</th><th>Verdict</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>Seat Height</td><td>450mm ± 5mm</td><td><input type="number" value="452" style="width:75px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>445</td><td>455</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>2</td><td>Backrest Angle</td><td>100° ± 2°</td><td><input type="number" value="99" style="width:75px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>98°</td><td>102°</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>3</td><td>Joint Strength</td><td>≥ 80 N/m²</td><td><input type="number" value="72" style="width:75px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;border-color:#ef4444;color:#ef4444;"></td><td>80</td><td>—</td><td><span class="status-badge status-rejected">FAIL</span></td></tr>
          <tr><td>4</td><td>Surface Roughness</td><td>Ra ≤ 3.2 µm</td><td><input type="number" value="2.8" style="width:75px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>—</td><td>3.2</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>5</td><td>Screw Torque</td><td>8–10 Nm</td><td><input type="number" value="9.2" style="width:75px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>8</td><td>10</td><td><span class="status-badge status-active">PASS</span></td></tr>
        </tbody>
      </table>
    </div>
    <div style="background:#fff1f2;border:1px solid #fca5a5;border-radius:8px;padding:12px 16px;margin:12px 20px 0;font-size:13px;color:#991b1b;">
      ⚠ Parameter 3 (Joint Strength) FAILED. 1 out of 5 parameters failed. Recommend halting line and investigating adhesive application.
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Defect Summary</div>
    <div class="form-grid">
      <div class="form-group"><label>Defect Type</label><select><option>Process Defect</option><option>Material Defect</option><option>Operator Error</option></select></div>
      <div class="form-group"><label>No. of Defective Units</label><input type="number" value="3"></div>
      <div class="form-group"><label>Disposition</label><select><option>Rework</option><option>Scrap</option><option>Use As Is</option></select></div>
      <div class="form-group"><label>Line Action</label><select><option>Continue — Monitor</option><option>Stop Line</option><option>Partial Hold</option></select></div>
    </div>
    <div class="form-grid" style="grid-template-columns:1fr;margin-top:12px;"><div class="form-group"><label>Remarks</label><textarea rows="2" placeholder="Inspector remarks...">Joint adhesive may be insufficient. Supervisor notified.</textarea></div></div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Result will be linked to WO and reflected in FPY metrics.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline" style="border-color:#ef4444;color:#ef4444;">Raise NCR</button><button class="btn btn-primary">Submit Result</button></div>
  </div>
</div>"""

    elif form_type == "oqc":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Outgoing Quality Control — OQC-2026-031 <span class="status-badge status-active" style="margin-left:8px;">Passed</span></h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Quality Management &rsaquo; Outgoing QC (OQC)</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Print Certificate</button><button class="btn btn-primary">Approve for Dispatch</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Final Inspection Header</div>
    <div class="form-grid">
      <div class="form-group"><label>OQC Reference</label><input type="text" value="OQC-2026-031" readonly></div>
      <div class="form-group"><label>Work Order</label><input type="text" value="WO-2026-0409" readonly></div>
      <div class="form-group"><label>Item</label><input type="text" value="FG-CH-001 — Wooden Chair (Finished)" readonly></div>
      <div class="form-group"><label>Finished Qty</label><input type="text" value="100 Pcs" readonly></div>
      <div class="form-group"><label>Batch / Lot</label><input type="text" value="WO-2026-0409-FG" readonly></div>
      <div class="form-group"><label>Sample Size (AQL 0.65)</label><input type="text" value="20 Pcs" readonly></div>
      <div class="form-group"><label>Customer / Sales Order</label><input type="text" value="SO-2026-118 — Al-Madar Furniture"></div>
      <div class="form-group"><label>Inspector</label><input type="text" value="Ahmed Khalid"></div>
      <div class="form-group"><label>Inspection Date</label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Inspection Plan</label><input type="text" value="QP-004" readonly></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Final Inspection Parameters</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Parameter</th><th>Specification</th><th>Result</th><th>AQL Accept #</th><th>Defects Found</th><th>Verdict</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>Dimensions (Overall)</td><td>Per drawing ± 2mm</td><td>Within tolerance</td><td>0</td><td>0</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>2</td><td>Surface Finish / Paint</td><td>No scratches, uniform coat</td><td>All OK</td><td>1</td><td>0</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>3</td><td>Weight</td><td>8.5 kg ± 0.3 kg</td><td>8.4 kg Avg</td><td>0</td><td>0</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>4</td><td>Load Test</td><td>≥ 120 kg static</td><td>125 kg OK</td><td>0</td><td>0</td><td><span class="status-badge status-active">PASS</span></td></tr>
          <tr><td>5</td><td>Labeling / Marking</td><td>Per customer spec</td><td>Correct label</td><td>0</td><td>0</td><td><span class="status-badge status-active">PASS</span></td></tr>
        </tbody>
      </table>
    </div>
    <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:12px 16px;margin:12px 20px 0;font-size:13px;color:#166534;font-weight:600;">
      ✔ ALL 5 PARAMETERS PASSED — Lot approved for dispatch. Certificate of Conformance ready.
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">OQC approval will trigger delivery note generation in logistics.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Print Certificate</button><button class="btn btn-primary">Approve for Dispatch</button></div>
  </div>
</div>"""

    elif form_type == "ncr":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Non-Conformance Report — NCR-2026-018 <span class="status-badge status-pending" style="margin-left:8px;">Under Review</span></h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Quality Management &rsaquo; NCR</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Close NCR</button><button class="btn btn-primary">Raise CAPA</button></div>
  </div>
  <div style="background:#fff1f2;border:1px solid #fca5a5;border-radius:8px;padding:14px 20px;font-size:13px;color:#991b1b;">
    ⚠ Critical Non-Conformance — Requires immediate CAPA and disposition decision.
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path></svg>NCR Details</div>
    <div class="form-grid">
      <div class="form-group"><label>NCR Number</label><input type="text" value="NCR-2026-018" readonly></div>
      <div class="form-group"><label>Source</label><select><option>IQC</option><option>IPQC</option><option>OQC</option><option>Customer Complaint</option></select></div>
      <div class="form-group"><label>Reference (IQC/WO/GRN)</label><input type="text" value="IQC-2026-055 / GRN-2026-055"></div>
      <div class="form-group"><label>Item Code / Name</label><input type="text" value="RM-STL-001 — Steel Sheet 2mm" readonly></div>
      <div class="form-group"><label>Batch / Lot</label><input type="text" value="BTH-2026-0044" readonly></div>
      <div class="form-group"><label>Qty Non-Conforming</label><input type="text" value="5 Kg"></div>
      <div class="form-group"><label>Defect Type</label><select><option>Thickness Variance</option><option>Surface Defect</option><option>Wrong Material</option><option>Contamination</option></select></div>
      <div class="form-group"><label>Severity</label><select><option>Critical</option><option>Major</option><option>Minor</option></select></div>
      <div class="form-group"><label>Raised By</label><input type="text" value="Ahmed Khalid"></div>
      <div class="form-group"><label>Raised On</label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Responsible Dept</label><select><option>Incoming QC</option><option>Production</option><option>Supplier</option></select></div>
      <div class="form-group"><label>Due Date for Closure</label><input type="date" value="2026-07-29"></div>
    </div>
    <div class="form-grid" style="grid-template-columns:1fr 1fr;margin-top:12px;">
      <div class="form-group"><label>Problem Description</label><textarea rows="3">Steel Sheet 2mm batch BTH-2026-0044 measured 1.7mm thickness on 5 of 200 Kg received from Gulf Steel Trading. Specification requires 2mm ± 0.1mm.</textarea></div>
      <div class="form-group"><label>Immediate Action Taken</label><textarea rows="3">5 Kg placed on Quality Hold (QH-2026-012). Supplier notified. Remaining lot under review pending full inspection.</textarea></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Disposition Decision</div>
    <div class="form-grid">
      <div class="form-group"><label>Disposition <span class="req">*</span></label><select><option>Return to Supplier</option><option>Rework &amp; Accept</option><option>Use As Is (Concession)</option><option>Scrap</option></select></div>
      <div class="form-group"><label>Disposition Approved By</label><input type="text" placeholder="QC Manager..."></div>
      <div class="form-group"><label>CAPA Required?</label><select><option>Yes</option><option>No</option></select></div>
      <div class="form-group"><label>CAPA Reference</label><input type="text" placeholder="Auto-generated on CAPA creation" readonly></div>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">NCR will be linked to Supplier Quality scorecard and quality reports.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Close NCR</button><button class="btn btn-primary">Raise CAPA</button></div>
  </div>
</div>"""

    elif form_type == "capa":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Corrective & Preventive Action — CAPA-2026-012 <span class="status-badge status-inprogress" style="margin-left:8px;">In Progress</span></h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Quality Management &rsaquo; CAPA</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Save Draft</button><button class="btn btn-primary">Submit &amp; Notify</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">CAPA Header</div>
    <div class="form-grid">
      <div class="form-group"><label>CAPA Number</label><input type="text" value="CAPA-2026-012" readonly></div>
      <div class="form-group"><label>Linked NCR</label><input type="text" value="NCR-2026-018" readonly></div>
      <div class="form-group"><label>CAPA Type</label><select><option>Corrective</option><option>Preventive</option><option>Both</option></select></div>
      <div class="form-group"><label>Priority</label><select><option>High</option><option>Medium</option><option>Low</option></select></div>
      <div class="form-group"><label>Initiated By</label><input type="text" value="Ahmed Khalid"></div>
      <div class="form-group"><label>Responsible Person</label><input type="text" value="Khalid Mohammed — QC Mgr"></div>
      <div class="form-group"><label>Initiated Date</label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Target Closure Date</label><input type="date" value="2026-08-05"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Root Cause Analysis</div>
    <div class="form-grid" style="grid-template-columns:1fr;gap:12px;">
      <div class="form-group"><label>Problem Statement</label><textarea rows="2">Steel Sheet 2mm received with 1.7mm actual thickness — out of 2mm ± 0.1mm spec.</textarea></div>
      <div class="form-group"><label>Root Cause (5-Why / Fishbone)</label><textarea rows="3">Why 1: Thickness OOS → Why 2: Supplier rolling mill calibration drift → Why 3: No mandatory CMM check before shipment → Why 4: No process control requirement in PO → Why 5: Supplier qualification process incomplete.</textarea></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Actions</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Action Type</th><th>Action Description</th><th>Responsible</th><th>Due Date</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>1</td><td><span class="status-badge status-rejected" style="font-size:10px;">Corrective</span></td><td>Return non-conforming 5 Kg to Gulf Steel Trading</td><td>Rami Hassan</td><td>2026-07-25</td><td><span class="status-badge status-inprogress">In Progress</span></td></tr>
          <tr><td>2</td><td><span class="status-badge status-rejected" style="font-size:10px;">Corrective</span></td><td>Add 100% thickness check to incoming inspection plan QP-002</td><td>Sara Mohammed</td><td>2026-07-24</td><td><span class="status-badge status-active">Done</span></td></tr>
          <tr><td>3</td><td><span class="status-badge status-blue" style="font-size:10px;background:#dbeafe;color:#1e40af;">Preventive</span></td><td>Update Supplier Qualification Requirements — add CMM certificate</td><td>Ahmed Khalid</td><td>2026-08-01</td><td><span class="status-badge status-draft">Open</span></td></tr>
          <tr><td>4</td><td><span class="status-badge status-blue" style="font-size:10px;background:#dbeafe;color:#1e40af;">Preventive</span></td><td>Conduct Supplier Audit at Gulf Steel within 30 days</td><td>QC Manager</td><td>2026-08-05</td><td><span class="status-badge status-draft">Open</span></td></tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-outline" style="margin:12px 20px;"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> Add Action</button>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Effectiveness Verification</div>
    <div class="form-grid">
      <div class="form-group"><label>Verification Method</label><select><option>Re-Inspection of Next Lot</option><option>Audit</option><option>Data Review</option></select></div>
      <div class="form-group"><label>Verification Date</label><input type="date" placeholder="After actions completed..."></div>
      <div class="form-group"><label>Verified By</label><input type="text" placeholder="QC Manager..."></div>
      <div class="form-group"><label>Effective?</label><select><option>Pending Verification</option><option>Yes — Close CAPA</option><option>No — Re-open</option></select></div>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">CAPA closure requires effectiveness verification sign-off.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Save Draft</button><button class="btn btn-primary">Submit &amp; Notify</button></div>
  </div>
</div>"""
    return ""


# ═══════════════════════════════════════════════════════════
# MATERIAL MANAGEMENT HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

MM_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">428</div><div class="kpi-label">Total Active SKUs</div></div>
    <div class="kpi-trend up">↑ 12 new this month</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">SAR 2.4M</div><div class="kpi-label">Total Stock Value</div></div>
    <div class="kpi-trend up">↑ 8% vs last month</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">14</div><div class="kpi-label">Low Stock / Reorder Alerts</div></div>
    <div class="kpi-trend down">↑ 3 since yesterday</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">7</div><div class="kpi-label">Pending Material Requests</div></div>
    <div class="kpi-trend neutral">→ Same as yesterday</div>
  </div>
</div>

<!-- Warehouse Utilization & Low Stock -->
<div class="dashboard-row">
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Warehouse Utilization</span><span class="dash-card-badge">Live</span></div>
    <div style="display:flex;flex-direction:column;gap:14px;margin-top:8px;">
      <div class="cap-row"><span style="width:160px;">WH-01 Raw Material</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:78%;background:#f59e0b;"></div></div><span class="cap-pct">78%</span></div>
      <div class="cap-row"><span style="width:160px;">WH-02 Finished Goods</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:22%;background:#22c55e;"></div></div><span class="cap-pct">22%</span></div>
      <div class="cap-row"><span style="width:160px;">WH-03 WIP Staging</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:91%;background:#ef4444;"></div></div><span class="cap-pct">91%</span></div>
      <div class="cap-row"><span style="width:160px;">WH-04 Spare Parts</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:45%;background:#3b82f6;"></div></div><span class="cap-pct">45%</span></div>
    </div>
  </div>
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">⚠ Low Stock / Reorder Alerts</span><a href="#" style="font-size:12px;color:var(--brand-yellow);text-decoration:none;">Create PO</a></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Item Code</th><th>Item Name</th><th>On Hand</th><th>Reorder Lvl</th><th>Shortage</th><th>Action</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">RM-WD-003</td><td>Teak Wood Board</td><td style="color:#ef4444;font-weight:600;">12</td><td>50</td><td style="color:#ef4444;font-weight:700;">−38</td><td><button class="btn btn-primary" style="padding:4px 8px;font-size:11px;">Reorder</button></td></tr>
          <tr><td style="font-weight:600;">RM-LTH-007</td><td>Leather Hide Grade A</td><td style="color:#ef4444;font-weight:600;">8 m²</td><td>30</td><td style="color:#ef4444;font-weight:700;">−22</td><td><button class="btn btn-primary" style="padding:4px 8px;font-size:11px;">Reorder</button></td></tr>
          <tr><td style="font-weight:600;">RM-PNT-002</td><td>Primer Coat Paint</td><td style="color:#ef4444;font-weight:600;">2 Ltr</td><td>20</td><td style="color:#ef4444;font-weight:700;">−18</td><td><button class="btn btn-primary" style="padding:4px 8px;font-size:11px;">Reorder</button></td></tr>
          <tr><td style="font-weight:600;">RM-SCR-010</td><td>Hex Screw M8</td><td style="color:#f59e0b;font-weight:600;">320</td><td>500</td><td style="color:#f59e0b;font-weight:700;">−180</td><td><button class="btn btn-outline" style="padding:4px 8px;font-size:11px;">Review</button></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:1.5;">
    <div class="dash-card-header"><span class="dash-card-title">Pending Transactions</span></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Doc No</th><th>Type</th><th>Ref</th><th>Date</th><th>Items</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:600;">MR-2026-042</td><td>Material Request</td><td>WO-2026-0412</td><td>2026-07-22</td><td>4</td><td><span class="status-badge status-pending">Pending</span></td></tr>
          <tr><td style="font-weight:600;">MI-2026-038</td><td>Material Issue</td><td>WO-2026-0412</td><td>2026-07-22</td><td>3</td><td><span class="status-badge status-draft">Draft</span></td></tr>
          <tr><td style="font-weight:600;">GRN-2026-055</td><td>GRN</td><td>PO-2026-018</td><td>2026-07-21</td><td>6</td><td><span class="status-badge status-pending">Pending QC</span></td></tr>
          <tr><td style="font-weight:600;">MT-2026-011</td><td>Transfer</td><td>WH-01→WH-03</td><td>2026-07-21</td><td>2</td><td><span class="status-badge status-completed">Completed</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Stock Value by Category</span></div>
    <div style="display:flex;flex-direction:column;gap:14px;margin-top:8px;">
      <div class="cap-row"><span style="width:120px;">Raw Material</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:65%;background:#3b82f6;"></div></div><span class="cap-pct" style="width:70px;color:#3b82f6;">SAR 1.56M</span></div>
      <div class="cap-row"><span style="width:120px;">Finished Goods</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:18%;background:#22c55e;"></div></div><span class="cap-pct" style="width:70px;color:#22c55e;">SAR 432K</span></div>
      <div class="cap-row"><span style="width:120px;">WIP</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:10%;background:#f59e0b;"></div></div><span class="cap-pct" style="width:70px;color:#f59e0b;">SAR 240K</span></div>
      <div class="cap-row"><span style="width:120px;">Spare Parts</span><div class="cap-bar-wrap"><div class="cap-bar" style="width:7%;background:#8b5cf6;"></div></div><span class="cap-pct" style="width:70px;color:#8b5cf6;">SAR 168K</span></div>
    </div>
  </div>
</div>
"""

MM_STOCK_VIEW_HTML = """
<div class="card">
  <div class="toolbar">
    <div class="toolbar-left">
      <div class="search-box">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" placeholder="Search by item code or name..." oninput="const q = this.value.toLowerCase(); this.closest('.card').querySelectorAll('.data-table tbody tr').forEach(r => r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none');">
      </div>
      <select style="padding:8px 12px;border:1px solid #cbd5e1;border-radius:6px;font-size:13px;color:#475569;outline:none;">
        <option>All Warehouses</option><option>WH-01 Raw Material</option><option>WH-02 Finished Goods</option><option>WH-03 WIP</option><option>WH-04 Spare Parts</option>
      </select>
      <select style="padding:8px 12px;border:1px solid #cbd5e1;border-radius:6px;font-size:13px;color:#475569;outline:none;">
        <option>All Item Groups</option><option>Raw Material</option><option>Finished Good</option><option>Consumable</option><option>Spare Parts</option>
      </select>
      <button class="btn btn-outline" style="border-color:#ef4444;color:#ef4444;">⚠ Show Low Stock Only</button>
    </div>
    <div class="toolbar-right">
      <button class="btn btn-outline">Export</button>
    </div>
  </div>
  <div class="table-responsive">
    <table class="data-table">
      <thead>
        <tr>
          <th>Item Code</th><th>Item Name</th><th>Item Group</th><th>Warehouse</th><th>Bin</th><th>UoM</th>
          <th>On Hand</th><th>Reserved</th><th>Available</th><th>Reorder Lvl</th><th>Stock Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight:600;">RM-WD-003</td><td>Teak Wood Board</td><td>Raw Material</td><td>WH-01</td><td>WH01-R01-A1</td><td>Pcs</td>
          <td style="font-weight:600;color:#ef4444;">12</td><td>12</td><td style="font-weight:600;color:#ef4444;">0</td><td>50</td>
          <td><span class="status-badge status-rejected">⚠ Below Reorder</span></td>
        </tr>
        <tr>
          <td style="font-weight:600;">RM-STL-001</td><td>Steel Sheet 2mm</td><td>Raw Material</td><td>WH-01</td><td>WH01-R02-B1</td><td>Kg</td>
          <td style="font-weight:600;">145</td><td>80</td><td style="font-weight:600;color:#22c55e;">65</td><td>200</td>
          <td><span class="status-badge status-pending">↓ Watch Level</span></td>
        </tr>
        <tr>
          <td style="font-weight:600;">RM-LTH-007</td><td>Leather Hide Grade A</td><td>Raw Material</td><td>WH-01</td><td>WH01-R01-A2</td><td>m²</td>
          <td style="font-weight:600;color:#ef4444;">8</td><td>8</td><td style="font-weight:600;color:#ef4444;">0</td><td>30</td>
          <td><span class="status-badge status-rejected">⚠ Below Reorder</span></td>
        </tr>
        <tr>
          <td style="font-weight:600;">FG-CH-001</td><td>Wooden Chair (Finished)</td><td>Finished Good</td><td>WH-02</td><td>WH02-R01-A1</td><td>Pcs</td>
          <td style="font-weight:600;">0</td><td>0</td><td style="font-weight:600;color:#94a3b8;">0</td><td>100</td>
          <td><span class="status-badge status-rejected">⚠ Zero Stock</span></td>
        </tr>
        <tr>
          <td style="font-weight:600;">RM-PNT-002</td><td>Primer Coat Paint</td><td>Consumable</td><td>WH-01</td><td>WH01-R01-A2</td><td>Ltr</td>
          <td style="font-weight:600;color:#ef4444;">2</td><td>0</td><td style="font-weight:600;color:#f59e0b;">2</td><td>20</td>
          <td><span class="status-badge status-rejected">⚠ Below Safety</span></td>
        </tr>
        <tr>
          <td style="font-weight:600;">RM-SCR-010</td><td>Hex Screw M8</td><td>Spare Parts</td><td>WH-04</td><td>WH04-S01-A1</td><td>Pcs</td>
          <td style="font-weight:600;">320</td><td>0</td><td style="font-weight:600;color:#22c55e;">320</td><td>500</td>
          <td><span class="status-badge status-pending">↓ Below Reorder</span></td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="pagination">
    <div>Showing 1 to 6 of 428 entries</div>
    <div class="pagination-controls">
      <button class="page-btn"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg></button>
      <button class="page-btn active">1</button>
      <button class="page-btn">2</button>
      <button class="page-btn">3</button>
      <button class="page-btn"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></button>
    </div>
  </div>
</div>
"""

def build_mm_form(form_type):
    if form_type == "mr":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Material Request — MR-2026-042</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Material Request</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-outline">Save Draft</button><button class="btn btn-primary">Submit Request</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>Request Details</div>
    <div class="form-grid">
      <div class="form-group"><label>MR Number</label><input type="text" value="MR-2026-042" readonly></div>
      <div class="form-group"><label>Request Type <span class="req">*</span></label><select><option>For Work Order</option><option>For Maintenance</option><option>For Project</option><option>General</option></select></div>
      <div class="form-group"><label>Work Order / Reference</label><input type="text" value="WO-2026-0412"></div>
      <div class="form-group"><label>Department <span class="req">*</span></label><select><option>Production</option><option>Maintenance</option><option>QC</option></select></div>
      <div class="form-group"><label>Requested By <span class="req">*</span></label><input type="text" value="Ahmed Al-Rashid"></div>
      <div class="form-group"><label>Request Date</label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Required By Date <span class="req">*</span></label><input type="date" value="2026-07-23"></div>
      <div class="form-group"><label>Issue Warehouse</label><select><option>WH-01 Raw Material</option><option>WH-04 Spare Parts</option></select></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Items Requested</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th>Required Qty</th><th>UoM</th><th>On-Hand Stock</th><th>Availability</th><th>Notes</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>RM-WD-003</td><td>Teak Wood Board</td><td><input type="number" value="50" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Pcs</td><td style="color:#ef4444;font-weight:600;">12</td><td><span class="status-badge status-rejected">Insufficient</span></td><td><input type="text" placeholder="Notes..." style="width:100%;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td></tr>
          <tr><td>2</td><td>RM-STL-001</td><td>Steel Sheet 2mm</td><td><input type="number" value="40" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Kg</td><td>145</td><td><span class="status-badge status-active">Available</span></td><td><input type="text" placeholder="Notes..." style="width:100%;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td></tr>
          <tr><td>3</td><td>RM-SCR-010</td><td>Hex Screw M8</td><td><input type="number" value="320" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Pcs</td><td>320</td><td><span class="status-badge status-active">Available</span></td><td><input type="text" placeholder="Notes..." style="width:100%;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td></tr>
          <tr><td>4</td><td>RM-PNT-002</td><td>Primer Coat Paint</td><td><input type="number" value="10" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Ltr</td><td style="color:#ef4444;font-weight:600;">2</td><td><span class="status-badge status-rejected">Insufficient</span></td><td><input type="text" placeholder="Notes..." style="width:100%;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td></tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-outline" style="margin:12px 20px;"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> Add Row</button>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">2 of 4 items have insufficient stock — auto-alert sent to store manager.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-outline">Save Draft</button><button class="btn btn-primary">Submit Request</button></div>
  </div>
</div>"""

    elif form_type == "mi":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Material Issue — MI-2026-038 <span class="status-badge status-draft" style="margin-left:8px;">Draft</span></h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Material Issue</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Issue</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>Issue Details</div>
    <div class="form-grid">
      <div class="form-group"><label>MI Number</label><input type="text" value="MI-2026-038" readonly></div>
      <div class="form-group"><label>Against (MR / WO) <span class="req">*</span></label><input type="text" value="MR-2026-042 / WO-2026-0412"></div>
      <div class="form-group"><label>Issue From Warehouse <span class="req">*</span></label><select><option>WH-01 Raw Material</option><option>WH-04 Spare Parts</option></select></div>
      <div class="form-group"><label>Issued By <span class="req">*</span></label><input type="text" value="Khalid Mohammed"></div>
      <div class="form-group"><label>Issue Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Posting Time</label><input type="time" value="13:00"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Items to Issue</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th>Batch / Serial</th><th>Bin Location</th><th>Requested Qty</th><th>Issue Qty</th><th>UoM</th><th>Stock After</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>RM-STL-001</td><td>Steel Sheet 2mm</td><td>BTH-2026-0041</td><td>WH01-R02-B1</td><td>40 Kg</td><td><input type="number" value="40" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Kg</td><td>105</td></tr>
          <tr><td>2</td><td>RM-SCR-010</td><td>Hex Screw M8</td><td>—</td><td>WH04-S01-A1</td><td>320 Pcs</td><td><input type="number" value="320" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Pcs</td><td>0</td></tr>
          <tr><td>3</td><td>RM-PNT-002</td><td>Primer Coat Paint</td><td>BTH-2026-0038</td><td>WH01-R01-A2</td><td>10 Ltr</td><td><input type="number" value="2" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;color:#ef4444;border-color:#ef4444;"></td><td>Ltr</td><td style="color:#ef4444;font-weight:600;">0 ⚠</td></tr>
        </tbody>
      </table>
    </div>
    <div style="background:#fef9c3;border:1px solid #fde047;border-radius:8px;padding:12px 16px;margin:12px 20px 0;font-size:13px;color:#854d0e;">
      ⚠ Item 3 (Primer Coat Paint) has only 2 Ltr in stock. Partial issue of 2 Ltr will be posted. Remaining 8 Ltr pending purchase.
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Stock ledger and cost entries will be posted automatically.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Issue</button></div>
  </div>
</div>"""

    elif form_type == "grn":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Goods Receipt Note — GRN-2026-055 <span class="status-badge status-pending" style="margin-left:8px;">Pending QC</span></h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Material Receipt</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-outline">Send to QC</button><button class="btn btn-primary">Accept & Post</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg>Receipt Details</div>
    <div class="form-grid">
      <div class="form-group"><label>GRN Number</label><input type="text" value="GRN-2026-055" readonly></div>
      <div class="form-group"><label>Purchase Order Ref <span class="req">*</span></label><input type="text" value="PO-2026-018"></div>
      <div class="form-group"><label>Supplier</label><input type="text" value="Al-Rashid Timber Co." readonly></div>
      <div class="form-group"><label>Receive to Warehouse <span class="req">*</span></label><select><option>WH-01 Raw Material</option><option>WH-04 Spare Parts</option></select></div>
      <div class="form-group"><label>Received By <span class="req">*</span></label><input type="text" value="Rami Hassan"></div>
      <div class="form-group"><label>Receipt Date <span class="req">*</span></label><input type="date" value="2026-07-21"></div>
      <div class="form-group"><label>Supplier Invoice No</label><input type="text" value="INV-ART-2026-1142"></div>
      <div class="form-group"><label>Vehicle / LR No</label><input type="text" value="LR-4521-KA"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Items Received</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th>PO Qty</th><th>Received Qty</th><th>Accepted</th><th>Rejected</th><th>UoM</th><th>Batch / Serial</th><th>Bin</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>RM-WD-003</td><td>Teak Wood Board</td><td>100</td><td><input type="number" value="98" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="number" value="98" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>0</td><td>Pcs</td><td>BTH-2026-0045</td><td>WH01-R01-A1</td></tr>
          <tr><td>2</td><td>RM-STL-001</td><td>Steel Sheet 2mm</td><td>200</td><td><input type="number" value="200" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td><input type="number" value="195" style="width:60px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td style="color:#ef4444;font-weight:600;">5</td><td>Kg</td><td>BTH-2026-0044</td><td>WH01-R02-B1</td></tr>
        </tbody>
      </table>
    </div>
    <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:12px 16px;margin:12px 20px 0;font-size:13px;">
      <span style="color:#166534;font-weight:600;">✔ Quality Inspection required before stock posting. 5 Kg of Steel Sheet rejected and returned to supplier.</span>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Stock ledger, valuation, and PO closure entries will be posted on acceptance.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-outline">Send to QC</button><button class="btn btn-primary">Accept & Post</button></div>
  </div>
</div>"""

    elif form_type == "mt":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Material Transfer — MT-2026-011</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Material Transfer</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Transfer</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg>Transfer Details</div>
    <div class="form-grid">
      <div class="form-group"><label>MT Number</label><input type="text" value="MT-2026-011" readonly></div>
      <div class="form-group"><label>Transfer Purpose</label><select><option>WO Material Supply</option><option>Replenishment</option><option>Staging</option><option>Consolidation</option></select></div>
      <div class="form-group"><label>From Warehouse <span class="req">*</span></label><select><option>WH-01 Raw Material</option><option>WH-04 Spare Parts</option></select></div>
      <div class="form-group"><label>To Warehouse <span class="req">*</span></label><select><option>WH-03 WIP Staging</option><option>WH-02 Finished Goods</option></select></div>
      <div class="form-group"><label>Transfer Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Transferred By <span class="req">*</span></label><input type="text" value="Khalid Mohammed"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Items to Transfer</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th>From Bin</th><th>To Bin</th><th>Batch</th><th>Transfer Qty</th><th>UoM</th><th>Available Qty</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>RM-WD-003</td><td>Teak Wood Board</td><td>WH01-R01-A1</td><td>WH03-S01</td><td>BTH-2026-0035</td><td><input type="number" value="12" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Pcs</td><td>12</td></tr>
          <tr><td>2</td><td>RM-STL-001</td><td>Steel Sheet 2mm</td><td>WH01-R02-B1</td><td>WH03-S02</td><td>BTH-2026-0044</td><td><input type="number" value="40" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>Kg</td><td>145</td></tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-outline" style="margin:12px 20px;"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> Add Row</button>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Stock ledger entries will be posted for both source and destination warehouses.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Transfer</button></div>
  </div>
</div>"""

    elif form_type == "adj":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Inventory Adjustment</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Inventory Adjustment</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Adjustment</button></div>
  </div>
  <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:14px 20px;font-size:13px;color:#9a3412;">
    ⚠ Inventory adjustments directly affect stock balances and valuations. Ensure approvals are obtained before posting.
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>Adjustment Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Adjustment Reference</label><input type="text" value="ADJ-2026-008" readonly></div>
      <div class="form-group"><label>Adjustment Type <span class="req">*</span></label><select><option>Physical Count Variance</option><option>Damage Write-Off</option><option>Expired Goods</option><option>Theft / Loss</option><option>System Correction</option></select></div>
      <div class="form-group"><label>Warehouse <span class="req">*</span></label><select><option>WH-01 Raw Material</option><option>WH-02 Finished Goods</option><option>WH-04 Spare Parts</option></select></div>
      <div class="form-group"><label>Approved By <span class="req">*</span></label><input type="text" placeholder="Select approver..."></div>
      <div class="form-group"><label>Adjustment Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Cost Center</label><input type="text" placeholder="Select cost center..."></div>
    </div>
    <div class="form-grid" style="grid-template-columns:1fr;margin-top:12px;"><div class="form-group"><label>Reason / Remarks</label><textarea rows="2" placeholder="Reason for inventory adjustment..."></textarea></div></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Adjustment Items</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>#</th><th>Item Code</th><th>Item Name</th><th>Batch</th><th>Bin</th><th>System Qty</th><th>Actual Qty</th><th>Variance</th><th>UoM</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>RM-LTH-007</td><td>Leather Hide Grade A</td><td>BTH-2026-0041</td><td>WH01-R01-A2</td><td>8</td><td><input type="number" value="7" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td style="color:#ef4444;font-weight:700;">−1</td><td>m²</td></tr>
          <tr><td>2</td><td>RM-SCR-010</td><td>Hex Screw M8</td><td>—</td><td>WH04-S01-A1</td><td>320</td><td><input type="number" value="310" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td style="color:#ef4444;font-weight:700;">−10</td><td>Pcs</td></tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Stock ledger and cost difference will be posted to the adjustment account.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post Adjustment</button></div>
  </div>
</div>"""

    elif form_type == "cc":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Cycle Count — CC-2026-015</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Cycle Count</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-outline">Save Progress</button><button class="btn btn-primary">Submit Count</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Count Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Count Reference</label><input type="text" value="CC-2026-015" readonly></div>
      <div class="form-group"><label>Warehouse <span class="req">*</span></label><input type="text" value="WH-01 Raw Material" readonly></div>
      <div class="form-group"><label>Zone / Rack</label><input type="text" value="Rack R01"></div>
      <div class="form-group"><label>Counted By <span class="req">*</span></label><input type="text" value="Rami Hassan"></div>
      <div class="form-group"><label>Count Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Verified By</label><input type="text" placeholder="Supervisor..."></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Count Sheet</div>
    <div class="table-responsive">
      <table class="data-table">
        <thead><tr><th>Item Code</th><th>Item Name</th><th>Batch</th><th>Bin</th><th>System Qty</th><th>Counted Qty</th><th>Variance</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>RM-WD-003</td><td>Teak Wood Board</td><td>BTH-2026-0035</td><td>WH01-R01-A1</td><td>12</td><td><input type="number" value="11" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td style="color:#ef4444;font-weight:700;">−1</td><td><span class="status-badge status-pending">Variance</span></td></tr>
          <tr><td>RM-STL-001</td><td>Steel Sheet 2mm</td><td>BTH-2026-0044</td><td>WH01-R02-B1</td><td>145</td><td><input type="number" value="145" style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td style="color:#22c55e;font-weight:700;">0</td><td><span class="status-badge status-active">Match</span></td></tr>
          <tr><td>RM-LTH-007</td><td>Leather Hide Grade A</td><td>BTH-2026-0041</td><td>WH01-R01-A2</td><td>8</td><td><input type="number" value="" placeholder="Count..." style="width:65px;padding:4px;border:1px solid #cbd5e1;border-radius:4px;"></td><td>—</td><td><span class="status-badge status-draft">Pending</span></td></tr>
        </tbody>
      </table>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:24px;padding:12px 20px;font-size:13px;font-weight:600;border-top:1px solid #f1f5f9;">
      <span>Items: <span style="color:#0f172a;">3</span></span>
      <span>Matched: <span style="color:#22c55e;">1</span></span>
      <span>Variance: <span style="color:#ef4444;">1</span></span>
      <span>Pending: <span style="color:#94a3b8;">1</span></span>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Variances will create inventory adjustment records for approval.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Save Progress</button><button class="btn btn-primary">Submit Count</button></div>
  </div>
</div>"""

    elif form_type == "pi":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Physical Inventory — PI-2026-003</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Material Management &rsaquo; Physical Inventory</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-outline">Freeze Stock</button><button class="btn btn-primary">Post PI</button></div>
  </div>
  <div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:8px;padding:14px 20px;font-size:13px;color:#1e40af;">
    ℹ Physical Inventory requires all stock movements in this warehouse to be frozen. Freeze before counting.
  </div>
  <div class="form-section card">
    <div class="form-section-title">PI Header</div>
    <div class="form-grid">
      <div class="form-group"><label>PI Reference</label><input type="text" value="PI-2026-003" readonly></div>
      <div class="form-group"><label>Warehouse <span class="req">*</span></label><select><option>WH-01 Raw Material</option><option>WH-02 Finished Goods</option></select></div>
      <div class="form-group"><label>Count Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Authorized By <span class="req">*</span></label><input type="text" placeholder="Management approval..."></div>
      <div class="form-group"><label>Stock Frozen?</label><select><option>Yes</option><option>No</option></select></div>
      <div class="form-group"><label>Count Method</label><select><option>Full Count</option><option>ABC Analysis</option></select></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Count Summary</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">
      <div style="background:#f8fafc;border-radius:8px;padding:16px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;">TOTAL ITEMS</div><div style="font-size:26px;font-weight:700;color:#0f172a;">428</div></div>
      <div style="background:#f0fdf4;border-radius:8px;padding:16px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;">MATCHED</div><div style="font-size:26px;font-weight:700;color:#22c55e;">398</div></div>
      <div style="background:#fff1f2;border-radius:8px;padding:16px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;">VARIANCE</div><div style="font-size:26px;font-weight:700;color:#ef4444;">22</div></div>
      <div style="background:#f8fafc;border-radius:8px;padding:16px;text-align:center;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;">NOT COUNTED</div><div style="font-size:26px;font-weight:700;color:#94a3b8;">8</div></div>
    </div>
    <div style="margin-top:16px;font-size:13px;color:#64748b;padding:0 4px;">Variance Value: <b style="color:#ef4444;">SAR −4,200</b> &nbsp;|&nbsp; Variance %: <b style="color:#ef4444;">−0.18%</b></div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">PI will create adjustment entries and unfreeze the warehouse on posting.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Post PI</button></div>
  </div>
</div>"""
    return ""


# ═══════════════════════════════════════════════════════════
# SHOP FLOOR EXECUTION HTML TEMPLATES
# ═══════════════════════════════════════════════════════════

SFE_DASHBOARD_HTML = """
<div class="dashboard-kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon kpi-green">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">6</div><div class="kpi-label">Production Lines Running</div></div>
    <div class="kpi-trend up">↑ 1 since last check</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-blue">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">412</div><div class="kpi-label">Total Output Today (Pcs)</div></div>
    <div class="kpi-trend up">↑ 12% vs target</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-purple">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">82%</div><div class="kpi-label">Overall OEE</div></div>
    <div class="kpi-trend up">↑ 3% vs yesterday</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon kpi-orange">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
    </div>
    <div class="kpi-body"><div class="kpi-value">3</div><div class="kpi-label">Downtime Events Today</div></div>
    <div class="kpi-trend down">↑ 2 vs yesterday</div>
  </div>
</div>

<!-- Machine Status Tiles -->
<div class="card dash-card" style="margin-top:16px; padding:20px;">
  <div class="dash-card-header"><span class="dash-card-title">Live Machine Status</span><span class="dash-card-badge">Updated: 12:32 PM</span></div>
  <div class="machine-grid">
    <div class="machine-tile running"><div class="machine-name">CNC Mach #1</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0412 | 87% OEE</div></div>
    <div class="machine-tile running"><div class="machine-name">CNC Mach #2</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0408 | 91% OEE</div></div>
    <div class="machine-tile idle"><div class="machine-name">Assembly Line 1</div><div class="machine-status-dot"></div><div class="machine-label">Idle</div><div class="machine-meta">Setup in progress</div></div>
    <div class="machine-tile running"><div class="machine-name">Assembly Line 2</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0413 | 78% OEE</div></div>
    <div class="machine-tile down"><div class="machine-name">Painting Booth</div><div class="machine-status-dot"></div><div class="machine-label">Breakdown</div><div class="machine-meta">Since 10:15 AM | 1h 17m</div></div>
    <div class="machine-tile maintenance"><div class="machine-name">Welding Bay</div><div class="machine-status-dot"></div><div class="machine-label">Maintenance</div><div class="machine-meta">PM Scheduled</div></div>
    <div class="machine-tile running"><div class="machine-name">Packaging Stn</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0409 | 95% OEE</div></div>
    <div class="machine-tile idle"><div class="machine-name">QC Station</div><div class="machine-status-dot"></div><div class="machine-label">Idle</div><div class="machine-meta">Awaiting batch</div></div>
  </div>
</div>

<div class="dashboard-row">
  <div class="card dash-card" style="flex:2;">
    <div class="dash-card-header"><span class="dash-card-title">Active Jobs — Current Shift</span><a href="#" style="font-size:12px; color:var(--brand-yellow); text-decoration:none;">View All</a></div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>WO Number</th><th>Operation</th><th>Work Center</th><th>Operator</th><th>Progress</th><th>Output</th><th>Status</th></tr></thead>
        <tbody>
          <tr>
            <td style="font-weight:600;">WO-2026-0412</td><td>Assembly</td><td>Assembly Line 2</td><td>Khalid M.</td>
            <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:80px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:71%;background:#f59e0b;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">71%</span></div></td>
            <td>142 / 200</td><td><span class="status-badge status-inprogress">In Progress</span></td>
          </tr>
          <tr>
            <td style="font-weight:600;">WO-2026-0408</td><td>Welding</td><td>Welding Bay</td><td>Sara M.</td>
            <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:80px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:30%;background:#f59e0b;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">30%</span></div></td>
            <td>45 / 150</td><td><span class="status-badge status-inprogress">In Progress</span></td>
          </tr>
          <tr>
            <td style="font-weight:600;">WO-2026-0413</td><td>Packaging</td><td>Packaging Stn</td><td>Rami H.</td>
            <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:80px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:95%;background:#22c55e;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">95%</span></div></td>
            <td>285 / 300</td><td><span class="status-badge status-inprogress">In Progress</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="card dash-card" style="flex:1;">
    <div class="dash-card-header"><span class="dash-card-title">Downtime Alerts</span><span class="dash-card-badge" style="background:#fee2e2;color:#991b1b;">3 Active</span></div>
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div style="border-left:3px solid #ef4444;padding:8px 12px;background:#fff5f5;border-radius:4px;">
        <div style="font-size:13px;font-weight:600;color:#0f172a;">Painting Booth — Breakdown</div>
        <div style="font-size:12px;color:#64748b;">Since 10:15 AM &nbsp;|&nbsp; 1h 17m elapsed</div>
        <div style="font-size:12px;color:#ef4444;margin-top:2px;">Reason: Nozzle Blockage</div>
      </div>
      <div style="border-left:3px solid #f59e0b;padding:8px 12px;background:#fffbeb;border-radius:4px;">
        <div style="font-size:13px;font-weight:600;color:#0f172a;">Assembly Line 1 — Setup Delay</div>
        <div style="font-size:12px;color:#64748b;">Since 11:30 AM &nbsp;|&nbsp; 1h elapsed</div>
        <div style="font-size:12px;color:#f59e0b;margin-top:2px;">Reason: Changeover in progress</div>
      </div>
      <div style="border-left:3px solid #3b82f6;padding:8px 12px;background:#eff6ff;border-radius:4px;">
        <div style="font-size:13px;font-weight:600;color:#0f172a;">Welding Bay — Scheduled PM</div>
        <div style="font-size:12px;color:#64748b;">Since 09:00 AM &nbsp;|&nbsp; 3h 32m elapsed</div>
        <div style="font-size:12px;color:#3b82f6;margin-top:2px;">Reason: Preventive Maintenance</div>
      </div>
    </div>
  </div>
</div>
"""

SFE_MONITORING_HTML = """
<div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
  <button class="btn btn-outline" style="font-size:12px;">All Lines</button>
  <button class="btn btn-primary" style="font-size:12px;">Running (6)</button>
  <button class="btn btn-outline" style="font-size:12px;border-color:#f59e0b;color:#f59e0b;">Idle (2)</button>
  <button class="btn btn-outline" style="font-size:12px;border-color:#ef4444;color:#ef4444;">Down (1)</button>
  <div style="margin-left:auto; display:flex; gap:8px;">
    <button class="btn btn-outline">
      <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 .49-3.5"></path></svg>
      Auto Refresh (30s)
    </button>
  </div>
</div>
<div class="card">
  <div class="toolbar">
    <div class="toolbar-left">
      <div class="search-box">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" placeholder="Search jobs..." oninput="const q = this.value.toLowerCase(); this.closest('.card').querySelectorAll('.data-table tbody tr').forEach(r => r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none');">
      </div>
    </div>
    <div class="toolbar-right">
      <span style="font-size:12px;color:#64748b;">Last updated: 12:32 PM</span>
    </div>
  </div>
  <div class="table-responsive">
    <table class="data-table">
      <thead><tr><th>WO Number</th><th>Item</th><th>Operation</th><th>Work Center</th><th>Operator</th><th>Shift</th><th>Target Qty</th><th>Produced</th><th>Scrap</th><th>Progress</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td style="font-weight:600;">WO-2026-0412</td><td>Wooden Chair</td><td>Assembly</td><td>Assembly Line 2</td><td>Khalid M.</td><td>Morning</td><td>200</td><td style="font-weight:600;color:#22c55e;">142</td><td>0</td>
          <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:70px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:71%;background:#f59e0b;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">71%</span></div></td>
          <td><span class="status-badge status-inprogress">In Progress</span></td>
        </tr>
        <tr><td style="font-weight:600;">WO-2026-0408</td><td>Steel Shelf Unit</td><td>Welding</td><td>Welding Bay</td><td>Sara M.</td><td>Morning</td><td>150</td><td style="font-weight:600;color:#22c55e;">45</td><td>0</td>
          <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:70px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:30%;background:#f59e0b;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">30%</span></div></td>
          <td><span class="status-badge status-inprogress">In Progress</span></td>
        </tr>
        <tr><td style="font-weight:600;">WO-2026-0413</td><td>Powder Coat Frame</td><td>Packaging</td><td>Packaging Stn</td><td>Rami H.</td><td>Morning</td><td>300</td><td style="font-weight:600;color:#22c55e;">285</td><td>1</td>
          <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:70px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:95%;background:#22c55e;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">95%</span></div></td>
          <td><span class="status-badge status-inprogress">In Progress</span></td>
        </tr>
        <tr><td style="font-weight:600;">WO-2026-0411</td><td>Metal Desk Frame</td><td>QC Inspection</td><td>QC Station</td><td>—</td><td>Morning</td><td>80</td><td>0</td><td>0</td>
          <td><div style="display:flex;align-items:center;gap:6px;"><div style="width:70px;background:#f1f5f9;border-radius:999px;height:6px;"><div style="width:0%;background:#94a3b8;height:100%;border-radius:999px;"></div></div><span style="font-size:12px;">0%</span></div></td>
          <td><span class="status-badge status-draft">Waiting</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

SFE_OPERATOR_HTML = """
<div style="display:grid;grid-template-columns:1fr 2fr;gap:16px;margin-top:8px;">
  <!-- Operator Profile -->
  <div style="display:flex;flex-direction:column;gap:16px;">
    <div class="card" style="padding:24px;text-align:center;">
      <div style="width:64px;height:64px;border-radius:50%;background:var(--brand-yellow);color:#0f172a;font-size:22px;font-weight:700;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;">KM</div>
      <div style="font-size:16px;font-weight:700;color:#0f172a;">Khalid Mohammed</div>
      <div style="font-size:12px;color:#64748b;margin-top:4px;">Operator ID: EMP-0042</div>
      <div style="margin-top:12px;"><span class="status-badge status-active">Active — Morning Shift</span></div>
      <div style="margin-top:16px;display:flex;flex-direction:column;gap:8px;text-align:left;">
        <div style="font-size:12px;color:#64748b;">Work Center: <span style="color:#0f172a;font-weight:600;">Assembly Line 2</span></div>
        <div style="font-size:12px;color:#64748b;">Shift Start: <span style="color:#0f172a;font-weight:600;">06:00 AM</span></div>
        <div style="font-size:12px;color:#64748b;">Logged In: <span style="color:#22c55e;font-weight:600;">06:03 AM</span></div>
        <div style="font-size:12px;color:#64748b;">Hours Worked: <span style="color:#0f172a;font-weight:600;">6h 29m</span></div>
      </div>
    </div>
    <div class="card" style="padding:20px;">
      <div class="form-section-title">Today's Output</div>
      <div style="display:flex;flex-direction:column;gap:12px;">
        <div><div style="font-size:11px;color:#64748b;margin-bottom:4px;">Qty Produced</div><div style="font-size:24px;font-weight:700;color:#22c55e;">142 Pcs</div></div>
        <div><div style="font-size:11px;color:#64748b;margin-bottom:4px;">Scrap</div><div style="font-size:24px;font-weight:700;color:#ef4444;">0 Pcs</div></div>
        <div><div style="font-size:11px;color:#64748b;margin-bottom:4px;">Efficiency</div><div style="font-size:24px;font-weight:700;color:#f59e0b;">87%</div></div>
      </div>
    </div>
  </div>

  <!-- Assigned Jobs -->
  <div style="display:flex;flex-direction:column;gap:16px;">
    <div class="card" style="padding:20px;">
      <div class="form-section-title">Current Assignment</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">
        <div style="background:#f8fafc;border-radius:8px;padding:14px;"><div style="font-size:11px;color:#64748b;">Work Order</div><div style="font-size:14px;font-weight:700;color:#0f172a;margin-top:4px;">WO-2026-0412</div></div>
        <div style="background:#f8fafc;border-radius:8px;padding:14px;"><div style="font-size:11px;color:#64748b;">Operation</div><div style="font-size:14px;font-weight:700;color:#0f172a;margin-top:4px;">Assembly</div></div>
        <div style="background:#f8fafc;border-radius:8px;padding:14px;"><div style="font-size:11px;color:#64748b;">Target</div><div style="font-size:14px;font-weight:700;color:#0f172a;margin-top:4px;">200 Pcs</div></div>
      </div>
      <div style="margin-bottom:8px;font-size:12px;font-weight:600;color:#64748b;">Progress — 142 / 200 Pcs (71%)</div>
      <div style="background:#f1f5f9;border-radius:999px;height:12px;"><div style="width:71%;background:var(--brand-yellow);height:100%;border-radius:999px;"></div></div>
      <div style="display:flex;gap:10px;margin-top:16px;">
        <button class="btn btn-primary">Log Production Entry</button>
        <button class="btn btn-outline" style="border-color:#ef4444;color:#ef4444;">Report Downtime</button>
      </div>
    </div>

    <div class="card" style="padding:20px;">
      <div class="form-section-title">Job Queue (Today)</div>
      <div class="table-responsive">
        <table class="data-table" style="margin-top:0;">
          <thead><tr><th>WO Number</th><th>Operation</th><th>Qty</th><th>Priority</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td style="font-weight:600;">WO-2026-0412</td><td>Assembly</td><td>200</td><td><span style="color:#ef4444;font-weight:600;">High</span></td><td><span class="status-badge status-inprogress">In Progress</span></td></tr>
            <tr><td style="font-weight:600;">WO-2026-0410</td><td>Assembly</td><td>60</td><td><span style="color:#f59e0b;font-weight:600;">Medium</span></td><td><span class="status-badge status-draft">Pending</span></td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card" style="padding:20px;">
      <div class="form-section-title">Today's Time Log</div>
      <div class="table-responsive">
        <table class="data-table" style="margin-top:0;">
          <thead><tr><th>Activity</th><th>WO / Operation</th><th>Start</th><th>End</th><th>Duration</th></tr></thead>
          <tbody>
            <tr><td><span class="status-badge status-active">Production</span></td><td>WO-0412 / Assembly</td><td>10:00 AM</td><td>—</td><td>2h 32m</td></tr>
            <tr><td><span class="status-badge status-draft">Break</span></td><td>—</td><td>09:30 AM</td><td>10:00 AM</td><td>30 min</td></tr>
            <tr><td><span class="status-badge status-active">Production</span></td><td>WO-0412 / Assembly</td><td>06:03 AM</td><td>09:30 AM</td><td>3h 27m</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
"""

SFE_MACHINES_HTML = """
<div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center;">
  <button class="btn btn-primary" style="font-size:12px;">All (8)</button>
  <button class="btn btn-outline" style="font-size:12px;border-color:#22c55e;color:#22c55e;">Running (5)</button>
  <button class="btn btn-outline" style="font-size:12px;border-color:#94a3b8;color:#94a3b8;">Idle (2)</button>
  <button class="btn btn-outline" style="font-size:12px;border-color:#ef4444;color:#ef4444;">Down (1)</button>
  <div style="margin-left:auto;display:flex;gap:8px;">
    <button class="btn btn-outline"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 .49-3.5"></path></svg>Refresh</button>
  </div>
</div>
<div class="machine-grid" style="grid-template-columns:repeat(4,1fr);">
  <div class="machine-tile running"><div class="machine-name">CNC Machine #1</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0412 · Cutting</div><div style="margin-top:8px;font-size:11px;color:#64748b;">OEE: <span style="font-weight:700;color:#22c55e;">87%</span> &nbsp;|&nbsp; Output: <span style="font-weight:600;">200 Pcs</span></div></div>
  <div class="machine-tile running"><div class="machine-name">CNC Machine #2</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0408 · Cutting</div><div style="margin-top:8px;font-size:11px;color:#64748b;">OEE: <span style="font-weight:700;color:#22c55e;">91%</span> &nbsp;|&nbsp; Output: <span style="font-weight:600;">45 Pcs</span></div></div>
  <div class="machine-tile idle"><div class="machine-name">Assembly Line 1</div><div class="machine-status-dot"></div><div class="machine-label">Idle</div><div class="machine-meta">Setup / Changeover</div><div style="margin-top:8px;font-size:11px;color:#64748b;">OEE: <span style="font-weight:700;color:#94a3b8;">—</span> &nbsp;|&nbsp; Since: <span style="font-weight:600;">11:30 AM</span></div></div>
  <div class="machine-tile running"><div class="machine-name">Assembly Line 2</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0412 · Assembly</div><div style="margin-top:8px;font-size:11px;color:#64748b;">OEE: <span style="font-weight:700;color:#f59e0b;">78%</span> &nbsp;|&nbsp; Output: <span style="font-weight:600;">142 Pcs</span></div></div>
  <div class="machine-tile down"><div class="machine-name">Painting Booth</div><div class="machine-status-dot"></div><div class="machine-label">Breakdown</div><div class="machine-meta">Nozzle Blockage</div><div style="margin-top:8px;font-size:11px;color:#64748b;">Down since: <span style="font-weight:700;color:#ef4444;">10:15 AM</span> &nbsp;|&nbsp; 1h 17m</div></div>
  <div class="machine-tile maintenance"><div class="machine-name">Welding Bay</div><div class="machine-status-dot"></div><div class="machine-label">Maintenance</div><div class="machine-meta">Scheduled PM</div><div style="margin-top:8px;font-size:11px;color:#64748b;">Since: <span style="font-weight:700;color:#3b82f6;">09:00 AM</span> &nbsp;|&nbsp; 3h 32m</div></div>
  <div class="machine-tile running"><div class="machine-name">Packaging Stn</div><div class="machine-status-dot"></div><div class="machine-label">Running</div><div class="machine-meta">WO-2026-0413 · Packaging</div><div style="margin-top:8px;font-size:11px;color:#64748b;">OEE: <span style="font-weight:700;color:#22c55e;">95%</span> &nbsp;|&nbsp; Output: <span style="font-weight:600;">285 Pcs</span></div></div>
  <div class="machine-tile idle"><div class="machine-name">QC Station</div><div class="machine-status-dot"></div><div class="machine-label">Idle</div><div class="machine-meta">Awaiting batch</div><div style="margin-top:8px;font-size:11px;color:#64748b;">OEE: <span style="font-weight:700;color:#94a3b8;">—</span> &nbsp;|&nbsp; Since: <span style="font-weight:600;">09:45 AM</span></div></div>
</div>
"""

def build_sfe_form(form_type):
    if form_type == "job_assign":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Job Assignment</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Shop Floor Execution &rsaquo; Job Assignment</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Assign Jobs</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>Assignment Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Work Order <span class="req">*</span></label><input type="text" placeholder="WO-2026-..."></div>
      <div class="form-group"><label>Operation <span class="req">*</span></label><select><option>Select operation...</option><option>Cutting</option><option>Assembly</option><option>Painting</option><option>QC Inspection</option></select></div>
      <div class="form-group"><label>Work Center <span class="req">*</span></label><input type="text" placeholder="Select work center..."></div>
      <div class="form-group"><label>Operator <span class="req">*</span></label><select><option>Select operator...</option><option>Ahmed K.</option><option>Khalid M.</option><option>Sara M.</option><option>Rami H.</option></select></div>
      <div class="form-group"><label>Machine / Resource</label><select><option>Auto-assign</option><option>CNC Machine #1</option><option>CNC Machine #2</option><option>Assembly Line 1</option><option>Assembly Line 2</option></select></div>
      <div class="form-group"><label>Planned Start Time</label><input type="time" value="06:00"></div>
      <div class="form-group"><label>Target Quantity <span class="req">*</span></label><input type="number" placeholder="0"></div>
      <div class="form-group"><label>Priority</label><select><option>High</option><option>Medium</option><option>Low</option></select></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Available Operators</div>
    <div class="table-responsive">
      <table class="data-table"><thead><tr><th>Operator</th><th>Work Center</th><th>Current Status</th><th>Skills</th><th>Availability</th></tr></thead>
      <tbody>
        <tr><td>Ahmed K.</td><td>CNC Machining</td><td><span class="status-badge status-active">Available</span></td><td>CNC, Cutting, Welding</td><td>From 06:00 AM</td></tr>
        <tr><td>Khalid M.</td><td>Assembly Line 2</td><td><span class="status-badge status-inprogress">Busy</span></td><td>Assembly, Packaging</td><td>From 02:00 PM</td></tr>
        <tr><td>Sara M.</td><td>Welding Bay</td><td><span class="status-badge status-inprogress">Busy</span></td><td>Welding, Fabrication</td><td>From 01:00 PM</td></tr>
        <tr><td>Rami H.</td><td>Packaging Stn</td><td><span class="status-badge status-active">Available</span></td><td>Packaging, QC</td><td>From 06:00 AM</td></tr>
      </tbody></table>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Assignments are logged in the Activity Log for audit purposes.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Assign Jobs</button></div>
  </div>
</div>"""

    elif form_type == "production_entry":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Production Entry — Operation Confirmation</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Shop Floor Execution &rsaquo; Production Entry</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Confirm Production</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>Work Order Reference</div>
    <div class="form-grid">
      <div class="form-group"><label>Work Order # <span class="req">*</span></label><input type="text" value="WO-2026-0412" placeholder="Scan or enter WO..."></div>
      <div class="form-group"><label>Operation <span class="req">*</span></label><input type="text" value="Assembly" readonly></div>
      <div class="form-group"><label>Work Center</label><input type="text" value="Assembly Line 2" readonly></div>
      <div class="form-group"><label>Operator</label><input type="text" value="Khalid Mohammed" readonly></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>Production Quantities</div>
    <div class="form-grid">
      <div class="form-group"><label>Qty to Confirm <span class="req">*</span></label><input type="number" placeholder="0" value="58"></div>
      <div class="form-group"><label>Scrap Qty</label><input type="number" placeholder="0" value="0"></div>
      <div class="form-group"><label>Rework Qty</label><input type="number" placeholder="0" value="0"></div>
      <div class="form-group"><label>UoM</label><input type="text" value="Pcs" readonly></div>
      <div class="form-group"><label>Posting Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Posting Time</label><input type="time" value="12:32"></div>
      <div class="form-group"><label>Actual Start Time</label><input type="time" value="10:00"></div>
      <div class="form-group"><label>Actual End Time</label><input type="time" value="12:30"></div>
    </div>
    <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:14px;margin-top:12px;">
      <div style="font-size:13px;font-weight:600;color:#166534;">Summary after this entry:</div>
      <div style="display:flex;gap:24px;margin-top:8px;font-size:13px;">
        <span>Previously: <b>142 Pcs</b></span>
        <span>This Entry: <b>+58 Pcs</b></span>
        <span>Total After: <b style="color:#166534;">200 Pcs ✔ Complete</b></span>
      </div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Notes</div>
    <div class="form-grid" style="grid-template-columns:1fr;"><div class="form-group"><textarea rows="3" placeholder="Production remarks..."></textarea></div></div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Material backflush will be posted automatically on confirmation.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Confirm Production</button></div>
  </div>
</div>"""

    elif form_type == "downtime":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Downtime Recording</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Shop Floor Execution &rsaquo; Downtime Recording</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary" style="background:#ef4444;color:#fff;">Record Downtime</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>Downtime Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Machine / Work Center <span class="req">*</span></label><select><option>Painting Booth</option><option>CNC Machine #1</option><option>Assembly Line 1</option><option>Welding Bay</option></select></div>
      <div class="form-group"><label>Downtime Type <span class="req">*</span></label><select><option>Breakdown</option><option>Planned Maintenance</option><option>Setup / Changeover</option><option>No Material</option><option>No Operator</option><option>Quality Issue</option></select></div>
      <div class="form-group"><label>Reason Code <span class="req">*</span></label><select><option>DT-001: Nozzle Blockage</option><option>DT-002: Motor Failure</option><option>DT-003: Power Outage</option><option>DT-004: Tooling Worn</option></select></div>
      <div class="form-group"><label>Reported By</label><input type="text" value="Ahmed K."></div>
      <div class="form-group"><label>Start Date/Time <span class="req">*</span></label><input type="datetime-local" value="2026-07-22T10:15"></div>
      <div class="form-group"><label>End Date/Time</label><input type="datetime-local" placeholder="If still ongoing, leave blank"></div>
      <div class="form-group"><label>Linked WO (if any)</label><input type="text" placeholder="WO-2026-..."></div>
      <div class="form-group"><label>Maintenance Request?</label><select><option>Yes — Create MWO</option><option>No</option></select></div>
    </div>
    <div class="form-grid" style="grid-template-columns:1fr;margin-top:12px;"><div class="form-group"><label>Description / Action Taken</label><textarea rows="3" placeholder="Describe the issue and actions taken...">Nozzle on Painting Booth blocked. Maintenance called.</textarea></div></div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Downtime is posted to the OEE and maintenance reports automatically.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary" style="background:#ef4444;color:#fff;">Record Downtime</button></div>
  </div>
</div>"""

    elif form_type == "labor":
        return """
<div class="wo-form-wrapper">
  <div class="form-header-bar">
    <div><h2 style="margin:0;font-size:16px;font-weight:700;color:#0f172a;">Labor Time Entry</h2>
    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Shop Floor Execution &rsaquo; Labor Time Entry</div></div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Save Time Entry</button></div>
  </div>
  <div class="form-section card">
    <div class="form-section-title"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>Time Entry Details</div>
    <div class="form-grid">
      <div class="form-group"><label>Operator <span class="req">*</span></label><select><option>Khalid Mohammed</option><option>Ahmed K.</option><option>Sara M.</option></select></div>
      <div class="form-group"><label>Work Order <span class="req">*</span></label><input type="text" value="WO-2026-0412" placeholder="WO-2026-..."></div>
      <div class="form-group"><label>Operation <span class="req">*</span></label><select><option>Assembly</option><option>Cutting</option><option>Painting</option></select></div>
      <div class="form-group"><label>Activity Type</label><select><option>Production</option><option>Setup</option><option>Rework</option><option>Training</option></select></div>
      <div class="form-group"><label>Date <span class="req">*</span></label><input type="date" value="2026-07-22"></div>
      <div class="form-group"><label>Start Time <span class="req">*</span></label><input type="time" value="10:00"></div>
      <div class="form-group"><label>End Time <span class="req">*</span></label><input type="time" value="12:32"></div>
      <div class="form-group"><label>Duration (Auto)</label><input type="text" value="2h 32m" readonly style="background:#f8fafc;color:#64748b;"></div>
    </div>
  </div>
  <div class="form-section card">
    <div class="form-section-title">Today's Time Log — Khalid Mohammed</div>
    <div class="table-responsive">
      <table class="data-table" style="margin-top:0;">
        <thead><tr><th>Activity</th><th>WO / Operation</th><th>Start</th><th>End</th><th>Duration</th></tr></thead>
        <tbody>
          <tr><td><span class="status-badge status-active">Production</span></td><td>WO-0412 / Assembly</td><td>10:00 AM</td><td>12:32 PM</td><td>2h 32m</td></tr>
          <tr><td><span class="status-badge status-draft">Break</span></td><td>—</td><td>09:30 AM</td><td>10:00 AM</td><td>30 min</td></tr>
          <tr><td><span class="status-badge status-active">Production</span></td><td>WO-0412 / Assembly</td><td>06:03 AM</td><td>09:30 AM</td><td>3h 27m</td></tr>
        </tbody>
      </table>
    </div>
    <div style="display:flex;justify-content:flex-end;padding:12px 0 0;gap:24px;font-size:13px;font-weight:600;">
      <span>Total Production: <span style="color:#22c55e;">5h 59m</span></span>
      <span>Break: <span style="color:#94a3b8;">30m</span></span>
      <span>Total Logged: <span style="color:#0f172a;">6h 29m</span></span>
    </div>
  </div>
  <div class="form-footer">
    <div style="font-size:12px;color:#94a3b8;">Time entries are used for labor cost calculation and payroll export.</div>
    <div style="display:flex;gap:10px;"><button class="btn btn-outline">Cancel</button><button class="btn btn-primary">Save Time Entry</button></div>
  </div>
</div>"""
    return ""

# ─────────────────────────────────────────────
# BUILD CONTENT MAP (page_id → html string)
# ─────────────────────────────────────────────
content_map = {}
for page_id, cfg in PAGE_CONFIGS.items():
    ptype = cfg.get("type", "list")
    title = page_id.replace("_", " ").title()
    if ptype == "dashboard":
        content_map[page_id] = DASHBOARD_HTML
    elif ptype == "wo_dashboard":
        content_map[page_id] = WO_DASHBOARD_HTML
    elif ptype == "wo_form":
        content_map[page_id] = build_wo_form_html(cfg.get("mode", "create"))
    elif ptype == "wo_detail":
        content_map[page_id] = WO_DETAIL_HTML
    elif ptype == "sfe_dashboard":
        content_map[page_id] = SFE_DASHBOARD_HTML
    elif ptype == "sfe_monitoring":
        content_map[page_id] = SFE_MONITORING_HTML
    elif ptype == "sfe_operator":
        content_map[page_id] = SFE_OPERATOR_HTML
    elif ptype == "sfe_machines":
        content_map[page_id] = SFE_MACHINES_HTML
    elif ptype == "sfe_job_assign_form":
        content_map[page_id] = build_sfe_form("job_assign")
    elif ptype == "sfe_production_form":
        content_map[page_id] = build_sfe_form("production_entry")
    elif ptype == "sfe_downtime_form":
        content_map[page_id] = build_sfe_form("downtime")
    elif ptype == "sfe_labor_form":
        content_map[page_id] = build_sfe_form("labor")
    elif ptype == "mm_dashboard":
        content_map[page_id] = MM_DASHBOARD_HTML
    elif ptype == "mm_stock_view":
        content_map[page_id] = MM_STOCK_VIEW_HTML
    elif ptype == "mm_mr_form":
        content_map[page_id] = build_mm_form("mr")
    elif ptype == "mm_mi_form":
        content_map[page_id] = build_mm_form("mi")
    elif ptype == "mm_grn_form":
        content_map[page_id] = build_mm_form("grn")
    elif ptype == "mm_mt_form":
        content_map[page_id] = build_mm_form("mt")
    elif ptype == "mm_adj_form":
        content_map[page_id] = build_mm_form("adj")
    elif ptype == "mm_cc_form":
        content_map[page_id] = build_mm_form("cc")
    elif ptype == "mm_pi_form":
        content_map[page_id] = build_mm_form("pi")
    elif ptype == "qm_dashboard":
        content_map[page_id] = QM_DASHBOARD_HTML
    elif ptype == "qm_iqc_form":
        content_map[page_id] = build_qm_form("iqc")
    elif ptype == "qm_ipqc_form":
        content_map[page_id] = build_qm_form("ipqc")
    elif ptype == "qm_oqc_form":
        content_map[page_id] = build_qm_form("oqc")
    elif ptype == "qm_ncr_form":
        content_map[page_id] = build_qm_form("ncr")
    elif ptype == "qm_capa_form":
        content_map[page_id] = build_qm_form("capa")
    elif ptype == "mnt_dashboard":
        content_map[page_id] = MNT_DASHBOARD_HTML
    elif ptype == "sub_dashboard":
        content_map[page_id] = SUB_DASHBOARD_HTML
    elif ptype == "sub_order_form":
        content_map[page_id] = build_sub_form("order")
    elif ptype == "sub_issue_form":
        content_map[page_id] = build_sub_form("issue")
    elif ptype == "sub_receipt_form":
        content_map[page_id] = build_sub_form("receipt")
    elif ptype == "pc_dashboard":
        content_map[page_id] = PC_DASHBOARD_HTML
    elif ptype == "pc_rollup_form":
        content_map[page_id] = build_pc_form("rollup")
    elif ptype in ["ar_exec_dashboard", "ar_prod_kpi", "ar_inv_dash", "ar_oee_dash", "ar_qm_dash", "ar_mnt_dash", "ar_cost_dash"]:
        content_map[page_id] = AR_EXEC_DASHBOARD_HTML
    else:
        content_map[page_id] = build_list_html(page_id, cfg, title)

# ─────────────────────────────────────────────
# LOAD NAV DATA & BUILD FULL CONTENT MAP
# ─────────────────────────────────────────────
nav_data = json.load(open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\output_data.json', encoding='utf-8'))
config = nav_data['config']

for page_id, info in config.items():
    if page_id not in content_map:
        t = info.get('title', page_id.replace('_', ' ').title())
        grp = info.get('group', 'General')
        content_map[page_id] = build_list_html(page_id, {
            "type": "list",
            "columns": ["Record Code", "Item / Description", "Category / Group", "Reference Code", "Date Created", "Status", "Actions"],
            "rows": [
                {"Record Code": f"REC-2026-001", "Item / Description": f"{t} Primary Record", "Category / Group": grp, "Reference Code": "REF-8801", "Date Created": "2026-07-22", "Status": "active"},
                {"Record Code": f"REC-2026-002", "Item / Description": f"{t} Operational Entry", "Category / Group": grp, "Reference Code": "REF-8802", "Date Created": "2026-07-20", "Status": "completed"},
                {"Record Code": f"REC-2026-003", "Item / Description": f"{t} Pending Review", "Category / Group": grp, "Reference Code": "REF-8803", "Date Created": "2026-07-18", "Status": "pending"},
            ]
        }, t)

content_map_js = json.dumps(content_map)

groups = {}
for page_id, info in config.items():
    g = info['group']
    if g not in groups:
        groups[g] = []
    groups[g].append({'id': page_id, 'title': info['title'], 'url': info['url']})

groups_json = json.dumps(groups, indent=4)
config_json = json.dumps(config, indent=4)

# ─────────────────────────────────────────────
# HTML TEMPLATE
# ─────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AureliaHRMS · Manufacturing</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{{{ url_for('static', filename='css/payroll.css') }}}}">
  <script src="{{{{ url_for('static', filename='js/global_search.js') }}}}"></script>
  <style>
    html, body {{ width:100vw; height:100vh; overflow:hidden; margin:0; padding:0; background:#f8fafc; }}
    .main-wrapper {{ width:calc(100vw - 200px); height:100vh; display:flex; flex-direction:column; overflow:hidden; }}
    .content {{ height:calc(100vh - 60px); overflow-y:auto; padding:16px; }}

    /* ── Tabs ── */
    .nav-tab {{ display:flex; align-items:center; gap:8px; }}
    .nav-tab .close-btn {{ display:inline-flex; align-items:center; justify-content:center; width:16px; height:16px; border-radius:50%; background:transparent; color:inherit; opacity:.6; font-size:14px; transition:all .2s; }}
    .nav-tab .close-btn:hover {{ background:rgba(0,0,0,.1); opacity:1; }}
    .top-nav .nav-links {{ gap:12px; }}

    /* ── Dropdown ── */
    .dropdown {{ position:relative; display:inline-block; margin-left:12px; }}
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
    .top-right-icons {{ display:flex; align-items:center; gap:16px; color:var(--text-light); margin-right:16px; }}
    .top-right-icons svg {{ cursor:pointer; }}
    .bell-icon-container {{ position:relative; display:inline-flex; }}
    .bell-dot {{ position:absolute; top:0; right:2px; width:6px; height:6px; background:#ef4444; border-radius:50%; border:1px solid var(--topbar-bg); }}

    /* ── Data grid ── */
    .card {{ background:#fff; border:1px solid #e2e8f0; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,.05); margin-top:16px; }}
    .toolbar {{ display:flex; justify-content:space-between; align-items:center; padding:16px 20px; border-bottom:1px solid #e2e8f0; flex-wrap:wrap; gap:10px; }}
    .toolbar-left, .toolbar-right {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
    .search-box {{ position:relative; }}
    .search-box svg {{ position:absolute; left:10px; top:50%; transform:translateY(-50%); color:#94a3b8; }}
    .search-box input {{ padding:8px 12px 8px 32px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; width:220px; outline:none; transition:border-color .2s; }}
    .search-box input:focus {{ border-color:var(--brand-yellow); }}
    .btn {{ display:inline-flex; align-items:center; gap:6px; padding:8px 14px; font-size:13px; font-weight:500; border-radius:6px; cursor:pointer; transition:all .2s; border:none; }}
    .btn-primary {{ background:var(--brand-yellow); color:#0f172a; }}
    .btn-primary:hover {{ filter:brightness(1.05); }}
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
    .page-btn.active {{ background:var(--brand-yellow); border-color:var(--brand-yellow); color:#0f172a; font-weight:600; }}
    .page-btn:hover:not(.active) {{ background:#f8fafc; }}

    /* ── Status Badges ── */
    .status-badge {{ display:inline-block; padding:3px 9px; border-radius:12px; font-size:11px; font-weight:600; }}
    .status-active      {{ background:#dcfce7; color:#166534; }}
    .status-inactive    {{ background:#f1f5f9; color:#475569; }}
    .status-approved    {{ background:#dbeafe; color:#1e40af; }}
    .status-inprogress  {{ background:#fef9c3; color:#854d0e; }}
    .status-draft       {{ background:#f1f5f9; color:#475569; }}
    .status-completed   {{ background:#dcfce7; color:#166534; }}
    .status-pending     {{ background:#fff7ed; color:#c2410c; }}
    .status-rejected    {{ background:#fee2e2; color:#991b1b; }}
    .status-overloaded  {{ background:#fee2e2; color:#991b1b; }}
    .status-underutil   {{ background:#e0f2fe; color:#0369a1; }}

    /* ── Dashboard ── */
    .dashboard-kpi-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:16px; }}
    .kpi-card {{ background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:20px; display:flex; align-items:flex-start; gap:14px; box-shadow:0 1px 3px rgba(0,0,0,.05); }}
    .kpi-icon {{ width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
    .kpi-blue   {{ background:#dbeafe; color:#2563eb; }}
    .kpi-green  {{ background:#dcfce7; color:#16a34a; }}
    .kpi-orange {{ background:#fff7ed; color:#ea580c; }}
    .kpi-purple {{ background:#f5f3ff; color:#7c3aed; }}
    .kpi-body {{ flex:1; }}
    .kpi-value {{ font-size:26px; font-weight:700; color:#0f172a; line-height:1; }}
    .kpi-label {{ font-size:12px; color:#64748b; margin-top:4px; }}
    .kpi-trend {{ font-size:11px; margin-top:6px; white-space:nowrap; }}
    .kpi-trend.up   {{ color:#16a34a; }}
    .kpi-trend.down {{ color:#ef4444; }}
    .kpi-trend.neutral {{ color:#64748b; }}
    .dashboard-row {{ display:flex; gap:16px; margin-top:16px; }}
    .dash-card {{ padding:20px; flex:1; }}
    .dash-card-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }}
    .dash-card-title {{ font-size:14px; font-weight:600; color:#0f172a; }}
    .dash-card-badge {{ font-size:11px; background:#f1f5f9; color:#475569; padding:3px 8px; border-radius:12px; }}
    .chart-placeholder {{ }}
    .chart-bars {{ display:flex; align-items:flex-end; gap:16px; height:130px; padding:0 8px; }}
    .chart-bar-group {{ display:flex; gap:4px; align-items:flex-end; flex-direction:column; }}
    .chart-bar {{ width:28px; border-radius:4px 4px 0 0; transition:opacity .2s; }}
    .chart-bar:hover {{ opacity:.8; }}
    .planned {{ background:#cbd5e1; }}
    .actual  {{ background:var(--brand-yellow); }}
    .bar-label {{ font-size:11px; color:#94a3b8; text-align:center; width:100%; margin-top:4px; }}
    .chart-bars {{ flex-direction:row; align-items:flex-end; }}
    .chart-bar-group {{ flex-direction:row; align-items:flex-end; }}
    .chart-legend {{ display:flex; align-items:center; gap:6px; font-size:11px; color:#64748b; margin-top:12px; }}
    .legend-dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
    .planned-dot {{ background:#cbd5e1; }}
    .actual-dot  {{ background:var(--brand-yellow); }}
    .capacity-list {{ display:flex; flex-direction:column; gap:14px; }}
    .cap-row {{ display:flex; align-items:center; gap:10px; font-size:12.5px; color:#334155; }}
    .cap-row > span:first-child {{ width:130px; flex-shrink:0; }}
    .cap-bar-wrap {{ flex:1; background:#f1f5f9; border-radius:999px; height:8px; overflow:hidden; }}
    .cap-bar {{ height:100%; border-radius:999px; transition:width .4s; }}
    .cap-pct {{ width:38px; text-align:right; font-weight:600; font-size:12px; color:#475569; }}

    /* ── Form / Detail View ── */
    .wo-form-wrapper {{ display:flex; flex-direction:column; gap:16px; }}
    .form-header-bar {{ display:flex; justify-content:space-between; align-items:center; margin-top:4px; }}
    .form-section {{ padding:20px; }}
    .form-section-title {{ display:flex; align-items:center; gap:8px; font-size:13px; font-weight:700; color:#0f172a; margin-bottom:16px; border-bottom:1px solid #f1f5f9; padding-bottom:12px; }}
    .form-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }}
    .form-group {{ display:flex; flex-direction:column; gap:6px; }}
    .form-group label {{ font-size:12px; font-weight:600; color:#475569; }}
    .form-group input, .form-group select, .form-group textarea {{
      padding:8px 10px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; color:#0f172a;
      outline:none; transition:border-color .2s; font-family:inherit; width:100%; box-sizing:border-box;
    }}
    .form-group input:focus, .form-group select:focus, .form-group textarea:focus {{ border-color:var(--brand-yellow); }}
    .form-group input[readonly] {{ background:#f8fafc; color:#64748b; cursor:not-allowed; }}
    .req {{ color:#ef4444; }}
    .attachment-zone {{
      border:2px dashed #cbd5e1; border-radius:8px; padding:20px; text-align:center;
      display:flex; align-items:center; justify-content:center; gap:10px; cursor:pointer; margin-top:12px;
      transition:border-color .2s;
    }}
    .attachment-zone:hover {{ border-color:var(--brand-yellow); }}
    .form-footer {{ display:flex; justify-content:space-between; align-items:center; background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px 20px; }}

    /* ── Machine Tiles (SFE) ── */
    .machine-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:12px; }}
    .machine-tile {{ border-radius:10px; padding:16px; border:1px solid; position:relative; cursor:pointer; transition:transform .15s, box-shadow .15s; }}
    .machine-tile:hover {{ transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,.1); }}
    .machine-name {{ font-size:13px; font-weight:700; color:#0f172a; margin-bottom:8px; }}
    .machine-status-dot {{ width:10px; height:10px; border-radius:50%; margin-bottom:4px; }}
    .machine-label {{ font-size:12px; font-weight:600; margin-bottom:4px; }}
    .machine-meta {{ font-size:11px; }}
    .machine-tile.running {{ background:#f0fdf4; border-color:#86efac; }}
    .machine-tile.running .machine-status-dot {{ background:#22c55e; box-shadow:0 0 0 3px rgba(34,197,94,.2); }}
    .machine-tile.running .machine-label {{ color:#16a34a; }}
    .machine-tile.running .machine-meta {{ color:#64748b; }}
    .machine-tile.idle {{ background:#f8fafc; border-color:#cbd5e1; }}
    .machine-tile.idle .machine-status-dot {{ background:#94a3b8; }}
    .machine-tile.idle .machine-label {{ color:#64748b; }}
    .machine-tile.idle .machine-meta {{ color:#94a3b8; }}
    .machine-tile.down {{ background:#fff1f2; border-color:#fca5a5; }}
    .machine-tile.down .machine-status-dot {{ background:#ef4444; box-shadow:0 0 0 3px rgba(239,68,68,.2); animation: pulse 1.5s infinite; }}
    .machine-tile.down .machine-label {{ color:#dc2626; }}
    .machine-tile.down .machine-meta {{ color:#ef4444; }}
    .machine-tile.maintenance {{ background:#eff6ff; border-color:#93c5fd; }}
    .machine-tile.maintenance .machine-status-dot {{ background:#3b82f6; }}
    .machine-tile.maintenance .machine-label {{ color:#2563eb; }}
    .machine-tile.maintenance .machine-meta {{ background:#3b82f6; }}
    @keyframes pulse {{ 0%,100% {{ box-shadow:0 0 0 3px rgba(239,68,68,.2); }} 50% {{ box-shadow:0 0 0 6px rgba(239,68,68,.1); }} }}

  </style>
</head>
<body>
  <aside class="sidebar">
    <a href="login.html" class="sidebar-brand" style="text-decoration:none; color:inherit;">
      <div class="logo-mark"><div class="diamond"></div></div>
      <span>AureliaERP</span>
    </a>
    <div class="sidebar-menu" id="sidebar-menu-container"></div>
  </aside>

  <div class="main-wrapper">
    <header class="top-nav">
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
        <a href="login.html?view=portal" class="datetime" style="color:var(--text-light); text-decoration:none; margin-right:16px; font-weight:500; font-size:13px;">&larr; Back to Portal</a>
        <div class="profile-menu-container" id="profileMenuContainer">
          <div class="user-avatar" id="profileAvatarBtn" onclick="toggleProfileMenu(event)">SR</div>
          <div class="profile-dropdown-card" id="profileDropdownCard">
            <div class="p-card-header">
              <div class="p-card-avatar">SR</div>
              <div class="p-card-info">
                <div class="p-card-name">Salim Rahal</div>
                <div class="p-card-role">HR Administrator</div>
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
      <div class="breadcrumbs">
        <span class="crumb" style="color:var(--text-muted); font-weight:500;" id="breadcrumb-group">Manufacturing</span>
        <span style="color:var(--text-muted); margin:0 4px;">·</span>
        <span class="crumb" style="color:var(--brand-yellow); font-weight:500;" id="breadcrumb-page">Overview</span>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:8px;">
        <h1 class="page-title" id="page-title" style="margin-bottom:0;">Loading...</h1>
      </div>
      <div id="page-content"></div>
    </main>
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
        const close  = (g === 'Production Planning' || g === 'Master Data' || g === ALL_GROUPS[0]) ? '' : `<span class="close-btn" onclick="closeTab(event,'${{g}}')">&times;</span>`;
        html += `<a href="#" class="nav-tab ${{active}}" onclick="setGroup('${{g}}');return false;">${{g}}${{close}}</a>`;
      }}
      const closed = ALL_GROUPS.filter(g => !openTabs.includes(g));
      if (closed.length > 0) {{
        html += `<div class="dropdown"><a href="#" style="padding:0;">Other <svg style="width:14px;height:14px;vertical-align:middle;margin-left:2px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></a><div class="dropdown-content">`;
        for (const g of closed) html += `<a href="#" onclick="addTab('${{g}}');return false;">+ ${{g}}</a>`;
        html += `</div></div>`;
      }}
      nav.innerHTML = html;
    }}

    function renderSidebar() {{
      const sb = document.getElementById('sidebar-menu-container');
      const pages = GROUPS[activeGroup] || [];
      let html = `<div class="menu-label">${{activeGroup.toUpperCase()}}</div>`;
      for (const p of pages) {{
        const active = p.id === activePage ? 'active' : '';
        const icon = `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>`;
        html += `<a href="#" class="menu-item ${{active}}" onclick="setPage('${{p.id}}');return false;">${{icon}}${{p.title}}</a>`;
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
      if (g === 'Production Planning' || g === 'Master Data' || g === ALL_GROUPS[0]) return;
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
                  <div style="font-size:13px; color:#64748b; font-weight:500;">HR Administrator · Employee ID: EMP-1002</div>
                </div>
              </div>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div class="form-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">First Name</label><input type="text" value="Salim" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Last Name</label><input type="text" value="Rahal" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Email Address</label><input type="email" value="salim.rahal@company.com" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Phone Number</label><input type="text" value="+966 50 123 4567" style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Department</label><input type="text" value="Human Resources" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
              <div class="form-group"><label style="display:block; font-size:12px; font-weight:600; color:#64748b; margin-bottom:4px;">Role Level</label><input type="text" value="HR Administrator (Level 4)" readonly style="width:100%; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#f8fafc;"></div>
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
              <h2 style="margin:0; font-size:17px; font-weight:700; color:#0f172a;">ERP Help Center &amp; Support</h2>
              <button onclick="closeGlobalModal()" style="background:none; border:none; font-size:22px; color:#94a3b8; cursor:pointer;">&times;</button>
            </div>
            <div style="margin-bottom:16px;">
              <input type="text" placeholder="Search FAQs, documentation, and user guides..." style="width:100%; padding:10px 14px; border:1px solid #cbd5e1; border-radius:8px; font-size:13.5px;" oninput="const q = this.value.toLowerCase(); this.parentElement.nextElementSibling.querySelectorAll('div').forEach(d => d.style.display = d.textContent.toLowerCase().includes(q) ? '' : 'none');">
            </div>
            <div style="display:grid; grid-template-columns:1fr; gap:10px;">
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📘 Production Planning &amp; MRP Quick Start</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">How to generate MRP plans and release Work Orders efficiently.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">🛠️ Maintenance &amp; Downtime Recording</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Step-by-step guide for logging breakdown tickets and PM schedules.</div></div>
              <div style="padding:12px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; cursor:pointer;"><strong style="font-size:13.5px; color:#0f172a;">📞 Contact Enterprise IT Desk</strong><div style="font-size:12px; color:#64748b; margin-top:2px;">Submit a priority ticket or contact support at support@company.com</div></div>
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
      if (confirm('Are you sure you want to sign out of AureliaHRMS?')) {{
        window.location.href = 'login.html';
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{ handleUrlRoutingOnLoad(GROUPS); renderTopNav(); renderSidebar(); renderContent(); wireGlobalSearch('manufacture'); }});
  </script>
</body>
</html>
"""

with open(r'c:\Users\Arfath.khan\Downloads\HRM2\hrms_payroll\templates\manufacture.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("manufacture.html updated successfully!")
