#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from dataclasses import dataclass, field
from datetime import datetime
import pprint

exercises = ["squat", "bench press", "deadlift"]


class ExerciseNameError(Exception):
    pass


@dataclass
class Exercise:
    name: str
    weight: float
    reps: int


@dataclass
class Workout:
    started: datetime
    exercises: List[Exercise] = field(default_factory=list)


@dataclass
class Logbook:
    workouts: List[Workout] = field(default_factory=list)


if __name__ == "__main__":
    logbook: Logbook = Logbook()
    name: str
    while name := input("exercise name? "):
        workout: Workout
        if name not in exercises + ["quit"]:
            raise ExerciseNameError(name)
        if name == "quit":
            break
        weight: float = float(input("weight? "))
        reps: int = int(input("reps? "))
        exercise: Exercise = Exercise(name, weight, reps)
        workout = Workout(datetime.now())
        workout.exercises.append(exercise)
        logbook.workouts.append(workout)
    pprint.pprint(logbook)
