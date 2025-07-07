from flask_openapi3 import OpenAPI, Info, Tag 
from flask import redirect
from flask_cors import CORS

from model import Session, Client

from schemas import *

from logger import logger

######################
#openapi 

info = Info(title="Sprint 1 API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# handle openapi cors 
CORS(app)

# documentation tags definition
openapi_documentation_tag = Tag(name="Documentation", description="Documentação da API do projeto Sprint 1")
openapi_client_tag = Tag(name="Client", description="Crud de Clientes")

#######################
# routes

# documentation route redirect to OpenAPI UI
@app.get('/', tags=[openapi_documentation_tag])
def home():
    return redirect('/openapi')

# client routes
@app.post('/clients', tags=[openapi_client_tag], responses={"201": ClientSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_client(form: ClientSchema):
    """Adiciona um cliente à base de dados

    """
    client = Client(
        name=form.name,
        email=form.email,
        phone=form.phone,
        document=form.document)
    
    try:
        session = Session()
        session.add(client)
        session.commit()

        logger.debug(f"Adicionado cliente: '{client.name}'")
        
        
        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "document": client.document,
        }, 201

    except Exception as e:
        logger.warning(f"Tracing  {e}")
        error_msg = "Error ao adicionar cliente"
        logger.warning(f"Erro ao adicionar cliente '{client.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/clients/<int:client_id>', tags=[openapi_client_tag], responses={"200": GetClientSchema ,"404": None , "400": ErrorSchema})
def get_client(path: ClientParamsSchema):
    """Pega os clientes da base de dados

    """
    try:
        session = Session()

        client = session.query(Client).filter(Client.id == path.client_id).first()
        
        if not client:
            error_msg = f"Cliente com ID {path.client_id} não encontrado"
            logger.warning(error_msg)
            return '', 404
        
        return show_client(client), 200

    except Exception as e:
        logger.warning(f"Tracing  {e}")
        error_msg = "Error ao buscar os clientes do banco"
        logger.warning(f"Erro ao pegar clientes, {error_msg}")
        return {"message": error_msg}, 500


@app.get('/clients', tags=[openapi_client_tag], responses={"200": GetAllClientsSchema , "400": ErrorSchema})
def get_clients():
    """Pega os clientes da base de dados

    """
    try:
        session = Session()

        clients = session.query(Client).all()
        
        return show_clients(clients), 200

    except Exception as e:
        logger.warning(f"Tracing  {e}")
        error_msg = "Error ao buscar os clientes do banco"
        logger.warning(f"Erro ao pegar clientes, {error_msg}")
        return {"message": error_msg}, 500

@app.get('/clients/quantity', tags=[openapi_client_tag], responses={"200": GetClientsQuantitySchema , "400": ErrorSchema})
def get_clients_quantity():
    """Pega a quantidade de clientes da base de dados
    """
    try:
        session = Session()

        clients_count =  session.query(Client).count()
        
        return {"count": clients_count}, 200

    except Exception as e:
        logger.warning(f"Tracing  {e}")
        error_msg = "Error ao buscar a quantidade de clientes do banco"
        logger.warning(f"Erro ao pegar clientes, {error_msg}")
        return {"message": error_msg}, 500


@app.delete('/clients/<int:client_id>', tags=[openapi_client_tag], responses={"204": None,"404": ErrorSchema,"500": ErrorSchema}
)
def delete_client(path: ClientParamsSchema):
    """Remove um cliente da base de dados"""
    try:
        print(path)
        session = Session()
        client = session.query(Client).filter(Client.id == path.client_id).first()

        if not client:
            error_msg = f"Cliente com ID {path.client_id} não encontrado"
            logger.warning(error_msg)
            return {"message": error_msg}, 404

        session.delete(client)
        session.commit()

        logger.debug(f"Deletado cliente: '{client.name}'")

        return '', 204

    except Exception as e:
        logger.warning(f"Tracing {e}")
        error_msg = "Erro ao remover cliente do banco"
        logger.warning(f"{error_msg}: {e}")
        return {"message": error_msg}, 500
