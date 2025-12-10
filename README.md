# Simple Blog REST API — Flask

This project is a RESTful Blog API built using Flask, SQLAlchemy, and JWT Authentication.
It includes user authentication, CRUD operations for blog posts, and pagination.

### Features

* User Registration, Login, Logout (JWT-based)
* Create, Read, Update, Delete blog posts
* View all posts with pagination
* View a single post by ID
* SQLite as the database
* Clean modular folder structure

### Setup Instructions
1. Clone Repository
``` bash
git clone <your-repo-link>
cd <project-folder>
```

2. Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # forLinux/Mac
venv\Scripts\activate       # for Windows
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the Application
```bash
python app.py
```

The server will start at:

http://127.0.0.1:5000

# API Endpoints

## Auth
Method	Endpoint	    Description
POST	/auth/register	Register a new user
POST	/auth/login	    Login user (JWT)
POST	/auth/logout	Logout user

## Posts
Method	Endpoint	    Description
POST    /posts	        Create a new post (JWT)
GET	    /posts	        List all posts (paginated)
GET	    /posts/<id>	    Get a single post
PUT	    /posts/<id>	    Update a post (JWT)
DELETE	/posts/<id>	    Delete a post (JWT) 

Testing with cURL
1. Register
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"secret"}'
```
2. Login

Generate a JWT token for an existing user.
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"secret"}'
```

Copy the access_token and use it in the next requests.

3. Create a Post
```bash
curl -X POST http://127.0.0.1:5000/posts \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-H "Content-Type: application/json" \
-d '{"title":"Test","content":"Content"}'
```

3. Update a Post
```bash
curl -X PUT http://127.0.0.1:5000/posts/1 \
-H "Authorization: Bearer YOUR_TOKEN_HERE" \
-H "Content-Type: application/json" \
-d '{"title":"Updated Title","content":"Updated Content"}'
```
4. Delete a Post
```bash
curl -X DELETE http://127.0.0.1:5000/posts/1 \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

5. Get All Posts (with Pagination)
```bash
curl "http://127.0.0.1:5000/posts?page=1&per_page=10"
```

6. Get a Single Post
```bash
curl http://127.0.0.1:5000/posts/1
```