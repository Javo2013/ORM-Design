from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column
from datetime import datetime

# 1️⃣ Create database engine
engine = create_engine("sqlite:///clinic.db", echo=True)

# 2️⃣ Base class
Base = declarative_base()

# 3️⃣ Create session
Session = sessionmaker(bind=engine)
session = Session()