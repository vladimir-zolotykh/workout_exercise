#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    Mapped,
    mapped_column,
    Session,
)
from datetime import datetime
from typing import List

Base = declarative_base()


class ExerciseName(Base):
    __tablename__ = "exercise_names"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Relationship to Exercise
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="exercise_name")


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    started: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    exercises: Mapped[List["Exercise"]] = relationship(
        back_populates="workout", cascade="all, delete-orphan"
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


if __name__ == "__main__":
    engine = create_engine(
        # "sqlite+pysqlite:///:memory:",
        "sqlite+pysqlite:///workout_model2_db.db",
        echo=True,
        future=True,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        squat = ExerciseName(name="Squat")
        bench = ExerciseName(name="Bench Press")
        session.add_all([squat, bench])
        session.commit()  # NOT NULL constraint failed: exercises.exercise_name_id
        workout1 = Workout(started=datetime.now())
        # without the commit() above `squat.id' is NULL
        new_exercise = Exercise(
            weight=100.0, reps=5, workout=workout1, exercise_name_id=squat.id
        )
        session.add(new_exercise)
        session.add(workout1)
        session.commit()
