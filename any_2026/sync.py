import requests
from datetime import datetime
import pandas as pd

from issue import Issue

# --- Local imports ---
from log import print_log
from file import File

# --- Configuration ---
from anytype import CREATE_URL, HEADERS

class Sync:
    def __init__(self, filepath: str, issues:list[Issue], log: list[str], skip_count:int, update_count:int, create_count:int, error_count:int):
        # self.file = File(filepath, name=f"Sync CSV {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.issues = issues
        self.skip_count = skip_count
        self.update_count = update_count
        self.create_count = create_count
        self.error_count = error_count
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log = log
        
        #Builds paylooad 
        payload = self.__create_payload()
        print_log(f" < Creating SYNC >")
        
        response = requests.post(CREATE_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        self.object_id = response_json.get("object", {}).get("id")
        self.last_updated = [pd.to_datetime(prop.get("date")) for prop in response_json.get("object", {}).get("properties") if prop.get("key") == "last_modified_date" or prop.get("key") == "created_date"] if response_json.get("object", {}).get("properties") else None
        self.last_updated = max(self.last_updated) if self.last_updated else None
        
    def __create_payload(self):
        """
        Builds the payload for creating or updating an Sync object.
        """
        return {
            "type_key": "sync", 
            "name": f"Sync of {self.date_time}",
            "properties": [
                # Note: The format (text, select, etc.) depends on your Anytype Relation definitions
                {"key": "bafyreidvgoofi3myciirwbepesaagfcrbzougjj2fx6sg7hwlsjev7xo2q", "format": "objects", "objects": [issue.object_id for issue in self.issues] if self.issues else []},
                {"key": "bafyreibepvz6te3fagm7uzyikjxxsvcujydja22j3yda52jz7cimvenpwe", "format": "text", "text": """
""".join(self.log).strip()},
                {"key": "bafyreibyamo6knxuqpooqulyigsko5ymfyudgfin4i6c42wohblq6nbdne", "format": "number", "number": self.create_count},
                {"key": "bafyreifw6d4ne7whghs2bd4nhj5aavgr5bkbnj25rvxbyv64zilyj5mlte", "format": "number", "number": self.update_count},
                {"key": "bafyreifnii7g4cb772galayxlubrg66wqwniby476aytyuuq3nsq7bwzmm", "format": "number", "number": self.error_count},
                {"key": "bafyreihcgzmkwqyc7i6eirs3mqem2c4vngj72l66n36kwvicvx5k7yv3ku", "format": "number", "number": self.skip_count},
                # {"key": "csv_file", "format": "file", "file": [self.file.object_id] if self.file else []}
            ]
        }
        
    def append_issue(self, issue):
        self.issues.append(issue)