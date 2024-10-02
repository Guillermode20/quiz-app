# Quiz App

This project is a Django-based quiz application. It uses SQLite for the questions database, HTML for the webpages, and Bootstrap 5 for styling.

## Technologies Used

- **Django**: Backend framework
- **SQLite**: Database for storing questions
- **HTML**: Markup language for webpages
- **Bootstrap 5**: CSS framework for styling

## Current Functionality

The current functionality is very limited as the core features are still under development.

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

Optional:
1. Create an admin profile with python manage.py createsuperuser
2. From here you can manually add questions through the admin panel

## Contributing

Feel free to fork the repository and submit pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
