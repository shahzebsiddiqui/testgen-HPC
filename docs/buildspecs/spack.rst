.. _spack_schema:

Spack Schema
=============

.. Note:: This feature is in active development.


buildtest can generate tests for the `spack <https://spack.readthedocs.io/en/latest/>`_ package manager which can be
used if you want to install or test packages as part of a repeatable process. You must set ``type: spack`` property
in buildspec to use the spack schema for validating the buildspec test. Currently, we have
`spack-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/spack-v1.0.schema.json>`_
JSON schema that defines the structure of how tests are to be written in buildspec. Shown below is the schema header. The
**required** properties are ``type``, ``executor`` and ``spack``.

.. code-block:: json

      "$id": "spack-v1.0.schema.json",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "spack schema version 1.0",
      "description": "The spack schema is referenced using ``type: spack`` which is used for generating tests using spack package manager",
      "type": "object",
      "required": [
        "type",
        "executor",
        "spack"
      ],

Install Specs
---------------

Let's start off with a simple example where we create a test that can ``spack install zlib``. Shown below
is a test named **install_zlib**. The **spack** keyword is a JSON object, in this test we define the root
of spack using the ``root`` keyword which informs buildtest where spack is located. buildtest will automatically
check the path and source the startup script. The ``install`` field is a JSON object that
contains a ``specs`` property which is a list of strings types that are name of spack packages to install. Each item in the
``specs`` property will be added as a separate ``spack install`` command.

The schema is designed to mimic spack commands which will be clear with more examples.

.. program-output:: cat ../tutorials/spack/install_zlib.yml

If you build this test and inspect the generated script, buildtest will source spack
startup script - **source $SPACK_ROOT/share/spack/setup-env.sh** based on the ``root`` property. In this example,
we have spack cloned in **$HOME/spack** which is **/Users/siddiq90/spack** and buildtest will find the
startup script which is in ``share/spack/setup-env.sh``.

.. code-block:: shell

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack install  zlib

Spack Environment
-----------------

buildtest can generate scripts to make use of `spack environments <https://spack.readthedocs.io/en/latest/environments.html>`_ which
can be useful if you want to install or test specs in an isolated environment.

Currently, we can create spack environment (``spack env create``) via name, directory and manifest file (``spack.yaml``, ``spack.lock``) and pass any
options to **spack env create** command. Furthermore, we can activate existing spack environment via name or directory using
``spack env activate`` and pass options to the command. buildtest can remove spack environments automatically before creating spack environment
or one can explicitly specify by name.

Activate Spack Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

In this next example, we will activate an existing environment ``m4`` and add spec for **m4** and concretize the spack environment.
The ``env`` is an object that mimics the ``spack env`` command. The ``activate`` field maps to ``spack env activate`` command.
The **name** property is of ``type: string`` which is name of spack environment you want to activate. The ``specs`` property in **env** section
maps to ``spack add <specs`` instead of ``spack install``.

The property ``concretize: true`` will run ``spack concretize`` command that is only available as part of the ``env`` object since this command
is only applicable in spack environments.

.. program-output:: cat ../tutorials/spack/concretize_m4.yml

If we build this test and inspect the generated test we see that spack will activate a spack environment **m4**, add specs in spack
environment via ``spack add m4`` and concretize the environment. The ``concretize`` is a boolean type, if its ``true`` we will run ``spack concretize -f``,
if its ``false`` this command will not be in script.

.. code-block:: shell

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env activate  m4
    spack add m4
    spack concretize -f

If we inspect the output file we see that m4 was concretized in the spack environment.

.. code-block:: shell

    ==> Package m4 was already added to m4
    ==> Concretized m4
    [+]  volmsbn  m4@1.4.19%apple-clang@11.0.3+sigsegv arch=darwin-bigsur-skylake
    [+]  bc6kuc4      ^libsigsegv@2.13%apple-clang@11.0.3 arch=darwin-bigsur-skylake

Create a Spack Environment by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this next example, we will create a spack environment named ``m4_zlib`` that will install
`m4` and `zlib` spec. The **create** field is a JSON object that maps to ``spack env create``
command which can pass some arguments in the form of key/value pairs. The ``name`` property
in **create** section is used to create a spack environment by name.

