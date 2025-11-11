from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column
from datetime import datetime

# 1️⃣ Create database engine
engine = create_engine("sqlite:///clinic.db", echo=True)

# 2️⃣ Base class
Base = declarative_base()
class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationship to pets
    pets: Mapped[list["Pet"]] = relationship("Pet", back_populates="owner")

    def __repr__(self):
        return f"<Owner(name={self.name}, phone={self.phone})>
# 3️⃣ Create session
Session = sessionmaker(bind=engine)
session = Session()