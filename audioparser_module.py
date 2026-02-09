from faster_whisper import WhisperModel
import os

def load_model(model_name: str = "faster-whisper-small"):
    if model_name == "faster-whisper-small":
        model = WhisperModel(
            model_size_or_path="models/faster-whisper-small",
            device="cpu",
            compute_type="int8"
        )
    return model

def transcribe_with_fast_whisper(
        audio_path: str,
        model: WhisperModel):
    """
    Transcribe audio using fast Whisper with language detection
    """
    print(f"Transcribing audio at {audio_path}")

    # transcribe with timestamps
    seg, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True  # Enable word-level timestamps
    )

    # Print detection language info
    print("Detected '{}' language with {} chance".format(
        info.language, info.language_probability
    ))

    # Process segments
    results = []
    for segment in seg:
        segment_dict = {
            "id": segment.id,
            "seek": segment.seek,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
            "tokens": segment.tokens,
            "temperature": segment.temperature,
            "avg_logprob": segment.avg_logprob,
            "compression_ratio": segment.compression_ratio,
            "no_speech_prob": segment.no_speech_prob,
            "words": [
                {
                    "start": word.start,
                    "end": word.end,
                    "word": word.word,
                    "probability": word.probability
                }
                for word in segment.words
            ] if segment.words else []
        }

        results.append(segment_dict)

    return results
