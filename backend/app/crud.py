from app.models import Download, DownloadStatus
from app.database import database

async def create_download(user_id: str, video_url: str, format: str, file_path: str):
    query = Download.__table__.insert().values(
        user_id=user_id,
        video_url=video_url,
        format=format,
        status=DownloadStatus.pending.name,
        file_path=file_path
    )
    return await database.execute(query)

async def update_download_status(file_path: str, status: str):
    query = (
        Download.__table__
        .update()
        .where(Download.file_path == file_path)
        .values(status=status)
    )
    return await database.execute(query)