The ``compiler_find: true`` is a boolean that determines if we need to find compilers in spack via
``spack compiler find``. This can be useful if you need to find compilers so spack can install specs
with a preferred compiler otherwise spack may have issues concretizing or install specs.
buildtest will run **spack compiler find** after sourcing spack.

.. note::
    The ``compiler_find`` option may not be useful if your compilers are already defined in
    one of your configuration scopes or ``spack.yaml`` that is part of your spack environment.

The ``option`` field can pass any command line arguments to ``spack install`` command
and this field is available for other properties.

.. program-output:: cat ../tutorials/spack/env_install.yml

If we build this test and see generated test we see that buildtest will create a
spack environment `m4_zlib` and activate the environment, add **m4** and **zlib**,
concretize the environment and install the specs.

.. code-block:: shell
    :emphasize-lines: 4

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack compiler find
    spack env create  m4_zlib
    spack env activate  m4_zlib
    spack add m4
    spack add zlib
    spack concretize -f
    spack install --keep-prefix


Now let's examine the output of this test, shown below is the summary of this test, as you can
see we have successfully installed **m4** and **zlib** in a spack environment ``m4_zlib``.

.. code-block:: shell
    :emphasize-lines: 16-24

    ==> Found no new compilers
    ==> Compilers are defined in the following files:
        /Users/siddiq90/.spack/darwin/compilers.yaml
    ==> Updating view at /Users/siddiq90/spack/var/spack/environments/m4_zlib/.spack-env/view
    ==> Created environment 'm4_zlib' in /Users/siddiq90/spack/var/spack/environments/m4_zlib
    ==> You can activate this environment with:
    ==>   spack env activate m4_zlib
    ==> Adding m4 to environment m4_zlib
    ==> Adding zlib to environment m4_zlib
    ==> Concretized m4
    [+]  volmsbn  m4@1.4.19%apple-clang@11.0.3+sigsegv arch=darwin-bigsur-skylake
    [+]  bc6kuc4      ^libsigsegv@2.13%apple-clang@11.0.3 arch=darwin-bigsur-skylake
    ==> Concretized zlib
     -   2hw3hzd  zlib@1.2.11%apple-clang@11.0.3+optimize+pic+shared arch=darwin-bigsur-skylake
    ==> Updating view at /Users/siddiq90/spack/var/spack/environments/m4_zlib/.spack-env/view
    ==> Installing environment m4_zlib
    ==> Installing zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    ==> No binary for zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj found: installing from source
    ==> Fetching https://mirror.spack.io/_source-cache/archive/c3/c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1.tar.gz
    ==> No patches needed for zlib
    ==> zlib: Executing phase: 'install'
    ==> zlib: Successfully installed zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
      Fetch: 0.84s.  Build: 6.98s.  Total: 7.82s.
    [+] /Users/siddiq90/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    ==> Updating view at /Users/siddiq90/spack/var/spack/environments/m4_zlib/.spack-env/view

Creating Spack Environment from Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can create spack environment from a directory using the ``dir`` property that
is available as part of ``create`` and ``activate`` field. In this next example we
create a spack environment in our $HOME directory and concretize **m4** in the spack
environment

.. program-output:: cat ../tutorials/spack/env_create_directory.yml

When creating spack environment using directory, buildtest will automatically add the
``-d`` option which is required when creating spack environments. However, one can also pass
this using the ``option`` field. Shown below is the generated script for the above test.

.. code-block:: shell
    :emphasize-lines: 3-4

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env create  -d /Users/siddiq90/spack-envs/m4
    spack env activate  -d /Users/siddiq90/spack-envs/m4
    spack add m4
    spack concretize -f

buildtest will create environment first followed by activating the spack environment.

Create Spack Environment from Manifest File (spack.yaml, spack.lock)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack can create environments from `spack.yaml` or `spack.lock` which can be used if you
have a spack configuration that works for your system and want to write a buildspec. While creating a spack environment,
you can use the ``manifest`` property to specify path to your ``spack.yaml`` or ``spack.lock``.

.. note::
    buildtest will not enforce that manifest names be **spack.yaml** or **spack.lock** since spack allows
    one to create spack environment from arbitrary name so long as it is a valid spack configuration.

