#!/usr/bin/env python3
"""
AI Client Modul
Verarbeitet Transkripte mit der OpenAI API
"""

import os
from pathlib import Path
import logging
from typing import Optional
from dotenv import load_dotenv
import openai
from tqdm import tqdm

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIClient:
    def __init__(self):
        """Initialisiert den AI Client mit OpenAI Konfiguration"""
        # Finde .env Datei
        env_path = Path(__file__).parent / '.env'
        logger.info(f"Suche .env Datei in: {env_path}")
        
        # Lade Umgebungsvariablen
        if not load_dotenv(env_path):
            raise EnvironmentError(f"Keine .env Datei gefunden unter: {env_path}")
            
        # Konfiguriere OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY nicht gefunden in .env")
        
        logger.info("API Key erfolgreich geladen")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo-16k"
        
    def process_prompt(self, prompt_path: Path) -> Optional[str]:
        """
        Verarbeitet einen vorbereiteten Prompt mit der OpenAI API
        
        Args:
            prompt_path: Pfad zur Prompt-Datei
            
        Returns:
            Optional[str]: API Antwort oder None bei Fehler
        """
        try:
            # Lese Prompt
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
                
            # API Aufruf
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du bist ein professioneller Content-Analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Fehler bei der API-Verarbeitung: {e}")
            return None
            
def process_all_transcripts(base_dir: str = "output"):
    """
    Verarbeitet alle Transkripte im Verzeichnis
    
    Args:
        base_dir: Basis-Verzeichnis für Ein-/Ausgabe
    """
    base_path = Path(base_dir)
    transcripts_dir = base_path / "transcripts"
    results_dir = base_path / "results"
    
    try:
        # Initialisiere Verzeichnisse
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Finde alle Prompts
        prompt_files = list(transcripts_dir.glob("*_summary_prompt.txt"))
        if not prompt_files:
            logger.info("Keine Prompts gefunden")
            return
            
        logger.info(f"Gefundene Prompts: {len(prompt_files)}")
        
        # Initialisiere AI Client
        client = AIClient()
        
        # Verarbeite jeden Prompt
        for prompt_path in tqdm(prompt_files, desc="Verarbeite Prompts"):
            # Erstelle Ausgabepfad
            result_path = results_dir / f"{prompt_path.stem.replace('_summary_prompt', '')}_result.txt"
            
            # Überspringe existierende
            if result_path.exists():
                logger.info(f"Überspringe existierendes Ergebnis: {result_path}")
                continue
                
            # Verarbeite mit API
            logger.info(f"Verarbeite: {prompt_path}")
            if result := client.process_prompt(prompt_path):
                # Speichere Ergebnis
                with open(result_path, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Ergebnis gespeichert: {result_path}")
            else:
                logger.error(f"Verarbeitung fehlgeschlagen: {prompt_path}")
                
    except Exception as e:
        logger.error(f"Fehler bei der Verarbeitung der Prompts: {e}")

if __name__ == "__main__":
    process_all_transcripts()