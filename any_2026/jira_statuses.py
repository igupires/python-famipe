import unicodedata

import requests

# --- Configuration ---
from log import print_log
from anytype import ANYTYPE_API_URL, SPACE_ID, HEADERS

class JiraStatus:
    JIRA_STATUSES = {}
    JIRA_STATUSES_ID = {}
    JIRA_STATUSES_LISTED = False
    
    def __init__(self, id: str, name: str):
        self.name = name
        normalized = unicodedata.normalize('NFD', name)
        normalized = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
        self.clean_name = normalized.lower().strip().replace(" ", "_")
        self.object_id = id
        
    def __repr__(self):
        return f"{self.name} ({self.clean_name}) [id: {self.object_id}]"

    @staticmethod
    def list_jira_statuses():
        """
        Fetches the list of Jira statuses in the Anytype workspace.
        """
        jira_statuses_url = f"{ANYTYPE_API_URL}/spaces/{SPACE_ID}/search"
        
        # The payload looks for objects matching the title and filters by the "issue" type key
        payload = {
            "types": ["jira_status"],
            "limit": 100
        }
        
        response = requests.post(jira_statuses_url, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        list = response.json().get("data", [])
        
        print_log(f"Found {len(list)} Jira statuses in Anytype.")
        
        # Maps Jira status names to their IDs for easy lookup
        jira_status_map  = {}
        jira_statuses_id = {}
        for status in list:
            name = status.get("name", "")
            id = status.get("id", "")
            jira_status_map[name] = JiraStatus(id, name)
            jira_statuses_id[id] = JiraStatus(id, name)
        
        JiraStatus.JIRA_STATUSES = jira_status_map
        JiraStatus.JIRA_STATUSES_ID = jira_statuses_id
        JiraStatus.JIRA_STATUSES_LISTED = True
        
        return jira_status_map