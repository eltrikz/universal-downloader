import gradio as gr
import yt_dlp
import os
import tempfile

def download_media(url, format_choice):
    if not url:
        return None, "Bitte gib einen Link ein."
    
    temp_dir = tempfile.gettempdir()
    
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'noplaylist': True,
        'quiet': False,
    }
    
    if format_choice == "Audio (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Video (MP4)
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            expected_filename = ydl.prepare_filename(info)
            
            if format_choice == "Audio (MP3)":
                base, _ = os.path.splitext(expected_filename)
                expected_filename = base + ".mp3"

            if os.path.exists(expected_filename):
                return expected_filename, f"Erfolgreich heruntergeladen: {info.get('title', 'Download')}"
            else:
                return None, "Download war erfolgreich, aber die Datei konnte nicht formatiert werden."
    except Exception as e:
        return None, f"Fehler beim Download: {str(e)}"

with gr.Blocks(title="Universal Downloader") as demo:
    gr.Markdown("# 🚀 Universal Downloader")
    gr.Markdown("Füge einen Link von YouTube, Instagram, Reddit, X (Twitter), Facebook etc. ein und lade das Video oder die Tonspur herunter.")
    
    url_input = gr.Textbox(label="Link einfügen", placeholder="https://...")
    format_choice = gr.Radio(["Video (MP4)", "Audio (MP3)"], label="Format", value="Video (MP4)")
    
    btn_download = gr.Button("Herunterladen", variant="primary")
    
    file_output = gr.File(label="Dein fertiger Download")
    text_output = gr.Textbox(label="Status")

    btn_download.click(
        fn=download_media,
        inputs=[url_input, format_choice],
        outputs=[file_output, text_output]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port, ssr_mode=False)
