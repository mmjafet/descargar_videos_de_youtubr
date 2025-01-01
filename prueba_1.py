from yt_dlp import YoutubeDL

video_url = "https://www.youtube.com/watch?v=VgDgWzBL7s4&ab_channel=AlejandroRAR"
ydl_opts = {
    'format': 'best',  # Descargar la mejor calidad de video
    'outtmpl': 'video.%(ext)s',  # Guardar el video con un nombre y extensión
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
print("Descarga completada!")
