-- PostgreSQL SQL Interview Prep Database Schema and Sample Data
-- This script creates toy databases for practicing SQL queries

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS employee_projects CASCADE;

-- ============================================
-- DEPARTMENTS TABLE
-- ============================================
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    budget NUMERIC(12, 2)
);

INSERT INTO departments (name, location, budget) VALUES
('Engineering', 'San Francisco', 500000.00),
('Sales', 'New York', 300000.00),
('Marketing', 'Los Angeles', 250000.00),
('HR', 'Chicago', 150000.00),
('Finance', 'Boston', 400000.00);

-- ============================================
-- EMPLOYEES TABLE
-- ============================================
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    salary NUMERIC(10, 2),
    hire_date DATE,
    manager_id INTEGER REFERENCES employees(id)
);

INSERT INTO employees (first_name, last_name, department_id, salary, hire_date, manager_id) VALUES
('Alice', 'Johnson', 1, 95000.00, '2020-01-15', NULL),
('Bob', 'Smith', 1, 85000.00, '2020-03-20', 1),
('Charlie', 'Brown', 1, 78000.00, '2021-06-10', 1),
('Diana', 'Martinez', 2, 72000.00, '2019-11-05', NULL),
('Eve', 'Davis', 2, 68000.00, '2020-08-15', 4),
('Frank', 'Wilson', 2, 70000.00, '2021-02-28', 4),
('Grace', 'Taylor', 3, 65000.00, '2020-05-12', NULL),
('Henry', 'Anderson', 3, 62000.00, '2021-09-01', 7),
('Ivy', 'Thomas', 4, 58000.00, '2019-07-20', NULL),
('Jack', 'Moore', 4, 55000.00, '2022-01-10', 9),
('Kate', 'Jackson', 5, 88000.00, '2018-12-03', NULL),
('Liam', 'White', 5, 82000.00, '2020-04-18', 11),
('Mia', 'Harris', 1, 92000.00, '2019-09-25', 1),
('Noah', 'Clark', 2, 75000.00, '2021-03-14', 4),
('Olivia', 'Lewis', 3, 67000.00, '2020-10-08', 7);

-- ============================================
-- PROJECTS TABLE
-- ============================================
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    budget NUMERIC(12, 2),
    status TEXT CHECK (status IN ('active', 'completed', 'on_hold'))
);

INSERT INTO projects (name, start_date, end_date, budget, status) VALUES
('Website Redesign', '2023-01-01', '2023-06-30', 150000.00, 'completed'),
('Mobile App Development', '2023-03-15', '2024-03-15', 300000.00, 'active'),
('Data Migration', '2023-05-01', '2023-12-31', 200000.00, 'active'),
('Marketing Campaign Q4', '2023-10-01', '2023-12-31', 80000.00, 'completed'),
('ERP System Upgrade', '2023-07-01', '2024-06-30', 500000.00, 'active');

-- ============================================
-- EMPLOYEE_PROJECTS (Many-to-Many)
-- ============================================
CREATE TABLE employee_projects (
    employee_id INTEGER REFERENCES employees(id),
    project_id INTEGER REFERENCES projects(id),
    hours_allocated INTEGER,
    role TEXT,
    PRIMARY KEY (employee_id, project_id)
);

INSERT INTO employee_projects (employee_id, project_id, hours_allocated, role) VALUES
(1, 2, 200, 'Lead Developer'),
(2, 2, 180, 'Backend Developer'),
(3, 2, 160, 'Frontend Developer'),
(1, 3, 100, 'Technical Advisor'),
(13, 3, 220, 'Project Manager'),
(4, 4, 150, 'Sales Lead'),
(5, 4, 120, 'Account Manager'),
(7, 4, 180, 'Marketing Manager'),
(8, 4, 160, 'Content Creator'),
(11, 5, 200, 'Financial Analyst'),
(12, 5, 180, 'Budget Manager');

-- ============================================
-- CUSTOMERS TABLE
-- ============================================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    country TEXT
);

INSERT INTO customers (name, email, phone, country, created_at) VALUES
('John Doe', 'john.doe@email.com', '555-0101', 'USA', '2023-01-15 10:30:00'),
('Jane Smith', 'jane.smith@email.com', '555-0102', 'USA', '2023-02-20 14:15:00'),
('Bob Johnson', 'bob.johnson@email.com', '555-0103', 'Canada', '2023-03-10 09:45:00'),
('Alice Brown', 'alice.brown@email.com', '555-0104', 'UK', '2023-04-05 16:20:00'),
('Charlie Davis', 'charlie.davis@email.com', '555-0105', 'USA', '2023-05-12 11:00:00'),
('Eva Wilson', 'eva.wilson@email.com', '555-0106', 'Australia', '2023-06-18 13:30:00'),
('David Miller', 'david.miller@email.com', '555-0107', 'USA', '2023-07-22 10:15:00'),
('Sarah Taylor', 'sarah.taylor@email.com', '555-0108', 'Canada', '2023-08-30 15:45:00'),
('Michael Anderson', 'michael.anderson@email.com', '555-0109', 'UK', '2023-09-14 12:00:00'),
('Lisa Thomas', 'lisa.thomas@email.com', '555-0110', 'USA', '2023-10-25 09:30:00');

