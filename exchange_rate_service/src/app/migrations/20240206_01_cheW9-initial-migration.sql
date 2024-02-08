CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE exchange_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    currency_pair_name VARCHAR(25) NOT NULL,
    price FLOAT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
