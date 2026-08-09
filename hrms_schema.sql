-- =====================================================================
--  HRMS DATABASE SCHEMA  (PostgreSQL 13+)
--  Modules : Core / Employee Master, Payslip & Payroll, Leaves,
--            Document Management, Flight Request, Resignation
--  Notes   : Uses ENUM types for statuses, TIMESTAMPTZ for audit,
--            surrogate SERIAL PKs, business codes as UNIQUE keys.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 0. ENUM TYPES
-- ---------------------------------------------------------------------
CREATE TYPE gender_enum            AS ENUM ('Male','Female','Other');
CREATE TYPE marital_status_enum    AS ENUM ('Single','Married','Divorced','Widowed');
CREATE TYPE employment_type_enum   AS ENUM ('Permanent','Contract','Probation','Temporary','Intern');
CREATE TYPE employee_status_enum   AS ENUM ('Active','On Leave','Suspended','Resigned','Terminated');
CREATE TYPE request_status_enum    AS ENUM ('Draft','Pending','Approved','Rejected','Cancelled');
CREATE TYPE component_type_enum    AS ENUM ('Earning','Deduction');
CREATE TYPE calc_type_enum         AS ENUM ('Fixed','Percentage','Formula');
CREATE TYPE payroll_status_enum    AS ENUM ('Draft','Processing','Processed','Approved','Paid','Cancelled');
CREATE TYPE trip_type_enum         AS ENUM ('One Way','Round Trip','Multi City');
CREATE TYPE ticket_class_enum      AS ENUM ('Economy','Premium Economy','Business','First');
CREATE TYPE resignation_status_enum AS ENUM ('Submitted','Manager Approved','HR Approved','Withdrawn','Completed','Rejected');
CREATE TYPE doc_verify_enum        AS ENUM ('Pending','Verified','Rejected','Expired');

