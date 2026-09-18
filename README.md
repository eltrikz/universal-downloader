# Universal Downloader

**Link rein. Format wählen. Datei herunterladen.**

Eine selbst gehostete Weboberfläche für Video- und Audio-Downloads: Füge eine unterstützte URL ein, wähle Video oder MP3 und stelle die gewünschte Auflösung oder MP3-Bitrate ein.

Built with **Python · Gradio · yt-dlp · FFmpeg**.

[Loslegen](#schnellstart-mit-docker) · [Feedback geben](https://github.com/eltrikz/universal-downloader/issues)

## Das bietet das Projekt

- **Bedienung im Browser:** Linkfeld, Formatauswahl, Auflösung oder Bitrate und Download-Datei in einer Oberfläche.
- **Video oder Audio:** Video-Download mit bevorzugtem MP4-Format oder Audio-Extraktion als MP3.
- **Exakte Videoauflösung:** Beste Qualität sowie 1080p, 720p, 480p, 360p und 144p.
- **Getrennte MP3-Bitrate:** 320, 256, 192 oder 128 kbps.
- **Selbst hosten:** Dockerfile mit Python 3.11 und FFmpeg enthalten.
- **Statusanzeige:** Rückmeldung zum Ergebnis oder zu Download-Fehlern.

Die unterstützten Quellen hängen von yt-dlp, der jeweiligen Plattform und der Zugänglichkeit des Inhalts ab. Eine URL ist keine Garantie für einen erfolgreichen Download.

## Schnellstart mit Docker

Voraussetzungen: Git und eine laufende Docker-Installation.

```sh
git clone https://github.com/eltrikz/universal-downloader.git
cd universal-downloader
docker build -t universal-downloader .
docker run --rm -p 127.0.0.1:10000:10000 universal-downloader
```

Öffne anschließend **http://localhost:10000**.

1. Füge einen Link zu einem eigenen oder zum Download freigegebenen Medium ein.
2. Wähle **Video (MP4)** oder **Audio (MP3)**.
3. Wähle die Videoauflösung oder MP3-Bitrate und klicke auf **Herunterladen**.
4. Speichere die Datei aus **Dein fertiger Download**.

## Qualitätsauswahl

| Bereich | Auswahl | Verhalten |
| --- | --- | --- |
| Video | Beste verfügbare Qualität | Lädt die beste verfügbare Videospur. |
| Video | 1080p, 720p, 480p, 360p oder 144p | Lädt nur die genau ausgewählte Höhe. Ist sie nicht vorhanden, bricht der Download mit einer Meldung ab. |
| MP3 | 320, 256, 192 oder 128 kbps | Konvertiert die Audiospur mit der ausgewählten Zielbitrate. |

Die App lädt bei einer gewählten Videohöhe keine andere Auflösung als Ersatz. Höhere MP3-Bitraten verbessern keine bereits verlustbehaftete Quelle.

## Aktueller Stand

Das Projekt ist eine frühe, kompakte Anwendung für einzelne Medienlinks. Ein Playlist- oder Stapel-Workflow, eine Anmeldung und eine Cookie-Konfiguration in der Oberfläche sind derzeit nicht implementiert. Die Docker-Anleitung ist aus dem vorhandenen Dockerfile abgeleitet; sie ist kein Nachweis eines durchgeführten Ende-zu-Ende-Tests.

Für den eigenen Rechner bindet der obige Docker-Befehl den Port nur an localhost. Die Anwendung enthält selbst keine Zugangskontrolle.

## Feedback willkommen

Fehlt dir eine Funktion oder schlägt ein Download fehl? [Erstelle ein Issue](https://github.com/eltrikz/universal-downloader/issues) mit der Plattform, der gewählten Einstellung und einer bereinigten Fehlermeldung. Bitte keine Cookies, Zugangsdaten oder privaten Medienlinks posten.

Wenn dir das Projekt hilft, freue ich mich über einen GitHub-Star.

## English summary

Universal Downloader is a self-hosted German-language web UI for yt-dlp. Paste a supported media URL, choose video or MP3 audio, select an exact video resolution or an MP3 bitrate, and retrieve the resulting file. Exact video selections fail when the source does not provide that height. A Dockerfile with FFmpeg is included.

Use it only for content you own or have permission to download.
