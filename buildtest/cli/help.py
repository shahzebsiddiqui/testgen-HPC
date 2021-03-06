def buildtest_help():
    """Entry point for ``buildtest help`` which display a summary of how to use buildtest commands"""

    print(
        """

Building Buildspecs
--------------------

Command                                                     Description

buildtest build -b <file>                                   Build a single buildspec file
buildtest build -b <dir>                                    Build all buildspecs recursively in a given directory
buildtest build -b <file> -b <dir>                          Build buildspecs by file and directory
buildtest build -b <file> -b <dir> -x <file> -x <dir>       Exclude files and directory when building buildspecs
buildtest build -t pass  -t python                          Build buildspecs by tagname 'pass' and 'python'
buildtest build -e <executor1> -e <executor2>               Building buildspecs by executor
buildtest build -b <file> -t <tagname1> -e <executor1>      Building buildspecs with file, directory, tags, and executors
buildtest build -t <tagname1> -ft <filter-tagname1>         Filter tests by tagname
buildtest -c config.yml build -b <file>                     Use buildtest configuration file 'config.yml' 
buildtest build -b <file> --rebuild 5                       Rebuild a test 5 times
buildtest build -b <file> --testdir /tmp                    Write tests in /tmp


View Test Report 
----------------

Command                                                     Description

buildtest report                                            Display all tests results
buildtest report --filter returncode=0                      Filter test results by returncode=0
buildtest report --filter state=PASS,tags=python            Filter test by multiple filter fields.
buildtest report --format name,state,buildspec              Format report table by field 'name', 'state', 'buildspec'
buildtest report --helpfilter                               List all filter fields
buildtest report --helpformat                               List all format fields
buildtest report --oldest                                   Retrieve oldest record for all tests 
buildtest report --latest                                   Retrieve latest record for all tests 
buildtest report -r <report-file>                           Specify alternate report file to display test results
buildtest report list                                       List all report files
buildtest report clear                                      Remove content of report file

Inspecting a Test
------------------

Command                                                     Description

buildtest inspect name hello                                Display all tests results
buildtest inspect name foo bar                              Display record of test name 'foo' and 'bar'
buildtest inspect list                                      Display all test names and ids
buildtest inspect id <ID>                                   Display record of test by unique identifer
buildtest query -o hello                                    Display content of output file for test name 'hello'
buildtest query -e hello                                    Display content of error file for test name 'hello'
buildtest query -d -o -e first hello foo  bar               Display first record of tests 'hello', 'foo', 'bar' and show output and error file 

    
Finding Buildspecs
----------------------

Command                                                     Description

buildtest buildspec find                                    Discover and validate all buildspecs and load all validated buildspecs in cache
buildtest buildspec find --rebuild                          Rebuild cache file
buildtest buildspec find --root /tmp --rebuild              Discover buildspecs in /tmp and rebuild buildspec cache
buildtest buildspec find --paths                            Print all root directories for buildspecs
buildtest buildspec find --buildspec                        List all available buildspecs from cache
buildtest buildspec find --tags                             List all unique tags from cache
buildtest buildspec find --executors                        List all unique executors from cache
buildtest buildspec find --maintainers                      List all maintainers from cache
buildtest buildspec find --maintainers-by-buildspecs        Show breakdown of all buildspecs by maintainer names.
buildtest buildspec find --filter type=script,tags=pass     Filter buildspec cache based on type=script and  tags='pass'
buildtest buildspec find --filter buildspec=<path>          Filter cache by buildspec file    
buildtest buildspec find --format name,description          Format table columns by field: 'name' and 'description 
buildtest buildspec find --group-by-tags                    Group tests by tag name
buildtest buildspec find --group-by-executor                Group tests by executor name            
buildtest buildspec find --helpfilter                       Show all filter fields
buildtest buildspec find --helpformat                       Show all format fields
buildtest buildspec find --terse -t                         Display output in machine readable format
    
Validate buildspecs
---------------------
    
Command                                                     Description

buildtest buildspec validate -b <file>                      Validate a buildspec with JSON Schema 
buildtest buildspec validate -b /tmp/ -x /tmp/network       Validate all buildspecs in directory /tmp but exclude /tmp/network
buildtest buildspec validate -t python -t mac               Validate all buildspecs for tagname 'python' and 'mac'
buildtest buildspec validate -e generic.local.bash          Validate all buildspecs for executor 'generic.local.bash'
   
Build History
---------------
    

Command                                                     Description

buildtest history list                                      List all build history files 
buildtest history query 0                                   Query content of history build identifier '0' 
buildtest history query 0 --log                             Open logfile for build identifier '0'

Buildtest Configuration 
------------------------

Command                                                     Description

buildtest config view                                       View content of configuration file
buildtest config validate                                   Validate configuration file with JSON schema
buildtest config executors                                  List all executors from configuration file
buildtest config systems                                    List all available system entries in configuration file
buildtest -c /tmp/config.yml config validate                Validate configuration file /tmp/config.yml

CDASH Support
---------------------

Command                                                     Description

buildtest cdash upload DEMO                                 Upload all tests to cdash with build name 'DEMO' 
buildtest cdash upload 'DAILY_CHECK' --report result.json   Upload all tests from report file result.json with build name 'DAILY_CHECK'
buildtest cdash upload --site laptop DEMO                   Upload tests to CDASH with site named called 'laptop' 
buildtest cdash upload -r /tmp/nightly.json nightly         Upload tests from /tmp/nightly.json to CDASH with buildname 'nightly'
buildtest cdash view                                        Open CDASH project in web-browser
buildtest cdash view --url <url>                            Open CDASH project in web-browser with a specified url

"""
    )
