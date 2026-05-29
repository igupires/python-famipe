import requests
from datetime import datetime

# --- Local imports ---
from log import print_log

# --- Configuration ---
from anytype import ANYTYPE_API_URL, SPACE_ID, HEADERS, JIRA_BASE_URL, TAG_DICT

class Task:
    def __init__(self, chave: str, sprints: list[str], resumo: str):
        """
        Creates a new Task object in the designated Space.
        """
        self.object_id = None
        self.chave = chave
        self.sprints = sprints
        self.resumo = resumo
        self.response_json = None

        # Builds paylooad and creates the task
        create_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects"

        payload = self.__create_payload()

        response = requests.post(create_url, headers=HEADERS, json=payload)
        response.raise_for_status()

        self.response_json = response.json()
        self.object_id = self.response_json.get("object", {}).get("id")

    @classmethod
    def from_existing(cls, id: str, chave: str, sprints: list[str], resumo: str):
        """
        Creates a Task object wrapper for an existing object.
        """
        task = cls.__new__(cls)
        task.object_id = id
        task.chave = chave
        task.sprints = sprints
        task.resumo = resumo
        task.response_json = None
        return task

    def __create_payload(self):
        """
        Builds the payload for creating or updating a Task object.
        """
        return {
            "name": f"{self.chave}: {self.resumo}",
            "body": f"**URL**: [{JIRA_BASE_URL}{self.chave}]({JIRA_BASE_URL}{self.chave})",
            "properties": [
                {"key": "tag", "multi_select": self.sprints},
                {"key": "url", "format": "text", "text": f"{JIRA_BASE_URL}{self.chave}"}
            ]
        }

    def __update_payload(self):
        """
        Builds the payload for creating or updating a Task object.
        """
        return {
            "name": f"{self.chave}: {self.resumo}",
            "properties": [
                {"key": "tag", "multi_select": self.sprints},
                {"key": "url", "format": "text", "text": f"{JIRA_BASE_URL}{self.chave}"}
            ]
        }
    
    def update_task(self, chave: str, sprints: list[str], resumo: str):
        """
        Updates an existing Task object.
        """
        update_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects/{self.object_id}"
        self.chave = chave
        self.sprints = sprints
        self.resumo = resumo
        
        payload = self.__update_payload()
        print_log(f" Updating task '{self.chave}' with payload: {payload}")
        
        # Updating usually utilizes a PATCH request in standard REST implementations
        response = requests.patch(update_url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
        
    @staticmethod
    def get_task(id:str):
        """
        Fetches a Task object by its ID.
        """
        print_log(f" Fetching task with ID '{id}'...")
        url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects/{id}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # If the search returns a list of data, the issue is already tracked
            if data.get("object"):
                obj = data["object"]
                name = obj.get("name", "")
                chave = name.split(":")[0] if ":" in name else name
                sprints = next((prop.get("multi_select", []) for prop in obj.get("properties", []) if prop.get("key") == "tag"), [])
                resumo = name.split(":")[1].strip() if ":" in name else ""
                return Task.from_existing(id, chave, sprints, resumo)
                
        return None
        
    @staticmethod
    def has_task(id:str):
        """
        Checks if a Task object exists by its ID.
        """
        url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/objects/{id}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # If the search returns a list of data, the issue is already tracked
            if data.get("object"):
                return True
                
        return False

    @staticmethod
    def get_task_by_title(issue_title: str):
        """
        Searches Anytype globally to see if an object matching the title exists.
        """
        search_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/search"
        
        # The payload looks for objects matching the title and filters by the "issue" type key
        payload = {
            "query": issue_title,
            "types": ["task"],
            "limit": 1
        }
        
        print_log(f" Start searching for task '{issue_title}'...")
        start_time = datetime.now()
        response = requests.post(search_url, headers=HEADERS, json=payload)
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        
        print_log(f" Search API call took {elapsed_time:.2f} seconds for task '{issue_title}'")
        
        if response.status_code == 200:
            data = response.json()
            # If the search returns a list of data, the issue is already tracked
            if data.get("data") and len(data["data"]) > 0:
                obj = data["data"][0]
                id = obj.get("id")
                name = obj.get("name", "")
                chave = name.split(":")[0] if ":" in name else name
                sprints = next((prop.get("multi_select", []) for prop in obj.get("properties", []) if prop.get("key") == "tag"), [])
                resumo = name.split(":")[1].strip() if ":" in name else ""
                return Task.from_existing(id, chave, sprints, resumo)
                
        return None