from pydantic import BaseModel , Field
from typing import Optional, List
from model.client import Client


class ClientSchema(BaseModel):
    """ Schema criação de um cliente
    """
    name: str = "Cliente teste"
    email: str = "teste@gmail.com"
    phone: str = "1234567890"
    document: Optional[str] = None

    
    
class GetAllClientsSchema(BaseModel):
    """ Schema para pegar todos os clientes
    """
    clients: List[ClientSchema]
    
class GetClientSchema(BaseModel):
    """ Schema para pegar todos os clientes
    """
    client: ClientSchema

class GetClientsQuantitySchema(BaseModel):
    """ Schema para pegar a quantidade de clientes
    """
    count: int

class ClientParamsSchema(BaseModel):
    """ Schema para os parâmetros de exclusão de cliente
    """
    client_id: int = Field(..., description='client id')

def show_clients(clients: List[Client]) -> dict:
    """ Retorna um objeto contendo os clientes.
    """
    clients_list = []
    for client in clients:
        clients_list.append({
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "document": client.document,
            "phone": client.phone,
        })

    return {"clients": clients_list}


def show_client(client: Client) -> dict:
    """ Retorna um objeto contendo os clientes.
    """

    client_dict= {
        "name": client.name,
        "email": client.email,
        "document": client.document,
        "phone": client.phone,
    }

    return {"client": client_dict}
