#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

# ----------------------------------------------------------------------
# 1.  Declarative base
# ----------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


# ----------------------------------------------------------------------
# 2.  ORM entities
# ----------------------------------------------------------------------


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(40), nullable=False)

    # FK column points to *the* address row that belongs to this student.
    address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.address_id"), unique=True
    )
    address: Mapped["Address"] = relationship(
        back_populates="student",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys=[address_id],
    )

    def __repr__(self) -> str:
        return f"<Student {self.student_id} {self.first_name} {self.last_name}>"


class Address(Base):
    __tablename__ = "addresses"

    address_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(60), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(15), nullable=False)

    # “Link back” – points to the owning student.
    # Must be UNIQUE to keep the association one‑to‑one.
    student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.student_id"), unique=True
    )
    student: Mapped["Student"] = relationship(
        back_populates="address",
        uselist=False,
        foreign_keys=[student_id],
    )

    def __repr__(self) -> str:
        return f"<Address {self.address_id} {self.city} {self.zipcode}>"


if __name__ == "__main__":
    # Create and persist
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:

        s = Student(first_name="Ada", last_name="Lovelace")
        s.address = Address(address="12 Curzon St", city="London", zipcode="W1J 5HN")
        session.add(s)
        session.commit()

        # Query
        s2: Student = session.query(Student).filter_by(last_name="Lovelace").one()
        print(s2.address.city)  # → "London"

        # Removing the address:
        s2.address = None  # becomes an orphan ➜ will be deleted on flush
        session.commit()
