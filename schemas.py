from pydantic import BaseModel


class LoginSchema(BaseModel):
    """ Define como um usuário deve ser enviado para realizar o login.
    """
    email:  str
    pssw:   str

class LoginViewSchema(BaseModel):
    """ Define como um login será retornado.
    """
    user:   str = "Nome Sobrenome"
    email:  str = "exemplo@exemplo.com"
    token:  str = "XXXXX"
    message: str

class ValidationSchema(BaseModel):
    """Define como é o objeto enviado para validação de um usuário.
    """
    token:  str = "XXXXX"

class PermissionViewSchema(BaseModel):
    """Define como é o objeto retornado com as permissões de um usuário.
    """
    user:  str = "exemplo@exemplo.com"
    vendedor: int

class ValidationViewSchema(BaseModel):
    """Define como é o objeto retornado para validação de um usuário.
    """
    user:  str = "exemplo@exemplo.com"
    token:  str = "XXXXX"
    message: str

class ErrorSchema(BaseModel):
    """ Define como uma mensagem de erro será retornada
    """
    message: str
