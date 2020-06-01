Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Live Demo
https://fyyur-shruti.herokuapp.com/
### Tech Stack

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

<img width="947" alt="2020-06-02 00_54_37-Mail" src="https://user-images.githubusercontent.com/41858958/83446260-070df580-a46c-11ea-9073-d749020f02ac.png">
<img width="947" alt="2020-06-02 00_55_51-Mail" src="https://user-images.githubusercontent.com/41858958/83446254-04ab9b80-a46c-11ea-8a61-a5912d54256b.png">
<img width="949" alt="2020-06-02 00_56_01-Mail" src="https://user-images.githubusercontent.com/41858958/83446256-06755f00-a46c-11ea-8b4e-8ae714c12caa.png">
<img width="944" alt="2020-06-02 00_56_26-Mail" src="https://user-images.githubusercontent.com/41858958/83446259-070df580-a46c-11ea-831c-a8db17a85dc4.png">

<img width="946" alt="2020-06-02 00_55_06-Mail" src="https://user-images.githubusercontent.com/41858958/83446262-07a68c00-a46c-11ea-900c-91a962b41390.png">
<img width="947" alt="2020-06-02 00_55_29-Mail" src="https://user-images.githubusercontent.com/41858958/83446263-083f2280-a46c-11ea-8bf9-1887bcc8ad3e.png">
