from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column
from datetime import datetime

engine = create_engine("sqlite:///clinic.db", echo=True)

Base = declarative_base()

class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)

    pets: Mapped[list["Pet"]] = relationship("Pet", back_populates="owner")

    def __repr__(self):
        return f"<Owner(name={self.name}, phone={self.phone})>"


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    breed: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"))

    owner: Mapped["Owner"] = relationship("Owner", back_populates="pets")

    veterinarians: Mapped[list["Veterinarian"]] = relationship(
        "Veterinarian",
        secondary="appointments",
        back_populates="pets"
    )

    def __repr__(self):
        return f"<Pet(name={self.name}, species={self.species})>"


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
        return f"<Vet(name={self.name}, specialization={self.specialization})>"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"))
    veterinarian_id: Mapped[int] = mapped_column(ForeignKey("veterinarians.id"))
    appointment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="Scheduled")

    pet: Mapped["Pet"] = relationship("Pet")
    veterinarian: Mapped["Veterinarian"] = relationship("Veterinarian")

    def __repr__(self):
        return f"<Appointment(pet_id={self.pet_id}, vet_id={self.veterinarian_id}, status={self.status})>"


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(bind=engine)

# Owners
owner1 = Owner(name="John Smith", phone="302-555-1111", email="john@example.com")
owner2 = Owner(name="Mary Johnson", phone="302-555-2222", email="mary@example.com")
owner3 = Owner(name="David Brown", phone="302-555-3333", email="david@example.com")

# Pets
pet1 = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=5, owner=owner1)
pet2 = Pet(name="Mittens", species="Cat", breed="Siamese", age=3, owner=owner2)
pet3 = Pet(name="Tweety", species="Bird", breed="Canary", age=1, owner=owner3)
pet4 = Pet(name="Rocky", species="Dog", breed="Bulldog", age=4, owner=owner2)
pet5 = Pet(name="Luna", species="Cat", breed="Persian", age=2, owner=owner1)
pet6 = Pet(name="Max", species="Dog", breed="Beagle", age=6, owner=owner3)

# Veterinarians
vet1 = Veterinarian(name="Dr. Allen", specialization="Surgery", email="allen@clinic.com")
vet2 = Veterinarian(name="Dr. Kim", specialization="Dermatology", email="kim@clinic.com")

# Appointments
appt1 = Appointment(pet=pet1, veterinarian=vet1, notes="Annual check-up")
appt2 = Appointment(pet=pet2, veterinarian=vet2, notes="Skin allergy treatment")
appt3 = Appointment(pet=pet3, veterinarian=vet1, notes="Wing injury")
appt4 = Appointment(pet=pet4, veterinarian=vet2, notes="Ear infection")
appt5 = Appointment(pet=pet5, veterinarian=vet1, notes="Vaccination")
appt6 = Appointment(pet=pet6, veterinarian=vet2, notes="Routine check")

session.add_all([
    owner1, owner2, owner3,
    pet1, pet2, pet3, pet4, pet5, pet6,
    vet1, vet2,
    appt1, appt2, appt3, appt4, appt5, appt6
])

session.commit()