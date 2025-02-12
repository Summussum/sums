
\c budget_tracker


CREATE TABLE users (
    username TEXT PRIMARY KEY,
    email TEXT
);


CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    nickname TEXT NOT NULL,
    account_owner TEXT NOT NULL,
    bank TEXT NOT NULL,
    account_type TEXT,
    account_last_four INT,
    translator JSON NOT NULL,
    date_formatter TEXT NOT NULL,
    CONSTRAINT fk_accounts_users
        FOREIGN KEY (account_owner)
        REFERENCES users (username)
        ON DELETE CASCADE
);

CREATE TABLE budgets (
    budget_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    category_name TEXT NOT NULL,
    category_display TEXT NOT NULL,
    monthly_budget NUMERIC,
    annual_budget NUMERIC,
    CONSTRAINT fk_budgets_users
        FOREIGN KEY (username)
        REFERENCES users (username)
        ON DELETE CASCADE
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    amount NUMERIC NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_description TEXT,
    budget_id INT,
    note TEXT,
    account_owner TEXT NOT NULL,
    recurring BOOLEAN,
    account_nickname TEXT NOT NULL,
    CONSTRAINT fk_transactions_users
        FOREIGN KEY (account_owner)
        REFERENCES users (username)
        ON DELETE CASCADE
);
