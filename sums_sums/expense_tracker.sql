
\c budget_tracker


CREATE TABLE users (
    username TEXT PRIMARY KEY,
    passwd TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name TEXT NOT NULL,
    fieldnames TEXT []
);

CREATE TABLE banks_users (
    username TEXT NOT NULL,
    bank_id INT NOT NULL,
    PRIMARY KEY (username, bank_id),
    CONSTRAINT fk_banks_users_banks
        FOREIGN KEY (bank_id)
        REFERENCES banks (bank_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_banks_users_users
        FOREIGN KEY (username)
        REFERENCES users (username)
        ON DELETE CASCADE
);

CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    nickname TEXT,
    account_owner TEXT NOT NULL,
    account_type TEXT,
    account_last_four INT,
    bank_id INT NOT NULL,
    CONSTRAINT fk_accounts_users
        FOREIGN KEY (account_owner)
        REFERENCES users (username)
        ON DELETE CASCADE,
    CONSTRAINT fk_accounts_banks
        FOREIGN KEY (bank_id)
        REFERENCES banks (bank_id)
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
    account_id INT NOT NULL,
    budget_id INT,
    note TEXT,
    recurring BOOLEAN,
    CONSTRAINT fk_transactions_accounts
        FOREIGN KEY (account_id)
        REFERENCES accounts (account_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_transactions_budgets
        FOREIGN KEY (budget_id)
        REFERENCES budgets
        ON DELETE SET NULL
);

INSERT INTO users (username, passwd, email) VALUES ('test', 'admin123', 'testing@testing.com');