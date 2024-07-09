# Fish Market

a fish selling application built in Python using Django framework that's still under development, be patient for the complete project... :)

## Running the project

Immediately after installing all the dependencies, you can run the project by running the following command:

1. Set up the server with default users and populate utility tables with default data:

    ```bash
    python manage.py makemigrations # create the migrations
    python manage.py migrate # apply the migrations
    python manage.py setup # set up the server with default users and populate utility tables with default data
    ```

2. Run the server:

    ```bash
    python manage.py runserver
    ```
