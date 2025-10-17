import os
import pandas as pd
from datasets import load_dataset
import soundfile as sf
from tqdm import tqdm

OUTPUT_DIR = "../datasets/fake_speech/codecfake"
METADATA_PATH = "../metadata/fake_codecfake_metadata.xlsx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_codecfake_subset(num_samples: int = 20):
    dataset = load_dataset("rogertseng/CodecFake", split="train", trust_remote_code=True)

    metadata = []

    for idx, row in enumerate(tqdm(dataset, desc="Downloading fake audio")):
        if idx >= num_samples:
            break

        try:
            audio = row["audio"]
            speaker_id = row.get("speaker_id", "unknown")
            codec_name = row.get("codec_name", "unknown")
            duration = audio.get("duration", None)

            filename = f"codecfake_{idx}.wav"
            filepath = os.path.join(OUTPUT_DIR, filename)
            sf.write(filepath, audio["array"], audio["sampling_rate"])

            metadata.append({
                "filename": filename,
                "speaker_id": speaker_id,
                "codec": codec_name,
                "label": "fake",
                "duration": round(duration, 2) if duration else None,
                "path": filepath,
                "source": "CodecFake (rogertseng/CodecFake)"
            })

        except Exception as e:
            print(f"[ERROR] Skipping sample {idx}: {e}")
            continue

    if metadata:
        df = pd.DataFrame(metadata)
        os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
        df.to_excel(METADATA_PATH, index=False)
        print(f"Saved metadata to: {METADATA_PATH}")
    else:
        print("No fake samples were processed.")

if __name__ == "__main__":
    download_codecfake_subset(num_samples=20)
