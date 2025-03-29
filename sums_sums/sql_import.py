from django.db import migrations


def populate_db():
    return migrations.RunSQL(
        """
    CREATE TABLE accounts (
        account_id SERIAL PRIMARY KEY,
        nickname TEXT NOT NULL,
        user_id INT NOT NULL,
        bank TEXT NOT NULL,
        account_type TEXT,
        account_last_four INT,
        translator JSON NOT NULL,
        date_formatter TEXT NOT NULL,
        CONSTRAINT fk_accounts_auth_user
            FOREIGN KEY (user_id)
            REFERENCES auth_user (user_id)
            ON DELETE CASCADE
    );

    CREATE TABLE budgets (
        budget_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        category_name TEXT NOT NULL,
        category_display TEXT NOT NULL,
        monthly_budget NUMERIC,
        annual_budget NUMERIC,
        CONSTRAINT fk_budgets_auth_user
            FOREIGN KEY (user_id)
            REFERENCES auth_user (user_id)
            ON DELETE CASCADE
    );

    CREATE TABLE transactions (
        transaction_id SERIAL PRIMARY KEY,
        amount NUMERIC NOT NULL,
        transaction_date DATE NOT NULL,
        transaction_description TEXT,
        budget_id INT,
        note TEXT,
        user_id INT NOT NULL,
        recurring BOOLEAN,
        account_nickname TEXT NOT NULL,
        CONSTRAINT fk_transactions_auth_user
            FOREIGN KEY (user_id)
            REFERENCES auth_user (user_id)
            ON DELETE CASCADE
    );

    CREATE TABLE snapshots (
        snapshot_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        snapshot_year SMALLINT NOT NULL,
        snapshot_month SMALLINT NOT NULL,
        snapshot_budget JSONB NOT NULL,
        snapshot_expenses JSONB
    );


        """
    )