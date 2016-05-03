#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import hashlib

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
        "file_checksum": {
            "description": "MD5 checksum of specified file.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        file_path = self.env["file_path"]
        
        self.env["file_checksum"] = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

if __name__ == "__main__":
    processor = FileChecksummer()
    processor.execute_shell()