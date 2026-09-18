# Universal Downloader

**Kostenlos, lokal und ohne Werbung.**

Universal Downloader ist eine deutschsprachige Oberfläche für yt-dlp. Sie läuft auf dem eigenen Windows-PC, braucht weder Git noch Docker und zeigt keine Werbung. Link einfügen, vorhandene Videoauflösungen prüfen und als MP4 oder MP3 speichern.

> Die App selbst verlangt kein Konto und keine Zahlung. Nutze sie nur für Medien, die dir gehören oder für die du eine Download-Erlaubnis hast.

## Funktionen

- **MP4 in exakter Auflösung:** Erst analysieren, dann eine tatsächlich verfügbare Auflösung wählen, von 144p bis 4K, wenn die Quelle sie anbietet.
- **MP3 ohne Videoauswahl:** Bei Audio stehen nur die MP3-Bitraten 320, 256, 192 und 128 kbps zur Auswahl.
- **Speichert direkt in Dokumente:** Fertige Dateien liegen in Dokumente/Universal Downloader.
- **FFmpeg-Erkennung:** Die App erkennt die kostenlose WinGet-Version von FFmpeg automatisch.
- **Lokal im Browser:** Die Oberfläche ist unter http://localhost:10000 erreichbar.

Die Plattform, das jeweilige Video und yt-dlp bestimmen, welche Formate verfügbar sind. Wenn eine ausgewählte Auflösung nicht angeboten wird, meldet die App das, statt stillschweigend eine andere Auflösung herunterzuladen.

## Kostenlos auf Windows installieren — ohne Git und Docker

### 1. Projekt als ZIP herunterladen

1. Klicke oben auf dieser GitHub-Seite auf **Code**.
2. Wähle **Download ZIP**.
3. Entpacke die ZIP-Datei, zum Beispiel in deinen Downloads-Ordner.

Danach liegt die App normalerweise hier:

```text
C:/Users/DEIN-NAME/Downloads/universal-downloader-main/universal-downloader-main
```

### 2. Python installieren

Installiere die kostenlose aktuelle Python-Version von [python.org](https://www.python.org/downloads/windows/). Aktiviere im Installer unbedingt **Add Python to PATH**.

Öffne danach PowerShell im entpackten Projektordner. Am einfachsten: Im Explorer den Ordner öffnen, oben in die Adressleiste `powershell` schreiben und Enter drücken.

### 3. Benötigte Python-Pakete installieren

Führe in PowerShell aus:

```powershell
py -m pip install -r requirements.txt
```

### 4. FFmpeg kostenlos installieren

FFmpeg wird für MP3-Konvertierung und das Zusammenführen von Video und Ton gebraucht:

```powershell
winget install --id Gyan.FFmpeg -e --source winget
```

Die Meldung *Found an existing package already installed* ist in Ordnung. FFmpeg ist dann bereits vorhanden.

### 5. App starten

```powershell
py app.py
```

Öffne danach im Browser:

```text
http://localhost:10000
```

Verwende **nicht** `http://0.0.0.0:10000`: Das ist nur die interne Server-Adresse und funktioniert nicht im Browser.

## So benutzt du die App

1. Füge einen Link ein.
2. Für ein Video: **Video (MP4)** wählen und auf **Video analysieren** klicken.
3. Wähle eine der gefundenen Auflösungen und klicke auf **Herunterladen**.
4. Für Audio: **Audio (MP3)** wählen, die gewünschte Bitrate einstellen und auf **Herunterladen** klicken.
5. Die App zeigt den vollständigen Speicherpfad an. Alle Dateien liegen in Dokumente/Universal Downloader.

## Aktualisieren

Wenn eine neue Version auf GitHub verfügbar ist, beende die App mit `Ctrl+C` und führe im Projektordner aus:

```powershell
Invoke-WebRequest "https://raw.githubusercontent.com/eltrikz/universal-downloader/main/app.py" -OutFile app.py
py -m pip install --upgrade -r requirements.txt
py app.py
```

## Häufige Probleme

| Problem | Lösung |
| --- | --- |
| Browser meldet „This site can't be reached“ | Starte die App mit `py app.py` und öffne `http://localhost:10000`. |
| FFmpeg wurde nicht gefunden | Führe den WinGet-Befehl aus Abschnitt 4 aus und starte die App danach neu. |
| Gewünschte Auflösung fehlt | Die Quelle stellt diese Auflösung nicht bereit. Wähle eine der analysierten Auflösungen. |
| Download schlägt fehl | Aktualisiere die Python-Pakete mit `py -m pip install --upgrade -r requirements.txt` und versuche es erneut. |

## Hinweis

Dieses Projekt verwendet [yt-dlp](https://github.com/yt-dlp/yt-dlp). Unterstützung und verfügbare Formate hängen von der jeweiligen Quelle ab. Bitte veröffentliche weder Zugangsdaten noch Cookie-Dateien in Issues.
