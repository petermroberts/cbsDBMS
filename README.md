# cbsDBMS


## Running backend
- Change the database connection info in cbs-api/settings.py if necessary
- Delete all files except for __init__ from the migrations folder for each application
- Switch to the pipenv shell; “pipenv shell” in terminal
- In terminal run “python manage.py makemigrations”; “python manage.py migrate”; These commands prompt Django to create all the necessary tables in the database
- Run “python manage.py runserver”; this will run the backend on port 8000 by default
- Go to localhost:{port}/graphql/ to use the backend
