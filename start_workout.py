#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from dataclasses import dataclass, field
from datetime import datetime

exercises = ["squat", "bench press", "deadlift"]


@dataclass
class Exercise:
    name: str
    weight: float
    reps: int


@dataclass
class Workout:
    started: datetime
    exercises: List[Exercise] = field(default_factory=list)


if __name__ == "__main__":
    workout: Workout = Workout(datetime.now())
    name: str
    while name := input("exercise name? "):
        if name == "quit":
            break
        weight: float = float(input("weight? "))
        reps: int = int(input("reps? "))
        exercise: Exercise = Exercise(name, weight, reps)
        workout.exercises.append(exercise)
    print(workout)
