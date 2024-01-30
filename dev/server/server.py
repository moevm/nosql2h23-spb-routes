from fastapi import FastAPI
from fastapi import FastAPI, Depends, Request, Response, status, Body
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi_login import *

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

manager = LoginManager(SECRET, token_url='/auth/token', custom_exception=NotAuthenticatedException, use_cookie=True)
# manager.attach_middleware(app)
# manager.


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
    print(access_token, flush=True)
    # return {'access_token': access_token, 'token_type': 'bearer'}
    resp = RedirectResponse(url="/")
    if (isAdmin(user['email'])):
        resp = RedirectResponse(url="/admin")
    

    manager.set_cookie(resp, access_token)
    
    return resp


# @app.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("bearer")
#     resp = RedirectResponse(url="/login")
#     return resp
@app.get("/logout")
async def logout(request: Request, user = Depends(manager)):
    # Also tried following two comment lines
    # response.delete_cookie("access_token", domain="localhost")
    print(request.cookies.get('access-token'), flush=True)
    # response = templates.TemplateResponse("login.html", {"request": request, "title": "Login", "current_user": AnonymousUser()})
    response = RedirectResponse(url="/login", headers={'Authorization': ''})
    # response.set_cookie("")
    response.delete_cookie("access-token", domain="localhost")
    # response.set_cookie(key='access-token', value="", max_age=1)
    
    return response


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
def protected_route(request: Request, user=Depends(manager)):
    print("protected_route", user)
    print(request.headers.get('Authorization'), flush=True)
    return FileResponse(os.path.join(pages_path, "index.html"))


@app.post('/get/current/user')
def protected_route(request: Request, user=Depends(manager)):
    print("protected_route", user)
    print(request.headers.get('Authorization'), flush=True)
    return user

@app.post('/get/dysplayable/points')
def getDysplayablePoints(body = Body()):
    body = json.loads(body)

    print(body, flush=True)
    return json.dumps({"sights" : fake_db.getSightInArea(body)})
    
@app.post('/get/sight/by/id')
def getSightById (body = Body()):
    body = json.loads(body)

    print(body, flush=True)
    # return {'success' : 'ok'} 
    return fake_db.getSightById(body['id'])


@app.post('/create/route')
def createRoute (body = Body()):
    body = json.loads(body)

    print(body, flush=True)
    fake_db.createNewRoute("user", body)
    return {'success' : 'ok'} 
    
@app.post('/get/preferences')
def getPrefereces():
    return fake_db.getPrefereces()

@app.post('/search/sutable/routes')
def searchSutableRoutes (body= Body()):
    body = json.loads(body)

    print(body, flush=True)
    return fake_db.searchSutableRoutes(body)

def isAdmin(email):
    if "Admin" in fake_db.getUserRolesByEmail(email):
        return True
    return False

@app.get('/admin')
def protected_route(request: Request, user=Depends(manager)):
    print("protected_route")
    # roles = fake_db.getUserRolesByEmail(user['email'])
    if (isAdmin(user['email'])):
    # print(request.headers.get('Authorization'), flush=True)
        return FileResponse(os.path.join(pages_path, "admin.html"))
    return RedirectResponse(url="/login")

@app.post('/get/all/routes')
def getAllRoutes(body= Body()):
    body = json.loads(body)

    print(body, flush=True)
    return fake_db.getAllRoutes(body)


app.mount("/", StaticFiles(directory=os.path.abspath(os.path.join( os.path.dirname(__file__), '..', 'client', 'static'))), name="static")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3333)