-- ============================================
-- PRODUCTS TABLE
-- ============================================
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10, 2),
    category TEXT,
    stock_quantity INTEGER,
    supplier TEXT
);

INSERT INTO products (name, price, category, stock_quantity, supplier) VALUES
('Laptop Pro 15', 1299.99, 'Electronics', 45, 'TechSupply Inc'),
('Wireless Mouse', 29.99, 'Electronics', 150, 'TechSupply Inc'),
('Mechanical Keyboard', 89.99, 'Electronics', 78, 'TechSupply Inc'),
('USB-C Cable', 12.99, 'Accessories', 200, 'Cable World'),
('Laptop Stand', 49.99, 'Accessories', 92, 'Office Depot'),
('Noise-Canceling Headphones', 199.99, 'Electronics', 63, 'Audio Pro'),
('Webcam HD', 79.99, 'Electronics', 55, 'TechSupply Inc'),
('Desk Lamp LED', 39.99, 'Office', 110, 'Office Depot'),
('Office Chair Ergonomic', 299.99, 'Office', 28, 'Furniture Plus'),
('Monitor 27 inch', 349.99, 'Electronics', 34, 'TechSupply Inc'),
('External SSD 1TB', 129.99, 'Electronics', 88, 'Storage Solutions'),
('Phone Holder', 15.99, 'Accessories', 165, 'Office Depot'),
('Screen Protector', 9.99, 'Accessories', 250, 'TechSupply Inc'),
('Portable Charger', 45.99, 'Electronics', 72, 'Power Unlimited'),
('Backpack Laptop', 69.99, 'Accessories', 45, 'Bag Masters');

-- ============================================
-- ORDERS TABLE
-- ============================================
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER CHECK (quantity > 0),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled'))
);

INSERT INTO orders (customer_id, product_id, quantity, order_date, status) VALUES
(1, 1, 1, '2023-01-20 11:00:00', 'delivered'),
(1, 2, 2, '2023-01-20 11:00:00', 'delivered'),
(2, 3, 1, '2023-02-25 14:30:00', 'delivered'),
(3, 10, 1, '2023-03-15 10:15:00', 'delivered'),
(3, 2, 1, '2023-03-15 10:15:00', 'delivered'),
(4, 6, 1, '2023-04-10 16:45:00', 'delivered'),
(5, 9, 1, '2023-05-18 09:30:00', 'delivered'),
(5, 5, 2, '2023-05-18 09:30:00', 'delivered'),
(6, 11, 2, '2023-06-22 13:00:00', 'shipped'),
(7, 1, 1, '2023-07-28 10:45:00', 'delivered'),
(8, 7, 1, '2023-08-15 15:20:00', 'delivered'),
(8, 4, 3, '2023-08-15 15:20:00', 'delivered'),
(9, 14, 1, '2023-09-20 12:30:00', 'delivered'),
(10, 15, 1, '2023-10-30 10:00:00', 'shipped'),
(1, 11, 1, '2023-11-05 11:30:00', 'pending'),
(2, 8, 2, '2023-11-08 14:15:00', 'pending'),
(3, 13, 5, '2023-11-10 09:45:00', 'shipped'),
(4, 12, 1, '2023-11-12 16:00:00', 'pending'),
(5, 3, 1, '2023-11-15 10:30:00', 'pending'),
(6, 10, 1, '2023-11-18 13:45:00', 'pending');

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_manager ON employees(manager_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_product ON orders(product_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_employee_projects_emp ON employee_projects(employee_id);
CREATE INDEX idx_employee_projects_proj ON employee_projects(project_id);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================
CREATE VIEW employee_department_view AS
SELECT
    e.id,
    e.first_name || ' ' || e.last_name AS full_name,
    e.salary,
    e.hire_date,
    d.name AS department_name,
    d.location
FROM employees e
JOIN departments d ON e.department_id = d.id;

CREATE VIEW order_summary_view AS
SELECT
    o.order_id,
    c.name AS customer_name,
    p.name AS product_name,
    o.quantity,
    p.price,
    (o.quantity * p.price) AS total_amount,
    o.order_date,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;

-- ============================================
-- VERIFY DATA
-- ============================================
SELECT 'Departments' AS table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'Employees', COUNT(*) FROM employees
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Employee_Projects', COUNT(*) FROM employee_projects
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders;
