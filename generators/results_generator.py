import pandas as pd
import random

def generate_mock_results(training_df):
    results = []
    categories = training_df['category'].unique().tolist()
    
    # Vamos gerar resultados apenas para o split de 'test' ou 'val'
    test_data = training_df[training_df['split'].isin(['test', 'val'])]
    
    for _, row in test_data.iterrows():
        actual = row['category']
        
        # Simular acurácia de ~85%
        if random.random() > 0.15:
            predicted = actual
            confidence = random.uniform(0.85, 0.99)
        else:
            predicted = random.choice([c for c in categories if c != actual])
            confidence = random.uniform(0.40, 0.75)
            
        results.append({
            'actual_category': actual,
            'predicted_category': predicted,
            'confidence_score': round(confidence, 4),
            'inference_time_ms': round(random.uniform(50, 250), 2)
        })
        
    return pd.DataFrame(results)