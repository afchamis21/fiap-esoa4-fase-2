import pandas as pd
import random

def generate_plant_training_data(n_samples=200):
    categories = [
        'Healthy', 'Rust', 'Powdery Mildew', 
        'Leaf Spot', 'Blight', 'Mosaic Virus'
    ]
    
    data = []
    for i in range(1, n_samples + 1):
        cat = random.choice(categories)
        label_id = categories.index(cat)
        # 70% treino, 15% val, 15% teste
        split = random.choices(['train', 'val', 'test'], weights=[0.7, 0.15, 0.15])[0]
        
        path = f"dataset/{split}/{cat.lower().replace(' ', '_')}/img_{i:04d}.jpg"
        
        data.append({
            'image_path': path,
            'category': cat,
            'label_id': label_id,
            'split': split
        })
    
    return pd.DataFrame(data)