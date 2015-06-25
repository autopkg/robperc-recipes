#!/usr/bin/env python
#
# Copyright 2015 Rob percival
# Built on Greg Neagle's iconimporter tool code
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

import sys
sys.path.append('/usr/local/munki')
import os
from optparse import OptionParser
from munkilib import munkicommon
from munkilib import FoundationPlist
from munkilib import iconutils
from autopkglib import Processor, ProcessorError

__all__ = ["IconImporter"]

class IconImporter(Processor):
    description = "Tries to find and import icon(s) from target into icons folder of munki repo. Built on Greg Neagle's iconimporter."
    input_variables = {
        "MUNKI_REPO": {
            "required": True,
            "description": 
                "Path to target repo.",
        },
        "name": {
            "required": True,
            "description": 
                "Name of target to fetch icon(s) for. Should correspond to value of name key in pkginfo",
        },
        "force": {
            "required": False,
            "description":
                "Whether to force import icon from target even if already found. Default is False.",
        },
    }
    output_variables = {}

    __doc__ = description
    
    def main(self):
        repo = self.env["MUNKI_REPO"]
        name = self.env["name"]
        opts = '-i %s' %(name,)
        force = self.env.get("force", False)
        # generate icons!
        generate_pngs_from_munki_items(repo, force=force,
            itemlist=[name])
        # clean up
        munkicommon.cleanUpTmpDir()

"""
The following code is from Greg Neagle's iconimporter tool. 
Unfortunately it is not currently packaged by default with 
munkitools so I can't import it from there like the rest of the
modules...
"""

PREFSNAME = 'com.googlecode.munki.munkiimport.plist'
PREFSPATH = os.path.expanduser(os.path.join(u'~/Library/Preferences', PREFSNAME))
        
def generate_png_from_copy_from_dmg_item(install_item, repo_path):
    dmgpath = os.path.join(
        repo_path, 'pkgs', install_item['installer_item_location'])
    mountpoints = munkicommon.mountdmg(dmgpath)
    if mountpoints:
        mountpoint = mountpoints[0]
        apps = [item for item in install_item.get('items_to_copy', [])
                if item.get('source_item', '').endswith('.app')]
        if len(apps):
            app_path = os.path.join(mountpoint, apps[0]['source_item'])
            icon_path = iconutils.findIconForApp(app_path)
            if icon_path:
                png_path = os.path.join(
                    repo_path, u'icons', install_item['name'] + u'.png')
                result = iconutils.convertIconToPNG(icon_path, png_path)
                if result:
                    print_utf8(u'\tWrote: %s' % png_path)
                else:
                    print_err_utf8(u'\tError converting %s to png.' % icon_path)
            else:
                print_utf8(u'\tNo application icons found.')
        else:
            print_utf8(u'\tNo application icons found.')
        munkicommon.unmountdmg(mountpoint)

def generate_pngs_from_installer_pkg(install_item, repo_path):
    icon_paths = []
    mountpoint = None
    pkg_path = None
    item_path = os.path.join(
        repo_path, u'pkgs', install_item['installer_item_location'])
    if munkicommon.hasValidDiskImageExt(item_path):
        dmg_path = item_path
        mountpoints = munkicommon.mountdmg(dmg_path)
        if mountpoints:
            mountpoint = mountpoints[0]
            if install_item.get('package_path'):
                pkg_path = os.path.join(
                    mountpoint, install_item['package_path'])
            else:
                # find first item that appears to be a pkg at the root
                for fileitem in munkicommon.listdir(mountpoints[0]):
                    if munkicommon.hasValidPackageExt(fileitem):
                        pkg_path = os.path.join(mountpoint, fileitem)
                        break
    elif munkicommon.hasValidPackageExt(item_path):
        pkg_path = item_path
    if pkg_path:
        if os.path.isdir(pkg_path):
            icon_paths = iconutils.extractAppIconsFromBundlePkg(pkg_path)
        else:
            icon_paths = iconutils.extractAppIconsFromFlatPkg(pkg_path)

    if mountpoint:
        munkicommon.unmountdmg(mountpoint)

    if len(icon_paths) == 1:
        png_path = os.path.join(
            repo_path, u'icons', install_item['name'] + u'.png')
        result = iconutils.convertIconToPNG(icon_paths[0], png_path)
        if result:
            print_utf8(u'\tWrote: %s' % png_path)
    elif len(icon_paths) > 1:
        index = 1
        for icon_path in icon_paths:
            png_path = os.path.join(
                repo_path, u'icons',
                install_item['name'] + '_' + str(index) + u'.png')
            result = iconutils.convertIconToPNG(icon_path, png_path)
            if result:
                print_utf8(u'\tWrote: %s' % png_path)
            index += 1
    else:
        print_utf8(u'\tNo application icons found.')
        

def findItemsToCheck(repo_path, itemlist=None):
    '''Builds a list of items to check; only the latest version
    of an item is retained. If itemlist is given, include items
    only on that list.'''
    all_catalog_path = os.path.join(repo_path, 'catalogs/all')
    catalogitems = FoundationPlist.readPlist(all_catalog_path)
    itemdb = {}
    for catalogitem in catalogitems:
        if itemlist and catalogitem['name'] not in itemlist:
            continue
        name = catalogitem['name']
        if name not in itemdb:
            itemdb[name] = catalogitem
        elif (munkicommon.MunkiLooseVersion(catalogitem['version'])
              > munkicommon.MunkiLooseVersion(itemdb[name]['version'])):
            itemdb[name] = catalogitem
    pkg_list = []
    for key in itemdb.keys():
        pkg_list.append(itemdb[key])
    return pkg_list


def generate_pngs_from_munki_items(repo_path, force=False, itemlist=None):
    itemlist = findItemsToCheck(repo_path, itemlist=itemlist)
    icons_dir = os.path.join(repo_path, u'icons')
    if not os.path.exists(icons_dir):
        os.mkdir(icons_dir)
    for item in itemlist:
        print_utf8(u'Processing %s...' % item['name'])
        icon_name = item.get('icon_name') or item['name']
        if not os.path.splitext(icon_name)[1]:
            icon_name += u'.png'
        icon_path = os.path.join(
            repo_path, u'icons', icon_name)
        if os.path.exists(icon_path) and not force:
            print_utf8(u'Found existing icon at %s' % icon_name)
            continue
        installer_type = item.get('installer_type')
        if installer_type == 'copy_from_dmg':
            generate_png_from_copy_from_dmg_item(item, repo_path)
        elif installer_type in [None, '']:
            generate_pngs_from_installer_pkg(item, repo_path)
        else:
            print_utf8(u'\tCan\'t process installer_type: %s' % installer_type)


def print_utf8(text):
    '''Print Unicode text as UTF-8'''
    print text.encode('UTF-8')


def print_err_utf8(text):
    '''Print Unicode text to stderr as UTF-8'''
    print >> sys.stderr, text.encode('UTF-8')


def pref(prefname):
    """Returns a preference for prefname"""
    try:
        _prefs = FoundationPlist.readPlist(PREFSPATH)
    except Exception:
        return None
    if prefname in _prefs:
        return _prefs[prefname]
    else:
        return None

if __name__ == "__main__":
    processor = IconImporter()
    processor.execute_shell()
