# Login_API

API feita para o Back-end do sprint 3 da Pós-graducação em Desenvolvimento FullStack - PUC-RJ

Essa API controla todas as ações relacionadas a Login de usuário e sessão.

---
### Instalação

As dependências do programa estão contidas no arquivo requirements.txt e podem ser instaladas com o comando

```
pip install -r requirements.txt
```

---
### Executando o servidor


Para executar a API basta executar:

```
flask run --host 0.0.0.0 --port 5000
```
---
### Acesso no browser

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
## Docker

Construção da imagem Docker:

```
$ docker build -t login-api .
```
Execução do container:

```
$ docker run -p 5000:5000 login-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.

### Acesso
O usuário de teste cadastrado no sistema de login é:

Login: teste@teste.com

Senha: teste 

---
### OBS

Por se tratar de uma API integrada com outros sistemas:

[IntegracaoVenda_FrontEnd](https://github.com/glgaspar/IntegracaoVenda_FrontEnd.git)

[IntegracaoVenda_BackEnd](https://github.com/glgaspar/IntegracaoVenda_BackEnd.git)

[Login_API](https://github.com/glgaspar/Login_API.git)

Recomenda-se manter as portas indicadas. Caso contrário, será necessário adaptar as rotas dos programas nos respectivos arquivos .env.

As rotas estão fixadas usando o endereço interno do docker (host.docker.internal), então para executar os programas sem o uso do docker, será necessário alterar o caminho no arquivo .env.
