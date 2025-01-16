from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy import DateTime, func


class Base(DeclarativeBase):
    pass


class Application(Base):
    __tablename__ = "applications"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())