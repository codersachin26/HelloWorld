HelloWorld-Blog web app
       
**About**

HelloWorld is a blog web apllication In this Web apllication we have three types of users, the first one is Admin. Admin have all the privileges related to the website and second one is User.  The User can read blogs and like blogs and comments on blogs. The last one is that the Author has more privileges than the User. Author can write blogs and also see how many people comment,like their blogs  
HelloWorld website is user friendly and easy to use. All the important data will be stored in the database and it avoids any miscalculation.
 
It was made using Python 3.7.4 + Django and the database is SQLite. 
There is a login and registration functionality included.
User has his own blog page, where he can add new blog posts if User have Author account. Every authenticated user can comment on posts made by other users. Home page is a paginated list of all posts. Non-authenticated users can see all blog posts, but cannot add new posts or comment.
 
Prerequisites
[Optional] Install virtual environment:
$ python -m virtualenv env
[Optional] Activate virtual environment:
On macOS and Linux:
$ source env/bin/activate
On Windows:
$ .\env\Scripts\activate
Install dependencies:
$ pip install -r requirements.txt
How to run
Default
You can run the application from the command line with manage.py. Go to the root folder of the application.
Run makemigrations:
$ python manage.py makemigrations
 
Run migrations:
$ python manage.py migrate
 
Run createsuperuser:
$ python manage.py createsuperuser (name superuser)
Give Email and password
Run server on port 8000:
$ python manage.py runserver 8000 
 Goto browser on localhost port 8000:
   http://localhost:8000
 
 
 
 
 
Django Admin
It is possible to add additional admin user who can login to the admin site. Run the following command:
$ python manage.py createsuperuser
Enter your desired email and press enter.
email: admin_email
 
The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.
Password: **********
Password (again): *********
Superuser created successfully.
Go to the web browser and visit http://localhost:8000/admin
 
 
