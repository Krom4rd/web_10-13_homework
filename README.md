# Homework 13 Django 
# Email varification, reset password, securety

**Installation and launch**

- [ ] **_Activate the virtual environment_**

    python -m venv (venv_name)

    venv\Scripts\activate.bat

- [ ] **_Install dependencies_**
 
    pip install -r requirements.txt

- [ ] **_Create .env file and fill it_**

    example in env_example

- [ ] **_Create and run Docker postgresql container_**

    docker-compose up
    
- [ ] **_Go to the application folder_**

    cd homework_10

- [ ] **_Perform migrations for postgresql_**

    manage.py migrate
    
- [ ] **_Run server_**

    manage.py runserver

## Additional information

**If you want to create an admin user for the application.**
- [ ] **_Stop the server_**

    In the terminal press ctrl+c
    
- [ ] **_manage.py createsuperuser_**

- [ ] **_Run server_**

    manage.py runserver
    
    **Or create through the database**
    
### For the site administrator, the function of filling the application from the mongo database is available.

- [ ] Find a file by path
    homework_10\quotes\connect_mongo.py
- [ ] client = MongoClient(Your mongo client)
- [ ] db = (Name of your db in mongo)

**_Will only work with models created in mongo for homework 9_**
