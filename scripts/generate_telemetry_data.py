import pandas as pd
import numpy as np
import datetime
import random
import os
import json

np.random.seed(42)
random.seed(42)

def generate_messy_telemetry_json(num_rows=1000):
    
    data_list = []
    

    model_choices = ['gpt-4', 'GPT-4', 'gpt-4-turbo', 'GPT4', 'gpt-3.5-turbo', 'Claude-3', 'claude-3-opus', 'gemini-1.5-pro', 'Gemini-1.5-Pro', 'gemini_1.5']
    gpu_clusters = ['aws-us-east', 'gcp-asia', 'azure-eu', 'aws-us-west']
    
    for i in range(num_rows):

        timestamp = (datetime.datetime(2026, 5, 20) + datetime.timedelta(minutes=random.randint(0, 10000))).isoformat()
        session_id = f"USR_{random.randint(1000, 9999)}"
        model = random.choice(model_choices)
        
        input_tokens = int(np.random.randint(10, 2000))
        output_tokens = int(np.random.randint(5, 1000))
        
        base_latency = round((input_tokens * 0.5) + (output_tokens * 2.0) + np.random.normal(100, 50), 2)
        
        status_code = int(np.random.choice([200, 429, 500, 503], p=[0.80, 0.10, 0.05, 0.05]))
        gpu_cluster = random.choice(gpu_clusters)
        
        if status_code == 500:
            base_latency = round(random.uniform(15000, 35000), 2)
            
        if random.random() < 0.05:
            gpu_cluster = None  
            
        if random.random() < 0.08:
            input_tokens = None 
            
        latency_val = base_latency
        if random.random() < 0.04:
            latency_val = f"{base_latency} ms" 
            
        row_data = {
            "timestamp": timestamp,
            "session_id": session_id,
            "model_name": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_val,
            "status_code": status_code,
            "gpu_cluster": gpu_cluster
        }
        data_list.append(row_data)

    duplicates = random.sample(data_list, 30)
    data_list.extend(duplicates)

    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "llm_telemetry_v1_2026-05-26.json")
    
    with open(file_path, 'w') as f:
        json.dump(data_list, f, indent=4)
        
    print(f"Success: Messy JSON Data saved at: {file_path}")

if __name__ == "__main__":
    generate_messy_telemetry_json()