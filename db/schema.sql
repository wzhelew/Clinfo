-- MySQL schema for current Clinfo app models
CREATE DATABASE IF NOT EXISTS clinfo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE clinfo;

CREATE TABLE IF NOT EXISTS users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS invoices (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  invoice_no VARCHAR(100) NOT NULL,
  `date` DATE NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'Неплатена',
  user_id INT UNSIGNED NOT NULL,
  CONSTRAINT fk_invoices_users FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_invoices_user_date (user_id, `date`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS stock_items (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  item_name VARCHAR(200) NOT NULL,
  quantity DECIMAL(12,2) NOT NULL,
  unit VARCHAR(30) NOT NULL DEFAULT 'бр.',
  user_id INT UNSIGNED NOT NULL,
  CONSTRAINT fk_stock_items_users FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_stock_items_user_name (user_id, item_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS debts (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  description VARCHAR(255) NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  due_date DATE NULL,
  state VARCHAR(50) NOT NULL DEFAULT 'Дължима',
  user_id INT UNSIGNED NOT NULL,
  CONSTRAINT fk_debts_users FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_debts_user_due (user_id, due_date)
) ENGINE=InnoDB;
