DROP TABLE IF EXISTS training_data;
CREATE TABLE training_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    category TEXT NOT NULL,
    split TEXT DEFAULT 'train', -- train, test, val
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS model_results;
CREATE TABLE model_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actual_category TEXT NOT NULL,
    predicted_category TEXT NOT NULL,
    confidence_score REAL NOT NULL, -- Valor entre 0 e 1
    location_name TEXT NOT NULL,
    image_name TEXT NOT NULL,
    inference_time_ms REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);