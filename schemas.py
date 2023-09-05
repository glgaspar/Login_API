from pydantic import BaseModel


class LoginSchema(BaseModel):
    """ Define como um usuário deve ser enviado para realizar o login.
    """
    email:  str = "exemplo@exemplo.com"
    pssw:   str = "1234!@#$"

class LoginViewSchema(BaseModel):
    """ Define como um login será retornado.
    """
    user:   str = "Nome Sobrenome"
    email:  str = "exemplo@exemplo.com"
    token:  str = "XXXXX"
    message: str

class ValidationSchema(BaseModel):
    """Define como é o objeto para validação de um usuário.
    """
    token:  str = "XXXXX"

class ValidationViewSchema(BaseModel):
    email:  str = "exemplo@exemplo.com"
    token:  str = "XXXXX"
    message: str

class ErrorSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    message: str
