
import torch
import librosa
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
)

MODEL_NAME = "openai/whisper-tiny"
SAMPLE_RATE = 16000

# Load the model once when this module is imported.
print("Loading Whisper Tiny model...")

processor = WhisperProcessor.from_pretrained(MODEL_NAME)

model = WhisperForConditionalGeneration.from_pretrained(
    MODEL_NAME
)

model.eval()

print("Whisper Tiny is ready.")


def transcribe_audio(file_path: str) -> dict:
    """Transcribe an audio file using the local Whisper Tiny model."""

    audio, sample_rate = librosa.load(
        file_path,
        sr=SAMPLE_RATE,
        mono=True,
    )

    if len(audio) == 0:
        raise ValueError("The audio file is empty.")

    inputs = processor(
        audio,
        sampling_rate=sample_rate,
        return_tensors="pt",
    )

    with torch.no_grad():
        generated_ids = model.generate(
            inputs.input_features,
            max_new_tokens=225,
        )

    transcription = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0].strip()

    return {
        "text": transcription,
        "language": "en",
        "model": MODEL_NAME,
    }
