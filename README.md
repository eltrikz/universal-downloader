# Universal Downloader

**Free, local, and ad-free.**

Universal Downloader is an English web interface for yt-dlp. It runs on your own Windows PC, needs neither Git nor Docker, and shows no advertising. Paste a link, inspect available video resolutions, then save an MP4 or MP3.

> The app requires no account or payment. Only use it for media you own or are allowed to download.

## Features

- **MP4 at an exact resolution:** Analyze the media first, then choose a real available resolution from 144p through 4K when offered.
- **MP3 without a video selection:** Audio mode offers only 320, 256, 192, or 128 kbps.
- **Saves to Documents:** Finished files go to `Documents/Universal Downloader`.
- **FFmpeg detection:** The app automatically detects the free WinGet FFmpeg package.
- **Local-only access:** The server listens at `http://localhost:10000` and is not exposed on your network.

Platforms, individual media, and yt-dlp determine the formats that are available. If a requested resolution is unavailable, the app reports it instead of silently downloading another resolution.

## Free Windows installation — no Git or Docker

### 1. Download the project as a ZIP

1. Click **Code** on this GitHub page.
2. Select **Download ZIP**.
3. Extract the ZIP, for example in Downloads.

The app is normally located at:

```text
C:/Users/YOUR-NAME/Downloads/universal-downloader-main/universal-downloader-main
```

### 2. Install Python

Install the current free Python version from [python.org](https://www.python.org/downloads/windows/). In the installer, select **Add Python to PATH**.

Open PowerShell in the extracted project folder. In File Explorer, open the folder, type `powershell` into the address bar, and press Enter.

### 3. Install the Python packages

```powershell
py -m pip install -r requirements.txt
```

### 4. Install FFmpeg for free

```powershell
winget install --id Gyan.FFmpeg -e --source winget
```

The message *Found an existing package already installed* means it is already installed.

### 5. Start the app

```powershell
py app.py
```

Then open:

```text
http://localhost:10000
```

Do **not** open `http://0.0.0.0:10000`; that is a server bind address, not a browser address.

## Using the app

1. Paste a link.
2. For a video, choose **Video (MP4)** and click **Analyze video**.
3. Pick one of the detected resolutions, then click **Download**.
4. For audio, choose **Audio (MP3)**, choose a bitrate, then click **Download**.
5. Finished files are in `Documents/Universal Downloader`.

## Updating

Stop the app with `Ctrl+C`, then run:

```powershell
Invoke-WebRequest "https://raw.githubusercontent.com/eltrikz/universal-downloader/main/app.py" -OutFile app.py
py -m pip install --upgrade -r requirements.txt
py app.py
```

## Troubleshooting

| Problem | Solution |
| --- | --- |
| “This site can't be reached” | Start the app with `py app.py`, then open `http://localhost:10000`. |
| FFmpeg was not found | Run the FFmpeg install command above and restart the app. |
| A resolution is missing | The source does not offer that resolution; pick a detected option. |
| A download fails | Update packages with `py -m pip install --upgrade -r requirements.txt` and try again. |

## Note

This project uses [yt-dlp](https://github.com/yt-dlp/yt-dlp). Source support and available formats depend on each site. Never publish credentials or cookie files in an issue.