Shown below is an example buildspec that generates a test from a manifest file. The ``manifest`` property
is of ``type: string`` and this is only available as part of ``create`` property.

.. program-output:: cat ../tutorials/spack/env_create_manifest.yml

If we build this test and inspect the generated script we see ``spack env create`` command
will create an environment **manifest_example** using the manifest file that we provided.

.. code-block:: shell
    :emphasize-lines: 3

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env create  manifest_example /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/spack/example/spack.yaml
    spack env activate  manifest_example
    spack concretize -f

Removing Spack Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can remove spack environments which can be used if you are periodically running the same test where one is
creating the same environment. buildtest can automatically remove spack environment using the property ``remove_environment``
which will remove the environment before creating it with same name. This field is part of the ``create`` field and only works if
one is creating spack environments by name.

Alternately, buildtest provides the ``rm`` field which can be used for removing environment explicitly. In the ``rm``
field, the ``name`` is a required field which is the name of the spack environment to remove. The ``name`` field is of ``type: string``
Shown below are two example tests where we remove spack environment using the **remove_environment** and **rm** field.


.. program-output:: cat ../tutorials/spack/remove_environment_example.yml

If we look at the generated test, we notice that spack will remove environments names: **remove_environment**, **dummy**.

.. code-block:: shell
    :emphasize-lines: 3

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env rm -y remove_environment
    spack env create  remove_environment
    spack env activate  remove_environment
    spack add bzip2
    spack concretize -f

.. code-block:: shell
    :emphasize-lines: 3

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env rm -y dummy
    spack env create  dummy
    spack env activate  dummy
    spack add bzip2
    spack concretize -f

Pre and Post Commands
----------------------

The spack schema supports ability to write arbitrary shell script content using the ``pre_cmds`` and ``post_cmds``
field that are of ``type: string`` and buildtest will insert the content into the test exactly as it is defined by
these two fields.

In this next example, we will test an installation of `zlib` by cloning spack from upstream and use ``pre_cmds`` field
to specify where we will clone spack. In this example, we will clone spack under **/tmp**. Since we don't have a valid
root of spack since test hasn't been run, we can ignore check for spack paths by specifying ``verify_spack: false`` which
informs buildtest to skip spack path check. Generally, buildtest will raise an exception if path specified by ``root`` is
invalid and if ``$SPACK_ROOT/share/spack/setup-env.sh`` doesn't exist since this is the file that must be sourced.

The ``pre_cmds`` are shell commands that are run before sourcing spack, whereas the ``post_cmds`` are run at the very
end of the script. In the `post_cmds`, we will ``spack find`` that will be run after ``spack install``.
We remove spack root (``$SPACK_ROOT``) so that this test can be rerun again.

.. program-output:: cat ../tutorials/spack/pre_post_cmds.yml

If we build this test and inspect the generated script we see the following

.. code-block:: shell
    :emphasize-lines: 4-8,15-18

    #!/bin/bash


    ######## START OF PRE COMMANDS ########
    cd /tmp
    git clone https://github.com/spack/spack

    ######## END OF PRE COMMANDS   ########


    source /private/tmp/spack/share/spack/setup-env.sh
    spack install  zlib


    ######## START OF POST COMMANDS ########
    spack find
    rm -rf $SPACK_ROOT
    ######## END OF POST COMMANDS   ########

If we inspect the output, we see that `zlib` is installed as shown in output from ``spack find``

.. code-block:: shell
    :emphasize-lines: 9-10

    ==> Installing zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    ==> No binary for zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj found: installing from source
    ==> Fetching https://mirror.spack.io/_source-cache/archive/c3/c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1.tar.gz
    ==> No patches needed for zlib
    ==> zlib: Executing phase: 'install'
    ==> zlib: Successfully installed zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
      Fetch: 0.50s.  Build: 5.90s.  Total: 6.40s.
    [+] /private/tmp/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/zlib-1.2.11-2hw3hzdfy7e2ndzojgqoq472m5flsloj
    -- darwin-bigsur-skylake / apple-clang@11.0.3 -------------------
    zlib@1.2.11

Specifying Scheduler Directives
---------------------------------

The spack schema supports all of the :ref:`scheduler scheduler directives <batch_support>` such
as ``sbatch``, ``bsub``, ``pbs``, ``cobalt``, and ``batch`` property in the buildspec.

