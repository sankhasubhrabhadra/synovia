from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True) # Attached user owner ID
    idea = Column(Text, nullable=False)
    status = Column(String, default="pending", nullable=False, index=True)
    current_step = Column(String, default="manager", nullable=False)
    progress_percentage = Column(Integer, default=0)
    blueprint_json = Column(JSON, nullable=True)
    step_logs_json = Column(JSON, nullable=True, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Composite performance indexes for multi-user scaling
Index("idx_projects_user_created", ProjectDB.user_id, ProjectDB.created_at.desc())
