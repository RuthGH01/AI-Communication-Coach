
import torch
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration

MODEL_NAME = "openai/whisper-tiny"
AUDIO_PATH = r"C:\Users\hp\Downloads\audio_file3.ogg"

def main():
    print("Loading Whisper Tiny...")
    processor = WhisperProcessor.from_pretrained(MODEL_NAME)
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
    model.eval()

    print("Loading audio...")
    audio, sample_rate = librosa.load(
        AUDIO_PATH,
        sr=16000,
        mono=True
    )

    if len(audio) == 0:
        raise ValueError("The audio file is empty.")

    print(f"Audio duration: {len(audio) / sample_rate:.2f} seconds")
    print("Transcribing audio...")

    inputs = processor(
        audio,
        sampling_rate=sample_rate,
        return_tensors="pt"
    )

    with torch.no_grad():
        generated_ids = model.generate(
            inputs.input_features,
            max_new_tokens=225
        )

    transcription = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    print("\n--- TRANSCRIPTION ---")
    print(transcription if transcription.strip() else "[No speech recognized]")
    print("---------------------")

if __name__ == "__main__":
    main()
