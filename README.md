# content-aggregator
This is a content aggregator that gets different tech contents from different websites plus a blog forum(Made with Python & Django).
Live website: https://coral-app-u3c8u.ondigitalocean.app/



# STEPS

git clone https://github.com/Kingsolomon445/content-aggregator

## **Modify Secret Key so it works**
```
File to modify -> content_aggregator/content_aggregator/settings.py
change SECRET_KEY value into any random secret key or export to env as SECRET_KEY
```

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
python manage.py makemigrations
python manage.py migrate
```


## **Run the Server**
```
python manage.py runserver
```

## **Start Scheduler(Fetch Contents)**
```
python manage.py startjobs
```
Go to localhost:8000



