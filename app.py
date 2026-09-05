import gradio as gr
import yt_dlp
import os
import tempfile

def download_media(url, format_choice, quality_choice):
    if not url:
        return None, "Bitte gib einen Link ein."
    
    temp_dir = tempfile.gettempdir()
    
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'noplaylist': True,
        'quiet': False,
    }
    
    # Qualitäts-Mapping
    if "Beste" in quality_choice:
        vid_height = "" # best possible
        aud_qual = "320"
    elif "1080p" in quality_choice:
        vid_height = "[height<=1080]"
        aud_qual = "256"
    elif "720p" in quality_choice:
        vid_height = "[height<=720]"
        aud_qual = "192"
    else: # 480p
        vid_height = "[height<=480]"
        aud_qual = "128"

    if format_choice == "Audio (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': aud_qual,
            }],
        })
    else:
        # Video (MP4)
        if vid_height == "":
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:
            format_str = f'bestvideo{vid_height}[ext=mp4]+bestaudio[ext=m4a]/best{vid_height}[ext=mp4]/best'
            
        ydl_opts.update({
            'format': format_str,
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
                return expected_filename, f"Erfolgreich heruntergeladen: {info.get('title', 'Download')} ({quality_choice})"
            else:
                return None, "Download war erfolgreich, aber die Datei konnte nicht formatiert werden."
    except Exception as e:
        return None, f"Fehler beim Download: {str(e)}"

with gr.Blocks(title="Universal Downloader (Pro)") as demo:
    gr.Markdown("# 🚀 Universal Downloader (Pro)")
    gr.Markdown("Füge einen Link von YouTube, Instagram, Reddit, X, Facebook etc. ein und wähle deine gewünschte Qualität.")
    
    with gr.Row():
        url_input = gr.Textbox(label="Link einfügen", placeholder="https://...")
        
    with gr.Row():
        format_choice = gr.Radio(["Video (MP4)", "Audio (MP3)"], label="Format", value="Video (MP4)")
        quality_choice = gr.Dropdown(
            choices=[
                "Beste Qualität (Max / 320 kbps)", 
                "Hoch (1080p / 256 kbps)", 
                "Mittel (720p / 192 kbps)", 
                "Niedrig (480p / 128 kbps)"
            ], 
            label="Qualitätsstufe", 
            value="Beste Qualität (Max / 320 kbps)"
        )
    
    btn_download = gr.Button("Herunterladen", variant="primary")
    
    with gr.Row():
        file_output = gr.File(label="Dein fertiger Download")
    text_output = gr.Textbox(label="Status")

    btn_download.click(
        fn=download_media,
        inputs=[url_input, format_choice, quality_choice],
        outputs=[file_output, text_output]
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
