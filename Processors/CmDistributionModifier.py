#!/usr/local/autopkg/python
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

XML = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<installer-script minSpecVersion="1.000000" authoringTool="com.apple.PackageMaker" authoringToolVersion="3.0.6" authoringToolBuild="201">
    <title>CodeMeter Runtime Kit (KEXT3G)</title>
    <options customize="always" allow-external-scripts="no"/>
    <domains enable_localSystem="true"/>
    <background file="background" alignment="topleft" scaling="none"/>
    <readme file="ReadMe"/>
    <license file="License"/>
    <choices-outline>
        <line choice="choice0"/>
        <line choice="choice1"/>
        <line choice="choice2"/>
        <line choice="choice6"/>
        <line choice="choice7"/>
    </choices-outline>
    <choice id="choice0" title="CmDriver" customLocation="/">
        <pkg-ref id="com.wibu.CodeMeter.driver"/>
    </choice>
    <choice id="choice1" title="Kernel Extension (KEXT 3G)" tooltip="Kernel Extension 3G" description="This package contains the CodeMeter kernel extension (KEXT 3.Gen). This KEXT is required to seize hardware access to the CmStick and enables the user to do a firmware update. This Kext will not support any mass storage funtionality." customLocation="/">
        <pkg-ref id="com.wibu.CodeMeter.kext3"/>
    </choice>
    <choice id="choice2" title="Kernel Extension (KEXT 5G)" tooltip="Kernel Extension 5G" description="This package contains the CodeMeter kernel extension (KEXT 5.Gen). This KEXT is required to seize hardware access to the CmStick. This Kext enables to use mass storage functionality." customLocation="/">
        <pkg-ref id="com.wibu.CodeMeter.kext5"/>
    </choice>
    <choice id="choice6" title="AxProtector/Java support" tooltip="AxProtector for Java support files" description="This package contains the library to support AxProtector/Java applications." customLocation="/">
        <pkg-ref id="com.wibu.WIBU-KEY.axprot"/>
    </choice>
    <choice id="choice7" title="CodeMeter User Help" tooltip="CodeMeter User Help" description="This package contains the CodeMeter User Help." customLocation="/">
        <pkg-ref id="com.wibu.CodeMeter.help"/>
    </choice>
    <pkg-ref id="com.wibu.CodeMeter.driver" installKBytes="35548" version="5.21" auth="Root" onConclusion="RequireRestart">#cmdriver.pkg</pkg-ref>
    <pkg-ref id="com.wibu.CodeMeter.driver">
        <relocate search-id="pkmktoken24">
            <bundle id="com.codemeter.codemetercc"/>
        </relocate>
    </pkg-ref>
    <pkg-ref id="com.wibu.CodeMeter.kext3" installKBytes="8" version="5.21" auth="Root">#cmkext.pkg</pkg-ref>
    <pkg-ref id="com.wibu.CodeMeter.kext5" installKBytes="488" version="5.21" auth="Root">#cmkext5g.pkg</pkg-ref>
    <pkg-ref id="com.wibu.WIBU-KEY.axprot" installKBytes="5520" version="9.11" auth="Root">#axprotector.pkg</pkg-ref>
    <pkg-ref id="com.wibu.CodeMeter.help" installKBytes="12792" version="5.21" auth="Root">#cmuserhelp.pkg</pkg-ref>
    <locator>
        <search id="pkmktoken24-1" type="component">
            <bundle CFBundleIdentifier="com.codemeter.codemetercc" path="/Applications/CodeMeter.app"/>
        </search>
        <search id="pkmktoken24-0" type="script" script="pkmktoken24_combined()">
            <script>
function pkmktoken24_combined() {
	function pkmk_add_results_to_array(results, array) {
		for(i = 0; i &lt; results.length; i++)
			array.push(results[i]);
	}
	var result = new Array();
	var search;
	search = my.search.results['pkmktoken24-1'];
	if(search) pkmk_add_results_to_array(search, result);
	return result;
}
</script>
        </search>
        <search type="script" id="pkmktoken24" script="pkmktoken24_final()">
            <script>
function pkmktoken24_final() {
	var combined = my.search.results['pkmktoken24-0'];
	return combined;
}
</script>
        </search>
    </locator>
</installer-script>"""


__all__ = ["CmDistributionModifier"]

class CmDistributionModifier(Processor):
    description = "Modifies non-standard distribution file for CmInstall to install all kext packages properly as \
    canonical ChoiceChangesXML method would not work"
    input_variables = {
        "distribution": {
            "required": True,
            "description": "Path to distribution file."
        },
    }
    output_variables = {}
    
    __doc__ = description
    
    def main(self):
        # Determine base_url, version, product_name.
        filename = self.env["distribution"]
        f = open(filename, 'r+')
        f.seek(0)
        f.write(XML)
        f.truncate()
        f.close()
        self.output("Distribution file overwritten")
    

if __name__ == "__main__":
    processor = CmDistributionModifier()
    processor.execute_shell()