from ..utils.data_handler import DataHandler
from datetime import datetime as dt
from typing import List, Dict, Any

class Pets:
    def __init__(self):
        self.handler = DataHandler("pets")
        # IMPORTANTE: Instanciamos um handler de clientes diretamente aqui
        # para buscar o dono sem chamar o serviço 'Clients' (evita Loop Infinito)
        self.client_handler = DataHandler("clients")

    def list(self):
        """Lista todos os pets e popula os dados do dono."""
        data = self.handler.list_all()
        return self.get_relationship(data)

    def create(self, data: dict):
        self.handler.create({**data, "created_at": dt.now()})

    def delete(self, id):
        self.handler.delete(id)

    def update(self, id, data: dict):
        self.handler.update({**data, "id": id})

    def get_by_id(self, id):
        """Busca pet pelo ID e popula os dados do dono."""
        pet = self.handler.get_by_id(id)
        if pet:
            # Envelopa em lista para usar a função get_relationship e retorna o item único
            return self.get_relationship([pet])[0]
        return None

    def search(self, filters: dict):
        """Busca com filtros e popula os dados do dono."""
        filters_to_remove = ["logic", "operator"]
        
        data = self.handler.search({
            "logic": filters.get("logic", "AND"),
            "criteria": [
                {
                    "key": key, 
                    "value": value, 
                    "operator": filters.get("operator", "CONTAINS")
                }
                for key, value in filters.items() 
                if key not in filters_to_remove
            ]
        })
        return self.get_relationship(data)

    def get_relationship(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Substitui o ID do dono (owner_id) pelo objeto completo do Cliente.
        """
        for pet in data:
            owner_id = pet.get("owner_id")
            
            if owner_id:
                # Busca o cliente cru (raw) diretamente do banco
                owner = self.client_handler.get_by_id(owner_id)
                
                # Substitui o valor do campo 'owner_id' pelo objeto do cliente
                # Exemplo: "owner_id": 1  --->  "owner_id": { "id": 1, "name": "Fulano"... }
                pet["owner_id"] = owner
        
        return data