CREATE DATABASE natural_gas_db;

CREATE USER tec_energy_user WITH PASSWORD 'tec_energy';

GRANT ALL PRIVILEGES ON DATABASE natural_gas_db TO tec_energy_user;

-- Connect to db
\c natural_gas_db;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tec_energy_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tec_energy_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO tec_energy_user;