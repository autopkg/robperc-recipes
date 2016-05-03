#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import os

__all__ = ["ItemSizer"]

class ItemSizer(Processor):
    description = "Returns size of specified item in kibibytes (KiB)."
    input_variables = {
        "item_path": {
            "required": True,
            "description": "Path to item to retrieve size of."
        },
    }
    output_variables = {
        "item_size": {
            "description": "Size of specified item in kibibytes (KiB).",
        },
    }
    
    __doc__ = description
    
    def main(self):
        item_path = self.env["item_path"]
        
        self.env["item_size"] = str(os.path.getsize(item_path) / 1024)

if __name__ == "__main__":
    processor = ItemSizer()
    processor.execute_shell()