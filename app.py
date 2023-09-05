import sqlite3
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from schemas import *
from flask_cors import CORS
import random

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
login_tag = Tag(name="Login", description="Adição, visualização e remoção de produtos à base")
validation_tag = Tag(name="Validação", description="Adição de um comentário à um produtos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/login', tags=[login_tag],
            responses={"200": LoginViewSchema, "400": ErrorSchema})
def add_produto(form: LoginSchema):
    """
    Logs in user

    Returns message with login confirmation or rejection and user data
    """
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    validation = cursor.execute(f"SELECT EMAIL, PASSWORD  FROM  LOGIN WHERE  EMAIL='{form.email}'")
    validation_pass = validation.fetchone()
    
    if validation_pass and validation_pass[1] == form.pssw:
        user_info = cursor.execute(f"SELECT  NAME, EMAIL, TEL, ADDRESS FROM USERS WHERE EMAIL = '{form.email}'").fetchone()
        token = str(abs(hash(str(random.randint(0,9))+user_info[0]+str(random.randint(0,9))+user_info[1]+str(random.randint(0,9)))))
        cursor.execute(f"UPDATE LOGIN SET ACTIVE_TOKEN = '{token}' WHERE EMAIL = '{form.email}'")
        db.commit()
        return {
            "message":"Login successful",
            "user":user_info[0],
            "email":user_info[1],
            "token":token
        },  200
    else:
        return {"message":"Password no match"},  400


@app.post('/validate', tags=[validation_tag],
            responses={"200": ValidationViewSchema, "400": ErrorSchema})
def validate(form: ValidationSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """    
    print(form)
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    validation = cursor.execute(f"SELECT EMAIL, ACTIVE_TOKEN  FROM  LOGIN WHERE  ACTIVE_TOKEN='{form.token}'").fetchone()
    if validation and validation[1] == form.token:        
        return {
            "message":"Validation successful"
        },  200
    else:
        return {"message":"Token no match"},  400


# @app.post('/logout', tags=[validation_tag],
#             responses={"200": ValidationViewSchema})#, "404": ErrorSchema})
# def logout(form: ValidationSchema):
#     """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

#     Retorna uma representação dos produtos e comentários associados.
#     """    
#     db = sqlite3.connect('db.db')
#     cursor = db.cursor()
#     validation = cursor.execute(f"SELECT EMAIL, ACTIVE_TOKEN  FROM  LOGIN WHERE  ACTIVE_TOKEN='{form.token}'").fetchone()
#     if validation and validation[1] == form.token:        
#         return {
#             "message":"Validation successful"
#         },  200
#     else:
#         return {"message":"Token no match"},  400
        
