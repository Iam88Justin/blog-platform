# Intro
This project is a take-home project from Unified-Sentinel-Data-Networks. This is a blog platform where users can read and write blog posts. The system allow users to register, log in, create, edit, and delete their blog posts with additional features. 
Further details about the project is in Problem.md 

# Dependencies:
- Django 3.0+

# Functionalities
## User Registration and Authentication: 
Implement user registration, login, and logout functionality.

## Blog Post Management:
Allow users to create, edit, and delete their blog posts. Each post have fields for title, content, author, date.

## Comments: 
- Enable users to comment on blog posts

## Run server
Get to ./myproject directory run command: python manage.py runserver

## Authentication links
- http://127.0.0.1:8000/blogs/posts/signup/ to create an account first
- http://127.0.0.1:8000/accounts/login/ to login in to account
- http://127.0.0.1:8000/blogs/posts to go to home list page

## Post links
- http://127.0.0.1:8000/blogs/posts/create/ to create post
- http://127.0.0.1:8000/blogs/<slug:slug>/ to view specific post
- http://127.0.0.1:8000/blogs/posts/<slug:slug>/delete/ to delete specific post
- http://127.0.0.1:8000/blogs/posts/create/ to create post
- http://127.0.0.1:8000/blogs/posts/<slug:slug>/edit/ to edit post

For specific post action, choose html form tab then fill in the information


Comment section is still in work

