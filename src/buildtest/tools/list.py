############################################################################
#
#  Copyright 2017-2019
#
#  https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#  buildtest is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  buildtest is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################


"""
This module implements all the list operation in buildtest which include the
following:
1. List software (buildtest list -ls)
2. List Software and associated module file (buildtest list -svr)
3. List easyconfigs in module tree (buildtest list --easyconfigs)
"""

import json
import sys
from collections import OrderedDict
from operator import itemgetter

from buildtest.tools.modules import BuildTestModule
from buildtest.tools.easybuild import find_easyconfigs



def func_list_subcmd(args):
    """ This method is the entry point for buildtest list subcommand."""

    if args.easyconfigs:
        find_easyconfigs()
    if args.list_unique_software:
        list_software(args)
    if args.software_version_relation:
        list_software_version_relation(args)



def list_software(args):
    """ This method implements buildtest list -ls """

    module_obj = BuildTestModule()
    module_set = module_obj.get_unique_modules()

    if args.format == "json":
        json.dump(module_set, sys.stdout, indent=4, sort_keys=True)
    else:
        count = 0
        text = """
ID  |     Software
----|-----------------------------  """

        print (text)
        for item in module_set:
            count = count + 1
            print ((str(count) + "\t|").expandtabs(4), item)

        print ("Total Software Packages: ", len(module_set))


def list_software_version_relation(args):
    """ This method implements  buildtest list -svr """
    module_obj = BuildTestModule()
    module_dict = module_obj.get_module_spider_json()

    if args.format == "json":
        json.dump(module_dict, sys.stdout, indent=4, sort_keys=True)
    else:
        text = """
    ID  |        Module Name                         |      ModuleFile Path
    ----|--------------------------------------------|----------------------------- """
        print (text)
        sorted_keys = sorted(module_dict.keys())
        count = 0
        for mod_name in sorted_keys:
            for mpath in module_dict[mod_name].keys():
                count+=1
                print ((str(count) + "\t |").expandtabs(4),
                       "\t" + (module_dict[mod_name][mpath]["full"] + "\t |").expandtabs(
                           40) + "\t" + module_dict[mod_name][mpath]["path"])


        print (f"Total Software Modules: {count}")
