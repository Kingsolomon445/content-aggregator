# content-aggregator
This is a content aggregator that gets different tech contents from different websites plus a blog forum(Made with Python & Django).
Feel free to change the codes, add more functionalities , change design , whatever you wish.

Note: *I have an already running website for content aggregator so it is crucial to change design and maybe some functionalities and securities to your taste.*



# STEPS

git clone https://github.com/Kingsolomon445/content-aggregator

## From the project root directory

## **start a virtual environment and activate it**
```
python -m virtualenv venv
source venv/bin/activate
```

## **Install the required dependencies**
```
pip install -r requirements.txt
```

## **Create database tables**
```
python3 manage.py makemigrations
python3 manage.py migrate
```


## **Run the Server**
```
python3 manage.py runserver
```
Go to localhost:8000



