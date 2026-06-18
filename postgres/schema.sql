CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    account_owner VARCHAR(100)
);

CREATE TABLE issues (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    priority VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE issue_updates (
    id SERIAL PRIMARY KEY,
    issue_id INTEGER REFERENCES issues(id),
    update_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE next_actions (
    id SERIAL PRIMARY KEY,
    issue_id INTEGER REFERENCES issues(id),
    action_text TEXT NOT NULL,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    role_name VARCHAR(50) NOT NULL
);