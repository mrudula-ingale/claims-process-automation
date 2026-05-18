DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS claim_events;
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    customer_since DATE NOT NULL
);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE
);

CREATE TABLE claims (
    claim_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    claim_type TEXT NOT NULL,
    claim_amount REAL NOT NULL, 
    status TEXT NOT NULL,
    submitted_date DATE NOT NULL,
    closed_date DATE,
    priority TEXT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE claim_events (
    event_id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL,
    event_status TEXT NOT NULL,
    event_date DATE NOT NULL,
    notes TEXT,

    FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL,
    payment_amount REAL NOT NULL,
    payment_date DATE NOT NULL,
    payment_method TEXT NOT NULL,

    FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
);

