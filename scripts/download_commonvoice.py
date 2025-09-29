# scripts/download_commonvoice.py
import os
import time
import pandas as pd
import soundfile as sf
from datasets import load_dataset
from tqdm import tqdm

LANG_CODES = {
    "english": "en",
    "spanish": "es",
    "mandarin": "zh-CN",  # Simplified Chinese
    "french": "fr",
    "german": "de"
}

def download_commonvoice_subset(
    lang_name: str,
    lang_code: str,
    output_dir: str = "../datasets",  # Outside /scripts
    num_samples: int = 20,
    min_duration: float = 0.5,
    max_duration: float = 15.0,
) -> list[dict]:
    print(f"\n==== Downloading CommonVoice for {lang_name} [{lang_code}] ====")
    out_dir = os.path.join(output_dir, lang_name)
    os.makedirs(out_dir, exist_ok=True)
    print(f"Saving to: {os.path.abspath(out_dir)}")

    try:
        dataset = load_dataset(
            "mozilla-foundation/common_voice_11_0",
            lang_code,
            split="train[:5000]",
            trust_remote_code=True
        )
        print(f"Loaded {len(dataset)} rows.")
    except Exception as e:
        print(f"[SKIPPED] Could not load {lang_name}: {e}")
        return []

    metadata = []
    count = 0

    for idx, row in enumerate(tqdm(dataset, desc=f"Processing {lang_name}")):
        try:
            audio = row.get("audio")
            transcript = row.get("sentence", "").strip()
            duration = audio.get("duration", 0)
            accent = row.get("accent", "unknown")

            if not audio or audio["array"] is None:
                continue  # fine
            if not transcript or len(transcript.strip()) == 0:
                continue  # only filter out blanks


            filename = f"{lang_name}_{count}.wav"
            filepath = os.path.join(out_dir, filename)
            sf.write(filepath, audio["array"], audio["sampling_rate"])

            metadata.append({
                "filename": filename,
                "language": lang_name,
                "label": "real",
                "duration": round(duration, 2),
                "accent": accent,
                "transcript": transcript,
                "path": filepath,
                "source": "CommonVoice"
            })

            count += 1
            if count >= num_samples:
                break

            if count % 2 == 0:
                print(f"Saved: {filepath} | {transcript[:40]}...")

        except Exception as e:
            print(f"[ERROR] Row {idx}: {e}")
            continue

    print(f"==== Finished {lang_name}: {count} samples saved ====")
    return metadata


if __name__ == "__main__":
    all_metadata = []

    for lang, code in LANG_CODES.items():
        meta = download_commonvoice_subset(
            lang_name=lang,
            lang_code=code,
            num_samples=5  # Increase later if needed
        )
        all_metadata.extend(meta)

    # Save metadata to Excel
    if all_metadata:
        os.makedirs("../metadata", exist_ok=True)
        df = pd.DataFrame(all_metadata)
        df.to_excel("../metadata/aggregated_metadata.xlsx", index=False)
        print(f"\nMetadata saved to: ../metadata/aggregated_metadata.xlsx")
    else:
        print("\nNo samples were saved — check filter conditions.")
