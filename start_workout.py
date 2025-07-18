#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from dataclasses import dataclass, field
from datetime import datetime
import pprint

exercises: List[str] = ["squat", "bench press", "deadlift"]


class ExerciseNameError(Exception):
    pass


@dataclass
class Exercise:
    name: str
    weight: float
    reps: int


@dataclass
class Workout:
    name: str
    started: datetime
    exercises: List[Exercise] = field(default_factory=list)


@dataclass
class Logbook:
    workouts: List[Workout] = field(default_factory=list)


def abbreviated_input(prompt: str, choices: List[str] = exercises + ["quit"]) -> str:
    while True:
        user_input = input(f"{prompt} [{', '.join(choices)}] ?")
        matches = [
            choice for choice in choices if choice.lower().startswith(user_input)
        ]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) == 0:
            print("No match found. Try again.")
        else:
            print(f"Ambiguous input. It matches: {', '.join(matches)}. Try again.")


if __name__ == "__main__":
    workout_id: int = 0
    logbook: Logbook = Logbook()
    workout_name: str
    while workout_name := input("workout name? "):
        if workout_name == "quit":
            break
        workout: Workout
        if workout_name == "":
            workout_id += 1
            workout_name = f"workout#{workout_id}"
        workout = Workout(name=workout_name, started=datetime.now())
        exercise_name: str
        while exercise_name := abbreviated_input("exercise name"):
            if exercise_name not in exercises + ["quit"]:
                raise ExerciseNameError(exercise_name)
            if exercise_name == "quit":
                break
            weight: float = float(input("weight? "))
            reps: int = int(input("reps? "))
            exercise: Exercise = Exercise(exercise_name, weight, reps)
            workout.exercises.append(exercise)
        logbook.workouts.append(workout)
    pprint.pprint(logbook)
