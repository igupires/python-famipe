import mimetypes
import os

import requests
from anytype import ANYTYPE_VERSION, FILE_URL, HEADERS
from log import print_log

class File:
    def __init__(self, filepath:str, name: str):
        self.filepath = filepath
        self.name = name
        
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        with open(filepath, "r", encoding="utf-8") as file:
            self.content = file.read()

        print_log(f"File '{self.name}' loaded successfully from '{self.filepath}'.")
        print_log(f"Uploading to Anytype...'")
        
        payload = self.__create_payload()
        
        try:
            response = requests.post(FILE_URL, headers=HEADERS, files=payload)
            response.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            print_log(f" API > File Error processing '{self.name}': {e}")
            print_log(f" API > Payload 'payload': {payload}")
            raise e

        response_json = response.json()
        self.object_id = response_json.get("object", {}).get("id")

        
    def __create_payload(self):
        """
        Builds the payload for creating or updating an Issue object.
        """
        return {
            "file": self.content
        }