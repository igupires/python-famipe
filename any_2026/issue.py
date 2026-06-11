import requests
import pandas as pd
from datetime import datetime
from unidecode import unidecode
from task import Task
import json

# -- Local imports ---
from collaborator import Collaborator
from jira_statuses import JiraStatus
from log import print_log, fix_encoding, decode_request_body

# --- Configuration ---
from anytype import ANYTYPE_API_URL, SPACE_ID, HEADERS, JIRA_BASE_URL, CREATE_URL

class Issue:
    @classmethod
    def from_existing(cls, id: str, sprints: list[str], status: JiraStatus, chave: str, tipo: str, responsavel: list[Collaborator],
                      tester: list[Collaborator], resumo: str, relator: Collaborator, task: Task, last_updated: datetime):
        """
        Wraps an existing Issue object from the designated Space.
        """
        issue = cls.__new__(cls)
        issue.object_id = id
        issue.chave = chave
        issue.sprints = sprints
        issue.resumo = resumo.replace('"', '')  # Remove double quotes to prevent JSON issues
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
        self.resumo = resumo.replace('"', '')  # Remove double quotes to prevent JSON issues
        self.status = fix_encoding(status) if status else "backlog"
        self.tipo = tipo
        self.task = None
        self.last_updated = None
                
        # Ensure collaborators are listed and available for lookup  
        if not Collaborator.COLLABORATORS_LISTED:
            Collaborator.list_collaborators()
                
        # Ensure collaborators are listed and available for lookup  
        if not JiraStatus.JIRA_STATUSES_LISTED:
            JiraStatus.list_jira_statuses()
        
        # Collaborators
        self.responsavel = [Collaborator.COLLABORATORS.get(" ".join(name.lower().strip().split(" ")[:2]), None) for name in responsavel]
        self.tester = [Collaborator.COLLABORATORS.get(" ".join(name.lower().strip().split(" ")[:2]), None) for name in tester]
        self.relator = Collaborator.COLLABORATORS.get(" ".join(relator.lower().strip().split(" ")[:2]), None) if relator else None
        
        # Status
        self.status = JiraStatus.JIRA_STATUSES.get(self.status) if self.status else JiraStatus.JIRA_STATUSES.get("backlog")
        
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
        
        # Use json.dumps with ensure_ascii=False so non-ASCII characters are sent as UTF-8
        headers_copy = dict(HEADERS) if HEADERS else {}
        headers_copy.setdefault("Content-Type", "application/json; charset=utf-8")
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            response = requests.post(CREATE_URL, headers=headers_copy, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            body = decode_request_body(getattr(e.request, 'body', None))
            print_log(f" API > Issue Create Error processing '{self.chave}': {e}")
            print_log(f" Payload: {body}")
            raise
        
        response_json = response.json()
        self.object_id = response_json.get("object", {}).get("id")
        self.last_updated = [pd.to_datetime(prop.get("date")) for prop in response_json.get("object", {}).get("properties") if prop.get("key") == "last_modified_date" or prop.get("key") == "created_date"] if response_json.get("object", {}).get("properties") else None
        self.last_updated = max(self.last_updated) if self.last_updated else None

    def __create_payload(self):
        """
        Builds the payload for creating or updating an Issue object.
        """
        json = {
            "type_key": "jira_task", 
            "name": self.chave,
            "markdown": f"""# {self.resumo}

## 📋 URL
[{JIRA_BASE_URL}{self.chave}]({JIRA_BASE_URL}{self.chave})

## 📋📊  Relator

Relator: {self.relator.name if self.relator else 'N/A'}

            """,
            "properties": [
                # Note: The format (text, select, etc.) depends on your Anytype Relation definitions
                {"key": "bafyreidsudfn44vilqy4n6dhtajt4aubohjwagnfhmmfxc3megnh5cktka", "format": "text", "text": self.tipo},
                {"key": "bafyreiesx2xupjll5yrzversardre7obg5cavsetlsrdxylonw6pj2qaia", "multi_select": self.sprints},
                {"key": "bafyreibdiht2ujhr5txjn45ls5xzn6wdxg2amu4hwg2dollykirsastfim", "format": "objects", "objects": [self.task.object_id]},
                {"key": "bafyreihufpp4c3nrkvn4drfa2wqlpoddjm7he4eh6clfyvqba6i7aqkgf4", "select": self.status.clean_name if self.status else "backlog"},
                {"key": "bafyreihbmhx5mdi2stuj2mnicz5moob4kqjhqg6o4ikuf34wkjvrha2crm", "format": "text", "text": self.resumo},
                {"key": "bafyreihok7nqj6j6ynot64a25wacti4gzzy72h2kraq3hfynf3jalywbxe", "format": "url", "url": f"{JIRA_BASE_URL}{self.chave}"}           
            ]
        }
        
        properties = json["properties"]
        
        # Tester
        if self.tester:
            ids = [colab.object_id for colab in self.tester if colab]
            
            if ids:
                properties.append({"key": "bafyreibxqec67q6i6emfyczcuerazh52abbqai3jzotjgbhxnwwfp6xyx4", "format": "objects", "objects": ids})
        
        # Responsavel
        if self.responsavel:
            ids = [colab.object_id for colab in self.responsavel if colab]
            
            if ids:
                properties.append({"key": "bafyreicjflgchbxgssl42qonhugsxxxqzw5s3h5huqyxjhghn3mlflyvri", "format": "objects", "objects": ids})
        
        # Relator
        if self.relator:
            if self.relator.object_id:
                properties.append({"key": "bafyreiclzvky7ddxrlguy3bwvhp6eblbokyddynszbrqaugt7pkdyca7xi", "format": "objects", "objects": [self.relator.object_id]})
        
        return json

    def update_issue(self, sprints: list[str], status: str, chave: str, tipo: str, responsavel: list[str], tester: list[str], resumo: str, relator: str, force_update: bool = False):
        """
        Updates an existing Issue object.
        """
        if self.object_id == None:
            raise ValueError("Issue object is missing or does not contain an 'id' field.")
        
        self.chave = chave
        self.sprints = sprints
        self.resumo = resumo
        self.status = fix_encoding(status) if status else "backlog"
        self.tipo = tipo
                
        update_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects/{self.object_id}"
        
        # Collaborators
        self.responsavel = [Collaborator.COLLABORATORS.get(" ".join(name.split(" ")[:2]), None) for name in responsavel]
        self.tester = [Collaborator.COLLABORATORS.get(" ".join(name.split(" ")[:2]), None) for name in tester]
        self.relator = Collaborator.COLLABORATORS.get(" ".join(relator.split(" ")[:2]), None) if relator else None
        
        # Status
        self.status = JiraStatus.JIRA_STATUSES.get(self.status) if self.status else JiraStatus.JIRA_STATUSES.get("backlog")

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
        # Send UTF-8 JSON for updates as well (prevent \uXXXX escapes)
        headers_copy = dict(HEADERS) if HEADERS else {}
        headers_copy.setdefault("Content-Type", "application/json; charset=utf-8")
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            response = requests.patch(update_url, headers=headers_copy, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            body = decode_request_body(getattr(e.request, 'body', None))
            print_log(f" API > Issue Update Error processing '{self.chave}': {e}")
            print_log(f" Payload: {body}")
            raise
        
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
                
                #status
                status = JiraStatus.JIRA_STATUSES.get(status) if status else JiraStatus.JIRA_STATUSES.get("backlog")
                
                # task
                task = next((Task.get_task(prop.get("objects")[0]) for prop in obj.get("properties", []) if prop.get("key") == "task"), [])
                
                return Issue.from_existing(id, sprints, status, chave, tipo, responsavel, tester, resumo, relator, task, last_updated)
                
        return None