#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations

from typing import Optional

from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

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
        ForeignKey("addresses.address_id", ondelete="SET NULL"),
        unique=True,  # <-- guarantees at most one address per student
    )

    # -- Relationship ---------------------------------------------------
    # address: Mapped[Optional["Address"]] = relationship(
    #     back_populates="student",
    #     uselist=False,  # <-- one‑to‑one, not a list
    #     cascade="all, delete-orphan",
    # )

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
        ForeignKey("students.student_id", ondelete="CASCADE"),
        unique=True,
    )
    # student: Mapped[Optional[Student]] = relationship(
    #     back_populates="address",
    #     uselist=False,
    # )

    def __repr__(self) -> str:
        return f"<Address {self.address_id} {self.city} {self.zipcode}>"


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base.metadata.create_all(engine)
with Session(engine) as session:
    s = Student(first_name="Ada", last_name="Lovelace")
    s.address = Address(address="12 Curzon St", city="London", zipcode="W1J 5HN")
    session.add(s)
    session.commit()
    s2: Student = session.query(Student).filter_by(last_name="Lovelace").one()
    print(s2.address.city)  # → "London"
    s2.address = None  # becomes an orphan ➜ will be deleted on flush
    session.commit()
