import requests

# --- Configuration ---
from anytype import ANYTYPE_API_URL, SPACE_ID, HEADERS

class Collaborator:
    COLLABORATORS = {}
    COLLABORATORS_ID = {}
    COLLABORATORS_LISTED = False
    
    def __init__(self, id: str, name: str):
        self.name = name
        self.object_id = id
        
    def __repr__(self):
        return f"{self.name} [id: {self.object_id}]"

    @staticmethod
    def list_collaborators():
        """
        Fetches the list of collaborators in the Anytype workspace.
        """
        collaborators_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/search"
        
        # The payload looks for objects matching the title and filters by the "issue" type key
        payload = {
            "types": ["colaborador"],
            "limit": 100
        }
        
        response = requests.post(collaborators_url, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        list = response.json().get("data", [])
        
        # Maps collaborator names to their IDs for easy lookup
        collaborator_map  = {}
        collabotartors_id = {}
        for collab in list:
            name = collab.get("name", "")
            name_2 = " ".join(name.split(" ")[:2])
            id = collab.get("id", "")
            collaborator_map[name_2] = Collaborator(id, name)
            collabotartors_id[id] = Collaborator(id, name)
        
        Collaborator.COLLABORATORS = collaborator_map
        Collaborator.COLLABORATORS_ID = collabotartors_id
        Collaborator.COLLABORATORS_LISTED = True
        
        return collaborator_map