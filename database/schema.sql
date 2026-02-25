-- Esquema inicial placeholder para Control360 Almacenes.
-- Las tablas finales se completarán por partes según módulos.

CREATE TABLE IF NOT EXISTS clients (
  id INTEGER PRIMARY KEY,
  business_name TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS enabled_modules (
  id INTEGER PRIMARY KEY,
  client_id INTEGER NOT NULL,
  module_key TEXT NOT NULL,
  enabled INTEGER NOT NULL DEFAULT 1,
  plan_amount INTEGER NOT NULL,
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
