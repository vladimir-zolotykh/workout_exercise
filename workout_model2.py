#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import (
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    create_engine,
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
        squat = ensure_exercise(session, "squat")
        bench_press = ensure_exercise(session, "bench press")
        deadlift = ensure_exercise(session, "deadlift")
        session.add_all([squat, bench_press, deadlift])
        session.commit()  # NOT NULL constraint failed: exercises.exercise_name_id
        workout1 = Workout(started=datetime.now())
        # without the commit() above `squat.id' is NULL
        new_exercise = Exercise(
            weight=100.0, reps=5, workout=workout1, exercise_name=squat
        )
        session.add(new_exercise)
        session.add(workout1)
        session.commit()
