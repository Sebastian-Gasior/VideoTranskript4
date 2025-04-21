# Video-Transkriptions-Pipeline

Automatisierte Pipeline zum Herunterladen, Transkribieren und Analysieren von Videos mit KI-gestützter Zusammenfassung.

## Projektbeschreibung

Dieses Projekt bietet eine modulare Pipeline zur Verarbeitung von Videos. Es besteht aus drei Hauptkomponenten:

1. **Video-Downloader**: 
   - Lädt Videos von YouTube herunter oder kopiert lokale Videodateien
   - Extrahiert automatisch die Audiospur im WAV-Format
   - Unterstützt URLs und lokale Dateipfade in `video.txt`

2. **Transkriptions-Engine**:
   - Nutzt OpenAI Whisper für lokale Transkription
   - Unterstützt verschiedene Audio-/Videoformate
   - Generiert Transkripte und Analyse-Prompts

3. **KI-Analyse**:
   - Verwendet OpenAI GPT-3.5-Turbo für die Analyse
   - Erstellt strukturierte Zusammenfassungen
   - Generiert Social-Media-Beiträge und Übersetzungen

## Features

- Video-Download von YouTube und lokalen Dateien
- Automatische Transkription mit Whisper
- KI-gestützte Analyse mit GPT-3.5-Turbo
- Generierung von:
  - Deutschen Zusammenfassungen
  - Social Media Beiträgen
  - Englischen Übersetzungen

## Ordnerstruktur

```
projekt/
├── output/                     # Hauptausgabeverzeichnis
│   ├── videos/                # Heruntergeladene Videos/Audio
│   │   └── video_xyz.wav     # Extrahierte Audiodateien
│   ├── transcripts/          # Transkripte und Prompts
│   │   ├── video_xyz_transcript.txt    # Whisper Transkript
│   │   └── video_xyz_summary_prompt.txt # Vorbereiteter Prompt
│   └── results/              # KI-Analyseergebnisse
│       └── video_xyz_result.txt        # GPT-3.5 Ausgabe
│
├── downloader.py              # Video-Download und -Verarbeitung
├── transcribe.py             # Whisper Transkription
├── ai_client.py              # OpenAI GPT Integration
├── pipeline.py               # Orchestrierung der Pipeline
├── prompt.txt                # Template für KI-Analyse
├── video.txt                 # Quelldateien/URLs
├── requirements.uv           # Python-Abhängigkeiten
└── .env                      # API-Konfiguration
```

## Voraussetzungen

- Python 3.8+
- FFmpeg
- OpenAI API Key
- uv (Python Paketmanager)

## Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd VideoTranskript4
```

2. Python-Umgebung erstellen:
```bash
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Abhängigkeiten installieren:
```bash
uv pip install -r requirements.uv
```

4. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
# Fügen Sie Ihren OpenAI API Key in .env ein
```

## Verwendung

1. Video-URLs in `video.txt` einfügen:
```
# YouTube URLs
https://www.youtube.com/watch?v=example1
https://www.youtube.com/watch?v=example2

# Lokale Dateien
/pfad/zu/video.mp4
```

2. Pipeline ausführen:
```bash
python pipeline.py
```

Oder über VS Code:
- `Strg+Shift+B` für die vollständige Pipeline
- Task "Run Pipeline (Skip Download)" zum Überspringen des Downloads

## Modulare Ausführung

Die Pipeline kann auch modular ausgeführt werden:

1. Nur Download:
```bash
python downloader.py
```

2. Nur Transkription:
```bash
python transcribe.py
```

3. Nur KI-Analyse:
```bash
python ai_client.py
```

## Fehlerbehandlung

- Stellen Sie sicher, dass FFmpeg installiert ist
- Überprüfen Sie die OpenAI API Key Konfiguration
- Logs überprüfen für detaillierte Fehlerinformationen

## Dateiverarbeitung

1. **Video-Download**:
   - URLs/Pfade werden aus `video.txt` gelesen
   - Videos werden heruntergeladen/kopiert nach `output/videos/`
   - Audio wird automatisch extrahiert

2. **Transkription**:
   - Audio wird mit Whisper transkribiert
   - Transkript wird in `output/transcripts/` gespeichert
   - Analyse-Prompt wird vorbereitet

3. **KI-Analyse**:
   - Prompt wird aus `output/transcripts/` gelesen
   - GPT-3.5 generiert Analyse
   - Ergebnis wird in `output/results/` gespeichert

## Lizenz

MIT