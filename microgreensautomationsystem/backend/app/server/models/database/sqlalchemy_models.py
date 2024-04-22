from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Index, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "sqlite:///test.db"

class Base(DeclarativeBase):
    pass

class FactSystemEvents(Base):
    __tablename__ = "fact_system_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    system_type: Mapped[str] = mapped_column(String(5))
    system_state: Mapped[str] = mapped_column(String(3))
    system_event_timestamp: Mapped[datetime] = mapped_column(DateTime)
    record_created_timestamp: Mapped[datetime] = mapped_column(DateTime)

    idx_system_type_event_timestamp = Index("idx_system_type_event_timestamp", system_type, system_event_timestamp.desc())

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)