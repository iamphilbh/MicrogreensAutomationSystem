from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Index, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# TODO: Move this to a YAML configuration file.
DATABASE_URL = "sqlite:///test.db"

class Base(DeclarativeBase):
    pass

class SystemType(Base):
    __tablename__ = "system_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    system_type: Mapped[str] = mapped_column(String(5))

class SystemState(Base):
    __tablename__ = "system_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    system_state: Mapped[str] = mapped_column(String(3))

class SystemEvent(Base):
    __tablename__ = "system_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    system_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("system_types.id"))
    system_state_id: Mapped[int] = mapped_column(Integer, ForeignKey("system_states.id"))
    system_event_timestamp: Mapped[datetime] = mapped_column(DateTime)
    record_created_timestamp: Mapped[datetime] = mapped_column(DateTime)

    idx_system_type_event_timestamp = Index("idx_system_type_event_timestamp", system_type_id, system_event_timestamp.desc())

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)