# Django Google Login

A simple google login in which the oauth is used also integrated user register using django-allauth

## Installation

> [!IMPORTANT]  
>0. In order for the app to work rename the .envsample file to .env in the djangoLogin folder and paste the client id and secret in the .env<br>
>   [Get the client_id and secret here](https://docs.google.com/document/d/1XSqki1WFGAtaZ2xlj9rUcTjeOYjuQVKwKkG6EwGUKoI/edit?usp=sharing) <br>

1. Clone the repository:
   ```bash
   git clone https://github.com/Rapphie/simple-login-django.git [YourDirectoryName]
   ```
2. Navigate to your project directory:
   ```bash
   cd your-project-directory
   ```
3. Create virtual environment:
   ```bash
   python -m venv .venv
   ```
   Run this in terminal if successful (.venv) will be displayed
   ```bash
   .\.venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   python manage.py runserver
   ```
