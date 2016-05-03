#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import json

__all__ = ["JsonReader"]

class StringSplitter(Processor):
    description = "Reads JSON file and returns value for specified key."
    input_variables = {
        "json_file": {
            "required": True,
            "description": "Path to json file to read."
        },
        "json_key": {
            "required": True,
            "description": "Key to return corresponding value for."
        },
    }
    output_variables = {
        "json_value": {
            "description": "Value for specified json key.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        json_file = self.env["json_file"]
        json_key  = self.env["json_key"]
        
        self.env["json_value"] = json.load(open("json_file"))[json_key]

if __name__ == "__main__":
    processor = JsonReader()
    processor.execute_shell()