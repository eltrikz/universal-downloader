import os
import tempfile

import gradio as gr
import yt_dlp


VIDEO_QUALITIES = {
    "Beste verfügbare Qualität": None,
    "1080p": 1080,
    "720p": 720,
    "480p": 480,
    "360p": 360,
    "144p": 144,
}

AUDIO_BITRATES = {
    "320 kbps": "320",
    "256 kbps": "256",
    "192 kbps": "192",
    "128 kbps": "128",
}


def download_media(url, format_choice, video_quality, audio_quality):
    if not url:
        return None, "Bitte gib einen Link ein."

    temp_dir = tempfile.gettempdir()
    ydl_opts = {
        "outtmpl": os.path.join(temp_dir, "%(title).80B-%(id)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
        "quiet": False,
    }

    if format_choice == "Audio (MP3)":
        bitrate = AUDIO_BITRATES[audio_quality]
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }],
            "postprocessor_args": {
                "FFmpegExtractAudio": ["-b:a", f"{bitrate}k"]
            },
        })
    else:
        height = VIDEO_QUALITIES[video_quality]
        if height is None:
            video_format = "bestvideo*+bestaudio/best"
        else:
            # Exact height only: no fallback to a different resolution.
            video_format = f"bestvideo[height={height}]+bestaudio/best[height={height}]"
        ydl_opts.update({
            "format": video_format,
            "merge_output_format": "mp4",
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if format_choice == "Audio (MP3)":
            filename = os.path.splitext(filename)[0] + ".mp3"
            detail = f"MP3 mit Zielbitrate {bitrate} kbps"
        else:
            detail = f"Video in {height}p" if height else "Video in bester verfügbarer Qualität"

        if os.path.exists(filename):
            title = info.get("title", "Download")
            return filename, f"Heruntergeladen: {title} — {detail}"
        return None, "Der Download lief durch, aber die Ausgabedatei wurde nicht gefunden."
    except yt_dlp.utils.DownloadError as error:
        if format_choice == "Video (MP4)" and "Requested format is not available" in str(error):
            return None, f"{video_quality} ist für dieses Video nicht verfügbar."
        return None, f"Fehler beim Download: {error}"
    except Exception as error:
        return None, f"Fehler beim Download: {error}"


with gr.Blocks(title="Universal Downloader") as demo:
    gr.Markdown("# Universal Downloader")
    gr.Markdown(
        "Wähle bei Video eine exakte Auflösung. Ist sie bei der Quelle nicht vorhanden, "
        "wird keine andere Auflösung heruntergeladen."
    )
    url_input = gr.Textbox(label="Link einfügen", placeholder="https://...")
    with gr.Row():
        format_choice = gr.Radio(
            ["Video (MP4)", "Audio (MP3)"],
            label="Format",
            value="Video (MP4)",
        )
        video_quality = gr.Dropdown(
            choices=list(VIDEO_QUALITIES),
            label="Videoauflösung",
            value="Beste verfügbare Qualität",
        )
        audio_quality = gr.Dropdown(
            choices=list(AUDIO_BITRATES),
            label="MP3-Bitrate",
            value="320 kbps",
        )
    btn_download = gr.Button("Herunterladen", variant="primary")
    with gr.Row():
        file_output = gr.File(label="Dein fertiger Download")
        text_output = gr.Textbox(label="Status")

    btn_download.click(
        fn=download_media,
        inputs=[url_input, format_choice, video_quality, audio_quality],
        outputs=[file_output, text_output],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
