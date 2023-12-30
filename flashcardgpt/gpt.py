from typing import Optional
from openai import OpenAI
import instructor

from questions import MultipleQuestions

# Apply the patch to the OpenAI client
# enables response_model, validation_context keyword
client = instructor.patch(OpenAI())

system_prompt = """
You are an expert system who helps users study for exams.
You will produce multiple choice questions from content.
The questions must ask about important topics of the webpage given.
Each question must be specific to one particular topic and the answers should all be related.
For instance if there is an important date you can ask when an event happened and give a correct date and incorrect dates.
You will work hard to make sure the correct answers are factual and based on the information on the article.
For the incorrect answers you should make up facts that  are similar to the correct answers.

There will be four answers to each question with one correct answers.

Produce four different questions, each testing a different topic.

Output the questions in json format with each question and fields for each of the answers,
and for the list of correct answers.

Do not output any other text outside the json output
"""


def ask_ai(
    url: str, past_question_prompt: Optional[dict[str, str]]
) -> MultipleQuestions:
    if past_question_prompt is None:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"The website to make questions from is {url}"},
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"The website to make questions from is {url}"},
            past_question_prompt,
        ]

    return client.chat.completions.create(
        model="gpt-4",
        # model="gpt-3.5-turbo-0613",
        temperature=0.1,
        response_model=MultipleQuestions,
        messages=messages,
    )
