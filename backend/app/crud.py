from app.models import Download, DownloadStatus
from app.database import database
from sqlalchemy.future import select

async def create_download(user_id: str, video_url: str, format: str):
    query = Download.__table__.insert().values(
        user_id=user_id,
        video_url=video_url,
        format=format,
        status=DownloadStatus.pending.name,
    )
    return await database.execute(query)

async def update_download_status(id: str, status: str):
    query = (
        Download.__table__
        .update()
        .where(Download.id == id)
        .values(status=status)
    )
    return await database.execute(query)

async def update_download_s3_key(download_id: str, s3_key: str):
    query = select(Download).where(Download.id == download_id)
    result = await database.fetch_one(query)
    
    if result:
        update_query = (
            Download.__table__
            .update()
            .where(Download.id == download_id)
            .values(s3_key=s3_key)
        )
        await database.execute(update_query)

async def get_download_by_file_name(file_name: str):
    query = select(Download).where(Download.s3_key == file_name)
    return await database.fetch_one(query)