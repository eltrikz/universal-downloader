import os
import shutil

import gradio as gr
import yt_dlp


AUDIO_BITRATES = {
    "320 kbps": "320",
    "256 kbps": "256",
    "192 kbps": "192",
    "128 kbps": "128",
}

DOWNLOAD_DIR = os.path.join(
    os.path.expanduser("~"), "Documents", "Universal Downloader"
)


def find_ffmpeg_location():
    """Find FFmpeg on PATH or in the standard WinGet package folder."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return os.path.dirname(ffmpeg_path)

    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return None

    package_dir = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages")
    if not os.path.isdir(package_dir):
        return None

    for root, _, files in os.walk(package_dir):
        if "ffmpeg.exe" in files:
            return root
    return None


def analyze_media(url):
    if not url:
        return gr.update(choices=[], value=None), "Bitte gib zuerst einen Link ein."

    options = {"quiet": True, "noplaylist": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        heights = sorted({
            item["height"]
            for item in info.get("formats", [])
            if item.get("height") and item.get("vcodec") != "none"
        })
        choices = [f"{height}p" for height in heights]
        if not choices:
            return gr.update(choices=[], value=None), "Keine Videoauflösungen gefunden."

        title = info.get("title", "Dieses Video")
        available = ", ".join(choices)
        return (
            gr.update(choices=choices, value=choices[-1]),
            f"{title}: verfügbar sind {available}. Wähle eine Auflösung und lade sie herunter.",
        )
    except Exception as error:
        return gr.update(choices=[], value=None), f"Analyse fehlgeschlagen: {error}"


def toggle_quality_controls(format_choice):
    is_video = format_choice == "Video (MP4)"
    return (
        gr.update(visible=is_video),
        gr.update(visible=not is_video),
        gr.update(visible=is_video),
        gr.update(visible=is_video),
    )


def download_media(url, format_choice, video_quality, audio_quality):
    if not url:
        return None, "Bitte gib einen Link ein."

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    ydl_opts = {
        "outtmpl": os.path.join(
            DOWNLOAD_DIR, "%(title).80B-%(id)s-%(format_id)s.%(ext)s"
        ),
        "restrictfilenames": True,
        "noplaylist": True,
        "quiet": False,
    }

    ffmpeg_location = find_ffmpeg_location()
    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    if format_choice == "Audio (MP3)":
        if not ffmpeg_location:
            return None, "FFmpeg wurde nicht gefunden. Installiere es mit: winget install --id Gyan.FFmpeg -e --source winget"
        bitrate = AUDIO_BITRATES[audio_quality]
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }],
        })
        detail = f"MP3 mit Zielbitrate {bitrate} kbps"
    else:
        if not video_quality:
            return None, "Klicke zuerst auf Video analysieren und wähle eine verfügbare Auflösung."

        height = int(video_quality.removesuffix("p"))
        ydl_opts.update({
            "format": f"bestvideo[height={height}]+bestaudio/best[height={height}]",
            "merge_output_format": "mp4",
        })
        detail = f"Video in {height}p"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if format_choice == "Audio (MP3)":
            filename = os.path.splitext(filename)[0] + ".mp3"

        if os.path.exists(filename):
            title = info.get("title", "Download")
            return filename, f"Heruntergeladen: {title} — {detail}"
        return None, "Der Download lief durch, aber die Ausgabedatei wurde nicht gefunden."
    except yt_dlp.utils.DownloadError as error:
        if format_choice == "Video (MP4)" and "Requested format is not available" in str(error):
            return None, f"{video_quality} ist für dieses Video nicht verfügbar. Analysiere das Video erneut."
        return None, f"Fehler beim Download: {error}"
    except Exception as error:
        return None, f"Fehler beim Download: {error}"


with gr.Blocks(title="Universal Downloader") as demo:
    gr.Markdown("# Universal Downloader")
    gr.Markdown("Füge einen Link ein, analysiere die vorhandenen Videoauflösungen und wähle danach die gewünschte Qualität.")

    url_input = gr.Textbox(label="Link einfügen", placeholder="https://...")
    btn_analyze = gr.Button("Video analysieren")
    analysis_output = gr.Textbox(label="Verfügbare Auflösungen", interactive=False)

    with gr.Row():
        format_choice = gr.Radio(
            ["Video (MP4)", "Audio (MP3)"], label="Format", value="Video (MP4)"
        )
        video_quality = gr.Dropdown(
            choices=[], label="Videoauflösung", value=None
        )
        audio_quality = gr.Dropdown(
            choices=list(AUDIO_BITRATES), label="MP3-Bitrate", value="320 kbps", visible=False
        )

    btn_download = gr.Button("Herunterladen", variant="primary")
    with gr.Row():
        file_output = gr.File(label="Dein fertiger Download")
        text_output = gr.Textbox(label="Status")

    btn_analyze.click(
        fn=analyze_media,
        inputs=url_input,
        outputs=[video_quality, analysis_output],
    )
    format_choice.change(
        fn=toggle_quality_controls,
        inputs=format_choice,
        outputs=[video_quality, audio_quality, btn_analyze, analysis_output],
    )
    btn_download.click(
        fn=download_media,
        inputs=[url_input, format_choice, video_quality, audio_quality],
        outputs=[file_output, text_output],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
