from fastapi import FastAPI
from fastapi import FastAPI, Depends, Request, Response, status, Body
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi_login import LoginManager

from pydantic import BaseModel

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 

import os

import json





from logic import ServerLogic

SECRET = 'your-secret-key'

app = FastAPI()



class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(SECRET, token_url='/auth/token', custom_exception=NotAuthenticatedException)

fake_db = ServerLogic()# {'drdrew': {'password': '2301'}}




pages_path = directory=os.path.abspath(os.path.join( os.path.dirname(__file__), '..', 'client', 'pages'))




@manager.user_loader()
def load_user(email: str):
    user = fake_db.getUserByEmail(email)
    return user


@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    print ('email =', email, 'password = ', password)

    user = fake_db.getUserByEmail(email)
    print("user = ", user)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}



@app.post('/auth/create/user')
def createUser(body =  Body()):

    body = json.loads(body)

    email = body["email"]
    password = body["password"]
    firstName = body["firstName"]
    lastName = body["lastName"]
    phone = body["phone"]
    address = body["address"]

    print ('email =', email,\
            'password = ', password, \
            'firstName = ', firstName, \
            'lastName = ', lastName,\
            'phone = ', phone,\
            'address = ', address,\
                          sep='\n', flush=True)

    fake_db.createUser(body)

    return {"isUserCreated":True}



@app.get('/login', response_class=HTMLResponse)
def login():
    print("login")

    return FileResponse(os.path.join(pages_path, "login.html"))



@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    print("auth_exception_handler")
    return RedirectResponse(url='/login')


@app.get('/redirect_to_main_page')
def redirect_to_main_page(request: Request, user=Depends(manager)):
    Authorization = request.headers.get('Authorization')
    return RedirectResponse(url='/', headers={'Authorization': 'Bearer '+ Authorization})


@app.get('/')
def protected_route():#request: Request, user=Depends(manager)):
    print("protected_route")
    # print(request.headers.get('Authorization'), flush=True)
    return FileResponse(os.path.join(pages_path, "index.html"))


app.mount("/", StaticFiles(directory=os.path.abspath(os.path.join( os.path.dirname(__file__), '..', 'client', 'static'))), name="static")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3333)