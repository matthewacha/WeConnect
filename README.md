[![Build Status](https://travis-ci.org/matthewacha/WeConnect.svg?branch=ft-backend)](https://travis-ci.org/matthewacha/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/matthewacha/WeConnect/badge.svg?branch=ft-backend)](https://coveralls.io/github/matthewacha/WeConnect?branch=ft-backend)

# WeConnect
WeConnect provides a platform that brings businesses and individuals 
together. 
This platform creates awareness for businesses and gives the users the ability 
to write reviews about the businesses they have interacted with.


##############
#INSTRUCTIONS#
##############
1.Pre-requisites
2.Setup and intallations
3.Authors


PRE-REQUISITES

For developers, you need to have installed the following

1. Python 2.7

2. GitSys

Setup and Installation

clone the repo

`$git clone https://github.com/matthewacha/WeConnect.git`

For windows, run the 
`setup.bat`

For Linux, cygwin, OS X run 
`setup.sh` 

Use the following endpoints to demo

|EndPoint|Functionality|
|---------|------------|
|[POST/api/auth/register](#)|Creates a user account|
|[POST/api/auth/login](#)|Logs in a user|
|[POST/api/auth/logout](#)|Logs out a user|
|[POST/api/auth/reset-password](#)|Password reset|
|[POST/api/businesses](#)|Register a business|
|[PUT/api/businesses/<name>](#)|Updates a business profile|
|[DELETE/api/businesses/<name>](#)|Remove a business|
|[GET/api/businesses](#)|Retrieves all businesses|
|[GET/api/businesses/<name>](#)|Get a business|
|[POST/api/businesses/<name>/reviews](#)|Add a review for a business|
|[GET/api/businesses/<name>/reviews](#)|Get all reviews for a business|


Thank you for using WeConnect

