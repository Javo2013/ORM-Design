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

class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    breed: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"))

    # Relationships
    owner: Mapped["Owner"] = relationship("Owner", back_populates="pets")
    veterinarians: Mapped[list["Veterinarian"]] = relationship(
        "Veterinarian",
        secondary="appointments",
        back_populates="pets"
    )

    def __repr__(self):
        return f"<Pet(name={self.name}, species={self.species})>

class Veterinarian(Base):
    __tablename__ = "veterinarians"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    pets: Mapped[list["Pet"]] = relationship(
        "Pet",
        secondary="appointments",
        back_populates="veterinarians"
    )

    def __repr__(self):
        return f"<Vet(name={self.name}, specialization={self.specialization})>

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"))
    veterinarian_id: Mapped[int] = mapped_column(ForeignKey("veterinarians.id"))
    appointment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="Scheduled")

    # Relationships
    pet: Mapped["Pet"] = relationship("Pet")
    veterinarian: Mapped["Veterinarian"] = relationship("Veterinarian")

    def __repr__(self):
        return f"<Appointment(pet_id={self.pet_id}, vet_id={self.veterinarian_id}, status={self.status})>"
# 3️⃣ Create session
Session = sessionmaker(bind=engine)
session = Session()