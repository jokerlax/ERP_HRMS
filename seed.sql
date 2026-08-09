-- ============================================================================
--  HRMS · Payroll — seed data  (matches hrms_schema.sql)
--  Run AFTER hrms_schema.sql:   psql -d hrms -f seed.sql
--  Loads reference data, 8 employees + salary structures, one active loan,
--  and a closed June-2026 run so the screen has content on first launch.
-- ============================================================================
BEGIN;

-- locations -------------------------------------------------------------
INSERT INTO locations (location_code, location_name, address, country)
 VALUES ('AMM','Head Office','Amman','Jordan');

-- departments -----------------------------------------------------------
INSERT INTO departments (department_code, department_name) VALUES
 ('SAL','Sales'), ('PRD','Production'), ('FIN','Finance'),
 ('HR','HR'), ('ADM','Administration');

-- designations ----------------------------------------------------------
INSERT INTO designations (designation_code, designation_name) VALUES
 ('SM','Sales Manager'), ('SE','Sales Executive'),
 ('SACC','Senior Accountant'), ('PAY','Payroll Assistant'),
 ('WS','Workshop Supervisor'), ('MO','Machine Operator'),
 ('HRO','HR Officer'), ('OC','Office Coordinator');

-- pay components --------------------------------------------------------
-- BASIC / HRA / TRANS / SSC / LOAN are already seeded by hrms_schema.sql.
-- Add only the extra heads the payroll engine needs (idempotent).
INSERT INTO pay_components (component_code, component_name, component_type, display_order) VALUES
 ('INCOMETAX','Income Tax','Deduction',12),
 ('OT','Overtime','Earning',4),
 ('COMM','Sales Commission','Earning',5),
 ('BONUS','Bonus','Earning',6),
 ('LOP','Loss of Pay','Deduction',13)
ON CONFLICT (component_code) DO NOTHING;

-- employees -------------------------------------------------------------
INSERT INTO employees
 (employee_code, first_name, last_name, work_email, department_id, designation_id,
  location_id, employment_type, status, date_of_joining)
