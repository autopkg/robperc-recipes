#!/usr/bin/env python

from __future__ import absolute_import

import hashlib

from autopkglib import Processor, ProcessorError

__all__ = ["Sha256Summer"]

class Sha256Summer(Processor):
    description = "Returns SHA256 sum for specified file."
    input_variables = {
        "file_path": {
            "required": True,
            "description": "Path to file to perform SHA256 sum on."
        },
    }
    output_variables = {
        "file_sha256sum": {
            "description": "SHA256 sum for specified file.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        file_path = self.env["file_path"]
        
        self.env["file_sha256sum"] = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()

if __name__ == "__main__":
    processor = Sha256Summer()
    processor.execute_shell()
