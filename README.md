[![Build Status](https://travis-ci.org/matthewacha/WeConnect.svg?branch=ft-backend)](https://travis-ci.org/matthewacha/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/matthewacha/WeConnect/badge.svg?branch=ft-backend)](https://coveralls.io/github/matthewacha/WeConnect?branch=ft-backend)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b82ec19d796fcbec0ff2/test_coverage)](https://codeclimate.com/github/matthewacha/WeConnect/test_coverage)

WeConnect

WeConnect provides a platform that brings businesses and individuals 
together. 
This platform creates awareness for businesses and gives the users the ability 
to write reviews about the businesses they have interacted with.

INSTRUCTIONS

1.Pre-requisites
2.Setup and intallations
3.Authors


PRE-REQUISITES

For developers, you need to have installed the following

1. Python 2.7

2. GitSys

3.[Postgresql](https://www.postgresql.org/download/)

Setup and Installation

clone the repo

`$git clone https://github.com/matthewacha/WeConnect.git`

Setup your database, if you do not have postgresql installed please click on the 
link above.

To run the API on local server, navigate to `config.py` , change the user name and password to your username and password 
`postgresql://your_username:your_password@localhost/weconnect` 

Navigate to `__init__.py` in the app folder and set config environment to `config.Development`

For windows, run the 
`setup.bat`

For Linux, cygwin, OS X run 
`setup.sh` 

The above setup file will install and initialise a virtual environment, install dependencies using `pip`
and run the server.

RUNNING TESTS
To run tests input `python manage.py test` in the terminal
To view coverage input `coverage run manage.py test` followed by `coverage report`

VERSIONS
The API runs with two versions, Version 1 and Version 2

Input `http:127.0.0.1:5000/` followed by any of the following endpoints to demo version 1.

|EndPoint|Functionality|
|---------|------------|
|[POST/api/v1/auth/register](http://127.0.0.1:5000/apidocs/#!/User/post_api_v1_auth_register)|Creates a user account|
|[POST/api/v1/auth/login](#)|Logs in a user|
|[POST/api/v1/auth/logout](http://127.0.0.1:5000/apidocs/#!/User/post_api_v1_auth_logout)|Logs out a user|
|[POST/api/v1/auth/reset-password](#)|Password reset|
|[POST/api/v1/businesses](http://127.0.0.1:5000/apidocs/#!/Business/post_api_v1_businesses)|Register a business|
|[PUT/api/v1/businesses/<name>](#)|Updates a business profile|
|[DELETE/api/v1/businesses/<name>](http://127.0.0.1:5000/apidocs/#!/Business/delete_api_v1_businesses_name)|Remove a business|
|[GET/api/v1/businesses](http://127.0.0.1:5000/apidocs/#!/Business/get_api_v1_businesses)|Retrieves all businesses|
|[GET/api/v1/businesses/<name>](#)|Get a business|
|[POST/api/v1/businesses/<name>/reviews](http://127.0.0.1:5000/apidocs/#!/Review/post_api_v1_businesses_name_reviews)|Add a review for a business|
|[GET/api/v1/businesses/<name>/reviews](#)|Get all reviews for a business|

Use the following endpoints to demo version 2

|EndPoint|Functionality|
|---------|------------|
|[POST/api/v2/auth/register](#)|Creates a user account|
|[POST/api/v2/auth/login](#)|Logs in a user|
|[POST/api/v2/auth/logout](#)|Logs out a user|
|[POST/api/v2/auth/reset-password](#)|Password reset|
|[POST/api/v2/businesses](#)|Register a business|
|[PUT/api/v2/businesses/<name>](#)|Updates a business profile|
|[DELETE/api/v2/businesses/<name>](#)|Remove a business|
|[GET/api/v2/businesses](#)|Retrieves all businesses|
|[GET/api/v2/businesses/<name>](#)|Get a business|
|[POST/api/v2/businesses/<name>/reviews](#)|Add a review for a business|
|[GET/api/v2/businesses/<name>/reviews](#)|Get all reviews for a business|

For more about using the API check 127.0.0.1:5000/apidocs

 
Thank you for using WeConnect

