#!/usr/bin/env python

from __future__ import absolute_import

import hashlib
import os

from autopkglib import Processor, ProcessorError

__all__ = ["FileChecksummer"]

class FileChecksummer(Processor):
    description = "Returns MD5 checksum for specified file."
    input_variables = {
        "file_path": {
            "required": True,
            "description": "Path to file to checksum."
        },
    }
    output_variables = {
        "{file_name}_checksum": {
            "description": "MD5 checksum of specified file.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        file_path = self.env["file_path"]
        output_var = os.path.basename(file_path).split(".")[0] + "_checksum"
        self.env[output_var] = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

if __name__ == "__main__":
    processor = FileChecksummer()
    processor.execute_shell()