-- ---------------------------------------------------------------------
-- 1. ORGANISATION MASTERS
-- ---------------------------------------------------------------------
CREATE TABLE locations (
    location_id       SERIAL PRIMARY KEY,
    location_code     VARCHAR(20)  UNIQUE NOT NULL,
    location_name     VARCHAR(120) NOT NULL,
    address           TEXT,
    country           VARCHAR(60),
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE departments (
    department_id        SERIAL PRIMARY KEY,
    department_code      VARCHAR(20)  UNIQUE NOT NULL,
    department_name      VARCHAR(120) NOT NULL,
    parent_department_id INT REFERENCES departments(department_id),
    is_active            BOOLEAN DEFAULT TRUE,
    created_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE designations (
    designation_id    SERIAL PRIMARY KEY,
    designation_code  VARCHAR(20)  UNIQUE NOT NULL,
    designation_name  VARCHAR(120) NOT NULL,
    grade_level       INT,
    is_active         BOOLEAN DEFAULT TRUE
);

-- ---------------------------------------------------------------------
-- 2. SECURITY / USERS
-- ---------------------------------------------------------------------
CREATE TABLE roles (
    role_id      SERIAL PRIMARY KEY,
    role_code    VARCHAR(30) UNIQUE NOT NULL,   -- ADMIN, HR, MANAGER, EMPLOYEE
    role_name    VARCHAR(80) NOT NULL,
    description  TEXT
);

CREATE TABLE users (
    user_id        SERIAL PRIMARY KEY,
    username       VARCHAR(60) UNIQUE NOT NULL,
    email          VARCHAR(120) UNIQUE NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    employee_id    INT,                          -- FK added after employees created
    is_active      BOOLEAN DEFAULT TRUE,
    last_login_at  TIMESTAMPTZ,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_roles (
    user_id  INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role_id  INT NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- ---------------------------------------------------------------------
-- 3. EMPLOYEE MASTER  (central table every module hangs off)
-- ---------------------------------------------------------------------
CREATE TABLE employees (
    employee_id        SERIAL PRIMARY KEY,
    employee_code      VARCHAR(20)  UNIQUE NOT NULL,     -- EMP-0001
    first_name         VARCHAR(80)  NOT NULL,
    middle_name        VARCHAR(80),
    last_name          VARCHAR(80)  NOT NULL,
    gender             gender_enum,
    date_of_birth      DATE,
    marital_status     marital_status_enum,
    nationality        VARCHAR(60),
    personal_email     VARCHAR(120),
    work_email         VARCHAR(120),
    mobile             VARCHAR(30),
    -- org placement
    department_id      INT REFERENCES departments(department_id),
    designation_id     INT REFERENCES designations(designation_id),
    location_id        INT REFERENCES locations(location_id),
    manager_id         INT REFERENCES employees(employee_id),   -- self ref
    -- employment
    employment_type    employment_type_enum DEFAULT 'Permanent',
    date_of_joining    DATE NOT NULL,
    date_of_confirmation DATE,
    probation_end_date DATE,
    status             employee_status_enum DEFAULT 'Active',
    date_of_leaving    DATE,
    photo_path         VARCHAR(255),
    -- custom Excel upload fields
    facility_code      VARCHAR(50),
    facility_name      VARCHAR(150),
    parent_department_name VARCHAR(120),
    work_center        VARCHAR(100),
    shift              VARCHAR(100),
    supervisor_name    VARCHAR(150),
    supervisor_code    VARCHAR(20),
    expat              VARCHAR(20),
    person_classification VARCHAR(100),
    religion           VARCHAR(50),
    expatriate         VARCHAR(20),
    passport_number    VARCHAR(50),
    passport_issue_date DATE,
    passport_expiry_date DATE,
    labour_card        VARCHAR(50),
    lc_issue_date      DATE,
    lc_expiry_date     DATE,
    relieving_date     DATE,
    approved_relieving VARCHAR(20),
    labour_union       VARCHAR(100),
    separation_reason  VARCHAR(255),
    separation_mode    VARCHAR(100),
    person_category    VARCHAR(100),
    residence_card     VARCHAR(50),
    rc_issue           DATE,
    rc_expiry          DATE,
    created_at         TIMESTAMPTZ DEFAULT NOW(),
    updated_at         TIMESTAMPTZ DEFAULT NOW()
);

-- now the users -> employees FK
ALTER TABLE users
    ADD CONSTRAINT fk_users_employee
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id);

CREATE TABLE employee_bank_accounts (
    bank_account_id  SERIAL PRIMARY KEY,
    employee_id      INT NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    bank_name        VARCHAR(120) NOT NULL,
    account_no       VARCHAR(50)  NOT NULL,
    iban             VARCHAR(50),
    branch           VARCHAR(120),
    is_primary       BOOLEAN DEFAULT TRUE
);

-- =====================================================================
-- MODULE A :  LEAVES
-- =====================================================================
CREATE TABLE leave_types (
    leave_type_id      SERIAL PRIMARY KEY,
    leave_code         VARCHAR(20)  UNIQUE NOT NULL,   -- AL, SL, UL
    leave_name         VARCHAR(80)  NOT NULL,          -- Annual, Sick...
    default_days_year  NUMERIC(5,1) DEFAULT 0,
    is_paid            BOOLEAN DEFAULT TRUE,
    carry_forward      BOOLEAN DEFAULT FALSE,
    max_carry_forward  NUMERIC(5,1) DEFAULT 0,
    requires_document  BOOLEAN DEFAULT FALSE,          -- e.g. medical cert
    is_active          BOOLEAN DEFAULT TRUE
);

CREATE TABLE holidays (
    holiday_id     SERIAL PRIMARY KEY,
    holiday_date   DATE NOT NULL,
    holiday_name   VARCHAR(120) NOT NULL,
    location_id    INT REFERENCES locations(location_id),  -- NULL = all
    is_active      BOOLEAN DEFAULT TRUE,
    UNIQUE (holiday_date, location_id)
);

-- yearly entitlement / running balance per employee per leave type
CREATE TABLE leave_allocations (
    allocation_id   SERIAL PRIMARY KEY,
    employee_id     INT NOT NULL REFERENCES employees(employee_id),
    leave_type_id   INT NOT NULL REFERENCES leave_types(leave_type_id),
    year            INT NOT NULL,
    allocated_days  NUMERIC(5,1) DEFAULT 0,
    carried_days    NUMERIC(5,1) DEFAULT 0,
    used_days       NUMERIC(5,1) DEFAULT 0,
    -- generated balance column keeps it always correct
    balance_days    NUMERIC(5,1) GENERATED ALWAYS AS
                    (allocated_days + carried_days - used_days) STORED,
    UNIQUE (employee_id, leave_type_id, year)
);

CREATE TABLE leave_requests (
    leave_request_id  SERIAL PRIMARY KEY,
    request_no        VARCHAR(30) UNIQUE NOT NULL,
    employee_id       INT NOT NULL REFERENCES employees(employee_id),
    leave_type_id     INT NOT NULL REFERENCES leave_types(leave_type_id),
    from_date         DATE NOT NULL,
    to_date           DATE NOT NULL,
    is_half_day       BOOLEAN DEFAULT FALSE,
    total_days        NUMERIC(5,1) NOT NULL,
    reason            TEXT,
    status            request_status_enum DEFAULT 'Pending',
    approver_id       INT REFERENCES employees(employee_id),
    approved_at       TIMESTAMPTZ,
    approver_remarks  TEXT,
    document_path     VARCHAR(255),
    applied_at        TIMESTAMPTZ DEFAULT NOW(),
    CHECK (to_date >= from_date)
);

-- =====================================================================
-- MODULE B :  PAYSLIP & PAYROLL
-- =====================================================================
-- salary heads: basic, housing, transport, GOSI, loan deduction...
CREATE TABLE pay_components (
    component_id     SERIAL PRIMARY KEY,
    component_code   VARCHAR(20)  UNIQUE NOT NULL,
    component_name   VARCHAR(80)  NOT NULL,
    component_type   component_type_enum NOT NULL,      -- Earning / Deduction
    calc_type        calc_type_enum DEFAULT 'Fixed',
    is_taxable       BOOLEAN DEFAULT FALSE,
    display_order    INT DEFAULT 0,
    is_active        BOOLEAN DEFAULT TRUE
);

-- per-employee salary structure with effective dating (history preserved)
CREATE TABLE employee_salary_structures (
    structure_id     SERIAL PRIMARY KEY,
    employee_id      INT NOT NULL REFERENCES employees(employee_id),
    effective_from   DATE NOT NULL,
    effective_to     DATE,                              -- NULL = current
    currency         VARCHAR(3) DEFAULT 'JOD',
    remarks          TEXT,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (employee_id, effective_from)
);

CREATE TABLE salary_structure_lines (
    line_id          SERIAL PRIMARY KEY,
    structure_id     INT NOT NULL REFERENCES employee_salary_structures(structure_id) ON DELETE CASCADE,
    component_id     INT NOT NULL REFERENCES pay_components(component_id),
    amount           NUMERIC(14,2) DEFAULT 0,           -- fixed value
    percentage       NUMERIC(6,3),                      -- if calc_type = Percentage
    UNIQUE (structure_id, component_id)
);

-- one row per month/cycle to be processed
CREATE TABLE payroll_periods (
    period_id        SERIAL PRIMARY KEY,
    period_code      VARCHAR(20) UNIQUE NOT NULL,       -- 2026-07
    period_name      VARCHAR(60) NOT NULL,              -- July 2026
    start_date       DATE NOT NULL,
    end_date         DATE NOT NULL,
    pay_date         DATE,
    status           payroll_status_enum DEFAULT 'Draft',
    UNIQUE (start_date, end_date)
);

-- header for each payslip (employee x period)
CREATE TABLE payslips (
    payslip_id       SERIAL PRIMARY KEY,
    payslip_no       VARCHAR(30) UNIQUE NOT NULL,
    period_id        INT NOT NULL REFERENCES payroll_periods(period_id),
    employee_id      INT NOT NULL REFERENCES employees(employee_id),
    working_days     NUMERIC(5,1),
    lop_days         NUMERIC(5,1) DEFAULT 0,            -- loss of pay
    gross_earnings   NUMERIC(14,2) DEFAULT 0,
    total_deductions NUMERIC(14,2) DEFAULT 0,
    net_pay          NUMERIC(14,2) GENERATED ALWAYS AS
                     (gross_earnings - total_deductions) STORED,
    status           payroll_status_enum DEFAULT 'Draft',
    bank_account_id  INT REFERENCES employee_bank_accounts(bank_account_id),
    generated_at     TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (period_id, employee_id)
);

-- component-level breakdown of each payslip
CREATE TABLE payslip_lines (
    payslip_line_id  SERIAL PRIMARY KEY,
    payslip_id       INT NOT NULL REFERENCES payslips(payslip_id) ON DELETE CASCADE,
    component_id     INT NOT NULL REFERENCES pay_components(component_id),
    component_type   component_type_enum NOT NULL,
    amount           NUMERIC(14,2) DEFAULT 0
);

-- staff loans / salary advances, recovered through payroll as a deduction
CREATE TABLE employee_loans (
    loan_id            SERIAL PRIMARY KEY,
    employee_id        INT NOT NULL REFERENCES employees(employee_id),
    loan_type          VARCHAR(60) NOT NULL,
    principal_amount   NUMERIC(14,2) NOT NULL,
    installment_amount NUMERIC(14,2) NOT NULL,
    total_installments INT NOT NULL,
    paid_installments  INT DEFAULT 0,
    start_date         DATE NOT NULL,
    status             VARCHAR(20) DEFAULT 'active',   -- active / closed / on_hold
    created_at         TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_loan_employee ON employee_loans(employee_id);

-- =====================================================================
-- MODULE C :  DOCUMENT MANAGEMENT
-- =====================================================================
CREATE TABLE document_types (
    document_type_id  SERIAL PRIMARY KEY,
    type_code         VARCHAR(20) UNIQUE NOT NULL,      -- PASSPORT, VISA, CONTRACT
    type_name         VARCHAR(80) NOT NULL,
    has_expiry        BOOLEAN DEFAULT FALSE,
    is_mandatory      BOOLEAN DEFAULT FALSE,
    is_active         BOOLEAN DEFAULT TRUE
);

CREATE TABLE employee_documents (
    document_id       SERIAL PRIMARY KEY,
    employee_id       INT NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    document_type_id  INT NOT NULL REFERENCES document_types(document_type_id),
    document_no       VARCHAR(80),
    title             VARCHAR(150),
    file_path         VARCHAR(255) NOT NULL,
    file_size_kb      INT,
    issue_date        DATE,
    expiry_date       DATE,
    issuing_authority VARCHAR(120),
    verify_status     doc_verify_enum DEFAULT 'Pending',
    verified_by       INT REFERENCES employees(employee_id),
    verified_at       TIMESTAMPTZ,
    uploaded_at       TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_empdoc_expiry ON employee_documents(expiry_date);

-- =====================================================================
-- MODULE D :  FLIGHT / AIR-TICKET REQUEST
-- =====================================================================
-- annual air-ticket entitlement (common in Gulf/ME contracts)
CREATE TABLE flight_entitlements (
    entitlement_id    SERIAL PRIMARY KEY,
    employee_id       INT NOT NULL REFERENCES employees(employee_id),
    year              INT NOT NULL,
    tickets_allowed   INT DEFAULT 1,
    tickets_used      INT DEFAULT 0,
    default_class     ticket_class_enum DEFAULT 'Economy',
    UNIQUE (employee_id, year)
);

CREATE TABLE flight_requests (
    flight_request_id SERIAL PRIMARY KEY,
    request_no        VARCHAR(30) UNIQUE NOT NULL,
    employee_id       INT NOT NULL REFERENCES employees(employee_id),
    trip_type         trip_type_enum DEFAULT 'Round Trip',
    origin            VARCHAR(80)  NOT NULL,
    destination       VARCHAR(80)  NOT NULL,
    departure_date    DATE NOT NULL,
    return_date       DATE,
    passengers        INT DEFAULT 1,
    ticket_class      ticket_class_enum DEFAULT 'Economy',
    purpose           TEXT,
    linked_leave_id   INT REFERENCES leave_requests(leave_request_id), -- if annual-leave ticket
    estimated_cost    NUMERIC(14,2),
    status            request_status_enum DEFAULT 'Pending',
    approver_id       INT REFERENCES employees(employee_id),
    approved_at       TIMESTAMPTZ,
    approver_remarks  TEXT,
    applied_at        TIMESTAMPTZ DEFAULT NOW(),
    CHECK (return_date IS NULL OR return_date >= departure_date)
);

-- =====================================================================
-- MODULE E :  RESIGNATION / OFFBOARDING
-- =====================================================================
CREATE TABLE resignations (
    resignation_id    SERIAL PRIMARY KEY,
    resignation_no    VARCHAR(30) UNIQUE NOT NULL,
    employee_id       INT NOT NULL REFERENCES employees(employee_id),
    submitted_date    DATE NOT NULL DEFAULT CURRENT_DATE,
    notice_period_days INT DEFAULT 30,
    proposed_last_day DATE NOT NULL,
    approved_last_day DATE,
    reason            TEXT,
    status            resignation_status_enum DEFAULT 'Submitted',
    manager_id        INT REFERENCES employees(employee_id),
    manager_remarks   TEXT,
    hr_remarks        TEXT,
    is_rehire_eligible BOOLEAN,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- master of clearance departments (IT, Finance, Admin, HR...)
CREATE TABLE clearance_items (
    clearance_item_id SERIAL PRIMARY KEY,
    item_code         VARCHAR(20) UNIQUE NOT NULL,
    item_name         VARCHAR(120) NOT NULL,
    department_id     INT REFERENCES departments(department_id),
    display_order     INT DEFAULT 0,
    is_active         BOOLEAN DEFAULT TRUE
);

-- checklist rows generated per resignation
CREATE TABLE resignation_clearances (
    id                SERIAL PRIMARY KEY,
    resignation_id    INT NOT NULL REFERENCES resignations(resignation_id) ON DELETE CASCADE,
    clearance_item_id INT NOT NULL REFERENCES clearance_items(clearance_item_id),
    is_cleared        BOOLEAN DEFAULT FALSE,
    cleared_by        INT REFERENCES employees(employee_id),
    cleared_at        TIMESTAMPTZ,
    remarks           TEXT,
    UNIQUE (resignation_id, clearance_item_id)
);

-- =====================================================================
-- 4. GENERIC AUDIT LOG
-- =====================================================================
CREATE TABLE audit_log (
    audit_id     BIGSERIAL PRIMARY KEY,
    table_name   VARCHAR(60) NOT NULL,
    record_id    VARCHAR(40),
    action       VARCHAR(10) NOT NULL,   -- INSERT / UPDATE / DELETE
    changed_by   INT REFERENCES users(user_id),
    changed_at   TIMESTAMPTZ DEFAULT NOW(),
    old_values   JSONB,
    new_values   JSONB
);

-- ---------------------------------------------------------------------
-- 5. HELPFUL INDEXES
-- ---------------------------------------------------------------------
CREATE INDEX idx_emp_department  ON employees(department_id);
CREATE INDEX idx_emp_manager     ON employees(manager_id);
CREATE INDEX idx_emp_status      ON employees(status);
CREATE INDEX idx_leavereq_emp    ON leave_requests(employee_id, status);
CREATE INDEX idx_payslip_period  ON payslips(period_id);
CREATE INDEX idx_flightreq_emp   ON flight_requests(employee_id, status);
CREATE INDEX idx_resig_emp       ON resignations(employee_id, status);

-- ---------------------------------------------------------------------
-- 6. SAMPLE REFERENCE DATA (optional seed)
-- ---------------------------------------------------------------------
INSERT INTO roles (role_code, role_name) VALUES
 ('ADMIN','Administrator'),('HR','HR Officer'),
 ('MANAGER','Line Manager'),('EMPLOYEE','Employee');

INSERT INTO leave_types (leave_code, leave_name, default_days_year, is_paid, carry_forward, max_carry_forward, requires_document) VALUES
 ('AL','Annual Leave',21,TRUE,TRUE,10,FALSE),
 ('SL','Sick Leave',14,TRUE,FALSE,0,TRUE),
 ('UL','Unpaid Leave',0,FALSE,FALSE,0,FALSE),
 ('ML','Maternity Leave',70,TRUE,FALSE,0,TRUE);

INSERT INTO pay_components (component_code, component_name, component_type, calc_type, is_taxable, display_order) VALUES
 ('BASIC','Basic Salary','Earning','Fixed',TRUE,1),
 ('HRA','Housing Allowance','Earning','Fixed',FALSE,2),
 ('TRANS','Transport Allowance','Earning','Fixed',FALSE,3),
 ('SSC','Social Security','Deduction','Percentage',FALSE,10),
 ('LOAN','Loan Deduction','Deduction','Fixed',FALSE,11);

INSERT INTO document_types (type_code, type_name, has_expiry, is_mandatory) VALUES
 ('PASSPORT','Passport',TRUE,TRUE),
 ('ID','National ID',TRUE,TRUE),
 ('CONTRACT','Employment Contract',FALSE,TRUE),
 ('CERT','Certificate',FALSE,FALSE);

INSERT INTO clearance_items (item_code, item_name, display_order) VALUES
 ('IT','Return IT assets / disable accounts',1),
 ('FIN','Finance settlement / dues',2),
 ('ADMIN','Return ID card & office keys',3),
 ('HR','Exit interview & final papers',4);
-- =====================================================================
-- MODULE F :  CAB / TRANSPORT MANAGEMENT
-- =====================================================================
CREATE TYPE trip_status_enum       AS ENUM ('Scheduled','Ongoing','Completed','Cancelled');
CREATE TYPE booking_status_enum    AS ENUM ('Pending','Confirmed','Cancelled');

CREATE TABLE cab_vehicles (
    vehicle_id       SERIAL PRIMARY KEY,
    vehicle_number   VARCHAR(30) UNIQUE NOT NULL,
    cab_type         VARCHAR(50),
    capacity         INT DEFAULT 4,
    status           VARCHAR(20) DEFAULT 'Active',
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE cab_drivers (
    driver_id        SERIAL PRIMARY KEY,
    driver_name      VARCHAR(100) NOT NULL,
    phone            VARCHAR(30),
    license_number   VARCHAR(50) UNIQUE,
    status           VARCHAR(20) DEFAULT 'Active',
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE cab_trips (
    trip_id          SERIAL PRIMARY KEY,
    trip_no          VARCHAR(30) UNIQUE NOT NULL,
    employee_id      INT NOT NULL REFERENCES employees(employee_id),
    pickup_time      TIMESTAMPTZ NOT NULL,
    origin           VARCHAR(120) NOT NULL,
    destination      VARCHAR(120) NOT NULL,
    driver_id        INT REFERENCES cab_drivers(driver_id),
    vehicle_id       INT REFERENCES cab_vehicles(vehicle_id),
    cab_type         VARCHAR(50),
    trip_distance_km NUMERIC(6,2),
    trip_status      trip_status_enum DEFAULT 'Scheduled',
    booking_status   booking_status_enum DEFAULT 'Pending',
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================================
--  END OF SCHEMA
-- =====================================================================


-- ========================================================
-- ATTENDANCE MODULE
-- ========================================================

CREATE TABLE IF NOT EXISTS biometric_logs (
    log_id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    device_name VARCHAR(255) NOT NULL,
    punch_time TIMESTAMP NOT NULL,
    direction VARCHAR(10) CHECK (direction IN ('IN', 'OUT')),
    method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================================
-- EXPENSES MODULE
-- ========================================================

CREATE TABLE IF NOT EXISTS expense_claims (
    claim_id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    expense_date DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    description TEXT,
    receipt_file_path TEXT,
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
