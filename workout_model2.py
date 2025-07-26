#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
import pprint
from sqlalchemy import (
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Engine,
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
        # return f"<Workout(id={self.id}, started={self.started}, exercises={len(self.exercises)} items)>"
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


parser = argparse.ArgumentParser(
    description="Do [some actions] on workout_model",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "--permanent-db", default="workout_model2_db.db", help="what db file to use"
)
parser.add_argument("--memory-db", help="use memory db")
parser.add_argument(
    "--echo", help="Show db commands", action="store_true", default=False
)
ALL_COMMANDS: list[str] = [
    "init",
    "add-squat-workout",
    "show-exercise-names",
    "show-workouts",
    "add-squat-workout",
    "remove-workout-id",
]

parser.add_argument(
    "command",
    nargs="+",
    choices=ALL_COMMANDS,
)


if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    engine: Engine
    if args.memory_db:
        engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            echo=args.echo,
            future=True,
        )
    elif args.permanent_db:
        engine = create_engine(
            f"sqlite+pysqlite:///{args.permanent_db}",
            echo=args.echo,
            future=True,
        )
    else:
        raise RuntimeError("--permanent-db or --memory-db expected")

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for cmd in args.command:

            def do_init():
                {
                    name: ensure_exercise(session, name)
                    for name in (
                        "front_squat",
                        "squat",
                        "bench_press",
                        "deadlift",
                        "pullup",
                        "overhead_press",
                        "biceps_curl",
                    )
                }
                session.commit()

            def show_exercise_names():
                for ex_name in session.query(ExerciseName).all():
                    print(ex_name)

            def show_workouts():
                for w in session.query(Workout).all():
                    print(w)

            def add_squat_workout():
                workout = Workout(started=datetime.now())
                new_exercise = Exercise(
                    weight=100.0,
                    reps=5,
                    workout=workout,
                    exercise_name=ensure_exercise(session, "squat"),
                )
                session.add(new_exercise)
                session.commit()

            def remove_workout_id():
                workout = session.query(Workout).get(10)
                session.delete(workout)
                session.commit()

            all_functions = [
                do_init,
                add_squat_workout,
                show_exercise_names,
                show_workouts,
                add_squat_workout,
                remove_workout_id,
            ]
            {cmd: func for cmd, func in zip(ALL_COMMANDS, all_functions)}[cmd]()
