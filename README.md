# Universal Downloader

**Link rein. Format wählen. Datei herunterladen.**

Eine selbst gehostete Weboberfläche für Video- und Audio-Downloads: Füge eine unterstützte URL ein, wähle Video oder MP3 und stelle deine gewünschte Qualitätsstufe ein. Die deutsche Oberfläche führt dich durch den Download.

Built with **Python · Gradio · yt-dlp · FFmpeg**.

[Loslegen](#schnellstart-mit-docker) · [Feedback geben](https://github.com/eltrikz/universal-downloader/issues)

## Das bietet das Projekt

- **Bedienung im Browser:** Linkfeld, Formatauswahl, Qualitätsstufe und Download-Datei in einer Oberfläche.
- **Video oder Audio:** Video-Download mit bevorzugtem MP4-Format oder Audio-Extraktion als MP3.
- **Vier Qualitätsstufen:** Beste verfügbare Qualität sowie Voreinstellungen für 1080p, 720p und 480p.
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
3. Wähle die Qualitätsstufe und klicke auf **Herunterladen**.
4. Speichere die Datei aus **Dein fertiger Download**.

## Qualitätsauswahl

| Auswahl | Video-Voreinstellung | MP3-Zielbitrate |
| --- | --- | --- |
| Beste Qualität | Beste verfügbare Auswahl | 320 kbps |
| Hoch | Bevorzugt bis 1080p | 256 kbps |
| Mittel | Bevorzugt bis 720p | 192 kbps |
| Niedrig | Bevorzugt bis 480p | 128 kbps |

Die verfügbare Quelle bestimmt die tatsächliche Qualität. Höhere MP3-Zielbitraten verbessern keine bereits verlustbehaftete Quelle. Der Video-Fallback kann ein anderes Format oder eine andere Auflösung liefern; MP4 und die ausgewählte Höhenbegrenzung sind nicht in jedem Fall garantiert.

## Aktueller Stand

Das Projekt ist eine frühe, kompakte Anwendung für einzelne Medienlinks. Ein Playlist- oder Stapel-Workflow, eine Anmeldung und eine Cookie-Konfiguration in der Oberfläche sind derzeit nicht implementiert. Die Docker-Anleitung ist aus dem vorhandenen Dockerfile abgeleitet; sie ist kein Nachweis eines durchgeführten Ende-zu-Ende-Tests.

Für den eigenen Rechner bindet der obige Docker-Befehl den Port nur an localhost. Die Anwendung enthält selbst keine Zugangskontrolle.

## Feedback willkommen

Fehlt dir eine Funktion oder schlägt ein Download fehl? [Erstelle ein Issue](https://github.com/eltrikz/universal-downloader/issues) mit der Plattform, der gewählten Einstellung und einer bereinigten Fehlermeldung. Bitte keine Cookies, Zugangsdaten oder privaten Medienlinks posten.

Wenn dir das Projekt hilft, freue ich mich über einen GitHub-Star.

## English summary

Universal Downloader is a self-hosted German-language web UI for yt-dlp. Paste a supported media URL, choose video (MP4 preferred) or MP3 audio, select a quality preset, and retrieve the resulting file. A Dockerfile with FFmpeg is included. Source availability and platform support vary.

Use it only for content you own or have permission to download.
