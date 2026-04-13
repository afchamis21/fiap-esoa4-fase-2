DROP TABLE IF EXISTS training_data;
CREATE TABLE training_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    category TEXT NOT NULL,
    label_id INTEGER NOT NULL,
    split TEXT DEFAULT 'train', -- train, test, val
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS model_results;
CREATE TABLE model_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id INTEGER, -- ID correspondente na training_data
    actual_category TEXT NOT NULL,
    predicted_category TEXT NOT NULL,
    confidence_score REAL NOT NULL, -- Valor entre 0 e 1
    inference_time_ms REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);