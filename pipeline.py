#!/usr/bin/env python3
"""
Pipeline-Orchestrierung
Führt die gesamte Verarbeitungspipeline aus
"""

import logging
import subprocess
from pathlib import Path

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_step(step_name: str, command: list[str]) -> bool:
    """
    Führt einen Pipeline-Schritt aus
    
    Args:
        step_name: Name des Schritts für Logging
        command: Auszuführender Befehl als Liste
        
    Returns:
        bool: True wenn erfolgreich, False bei Fehler
    """
    try:
        logger.info(f"Starte {step_name}...")
        subprocess.run(command, check=True)
        logger.info(f"{step_name} erfolgreich abgeschlossen")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Fehler in {step_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unerwarteter Fehler in {step_name}: {e}")
        return False

def main():
    """Führt die gesamte Pipeline aus"""
    try:
        # Prüfe ob video.txt existiert
        if not Path("video.txt").exists():
            logger.error("video.txt nicht gefunden!")
            return
            
        # Prüfe ob prompt.txt existiert
        if not Path("prompt.txt").exists():
            logger.error("prompt.txt nicht gefunden!")
            return
            
        # Führe Pipeline-Schritte aus
        steps = [
            ("Download", ["python", "downloader.py"]),
            ("Transkription", ["python", "transcribe.py"]),
            ("KI-Analyse", ["python", "ai_client.py"])
        ]
        
        for step_name, command in steps:
            if not run_step(step_name, command):
                logger.error(f"Pipeline nach Fehler in {step_name} abgebrochen")
                return
                
        logger.info("Pipeline erfolgreich abgeschlossen!")
        
    except Exception as e:
        logger.error(f"Unerwarteter Fehler in der Pipeline: {e}")

if __name__ == "__main__":
    main()