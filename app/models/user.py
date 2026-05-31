from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String(50))
    middle_name = Column(String(50))
    last_name = Column(String(50))
    full_name = Column(String(150))          # Computed or stored
    phone = Column(String(20), unique=True, nullable=True)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Tints that this user created/owns (as the owner)
    tints = relationship(
        "Tint", 
        foreign_keys="Tint.user_id",  # Specify which foreign key to use
        back_populates="user", 
        cascade="all, delete-orphan"
    )
     # Tints that this user approved (as admin)
    approved_tints = relationship(
        "Tint",
        foreign_keys="Tint.approved_by",
        back_populates="approver"
    )

    # Relationships
    vehicles = relationship("Vehicle", back_populates="user", cascade="all, delete-orphan")
    # tints = relationship("Tint", back_populates="user", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")