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

    student_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    # ── Relationship only; no FK column here ──
    address: Mapped["Address"] = relationship(
        back_populates="student",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Student {self.student_id} {self.first_name} {self.last_name}>"


class Address(Base):
    __tablename__ = "addresses"

    address_id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    city: Mapped[str]
    zipcode: Mapped[str]

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE"),
        unique=True,
    )
    student: Mapped[Student] = relationship(back_populates="address", uselist=False)

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
    print(s2.address.city)  # "London"
    s2.address = None  # becomes an orphan ➜ will be deleted on flush
    session.commit()
