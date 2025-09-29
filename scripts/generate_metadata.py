# scripts/generate_metadata.py
import os
import librosa
import pandas as pd

dataset_root = "datasets"
metadata = []

for lang in os.listdir(dataset_root):
    lang_path = os.path.join(dataset_root, lang)
    for file in os.listdir(lang_path):
        full_path = os.path.join(lang_path, file)
        duration = librosa.get_duration(path=full_path)
        label = "real"  # since this batch is only real samples
        metadata.append({
            "filename": file,
            "language": lang,
            "label": label,
            "duration": round(duration, 2),
            "path": full_path
        })

df = pd.DataFrame(metadata)
os.makedirs("metadata", exist_ok=True)
df.to_excel("metadata/aggregated_metadata.xlsx", index=False)

print(f"Metadata saved. Total samples: {len(df)}")
