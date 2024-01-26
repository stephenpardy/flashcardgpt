# FlashcardGPT

AI-powered multiple choice question app.
A simple project to learn more about using LLMs in an app.

Uses OpenAI's API to create multiple choice questions based on the web url given
Randomizes the order of the answers to help avoid memorizing the questions.

Running:

1. Clone the repo locally
2. Install the package locally `pip install -e .`
3. Make sure you have an OpenAI api key added to your local environment variable `OPENAI_API_KEY`
4. cd into the `flashcardgpt` subfolder
5. Run with flask: `python app.py`
