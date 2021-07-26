# Dream Journal!
A simple flask app to record your dreams! 


## Install
Make sure you have python downloaded by running `$ python3 --version`.

Clone or download the Repo and navigate into the directory in your terminal
```
$ git clone xxx
$ cd dream-journal
```

Create a virtual env and activate
```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install Flask and confirm the installation was successful
```
$ pip install flask
$ flask --version
```

## Setup
Initialize the database
```
$ python init_db.py
```
Run the app
```
$ flask run
```

You should now be able to navigate to `http://localhost:5000/` in your browser to see the dream journal up and running! 