The directives are applied at top of script. Shown below is a toy example that will define
directives using **sbatch** and **batch** property. Note, this test won't submit job to scheduler
since we are not using the a slurm executor.

.. program-output:: cat ../tutorials/spack/spack_sbatch.yml

buildtest will generate the shell script with the job directives and set the name, output and error
files based on name of test. If we build this test, and inspect the generated test we see that
**#SBATCH** directives are written based on the **sbatch** and **batch** field.

.. code-block:: shell
    :emphasize-lines: 3-10

    #!/bin/bash

    ####### START OF SCHEDULER DIRECTIVES #######
    #SBATCH -N 1
    #SBATCH --ntasks=8
    #SBATCH --time=30
    #SBATCH --job-name=spack_sbatch_example
    #SBATCH --output=spack_sbatch_example.out
    #SBATCH --error=spack_sbatch_example.err
    ####### END OF SCHEDULER DIRECTIVES   #######


    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env activate  m4
    spack add m4
    spack concretize -f

Configuring Spack Mirrors
--------------------------

We can add `mirrors <https://spack.readthedocs.io/en/latest/mirrors.html>`_ in the
spack instance or spack environment using the ``mirror`` property which is available
in the ``spack`` and ``env`` section. If the ``mirrror`` property is part of the ``env`` section, the
mirror will be added to spack environment. The ``mirror`` is an object that expects a Key/Value pair where
the key is the name of mirror and value is location of the spack mirror.

In this next example,  we will define a mirror name **e4s** that points to https://cache.e4s.io as the mirror location.
Internally, this translates to ``spack mirror add e4s https://cache.e4s.io`` command.

.. program-output:: cat ../tutorials/spack/mirror_example.yml


If we look at the generated script for both tests, we see that mirror is added for both tests. Note that
one can have mirrors defined in their ``spack.yaml`` or one of the `configuration scopes <https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes>`_
defined by spack.

.. code-block:: shell
    :emphasize-lines: 3

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack mirror add e4s https://cache.e4s.io


    ######## START OF POST COMMANDS ########
    spack mirror list
    ######## END OF POST COMMANDS   ########

.. code-block:: shell
    :emphasize-lines: 5

    #!/bin/bash
    source /Users/siddiq90/spack/share/spack/setup-env.sh
    spack env create  spack_mirror
    spack env activate  spack_mirror
    spack mirror add e4s https://cache.e4s.io


    ######## START OF POST COMMANDS ########
    spack mirror list
    ######## END OF POST COMMANDS   ########

Spack Test
-----------

buildtest can run tests using ``spack test run`` that can be used for testing installed specs with
tests provided by spack. In order to run tests, you need to declare the ``test`` section
which is of ``type: object`` in JSON and ``run`` is a required property. The ``run`` section maps to ``spack test run``
that is responsible for running tests for a list of specs that are specified using the ``specs`` property.

Upon running the tests, we can retrieve results using ``spack test results`` which is configured using the ``results``
property. The **results** property expects one to specify the ``specs`` or ``suite`` or both in order to retrieve results.

The ``suite`` property is used to retrieve test results based on suite name, whereas ``specs`` property can be used to retrieve based
on spec format. Both properties are a list of string types.

In example below we install `bzip2` and run the test using ``spack test run bzip2``.

.. program-output:: cat ../tutorials/spack/spack_test.yml

If we look at the generated test, buildtest will automatically set ``--alias`` option to define name
of suite, otherwise spack will generate a random text for suitename which you won't know at time
of writing test that is required by ``spack test results`` to fetch the results.

.. code-block:: shell
    :emphasize-lines: 13-14

    #!/bin/bash


    ######## START OF PRE COMMANDS ########
    cd /tmp
    git clone https://github.com/spack/spack spack

    ######## END OF PRE COMMANDS   ########


    source /private/tmp/spack-test-no-env/share/spack/setup-env.sh
    spack install  bzip2
    spack test run  --alias bzip2 bzip2
    spack test results  bzip2


    ######## START OF POST COMMANDS ########
    spack find
    rm -rf $SPACK_ROOT
    ######## END OF POST COMMANDS   ########


Shown below is the example output of this test.


