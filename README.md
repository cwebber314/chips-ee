# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Checkout repo
Get the sources:

  git clone https://github.com/cwebber314/chips-ee
  cd chips-ee

## Setup local machine
Install heroku and gunicorn:

  sudo snap install --classic heroku
  sudo apt-get install gunicorn

Setup python:

  cd ~/path/to/chips-ee
  pip install -r requirements.txt


## Running Heroku Locally

  cd ~/path/to/chips-ee
  heroku local

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku
To publish, push the repo to git.  If heroku is configured properly it works:

  git push origin master

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
