# Quiz App

This project is a Django-based quiz application. It uses SQLite for the questions database, HTML for the webpages, and Bootstrap 5 for styling.

## Technologies Used

- **Django**: Backend framework
- **SQLite**: Database for storing questions
- **HTML**: Markup language for webpages
- **Bootstrap 5**: CSS framework for styling
- **ApexCharts.js**: 📊 Interactive JavaScript Charts built on SVG 

## Current Functionality

Very basic quiz, with only 10 questions and an end screen which displays score.

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
3. Load your questions, a placeholder question set is provided in the form of ```questions.json```:
    ```python manage.py load_questions
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:8000/`.
2. Start taking quizzes and enjoy!

Optional (but recommended):
1. Create an admin profile with ```python manage.py createsuperuser```
2. From here you can manually add questions through the admin panel

## Contributing

Feel free to fork the repository and submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
