#!/usr/bin/env python3
"""
Transkriptions-Modul
Erstellt Transkripte aus Audio-/Videodateien mit Whisper
"""

import logging
from pathlib import Path
import whisper
from tqdm import tqdm

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories():
    """
    Erstellt die benötigte Ordnerstruktur
    
    Returns:
        dict: Dictionary mit Verzeichnispfaden
    """
    base_dir = Path("output")
    dirs = {
        "videos": base_dir / "videos",
        "transcripts": base_dir / "transcripts",
        "results": base_dir / "results"
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs

def transcribe_audio(audio_path: Path, model: whisper.Whisper) -> str:
    """
    Transkribiert eine Audiodatei mit Whisper
    
    Args:
        audio_path: Pfad zur Audiodatei
        model: Geladenes Whisper-Modell
        
    Returns:
        str: Transkribierter Text oder None bei Fehler
    """
    try:
        logger.info(f"Transkribiere: {audio_path}")
        result = model.transcribe(str(audio_path))
        return result["text"]
    except Exception as e:
        logger.error(f"Fehler bei der Transkription: {e}")
        return None

def create_summary_prompt(transcript: str) -> str:
    """
    Erstellt den Prompt für die Zusammenfassung
    
    Args:
        transcript: Transkribierter Text
        
    Returns:
        str: Formatierter Prompt
    """
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
        return prompt_template.replace("{transcript}", transcript)
    except Exception as e:
        logger.error(f"Fehler beim Laden des Prompts: {e}")
        return None

def save_results(audio_path: Path, transcript: str, summary_prompt: str, dirs: dict):
    """
    Speichert Transkript und Zusammenfassungs-Prompt
    
    Args:
        audio_path: Pfad zur Audiodatei
        transcript: Transkribierter Text
        summary_prompt: Formatierter Prompt
        dirs: Dictionary mit Verzeichnispfaden
    """
    try:
        filename = audio_path.stem
        
        # Speichere Transkript
        transcript_path = dirs['transcripts'] / f"{filename}_transcript.txt"
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info(f"Transkript gespeichert: {transcript_path}")
        
        # Speichere Prompt im transcripts Ordner
        prompt_path = dirs['transcripts'] / f"{filename}_summary_prompt.txt"
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(summary_prompt)
        logger.info(f"Zusammenfassungs-Prompt gespeichert: {prompt_path}")
            
    except Exception as e:
        logger.error(f"Fehler beim Speichern der Ergebnisse: {e}")

def process_videos_folder():
    """Verarbeitet alle Audio-/Videodateien im videos-Ordner"""
    try:
        # Erstelle Ordnerstruktur
        dirs = setup_directories()
        
        # Finde alle Audiodateien
        audio_files = []
        for ext in [".wav", ".mp3", ".m4a", ".mp4"]:
            audio_files.extend(dirs['videos'].glob(f"*{ext}"))
        
        if not audio_files:
            logger.info("Keine Audio-/Videodateien gefunden")
            return
        
        logger.info(f"Gefundene Dateien: {len(audio_files)}")
        
        # Lade Whisper-Modell
        logger.info("Lade Whisper-Modell...")
        model = whisper.load_model("base")
        
        # Verarbeite jede Datei
        for audio_path in tqdm(audio_files, desc="Verarbeite Dateien"):
            # Prüfe ob bereits transkribiert
            transcript_path = dirs['transcripts'] / f"{audio_path.stem}_transcript.txt"
            if transcript_path.exists():
                logger.info(f"Überspringe existierendes Transkript: {transcript_path}")
                continue
            
            # Transkribiere
            if transcript := transcribe_audio(audio_path, model):
                # Erstelle Prompt
                if summary_prompt := create_summary_prompt(transcript):
                    # Speichere Ergebnisse
                    save_results(audio_path, transcript, summary_prompt, dirs)
                else:
                    logger.error("Prompt-Erstellung fehlgeschlagen")
            else:
                logger.error(f"Transkription fehlgeschlagen: {audio_path}")
                
    except Exception as e:
        logger.error(f"Fehler bei der Verarbeitung: {e}")

if __name__ == "__main__":
    process_videos_folder()