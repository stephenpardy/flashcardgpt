import random
from typing import Any
from pydantic import Field, BaseModel


class QuestionAnswer(BaseModel):
    question: str = Field(...)
    answers: list[str] = Field(...)
    correct_answers: list[str] = Field(...)


def format_question(question_dict: dict[str, Any]) -> dict[str, Any]:
    answers = question_dict["answers"]
    return {
        "question": question_dict["question"],
        # get them in a random order
        "answers": random.sample(answers, len(answers)),
    }


def is_correct(correct_answers: list[str], given_answers: list[str]) -> bool:
    return set(given_answers) == set(correct_answers)


class MultipleQuestions(BaseModel):
    questions: list[QuestionAnswer]
