import tkinter
import customtkinter
from tkinter import filedialog 
import yt_dlp
import threading
import os
import imageio_ffmpeg


ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
python_path = R"C:\Users\User\AppData\Local\Programs\Python\Python313"
os.environ['TCL_LIBRARY'] = os.path.join(python_path, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(python_path, 'tcl', 'tk8.6')

pasta_destino = ""

def escolher_pasta():
    global pasta_destino
    caminho = filedialog.askdirectory()
    if caminho:
        pasta_destino = caminho
        label_pasta.configure(text=f"Pasta: ...{caminho[-30:]}", text_color="white")

def startDownload():
    url = url_var.get()
    if not url:
        status_label.configure(text="Insira um link!", text_color="red")
        return
    if not pasta_destino:
        status_label.configure(text="Escolha uma pasta primeiro!", text_color="yellow")
        return

    def thread_download():
        try:
            status_label.configure(text="Baixando...", text_color="white")
            
            ydl_opts = {
                'ffmpeg_location': ffmpeg_path,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web']
                    }
                },
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            status_label.configure(text="Download concluído!", text_color="green")
        except Exception:
            status_label.configure(text="Erro no download.", text_color="red")

    threading.Thread(target=thread_download).start()

app = customtkinter.CTk()
app.geometry("720x520")
app.title("MP3 Downloader")

customtkinter.CTkLabel(app, text="Downloader de MP3", font=("Arial", 24)).pack(pady=20)

url_var = tkinter.StringVar()
link_entry = customtkinter.CTkEntry(app, width=500, height=40, placeholder_text="Cole o link do YouTube aqui", textvariable=url_var)
link_entry.pack(pady=10)

btn_pasta = customtkinter.CTkButton(app, text="Escolher pasta de destino", fg_color="gray", command=escolher_pasta)
btn_pasta.pack(pady=5)

label_pasta = customtkinter.CTkLabel(app, text="Nenhuma pasta selecionada", font=("Arial", 12))
label_pasta.pack()

status_label = customtkinter.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=20)

download_button = customtkinter.CTkButton(app, text="BAIXAR AGORA", width=200, height=50, font=("Arial", 16, "bold"), command=startDownload)
download_button.pack(pady=10)

if __name__ == '__main__':
    app.mainloop()