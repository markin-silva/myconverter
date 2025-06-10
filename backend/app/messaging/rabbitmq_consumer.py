import asyncio
import aio_pika
import json
import os
import yt_dlp

from app.database import database
from app.crud import update_download_status
from app.models import DownloadStatus

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

AUDIO_FORMATS = ['mp3', 'm4a', 'aac', 'wav', 'opus']
VIDEO_FORMATS = ['mp4', 'webm', 'mkv']

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"

async def handle_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())

        download_id = data["id"]
        url = data["url"]
        format_requested = data["format"]

        output_template = os.path.join(DOWNLOAD_DIR, f"{download_id}.%(ext)s")

        if format_requested in AUDIO_FORMATS:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_requested,
                    'preferredquality': '192',
                }],
                'outtmpl': output_template,
            }
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': format_requested,
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegMerger'
                }],
            }

        try:
            print(f"⏬ Iniciando download: {url} ({format_requested})")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            downloaded_files = os.listdir(DOWNLOAD_DIR)
            matching_files = [f for f in downloaded_files if download_id in f]

            if not matching_files:
                raise Exception("Arquivo não encontrado após download.")

            await update_download_status(download_id, DownloadStatus.completed.name)
            print(f"✅ Download finalizado: {matching_files[0]}")

        except Exception as e:
            await update_download_status(download_id, DownloadStatus.failed.name)
            print(f"❌ Erro no download {download_id}: {e}")

async def main():
    await database.connect()
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("download_queue", durable=True)

    await queue.consume(handle_message)
    print("🎧 Worker escutando a fila 'download_queue'...")
    await asyncio.Future()  # loop eterno

if __name__ == "__main__":
    asyncio.run(main())
