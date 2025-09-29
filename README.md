# DeepFaic Audio Curation

This repo curates a multilingual dataset for deepfake audio detection.

## Structure
- `datasets/`: Contains real and fake audio samples.
- `metadata/aggregated_metadata.xlsx`: Metadata including language, label, duration, and file path.
- `scripts/`: Contains scripts for downloading and generating metadata.

## Sources
- Real samples: Mozilla Common Voice
- Fake samples: Titech Parrots (via Hugging Face)

## Labels
- `real`: Genuine human speech
- `fake`: Synthetic deepfake audio

