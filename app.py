import sqlite3
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from schemas import *
from flask_cors import CORS
import random

info = Info(title="API de login e controle de sessão", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
login_tag = Tag(name="Login", description="Criação e deleção de tokens de sessão para usuários")
validation_tag = Tag(name="Validação", description="Validação de sessão de usuário")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/login', tags=[login_tag],
            responses={"200": LoginViewSchema, "400": ErrorSchema})
def add_produto(body: LoginSchema):
    """
    Faz login de um usuário

    Retorna dados da sessão iniciada
    """
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    validation = cursor.execute(f"SELECT EMAIL, PASSWORD  FROM  LOGIN WHERE  EMAIL='{body.email}'")
    validation_pass = validation.fetchone()
    
    if validation_pass and validation_pass[1] == body.pssw:
        user_info = cursor.execute(f"SELECT  NAME, EMAIL FROM LOGIN WHERE EMAIL = '{body.email}'").fetchone()
        token = str(abs(hash(str(random.randint(0,9))+user_info[0]+str(random.randint(0,9))+user_info[1]+str(random.randint(0,9)))))
        cursor.execute(f"UPDATE LOGIN SET ACTIVE_TOKEN = '{token}' WHERE EMAIL = '{body.email}'")
        db.commit()
        return {
            "message":"Login successful",
            "user":user_info[0],
            "email":user_info[1],
            "token":token
        },  200
    else:
        print("Password no match")
        return {"message":"Usuário ou senha incorreto"},  400

@app.post('/logout', tags=[login_tag],
            responses={"200": LogoutViewSchema, "404": ErrorSchema})
def logout(body: ValidationSchema):
    """Faz logout de um usuário

    Retorna confirmação do encerramento da sessão e eliminação do token
    """ 
    try:   
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        cursor.execute(f"UPDATE LOGIN SET ACTIVE_TOKEN = '' WHERE  ACTIVE_TOKEN='{body.token}'").fetchone() 
        db.commit()
        return {
            "message":"Logout successful"
        },  200
    except:
        return {"message":"Token no match"},  500
        

@app.post('/validate', tags=[validation_tag],
            responses={"200": ValidationViewSchema, "400": ErrorSchema})
def validate(body: ValidationSchema):
    """Valida existência da sessão de um usuário a partir de um token 

    Retorna confirmação da existência da sessão
    """    
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    query = f"SELECT EMAIL, ACTIVE_TOKEN  FROM  LOGIN WHERE  ACTIVE_TOKEN={body.token}"
    validation = cursor.execute(query).fetchone()
    if validation and validation[1] == body.token:        
        return {
            "message":"Validation successful",
            "user":validation[0]
        },  200
    else:
        return {"message":"Token no match"},  400


@app.get('/permission', tags=[validation_tag],
            responses={"200": PermissionViewSchema, "400": ErrorSchema})
def permission(query: ValidationSchema):
    """Busaca permissões de um usuário a partir de um token 

    Retorna confirmação da existência da sessão
    """
    token = query.dict().get('token')
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    query = f"SELECT EMAIL, VENDEDOR, ACTIVE_TOKEN FROM  LOGIN WHERE  ACTIVE_TOKEN='{token}'"
    validation = cursor.execute(query).fetchone()
    if validation and validation[2] == str(token):        
        return {
            "message":"Validation successful",
            "user":validation[0],
            "vendedor":validation[1]
        },  200
    else:
        return {"message":"Token no match"},  400

