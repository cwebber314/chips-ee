# Python and Heroku App 

This is a little bit more than a Hello World example using Django and Heroku.  The site contains some simple math and other utilities related to PSSE. 

It's published [here] (https://chips-ee.herokuapp.com/)

## Checkout repo
Get the sources:
```
  git clone https://github.com/cwebber314/chips-ee
  cd chips-ee
```

## Setup local machine
Install heroku and gunicorn:
```
  sudo snap install --classic heroku
  sudo apt-get install gunicorn
```

Setup python:
```
  cd ~/path/to/chips-ee
  pip install -r requirements.txt
```

## Running Heroku Locally
To run with the heroku environment:
```
  cd ~/path/to/chips-ee
  heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

You can also run outside of the heroku environment.  Make sure your local Python
environment is setup:
```
    pip install -r requirements.txt
```

The start the django server:
```
    python manage.py runserver 0.0.0.0:5000
```

## Deploying to Heroku
To publish, push the repo to git.  If heroku is configured properly it works:

  git push origin master

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
