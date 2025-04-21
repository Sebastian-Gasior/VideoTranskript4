#!/usr/bin/env python3
"""
Video-Download Modul
Lädt Videos von YouTube herunter oder kopiert lokale Dateien
"""

import os
from pathlib import Path
import subprocess
import sys
import glob
import certifi
import ssl
from yt_dlp import YoutubeDL
import logging
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

def read_video_urls(filename: str) -> list[str]:
    """
    Liest Video-URLs aus einer Textdatei
    
    Args:
        filename: Pfad zur URL-Datei
        
    Returns:
        list[str]: Liste der gefundenen URLs
    """
    if not os.path.exists(filename):
        logger.error(f"Fehler: Die Datei {filename} existiert nicht!")
        return []
    
    urls = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def download_video(url: str, output_dir: Path) -> bool:
    """
    Download ein Video von der angegebenen URL
    
    Args:
        url: Video-URL oder Dateipfad
        output_dir: Ausgabeverzeichnis
        
    Returns:
        bool: True wenn erfolgreich, False bei Fehler
    """
    # Prüfe ob lokale Datei
    if os.path.exists(url):
        try:
            # Kopiere und konvertiere zu WAV
            output_path = output_dir / f"{Path(url).stem}.wav"
            subprocess.run([
                'ffmpeg', '-i', url,
                '-vn', '-acodec', 'pcm_s16le',
                '-ar', '44100', '-ac', '2',
                str(output_path)
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Fehler bei der Konvertierung: {e}")
            return False
    
    # YouTube Download
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True
    }
    
    try:
        with YoutubeDL(options) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        logger.error(f"Fehler beim Download: {e}")
        return False

def check_ffmpeg() -> bool:
    """
    Überprüft die FFmpeg-Installation
    
    Returns:
        bool: True wenn FFmpeg verfügbar ist
    """
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("FFmpeg ist korrekt installiert")
            return True
        else:
            logger.error("FFmpeg wurde nicht gefunden!")
            return False
    except Exception as e:
        logger.error(f"Fehler bei der FFmpeg-Überprüfung: {e}")
        return False

def main():
    """Hauptfunktion für den Video-Download"""
    try:
        # FFmpeg-Check
        if not check_ffmpeg():
            logger.error("Bitte stellen Sie sicher, dass FFmpeg korrekt installiert ist!")
            sys.exit(1)
        
        # Erstelle Ordnerstruktur
        dirs = setup_directories()
        logger.info(f"Ausgabeverzeichnis für Videos: {dirs['videos'].absolute()}")
        
        # Lese URLs
        urls = read_video_urls("video.txt")
        if not urls:
            logger.info("Keine URLs gefunden!")
            return
        
        logger.info(f"Gefundene URLs: {len(urls)}")
        
        # Verarbeite jede URL
        erfolge = 0
        for url in tqdm(urls, desc="Verarbeite Videos"):
            logger.info(f"\nVerarbeite: {url}")
            if download_video(url, dirs['videos']):
                erfolge += 1
        
        logger.info(f"\nZusammenfassung: {erfolge} von {len(urls)} Downloads erfolgreich")
        
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()