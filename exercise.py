#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase): ...  # noqa: E701


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    started: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # 2‑way relationship: Workout ➜ Exercise (one‑to‑many)
    # `back_populates` keeps both ends in sync.
    exercises: Mapped[List["Exercise"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Workout id={self.id} name={self.name!r} exercises={len(self.exercises)}>"
        )


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    weight_kg: Mapped[float]
    reps: Mapped[int]
    # --- Foreign‑key column that makes this row belong to ONE workout ---
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE")
    )
    workout: Mapped["Workout"] = relationship(back_populates="exercises")

    def __repr__(self) -> str:
        return f"<Exercise id={self.id} {self.name} {self.weight_kg} kg × {self.reps} reps>"


# In‑memory SQLite for demo; switch to your real DB URI in practice
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
Base.metadata.create_all(engine)
with Session(engine) as session:
    # Create a workout with three exercises
    w = Workout(name="Monday Heavy Squat Day")
    w.exercises.extend(
        [
            Exercise(name="Squat", weight_kg=110, reps=5),
            Exercise(name="Paused Squat", weight_kg=100, reps=3),
            Exercise(name="Front Squat", weight_kg=80, reps=3),
        ]
    )
    session.add(w)
    session.commit()
    loaded = session.get(Workout, w.id)
    print(loaded)  # ➜ <Workout id=1 name='Monday Heavy Squat Day' exercises=3>
    print(loaded.exercises[0])  # ➜ <Exercise id=1 Squat 110 kg × 5 reps>