.. code-block:: shell
    :emphasize-lines: 26-29

    ==> libiconv: Executing phase: 'configure'
    ==> libiconv: Executing phase: 'build'
    ==> libiconv: Executing phase: 'install'
    ==> libiconv: Successfully installed libiconv-1.16-xgemfyqy3gsdz3lk7wy3ejudfaksja4x
      Fetch: 1.54s.  Build: 33.03s.  Total: 34.57s.
    [+] /private/tmp/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/libiconv-1.16-xgemfyqy3gsdz3lk7wy3ejudfaksja4x
    ==> Installing diffutils-3.7-3dfrh6li733xxcenwyjhwyta7xkh3udq
    ==> No binary for diffutils-3.7-3dfrh6li733xxcenwyjhwyta7xkh3udq found: installing from source
    ==> Fetching https://mirror.spack.io/_source-cache/archive/b3/b3a7a6221c3dc916085f0d205abf6b8e1ba443d4dd965118da364a1dc1cb3a26.tar.xz
    ==> No patches needed for diffutils
    ==> diffutils: Executing phase: 'autoreconf'
    ==> diffutils: Executing phase: 'configure'
    ==> diffutils: Executing phase: 'build'
    ==> diffutils: Executing phase: 'install'
    ==> diffutils: Successfully installed diffutils-3.7-3dfrh6li733xxcenwyjhwyta7xkh3udq
      Fetch: 1.32s.  Build: 52.35s.  Total: 53.67s.
    [+] /private/tmp/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/diffutils-3.7-3dfrh6li733xxcenwyjhwyta7xkh3udq
    ==> Installing bzip2-1.0.8-avjwvsoaivuflugopwk4ap7rffhejxzu
    ==> No binary for bzip2-1.0.8-avjwvsoaivuflugopwk4ap7rffhejxzu found: installing from source
    ==> Fetching https://mirror.spack.io/_source-cache/archive/ab/ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269.tar.gz
    ==> Ran patch() for bzip2
    ==> bzip2: Executing phase: 'install'
    ==> bzip2: Successfully installed bzip2-1.0.8-avjwvsoaivuflugopwk4ap7rffhejxzu
      Fetch: 1.42s.  Build: 1.84s.  Total: 3.26s.
    [+] /private/tmp/spack/opt/spack/darwin-bigsur-skylake/apple-clang-11.0.3/bzip2-1.0.8-avjwvsoaivuflugopwk4ap7rffhejxzu
    ==> Spack test bzip2
    ==> Testing package bzip2-1.0.8-avjwvso
    ==> Results for test suite 'bzip2':
    ==>   bzip2-1.0.8-avjwvso PASSED
    -- darwin-bigsur-skylake / apple-clang@11.0.3 -------------------
    bzip2@1.0.8
    diffutils@3.7
    libiconv@1.16


We can search for test results using the spec format instead of suite name. In the ``results`` property we can
use ``specs`` field instead of ``suite`` property to specify a list of spec names to run. In spack, you can retrieve
the results using ``spack test results -- <spec>``, note that double dash ``--`` is in front of spec name. We can
pass options to ``spack test results`` using the **option** property which is available for ``results`` and
``run`` property. Currently, spack will write test results in ``$HOME/.spack/tests`` and we can use ``spack test remove``
to clear all test results. This can be done in buildspec using the ``remove_tests`` field which
is a boolean. If this is set to **True** buildtest will run ``spack test remove -y`` to remove all test suites before running
the tests.

.. program-output:: cat ../tutorials/spack/spack_test_specs.yml

In the generated test, we see that buildtest will remove all testsuites using ``spack test remove -y``
and query results based on spec format. The options are passed into ``spack test results`` based on
the ``option`` field specified under the ``results`` section.


.. code-block:: shell
    :emphasize-lines: 13-15

    #!/bin/bash


    ######## START OF PRE COMMANDS ########
    cd /tmp
    git clone https://github.com/spack/spack

    ######## END OF PRE COMMANDS   ########


    source /private/tmp/spack/share/spack/setup-env.sh
    spack install  bzip2
    spack test remove -y
    spack test run  --alias bzip2 bzip2
    spack test results -l -- bzip2


    ######## START OF POST COMMANDS ########
    spack find
    rm -rf $SPACK_ROOT
    ######## END OF POST COMMANDS   ########
