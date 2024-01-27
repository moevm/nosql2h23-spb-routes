from fastapi import FastAPI
from fastapi import FastAPI, Depends, Request, Response, status
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse

SECRET = 'your-secret-key'

app = FastAPI()

from fastapi_login import LoginManager

class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(SECRET, token_url='/auth/token', custom_exception=NotAuthenticatedException)

fake_db = {'drdrew': {'password': '2301'}}

from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 

import os



pages_path = directory=os.path.abspath(os.path.join( os.path.dirname(__file__), '..', 'client', 'pages'))

# index_page_file = open(os.path.join(pages_path, "index.html"), "r")
# index_page = index_page_file.read()

# login_page_file = open(os.path.join(pages_path, "login.html"), "r")
# login_page = login_page_file.read()


# print (login_page)

# @app.get('/')
# def login ():
#     return FileResponse(os.path.join(pages_path, "index.html"))



@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user


from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    print ('email =', email, 'password = ', password)

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
    # return RedirectResponse(url='/', headers={'Authorization': 'Bearer '+ access_token})



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
def protected_route(request: Request, user=Depends(manager)):
    print("protected_route")
    print(request.headers.get('Authorization'), flush=True)
    return FileResponse(os.path.join(pages_path, "index.html"))


app.mount("/", StaticFiles(directory=os.path.abspath(os.path.join( os.path.dirname(__file__), '..', 'client', 'static'))), name="static")


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3333)