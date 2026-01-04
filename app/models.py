import uuid 
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# from app.db import Base

class Base(DeclarativeBase):
    pass
    
class UserDB(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )
    
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email}, age={self.age})"