#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import (
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column,
    Session,
)
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


class ExerciseName(Base):
    __tablename__ = "exercise_names"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="exercise_name")

    def __repr__(self):
        return f"<ExerciseName(id={self.id}, name={self.name})>"


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    started: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    exercises: Mapped[List["Exercise"]] = relationship(
        back_populates="workout", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Workout(id={self.id}, started={self.started.date().isoformat()}, "
            f"exercises={', '.join(e.exercise_name.name for e in self.exercises)}>"
        )


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)

    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"), nullable=False)
    workout: Mapped["Workout"] = relationship(back_populates="exercises")

    exercise_name_id: Mapped[int] = mapped_column(
        ForeignKey("exercise_names.id"), nullable=False
    )
    exercise_name: Mapped["ExerciseName"] = relationship(back_populates="exercises")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.exercise_name}, weight={self.weight}, reps={self.reps})>"


def ensure_exercise(session: Session, name: str) -> ExerciseName:
    """Get existing ExerciseName object, or create a new one

    return the ExerciseName object"""

    instance = session.query(ExerciseName).filter_by(name=name).first()
    if instance:
        return instance
    instance = ExerciseName(name=name)
    session.add(instance)
    session.commit()  # ensure id is assigned
    return instance
