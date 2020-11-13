# Application Name:- HelloWorld
       
## About:-

<b> HelloWorld </b> is a blog web apllication In this Web apllication. The User can read,like and comment on blogs.
 And User can also create Author account. Author can write blogs and also see how many people comment,like their blogs  

I made this web appliaction using Python 3.7.4 + Django and the database is SQLite. 
There is a login and registration functionality included.

# How To Use?
 
## Prerequisites:-
### On Windows:
* $ .\env\Scripts\activate
### Install dependencies:
* $ pip install -r requirements.txt

### make migrations
You can run the application from the command line with manage.py. Go to the root folder of the application.
Run makemigrations:
* $ python manage.py makemigrations
 
### Run migrations:
* $ python manage.py migrate
 
### Run createsuperuser:
* $ python manage.py createsuperuser (name superuser)
* Give Email and password
* Run server on port 8000:
* $ python manage.py runserver 8000 
 Goto browser on localhost port 8000:
   http://localhost:8000
 
 
 
 
 
## Django Admin
It is possible to add additional admin user who can login to the admin site. Run the following command:
* $ python manage.py createsuperuser
Enter your desired email and press enter.
email: admin_email
 
The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.
Password: **********
Password (again): *********
Superuser created successfully.
Go to the web browser and visit http://localhost:8000/admin
 
 