VALUES
 ('EMP-0012','Yousef','Al-Masri','yousef@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='SAL'),
   (SELECT designation_id FROM designations WHERE designation_code='SM'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2019-02-03'),
 ('EMP-0031','Lina','Haddad','lina@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='FIN'),
   (SELECT designation_id FROM designations WHERE designation_code='SACC'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2020-06-19'),
 ('EMP-0044','Omar','Khalil','omar@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='PRD'),
   (SELECT designation_id FROM designations WHERE designation_code='WS'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2018-09-11'),
 ('EMP-0057','Rania','Suleiman','rania@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='HR'),
   (SELECT designation_id FROM designations WHERE designation_code='HRO'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2022-01-02'),
 ('EMP-0063','Tariq','Nassar','tariq@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='SAL'),
   (SELECT designation_id FROM designations WHERE designation_code='SE'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2023-03-23'),
 ('EMP-0075','Dana','Aburahma','dana@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='ADM'),
   (SELECT designation_id FROM designations WHERE designation_code='OC'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2021-11-14'),
 ('EMP-0088','Sami','Barakat','sami@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='PRD'),
   (SELECT designation_id FROM designations WHERE designation_code='MO'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2020-08-07'),
 ('EMP-0091','Maya','Fares','maya@aurelia.jo',
   (SELECT department_id FROM departments WHERE department_code='FIN'),
   (SELECT designation_id FROM designations WHERE designation_code='PAY'),
   (SELECT location_id FROM locations WHERE location_code='AMM'),'Permanent','Active','2024-04-30');

-- bank accounts ---------------------------------------------------------
INSERT INTO employee_bank_accounts (employee_id, bank_name, account_no, iban, is_primary)
SELECT employee_id, 'Cairo Amman Bank', right(employee_code,4)||'00'||right(employee_code,4),
       'JO94 CBJO 0000 '||right(employee_code,4), TRUE
FROM employees;

-- active salary structure per employee (effective_to NULL = current) ----
INSERT INTO employee_salary_structures (employee_id, effective_from, currency)
SELECT employee_id, date_of_joining, 'JOD' FROM employees;

-- structure lines: basic, housing, transport, income tax ---------------
WITH pay(code, basic, housing, transport, tax) AS (VALUES
  ('EMP-0012',900,250,100,42),
  ('EMP-0031',800,220, 90,28),
  ('EMP-0044',720,180, 80,20),
  ('EMP-0057',650,160, 80,12),
  ('EMP-0063',560,140, 70, 9),
  ('EMP-0075',520,130, 70, 7.5),
  ('EMP-0088',480,120, 60, 5.5),
  ('EMP-0091',520,130, 70, 7.5)
)
INSERT INTO salary_structure_lines (structure_id, component_id, amount)
SELECT ss.structure_id, c.component_id,
       CASE c.component_code
         WHEN 'BASIC'     THEN p.basic
         WHEN 'HRA'       THEN p.housing
         WHEN 'TRANS'     THEN p.transport
         WHEN 'INCOMETAX' THEN p.tax
       END
FROM pay p
JOIN employees e                    ON e.employee_code = p.code
JOIN employee_salary_structures ss  ON ss.employee_id = e.employee_id
JOIN pay_components c               ON c.component_code IN ('BASIC','HRA','TRANS','INCOMETAX');

-- one active loan for Lina ---------------------------------------------
-- (schema note) employee_loans lives in the payroll module; if your schema
-- version does not include it, remove this block.
INSERT INTO employee_loans
 (employee_id, loan_type, principal_amount, installment_amount,
  total_installments, paid_installments, start_date, status)
SELECT employee_id, 'Personal Loan', 900, 75, 12, 4, '2026-03-01', 'active'
FROM employees WHERE employee_code = 'EMP-0031';

-- historical closed run: June 2026 -------------------------------------
INSERT INTO payroll_periods
 (period_code, period_name, start_date, end_date, pay_date, status)
VALUES ('2026-06','June 2026','2026-06-01','2026-06-30','2026-06-28','Paid');

-- generate June payslips from each structure (all present, 22 days) -----
WITH per AS (SELECT period_id FROM payroll_periods WHERE period_code='2026-06'),
comp AS (
  SELECT e.employee_id,
         SUM(sl.amount) FILTER (WHERE c.component_code='BASIC')     AS basic,
         SUM(sl.amount) FILTER (WHERE c.component_code='HRA')   AS housing,
         SUM(sl.amount) FILTER (WHERE c.component_code='TRANS') AS transport,
         SUM(sl.amount) FILTER (WHERE c.component_code='INCOMETAX') AS tax
  FROM employees e
  JOIN employee_salary_structures ss ON ss.employee_id=e.employee_id AND ss.effective_to IS NULL
  JOIN salary_structure_lines sl     ON sl.structure_id=ss.structure_id
  JOIN pay_components c              ON c.component_id=sl.component_id
  GROUP BY e.employee_id
),
calc AS (
  SELECT c.*, round((c.basic+c.housing+c.transport)*0.075, 2) AS ss,
         COALESCE(l.installment_amount,0) AS loan,
         b.bank_account_id
  FROM comp c
  LEFT JOIN employee_loans l ON l.employee_id=c.employee_id AND l.status='active'
  LEFT JOIN employee_bank_accounts b ON b.employee_id=c.employee_id AND b.is_primary
),
ins AS (
  INSERT INTO payslips
    (payslip_no, period_id, employee_id, working_days, lop_days,
     gross_earnings, total_deductions, status, bank_account_id, generated_at)
  SELECT 'PS-2026-06-'||lpad(employee_id::text,4,'0'),
         (SELECT period_id FROM per), employee_id, 22, 0,
         (basic+housing+transport),
         (ss+tax+loan),
         'Paid', bank_account_id, now()
  FROM calc
  RETURNING payslip_id, employee_id
)
INSERT INTO payslip_lines (payslip_id, component_id, component_type, amount)
SELECT i.payslip_id, pc.component_id, pc.component_type, x.amt
FROM ins i
JOIN calc c ON c.employee_id = i.employee_id
CROSS JOIN LATERAL (VALUES
  ('BASIC',      c.basic),
  ('HRA',        c.housing),
  ('TRANS',      c.transport),
  ('SSC',        c.ss),
  ('INCOMETAX',  c.tax),
  ('LOAN',       c.loan)
) AS x(code, amt)
JOIN pay_components pc ON pc.component_code = x.code
WHERE x.amt > 0 OR pc.component_type = 'Earning';

-- cab vehicles -----------------------------------------------------------
INSERT INTO cab_vehicles (vehicle_number, cab_type, capacity) VALUES
 ('DXB-1234', 'Sedan', 4),
 ('DXB-5678', 'SUV', 6),
 ('DXB-9012', 'Minivan', 8);

-- cab drivers ----------------------------------------------------------
INSERT INTO cab_drivers (driver_name, phone, license_number) VALUES
 ('Ahmed Ali', '+971-50-1234567', 'DL-001'),
 ('Raj Kumar', '+971-55-9876543', 'DL-002'),
 ('Syed Khan', '+971-52-4567890', 'DL-003');

-- cab trips ------------------------------------------------------------
INSERT INTO cab_trips 
 (trip_no, employee_id, pickup_time, origin, destination, driver_id, vehicle_id, cab_type, trip_distance_km, trip_status, booking_status)
VALUES
 ('TRP-1001', (SELECT employee_id FROM employees WHERE employee_code='EMP-0012'), '2026-07-09 08:30:00+00', 'Home (Marina)', 'Office (DIFC)', 1, 1, 'Sedan', 15.5, 'Completed', 'Confirmed'),
 ('TRP-1002', (SELECT employee_id FROM employees WHERE employee_code='EMP-0031'), '2026-07-09 18:00:00+00', 'Office (DIFC)', 'Dubai Mall', 2, 2, 'SUV', 5.2, 'Completed', 'Confirmed'),
 ('TRP-1003', (SELECT employee_id FROM employees WHERE employee_code='EMP-0044'), '2026-07-10 09:00:00+00', 'Home (JLT)', 'Office (DIFC)', 3, 3, 'Minivan', 18.0, 'Completed', 'Confirmed'),
 ('TRP-1004', (SELECT employee_id FROM employees WHERE employee_code='EMP-0057'), '2026-07-11 08:45:00+00', 'Home (Business Bay)', 'Office (DIFC)', 1, 1, 'Sedan', 3.5, 'Ongoing', 'Confirmed'),
 ('TRP-1005', (SELECT employee_id FROM employees WHERE employee_code='EMP-0063'), '2026-07-11 17:30:00+00', 'Office (DIFC)', 'Home (Marina)', 2, 2, 'SUV', 15.5, 'Scheduled', 'Confirmed'),
 ('TRP-1006', (SELECT employee_id FROM employees WHERE employee_code='EMP-0075'), '2026-07-12 09:15:00+00', 'Home (Deira)', 'Office (DIFC)', 3, 3, 'Minivan', 12.0, 'Scheduled', 'Pending'),
 ('TRP-1007', (SELECT employee_id FROM employees WHERE employee_code='EMP-0088'), '2026-07-08 19:00:00+00', 'Office (DIFC)', 'Airport (DXB)', 1, 1, 'Sedan', 14.2, 'Cancelled', 'Cancelled');

COMMIT;
