# Endless Quiz App
Playable version, hosted by Python Anywhere: [Play](https://guillermode20.pythonanywhere.com/)

This project is a Django-based quiz application. It uses SQLite for the questions database, HTML for the webpages, and Bootstrap 5 for styling.

This is a fork of my original project that replaces the local database with fetching trivia questions from the [Open Trivia Database](https://opentdb.com/). 

## Technologies Used

- **Django**: Backend framework
- **SQLite**: Database for storing questions
- **HTML**: Markup language for webpages
- **Bootstrap 5**: CSS framework for styling

## Current Functionality

An Endless Quiz App that provides infinite quiz questions alongside a stats page to keep track of your progress. 

## To-do
- Prevent manually refreshing from changing question
    - could be done by preventing a question from being checked as "completed" only when answered
- Add more questions and integrate the scoring into a separate window/on screen elsewhere
- Beautify UI more (particularly buttons)
- Add unit testing and proper logging
- Add proper comments

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/quiz-app.git
    ```
2. Navigate to the project directory:
    ```bash
    cd quiz-app
    ```
3. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:8000/`.
2. Start taking quizzes and enjoy!

Optional (but recommended):
1. Create an admin profile with ```python manage.py createsuperuser```

## Contributing

Feel free to fork the repository and submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.

Data from this repository is available under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

### Attribution

Data sourced from the [Open Trivia Database](https://opentdb.com/) is licensed under CC BY-SA 4.0. You can find more information at: https://opentdb.com/.

### Modifications

If any modifications were made to the original data, they are described in this repository's documentation or in relevant files.
