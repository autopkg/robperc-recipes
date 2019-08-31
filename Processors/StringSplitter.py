#!/usr/bin/env python

from __future__ import absolute_import
from autopkglib import Processor, ProcessorError

__all__ = ["StringSplitter"]

class StringSplitter(Processor):
    description = "Splits string on specified delimiter and returns substring at specified index."
    input_variables = {
        "string": {
            "required": True,
            "description": "String to split."
        },
        "delimiter": {
            "required": False,
            "description": "Delimiter to split string on. Defaults to ' '",
            "default": ' '
        },
        "index": {
            "required": True,
            "description": "Index of substring to return."
        },
    }
    output_variables = {
        "out_string": {
            "description": "Substring at specified index to return.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        string = self.env["string"]
        delim  = self.env["delimiter"]
        index  = int(self.env["index"])

        subs   = string.split(delim)
        if index > len(subs):
            index = -1
        self.env["out_string"] = subs[index]

if __name__ == "__main__":
    processor = StringSplitter()
    processor.execute_shell()