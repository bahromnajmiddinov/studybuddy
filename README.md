# StudyBuddy - A Collaborative Learning Platform (Django)

 ## Installation

1. **Create a virtual environment:**

   - Choose a virtual environment tool (e.g., `venv`, `virtualenv`, `pipenv`). Refer to their documentation for specific commands. Here's an example using `venv`:

     ```bash
     python -m venv venv
     source venv/bin/activate  # Linux/macOS
     venv\Scripts\activate.bat  # Windows
     ```

2. **Install dependencies:**

   - Activate the virtual environment.
   - Install the required packages from `requirements.txt`:

     ```bash
     pip install -r requirements.txt
     ```
     
## Usage

1. **Migrate database (if applicable):**

   ```bash
   python manage.py migrate
2. **Start the development server:**
   ```bash
   python manage.py runserver
