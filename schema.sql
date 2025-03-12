CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL,
    stock_count REAL,
    product_value REAL,
    stock_category TEXT NOT NULL,
    product_category TEXT NOT NULL,
    sage_code TEXT,
    supplier TEXT,
    sold_as TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_take (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_count TEXT NOT NULL,
    product_category TEXT NOT NULL,
    date_added TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial product data
INSERT INTO products (name, price, description) VALUES
-- (name, cost, stock_count, product_value, category, sage_code, supplier, sold_as)
('Topside', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Silverside', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Brisket', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Skirts', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Frozen 95vl', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Fresh 95vl', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('85vl', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Blades', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Chuck', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Fore Rib', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Pressed Fat', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),
('Diced Beef', 0, 0, 0, 'fresh', 'beef', '', '', 'kilo'),

