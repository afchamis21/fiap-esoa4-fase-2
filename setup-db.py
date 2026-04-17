import sqlite3
import os
import cv2
import time
import numpy as np
import tensorflow as tf
import pandas as pd

from random import choices, randint
from datetime import datetime
from dataclasses import dataclass

os.environ["TF_USE_LEGACY_KERAS"] = "1"

@dataclass
class CvResult:
    id: int
    actual_category: str
    predicted_category: str
    confidence_score: int
    location_name: str
    inference_time_ms: int
    image_name: str
    created_at: datetime


@dataclass
class CvEntry:
    id: int
    image_path: str
    category: str
    split: str
    created_at: datetime

def get_split() -> str:
    return choices(['train', 'val', 'test'], weights=[0.7, 0.15, 0.15])[0]


def get_category() -> str:
    return choices([
        "Ferrugem",
        "Mancha Alvo",
        "Míldio",
        "Oídio",
        "Podridão Radicular"
    ], weights=[0.28, 0.15, 0.20, 0.22, 0.15])[0]


def get_location() -> str:
    return choices([
        "Fazenda Sol Nascente",
        "Sítio Bela Vista",
        "Agropecuária Vale Verde",
        "Estância Ouro Branco",
        "Rancho Águas Claras"
    ], weights=[0.3, 0.15, 0.15, 0.18, 0.22])[0]


model = None
class_names = None

def load_model():
    global model
    global class_names
    if model:
        return model
    try:
        model = tf.keras.models.load_model("keras_model.h5", compile=False)
        class_names = open("labels.txt", "r", encoding="utf-8").readlines()
        print("Sucesso! Modelo carregado.")
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        exit()


def do_cv(filepath: str) -> CvResult:
    frame = cv2.imread(filepath)
    if frame is None:
        raise ValueError(f"Não foi possível ler a imagem: {filepath}")

    basename = os.path.basename(filepath)

    start_time = time.time()

    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    prediction = model.predict(image, verbose=0)
    
    end_time = time.time()
    inference_time_ms = int((end_time - start_time) * 1000)

    index = np.argmax(prediction)
    class_name = class_names[index][2:].strip() 
    
    confidence_score = int(prediction[0][index] * 100)

    is_healthy = class_name == "Saudavel"

    cat = "Saudável" if is_healthy else get_category()

    if is_healthy:
        cv2.imwrite(f"./output/healthy/{basename}", frame)
    else:
        cv2.imwrite(f"./output/not_healthy/{basename}", frame)

    print(f"Imagem {basename}, analisada em {inference_time_ms} ms. Resultado: {cat}. {class_name=}")

    return CvResult(
        id=randint(0, 1000),                                     
        actual_category=cat,          
        predicted_category=cat,
        confidence_score=confidence_score,
        location_name=get_location(),                  
        inference_time_ms=inference_time_ms,
        created_at=datetime.now()     ,
        image_name=basename          
    )


def init_db():
    db_path = 'data/database.db'
    sql_path = 'data/init.sql'
    
    # Garante que a pasta existe
    os.makedirs('data', exist_ok=True)
    
    # Conecta (se não existir, ele cria o arquivo)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lê seu arquivo de mocks
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    input_files = os.listdir("input");
    paths = list(map(lambda p: os.path.join("input", p), input_files))
    
    try:
        cursor.executescript(sql_script)

        entries = list(map(lambda f: CvEntry(
            id=randint(1, 1000),
            category=get_category(),
            created_at=datetime.now(),
            image_path=f"./input/{f}",
            split=get_split()
        ), input_files));
        df_training = pd.DataFrame(entries)
        df_training.to_sql("training_data", conn, if_exists='replace', index=False)
        df_training.to_csv("TrainingData.csv")

        results = list(map(do_cv, paths))
        df_results = pd.DataFrame(results)
        df_results.to_sql("model_results", conn, if_exists='replace', index=False)
        df_results.to_csv("Results.csv")

        print(f"✅ Setup concluído: {len(df_training)} imagens e {len(df_results)} predições.")
        conn.commit()
        print(f"✅ Banco {db_path} atualizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao rodar SQL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    os.makedirs("./output", exist_ok=True)
    os.makedirs("./output/healthy", exist_ok=True)
    os.makedirs("./output/not_healthy", exist_ok=True)

    model = load_model();
    init_db()