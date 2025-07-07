from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class DownloadStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    video_url = Column(String, nullable=False)
    format = Column(String, nullable=False)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.pending)
    s3_key = Column(String, nullable=True)

