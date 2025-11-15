import csv
from flask import current_app
import os
from typing import List, Dict, Any

class DataHandler:
    def __init__(self, csv_filename: str):
        self.filename = os.path.join(current_app.instance_path, f"{csv_filename}.csv")
    
    def list_all(self):
        with open(self.filename, "r", newline="") as f:
            data = list(csv.reader(f))

            ## nova lista que vai receber os dicionários
            new_list = []

            ## percorre as linhas do csv
            for index, line in enumerate(data):
                ## se a linha não for a primeira que apenas contém as colunas do csv
                if index != 0:
                    ## cria um dicionário base que vai receber os valores da linha em chave:valor
                    new_dict = dict()
                    ## para cada elemento da linha, irá adicionar um "chave:valor" no novo dicionário, com base na coluna da lista
                    for l_index, l in enumerate(line): 
                        key = data[0][l_index]
                        new_dict[key.strip()] = l
                    new_list.append(new_dict)
            
            return new_list
        
    def create(self, data: dict):
        data["id"] = self.get_last_id() + 1
        headers = self.get_header_order()

        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([data.get(key) for key in headers])
    
    def get_by_id(self, id):
        data = self.list_all()

        value = list(filter(lambda item: item["id"] == str(id), data))
        return value[0] if len(value) > 0 else None
    
    def check_criterion(self, item_value, operator, criterion_value):
        op = operator.upper()

        if item_value is None:
            item_value = ""
        if criterion_value is None:
            criterion_value = ""

        str_item_val = str(item_value).lower()
        str_crit_val = str(criterion_value).lower()

        if op == "EQUAL":
            return str_item_val == str_crit_val
        
        if op == "NOT_EQUAL":
            return str_item_val != str_crit_val

        if op == "CONTAINS":
            return str_crit_val in str_item_val

        try:
            num_item_val = float(item_value)
            num_crit_val = float(criterion_value)
        except (ValueError, TypeError):
            return False 
            
        if op == "LESS_THAN":
            return num_item_val < num_crit_val
        if op == "MORE_THAN":
            return num_item_val > num_crit_val
        if op == "LESS_THAN_OR_EQUAL":
            return num_item_val <= num_crit_val
        if op == "MORE_THAN_OR_EQUAL":
            return num_item_val >= num_crit_val

        return False

    def search(self, filters: dict):
        """{
                "logic": OR or AND,
                \n
                "criteria": [\n
                    {"key": "nome",\n "operator": EQUAL or NOT_EQUAL or CONTAINS or LESS_THAN or MORE_THAN or LESS_THAN_OR_EQUAL or MORE_THAN_OR_EQUAL,\n "value": "Rex"},\n
                ]
            }"""
        
        data = self.list_all()
        
        logic = filters.get("logic", "AND").upper()
        criteria = filters.get("criteria", [])

        if not criteria:
            return []

        filtered_results = []
        for item in data:
            
            check_results = (
                self.check_criterion(
                    item.get(c["key"]),
                    c["operator"],
                    c["value"]
                ) for c in criteria
            )
            
            if logic == "AND":
                if all(check_results):
                    filtered_results.append(item)
            
            elif logic == "OR":
                if any(check_results):
                    filtered_results.append(item)

        return filtered_results

    def delete(self, id):
        exist = self.get_by_id(id)
        if not exist:
            raise Exception("ID não existe")
        
        data = self.list_all()

        data_filtered = filter(lambda item: item["id"] != str(id), data)
        new_data = self.json_to_csv_array(data_filtered)

        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(new_data)

    def get_header_order(self):
        with open(self.filename, "r", newline="") as f:
            data = list(csv.reader(f))
            return list(map(lambda item: item.strip(), data[0]))

    def json_to_csv_array(self, data: List[Dict[str, Any]]) -> List[List[Any]]:
        headers = self.get_header_order()
        csv_data = [headers]
        for item in data:
            row = [item.get(key, "") for key in headers]
            csv_data.append(row)

        return csv_data
        
    def update(self, data: dict):
        exist = self.get_by_id(data.get("id"))
        if not exist:
            raise Exception("ID não existe")
        
        all_data = self.list_all()
        new_data = []

        for item in all_data:
            if item.get("id") == str(data.get("id")):
                new_item = {**item, **data}
                new_data.append(new_item)
            else:
                new_data.append(item)

        new_data = self.json_to_csv_array(new_data)
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(new_data)

    def get_last_id(self):
        all_data = self.list_all()

        if not all_data:
            return 0
        
        last_id = max([int(item.get("id", 0)) for item in all_data])
        return last_id

    