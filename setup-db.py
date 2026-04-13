import sqlite3
import os

from generators.plant_generator import generate_plant_training_data
from generators.results_generator import generate_mock_results

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
    
    try:
        cursor.executescript(sql_script)

        # 2. Gera e guarda dados de treino
        print("🌱 Gerando metadados das imagens...")
        df_training = generate_plant_training_data(400)
        df_training.to_sql("training_data", conn, if_exists='replace', index=False)
        
        # 3. Gera e guarda resultados do modelo baseados no treino
        print("📊 Gerando resultados mockados da IA...")
        df_results = generate_mock_results(df_training)
        df_results.to_sql("model_results", conn, if_exists='replace', index=False)

        print(f"✅ Setup concluído: {len(df_training)} imagens e {len(df_results)} predições.")
        conn.commit()
        print(f"✅ Banco {db_path} atualizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao rodar SQL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()