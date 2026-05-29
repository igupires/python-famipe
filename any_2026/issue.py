import requests
import pandas as pd
from datetime import datetime
from unidecode import unidecode
from task import Task

# -- Local imports ---
from collaborator import Collaborator
from log import print_log

# --- Configuration ---
from anytype import ANYTYPE_API_URL, SPACE_ID, HEADERS, JIRA_BASE_URL, CREATE_URL

class Issue:
    @classmethod
    def from_existing(cls, id: str, sprints: list[str], status: str, chave: str, tipo: str, responsavel: list[Collaborator],
                      tester: list[Collaborator], resumo: str, relator: Collaborator, task: Task, last_updated: datetime):
        """
        Wraps an existing Issue object from the designated Space.
        """
        issue = cls.__new__(cls)
        issue.object_id = id
        print_log(f" Wrapping existing issue with ID: {id}")
        issue.chave = chave
        issue.sprints = sprints
        issue.resumo = resumo
        issue.status = status
        issue.tipo = tipo
        
        if task is None:
            raise ValueError(f"Task object is missing for issue with chave: {chave}")
        
        issue.task = task
        issue.last_updated = last_updated
        
        # Collaborators
        issue.responsavel = responsavel
        issue.tester = tester
        issue.relator = relator
        return issue

    def __init__(self, sprints: list[str], status: str,
                 chave: str, tipo: str, responsavel: list[str], tester: list[str], resumo: str, relator: str):
        """
        Creates a new Issue object in the designated Space.
        """
        self.object_id = None
        self.chave = chave
        self.sprints = sprints
        self.resumo = resumo
        self.status = unidecode(status.lower().replace(" ", "_")) if status else "backlog"
        self.tipo = tipo
        self.task = None
        self.last_updated = None
                
        # Ensure collaborators are listed and available for lookup  
        if not Collaborator.COLLABORATORS_LISTED:
            Collaborator.list_collaborators()
        
        # Collaborators
        self.responsavel = [Collaborator.COLLABORATORS.get(" ".join(name.lower().strip().split(" ")[:2]), None) for name in responsavel]
        self.tester = [Collaborator.COLLABORATORS.get(" ".join(name.lower().strip().split(" ")[:2]), None) for name in tester]
        self.relator = Collaborator.COLLABORATORS.get(" ".join(relator.lower().strip().split(" ")[:2]), None) if relator else None
        
        #Verifies if the task already exists, if it does not exist, it creates a new one
        try:
            # 4b. Create untracked issue
            print_log(" New issue. Creating new task...")
            self.task = Task(self.chave, self.sprints, self.resumo)
            print_log(" Task creation successful.")
                
        except requests.exceptions.RequestException as e:
            print_log(f" API > Task Error processing '{self.chave}': {e}")
            raise e
        
        #Builds paylooad 
        payload = self.__create_payload()
        
        response = requests.post(CREATE_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        self.object_id = response_json.get("object", {}).get("id")
        self.last_updated = [pd.to_datetime(prop.get("date")) for prop in response_json.get("object", {}).get("properties") if prop.get("key") == "last_modified_date" or prop.get("key") == "created_date"] if response_json.get("object", {}).get("properties") else None
        self.last_updated = max(self.last_updated) if self.last_updated else None

    def __create_payload(self):
        """
        Builds the payload for creating or updating an Issue object.
        """
        return {
            "type_key": "jira_task", 
            "name": self.chave,
            "markdown": f"""# {self.resumo}

            ## 📋 URL
            [{JIRA_BASE_URL}{self.chave}]({JIRA_BASE_URL}{self.chave})

            ## 📋📊  Relator

            Relator: {self.relator}

            """,
            "properties": [
                # Note: The format (text, select, etc.) depends on your Anytype Relation definitions
                {"key": "testador", "format": "objects", "objects": self.tester if self.tester else []},
                {"key": "desenvolvedor", "format": "objects", "objects": self.responsavel if self.responsavel else []},
                {"key": "tipo", "format": "text", "text": self.tipo},
                {"key": "tag", "multi_select": self.sprints},
                {"key": "task", "format": "objects", "objects": [self.task.object_id]},
                {"key": "status", "select": self.status},
                {"key": "description", "format": "text", "text": self.resumo},
                {"key": "url", "format": "text", "text": f"{JIRA_BASE_URL}{self.chave}"}           
            ]
        }

    def update_issue(self, sprints: list[str], status: str, chave: str, tipo: str, responsavel: list[Collaborator], tester: list[Collaborator], resumo: str, relator: Collaborator, force_update: bool = False):
        """
        Updates an existing Issue object.
        """
        if self.object_id == None:
            raise ValueError("Issue object is missing or does not contain an 'id' field.")
        
        self.chave = chave
        self.sprints = sprints
        self.resumo = resumo
        self.status = unidecode(status.lower().replace(" ", "_")) if status else "backlog"
        self.tipo = tipo
                
        update_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects/{self.object_id}"
        
        # Collaborators
        self.responsavel = [Collaborator.COLLABORATORS.get(" ".join(name.lower().strip().split(" ")[:2]), None) for name in responsavel]
        self.tester = [Collaborator.COLLABORATORS.get(" ".join(name.lower().strip().split(" ")[:2]), None) for name in tester]
        self.relator = Collaborator.COLLABORATORS.get(" ".join(relator.lower().strip().split(" ")[:2]), None) if relator else None
        
        #Verifies if the task already exists, if it does not exist, it creates a new one
        try:
            if self.task is not None:
                # 4a. Update tracked issue
                if force_update:
                    print_log(f" Found existing task. Updating...")
                    self.task.update_task(chave, sprints, resumo)
                else:
                    print_log(f" Found existing task. Skipping update due to -f flag...")
            else:
                # 4b. Create untracked issue
                print_log(" Task not found in Anytype. Creating new object...")
                self.task = Task(self.chave, self.sprints, self.resumo)
                print_log(" Creation successful.")
                
        except requests.exceptions.RequestException as e:
            print_log(f" API > Task Error processing '{self.chave}': {e}")
            raise e
        
        #Builds paylooad 
        payload = self.__create_payload()
        
        # Updating usually utilizes a PATCH request in standard REST implementations
        response = requests.patch(update_url, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        self.last_updated = [pd.to_datetime(prop.get("date")) for prop in response_json.get("object", {}).get("properties") if prop.get("key") == "last_modified_date" or prop.get("key") == "created_date"] if response_json.get("object", {}).get("properties") else None
        self.last_updated = max(self.last_updated) if self.last_updated else None
        return response_json

    @staticmethod
    def get_issue_by_title(issue_title):
        """
        Searches Anytype globally to see if an object matching the title exists.
        """
        search_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/search"
        
        # The payload looks for objects matching the title and filters by the "issue" type key
        payload = {
            "query": issue_title,
            "types": ["jira_task"],
            "limit": 1
        }
        
        
        print_log(f" Start searching for issue '{issue_title}'...")
        start_time = datetime.now()
        response = requests.post(search_url, headers=HEADERS, json=payload)
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        
        print_log(f" Search API call took {elapsed_time:.2f} seconds for issue '{issue_title}'")
        
        if response.status_code == 200:
            data = response.json()
            # If the search returns a list of data, the issue is already tracked
            if data.get("data") and len(data["data"]) > 0:
                obj = data["data"][0]
                id = obj.get("id")
                chave = obj.get("name", "")
                sprints = next((select.get("key") for select in prop.get("multi_select", []) if select.get("key")) for prop in obj.get("properties", []) if prop.get("key") == "tag")
                status = next((prop.get("select", "").get("name", "") for prop in obj.get("properties", []) if prop.get("key") == "status"), [])
                tipo = next((prop.get("text", "") for prop in obj.get("properties", []) if prop.get("key") == "tipo"), "")
                resumo = next((prop.get("text", "") for prop in obj.get("properties", []) if prop.get("key") == "description"), "")
                
                last_updated = [pd.to_datetime(prop.get("date")) for prop in obj.get("properties", []) if prop.get("key") == "last_modified_date" or prop.get("key") == "created_date"] if obj.get("properties") else None
                last_updated = max(last_updated) if last_updated else None
                
                # collaborators
                responsavel = [Collaborator.COLLABORATORS_ID.get(o) for prop in obj.get("properties", []) if prop.get("key") == "desenvolvedor" for o in prop.get("objects", [])]
                tester = [Collaborator.COLLABORATORS_ID.get(o) for prop in obj.get("properties", []) if prop.get("key") == "testador" for o in prop.get("objects", [])]
                relator = next((Collaborator.COLLABORATORS_ID.get(o) for prop in obj.get("properties", []) if prop.get("key") == "relator" for o in prop.get("objects", [])), None)
                
                # task
                task = next((Task.get_task(prop.get("objects")[0]) for prop in obj.get("properties", []) if prop.get("key") == "task"), [])
                
                return Issue.from_existing(id, sprints, status, chave, tipo, responsavel, tester, resumo, relator, task, last_updated)
                
        return None