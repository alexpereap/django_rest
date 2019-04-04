# Django restful
Thank you for testing this application! :)<br />
The application displays a login form, as the home page with an url to the sign up page.<br />
In the sign up page you can create your user and login from the home page.<br />
Once authenticaded, you will see a dashboard, listing all of the movies and recommended movies.<br />
The dashboard tables for movies and recommended movies are REACT components, that use the API endpoints via AJAX to list and delete them.<br />
The application features a full restful API for handling the movie model (more details below)<br />
The application has a 100% test coverage (more details below)<br />
# Installation using virtualenv:
Install dependencies and run the server: (To run the server we'll use virtualenv over python3)<br />
Make sure you use python3 as the virtualenv python version<br />
```sh
$ cd django_rest
for python3 default machines:
$ virtualenv env && source env/bin/activate && pip install -r requirements.txt
for machines with another version of python as default:
$ virtualenv -p python3 env && source env/bin/activate && pip install -r requirements.txt
$ cd django_rest
$ python manage.py run server
visit http://localhost:8000
```
# Structure:
- Backend: django_rest/omni_bnk contains all of the django application source code, there is a Movie class on the models.py and the views.py contains all of the application logic, including the restful API endpoints.<br />
- Frontend: react_componets/movie/src contains the source code for the REACT component build to list and delete the movies in the application.

# RESTFUL API
- The restful API was built, using the django restframework module: https://www.django-rest-framework.org/<br />
- Its implementation is on the django_rest/omni_bnk/views.py from line 85.<br />
- Supports basic authentication with username and password (Basic base64(username:password) ) and session authentication.<br />
- Supports the common crud verbs (get, post, put, delete) and its fully tested in the django_rest/tests/test_rest_api.py file.<br />
- In the application, the API is used by the REACT component making ajax requests to list the movies and delete them.<br />
## Methods:<br />
GET: /api/movies/ (get all of the movies)<br />
GET: /api/movies?recommended (get only recommended movies)<br />
GET: /api/movies/movie_id (get a specific movie)<br />
POST: /api/movies (stores a movie)<br />
payload:
```json
{
	"movie": {
		"name": "Inception",
		"director": "Christopher Nolan",
		"year": "2010",
		"recommended": true
	}
}
```
PUT: /api/movies/movie_id (updates a movie)<br />
payload:
```json
{
	"movie": {
        "recommended": false,
        ...
	}
}
```
DELETE: /api/movies/move_id (deletes a movie)

# Tests
- Implementation of unit tests using the coverage module, as support tool to fully test the application.<br />
- The test files are under django_rest/omni_bnk/tests folder.<br />
- The test_views.py contains the test for the Movie module and the views<br />
- The test_rest_api.py contains the tests for the restful api<br /><br />
## coverage testing:
```sh
$ cd django_rest
$ coverage run manage.py test omni_bnk -v 2
$ coverage report --include="omni_bnk/*"
$ coverage html --include="omni_bnk/*"
open htmlcov/index.html in the parent folder
```
## django unit testing:
```sh
$ cd django_rest
$ python manage.py test
```
# Comments
The application uses a sqlite3db, that comes by default in this repo with the app migrations done and one user included (alexp)<br />
Do not delete the alexp user! since is the one used by the react component to authenticate against the API!

# Thank you