# Django Google Login
A simple google login in which the oauth is used also integrated user register using django-allauth

## Installation
0. In order for the app to work access the google api keys and secret through link below and change it in the settings.py  <br>
[Get the client_id and secret here](https://docs.google.com/document/d/1XSqki1WFGAtaZ2xlj9rUcTjeOYjuQVKwKkG6EwGUKoI/edit?usp=sharing) <br>
SOCIALACCOUNT_PROVIDERS = {<br>
"google": {<br>
        "APP": {<br>
            <mark>"client_id": "",</mark><br>
            <mark>"secret": "",</mark><br>
        },<br>
        "SCOPE": [<br>
            "profile",<br>
            "email",<br>
        ],
        "AUTH_PARAMS": {"access_type": "online"},
        "METHOD": "oauth2",
        "VERIFIED_EMAIL": True,  # Enable PKCE (Proof Key for Code Exchange)
    }
}



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
