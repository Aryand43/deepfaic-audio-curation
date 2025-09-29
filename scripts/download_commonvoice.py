# scripts/download_commonvoice.py
import os
from datasets import load_dataset
import soundfile as sf
from tqdm import tqdm

LANG_CODES = {
    "english": "en",
    "filipino": "tl",
    "spanish": "es",
    "mandarin": "zh-CN"  # adjust if needed
}

def download_commonvoice_subset(
    lang_name: str,
    lang_code: str,
    output_dir: str = "datasets",
    num_samples: int = 20,
    min_duration: float = 1.0,
    max_duration: float = 10.0,
    accent_filter: list[str] = None
) -> list[dict]:
    print(f"\nDownloading CommonVoice for {lang_name} [{lang_code}]...")

    # Only grab first 500 rows to avoid multi-GB downloads
    dataset = load_dataset("mozilla-foundation/common_voice_11_0", lang_code, split="train[:500]", trust_remote_code=True)

    os.makedirs(f"{output_dir}/{lang_name}", exist_ok=True)

    metadata = []
    count = 0

    for row in tqdm(dataset):
        try:
            audio = row.get("audio")
            duration = audio["duration"]
            accent = row.get("accent", None)

            if not audio or audio["array"] is None:
                continue
            if duration < min_duration or duration > max_duration:
                continue
            if accent_filter and accent not in accent_filter:
                continue

            filename = f"{lang_name}_{count}.wav"
            filepath = os.path.join(output_dir, lang_name, filename)
            sf.write(filepath, audio["array"], audio["sampling_rate"])

            metadata.append({
                "filename": filename,
                "language": lang_name,
                "label": "real",  # fake will come from other datasets
                "duration": round(duration, 2),
                "accent": accent or "unknown",
                "path": filepath,
                "source": "CommonVoice"
            })

            count += 1
            if count >= num_samples:
                break

        except Exception as e:
            print("Error:", e)
            continue

    print(f"Downloaded {count} samples for {lang_name}")
    return metadata

if __name__ == "__main__":
    for lang, code in LANG_CODES.items():
        download_commonvoice_subset(
            lang_name=lang,
            lang_code=code,
            num_samples=5  # 5 per language for quick test
        )
