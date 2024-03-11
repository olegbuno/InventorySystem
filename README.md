# Cyberpunk Inventory Management System

A simple inventory management system for a cyberpunk-themed game
using FastAPI, SQLAlchemy, and PostgreSQL. The system will manage items that players can
acquire in the game. These items could range from cybernetic enhancements to weapons and
gadgets. The API will provide basic CRUD (Create, Read, Update, Delete) functionality for these
items.

## Usage

```python
docker-compose up --build
```
Go to http://127.0.0.1:8000/ or http://localhost:8000/ to see main page:
```{"message":"Welcome to the Cyberpunk Inventory Management System"}```

With http://127.0.0.1:8000/docs you can see and test all the endpoints. Keep in mind that only 
authorized users can make all CRUD methods to the item's endpoints.
- So, firstly you need to register a user using the POST method to ```/register/``` endpoint
- After you can authorize providing only username and password credentials on http://127.0.0.1:8000/docs
by clicking the 'Authorize' button top right
- Now you have access to make all the CRUD operations since with items endpoints

## Testing
- To run pytests you have to create a database 'inventory' and provide proper credentials in the 
'.env.testing' file for:
```SQLALCHEMY_DATABASE_URL=postgresql://postgres:admin@localhost/inventory```
- After go to the 'tests' folder and run ```pytest``` in your terminal
