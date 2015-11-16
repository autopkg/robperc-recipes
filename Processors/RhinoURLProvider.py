#!/usr/bin/env python
#
# Copyright 2015 Rob percival
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from autopkglib import Processor, ProcessorError

__all__ = ["RhinoURLProvider"]

class RhinoURLProvider(Processor):
    description = "Returns a URL to latest Rhino release download using information \
    scraped from the Rhino release notes page."
    input_variables = {
        "release_url": {
            "required": True,
            "description": "Path string to latest release notes."
        },
    }
    output_variables = {
        "rhino_url": {
            "description": "URL to the latest Rhino release download.",
        },
    }
    
    __doc__ = description
    
    def main(self):
        # Determine base_url, version, product_name.
        release_url = self.env["release_url"]
        release = release_url.split('/')[-2]
        version = release.split("release-")[1]
        version = '.'.join(version.split('-'))
        major = str(float('.'.join(version.split('.')[:-1])))
        url = "http://files.mcneel.com/Releases/Rhino/MAJOR/Mac/Rhinoceros_VERSION.dmg".replace("MAJOR", major).replace("VERSION", version)
        self.env["rhino_url"] = url
    

if __name__ == "__main__":
    processor = RhinoURLProvider()
    processor.execute_shell()