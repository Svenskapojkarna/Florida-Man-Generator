# PWP SPRING 2020
# Florida Man Generator
# Group information
* Student 1. Aleksi Hytönen, hytonenaleksi@gmail.com
* Student 2. Markus Oja, markus.oja@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

# Overview of the API
## Structure
### (root)

LICENSE = License of the project<br>
README.md. = THIS readmefile.<br>
api_test.py = Test file for api-method testing.<br>
apiary.apib. = Blueprint from Apiary<br>
app.py =  Main function(?).<br>
db_test.py = Test file for database testing.<br>
meetings.md = File containing meeting notes.<br>
requirements.txt = Requirements file for installation.<br>

### db <Database>

db_test.py = Unit tests for the database.<br>
db.py = Database models.<br>
populate.py = Populate the database with initial values.<br>
README.md = Instructions on how to use the database.<br>
test.db = Populated database with initial values.

### src <Source Code>
#### builders <Builders for all resources>

addedarticlebuilder.py = Builder for added article resource.<br>
articlebuilder.py = Builder for article resource.<br>
masonbuilder.py = Builder to create resources. Used in other builders as dependency.<br>
userbuilder.py = Builder for user resource.

#### Resources <The actual resources of the API>

addedarticleresource.py = Resource for added article collection and item.<br>
articleresource.py = Resource for article collection and item.<br>
entrypoint.py = Application entrypoint.<br>
userresource.py = Resource for user collection and item.

### Client/src <Source code for API client>
#### components

AddedArticle.jsx = One added article component.<br>
api.js = Global configuration of API<br>
Article.jsx = One initial article component<br>
serviceWorker.js = Needed for React application

#### pages

App.jsx = Landing page.<br>
CheckInitialMemes.jsx = Page to search for the initial memes.<br>
CheckUserMemes.jsx = Page to search, edit and delete user created articles. User can also create a new article for himself.<br>
CreateNewArticle.jsx = Page to create a new user and a new article.

## Usage
### Installing dependencies
0. (Install virtualenv)
(virtualenv is not in requirements)
(in case with problems on Windows, try first installing with)
```shell
python -m pip install virtualenv --user
```

1. Activate python virtual environment in command line
```shell
virtualenv pwp
```

2. Activate virtual environment
```shell
pwp\Scripts\activate.bat
```
3. install dependencies
```shell
pip install -r requirements.txt
```
4. start the API
```shell
flask run
```
## Test the API
Run apitest and db_test with pytest in the root folder.
Configure it to check both app.py and src folder.
To do this:
```shell
pytest --cov=app --cov=src
```
## Tests
### db_test
```shell
pytest db_test.py
```
This command will test CRUD operations in each model.
In addition, uniqueness of the date will be tested.
The tests will also check that the headline and the modification date are not null.
### api_test
```shell
pytest api_test.py
```
This command will test the API methods for each resource.
(At the moment it tests only user)