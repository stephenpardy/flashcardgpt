import random
from typing import Any, Optional
from flask import Flask, render_template, request, jsonify, session

from questions import QuestionAnswer, MultipleQuestions, is_correct, format_question
from gpt import ask_ai

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = random.randbytes(8)


def get_accurate_questions(question_bank: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Get questions that have not been flagged for inacurracies."""
    return [q for q in question_bank if "incorrect" not in q["flags"]]


def get_available_questions(question_bank: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Get questions that are available to ask."""
    return [q for q in get_accurate_questions(question_bank) if q["id"] not in session["studied_questions"]]


def get_next_question(question_bank: list[dict[str, Any]]) -> dict[str, Any]:
    """Get a random question which hasn't been asked this session."""
    possible_questions = get_available_questions(question_bank)
    this_question = random.choice(possible_questions)
    return this_question


def done_studying(question_bank: list[dict[str, Any]]) -> bool:
    """We are done studying when all the questions are either marked inaccurate or have been studied."""
    return not bool(get_available_questions(question_bank))


def format_past_questions(question_bank: list[dict[str, Any]]) -> Optional[dict[str, str]]:
    """Make the existing questions into prompts for the future."""
    if not question_bank:
        return None
    
    content = "But avoid repeating the following questions: " + ", ".join(
        f"'{q["question"]}'" for q in question_bank 
    )
    prompt = {"role": "user", "content": content}
    return prompt


def generate_questions(url: str, question_bank: list[dict[str, Any]]) -> list[dict[str, Any]]:
    n_questions = len(question_bank)
    prompt = format_past_questions(question_bank)
    new_questions = ask_ai(url, prompt).model_dump()["questions"]
    print(f"generated {len(new_questions)} questions")
    
    for i, question in enumerate(new_questions):
        question["id"] = i + n_questions
        question["guesses"] = []
        question["evaluations"] = []
        question["flags"] = []

    return new_questions


@app.route("/", methods=["GET", "POST"])
def question():
    correct = None
    if request.method == "POST":
        # Process the submitted data

        match request.form:
            case {"url": url, **remainder}:
                # Handle URL submission
                session["url"] = url
                print("Generating questions")
                # generate the questions
                new_questions = generate_questions(
                    url, session["question_bank"] if "question_bank" in session else []
                )

                session["question_bank"] =  new_questions
                session["studied_questions"] = []
            case {"answer": answer, **remainder}:
                # handle basic answer submission
                question_bank = session["question_bank"]
                if "current_question" in session:
                    correct_answers = session["current_question"]["correct_answers"]
                    correct = is_correct(correct_answers, [answer])
                    for q in question_bank:
                        if q["id"] == session["current_question"]["id"]:
                            q["evaluations"].append(correct)
                            q["guesses"].append(answer)

                    session["question_bank"] = question_bank
                    session["studied_questions"] = session["studied_questions"] + [session["current_question"]["id"]]

            case {"flag": flag_value, **remainder}:
                # handle flagging the question
                question_bank = session["question_bank"]
                if "current_question" in session:
                    for q in question_bank:
                        if q["id"] == session["current_question"]["id"]:
                            q["flags"].append(flag_value)

                    session["question_bank"] = question_bank
            case {"action": "more", **remainder}:
                # handle situations where the user wants to study more
                print("Generating questions")
                # generate more questions
                new_questions = generate_questions(session["url"], session["question_bank"])
                session["question_bank"] =  session["question_bank"] + new_questions
                session["studied_questions"] = []
            case {"action": "again", **remainder}:
                # just clear our study flags and go again
                session["studied_questions"] = []
            case {"action": "new", **remainder}:
                return render_template("url.html")

    if "url" in session and "question_bank" in session:
        if done_studying(session["question_bank"]):

            return render_template(
                "roundup.html",
                question_bank=session["question_bank"],
                study={"url": session["url"]},
            )

        else:
            session["current_question"] = get_next_question(session["question_bank"])
            return render_template(
                "question.html",
                question=format_question(session["current_question"]),
                study={"url": session["url"]},
            )

    return render_template("url.html")


if __name__ == "__main__":
    app.run(debug=True)
