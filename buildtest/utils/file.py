"""
This module provides some generic file and directory level operation that
include the following:
1. Check if File and Directory exist
2. Create File and Directory
3. Check if string is in file
4. Walk a directory tree based on single and multiple extension
5. Strip Hidden file character
"""

import os
import logging

logger = logging.getLogger(__name__)


def is_file(fname):
    """This method will check if file exist and if not found throws an exception.

    :param file: file path
    :type file: str, required

    :return: returns True if file exists otherwise terminates with an exception
    :rtype: bool
    """

    # resolve_path will return the full canonical filename or return None if file doesn't exist
    fname = resolve_path(fname)

    # if return is None we return False since file is non-existent
    if not fname:
        return False

    # at this stage we know it's a valid file but we don't know if its a file or directory
    if os.path.isfile(fname):
        return True

    return False


def is_dir(dirname):
    """This method will check if a directory exist and if not found throws an exception.

       Parameters:

       :param dir: directory path
       :type dir: str, required

       :return: returns ``True`` if directory exists otherwise returns ``False``
       :rtype: bool
    """

    # resolve_path will return the full canonical directory name or return None if directory doesn't exist
    dirname = resolve_path(dirname)

    # if return is None we stop here and return False since directory is non-existent.
    if not dirname:
        return False

    # at this stage we know it's a valid file but we don't know if its a file or directory
    if os.path.isdir(dirname):
        return True

    return False


def walk_tree(root_dir, ext):
    """This method will traverse a directory tree and return list of files
       based on extension type. This method invokes is_dir() to check if directory
       exists before traversal.

       Parameters:

       :param root_dir: directory path to traverse
       :type root_dir: str, required
       :param ext: file extensions to search in traversal
       :type ext: str, required

       :return: returns a list of file paths
       :rtype: list
    """

    list_files = []
    # if directory doesn't exist let's return empty list before doing a directory traversal since no files to traverse
    if not is_dir(root_dir):
        return list_files

    for root, subdir, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith(ext):
                list_files.append(os.path.join(root, fname))

    return list_files


def create_dir(dirname):
    """Create directory if it doesn't exist. Runs a "try" block
       to run os.makedirs() which creates all sub-directories if they
       dont exist. Catches exception of type OSError and prints message

       Parameters:

       :param dirname: directory path to create
       :type dirname: string, required

       :return: creates the directory or print an exception message upon failure
       :rtype: Catches exception of type OSError
    """

    # these three lines implement same as ``resolve_path`` will return None when it's not a known file. We expect
    # input to create_dir will be a non-existent path so we run these lines manually
    dirname = os.path.expanduser(dirname)
    dirname = os.path.expandvars(dirname)
    dirname = os.path.realpath(dirname)

    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
            logger.debug("Creating Directory: %s", dirname)
        except OSError as err:
            print(err)
            raise


def resolve_path(path):
    """This method will resolve a file path to account for shell expansion and resolve paths in
       when a symlink is provided in the file. This method assumes file already exists.

       Parameters:

       :param path: file path to resolve
       :type path: str, required
       :return: return realpath to file if found otherwise return None
       :rtype: str or None
    """

    # apply shell expansion  when file includes something like $HOME/example
    path = os.path.expandvars(path)
    # apply user expansion when file includes something like  ~/example
    path = os.path.expanduser(path)

    real_path = os.path.realpath(path)

    if os.path.exists(real_path):
        return real_path

def read_file(filepath):
    """ This method provides capability to read a file.

        Parameters:

        :param filepath: file name to read
        :type filepath: str, required
        :return: return content of file
        :rtype: list
    """

    # type check filepath to ensure its a string, if not return None
    if not isinstance(filepath,str):
        return None

    # resolve_path will handle shell and user expansion and account for any symlinks and check for file existence.
    # if resolve_path does not return gracefully it implies file does not exist and will return None
    filepath = resolve_path(filepath)

    # if it's invalid file let's return None
    if not filepath:
        return None

    content = []
    fd = open(filepath, "r")

    while True:

        line = fd.readline()
        if line:
            content.append(line)
        else:
            break

    return content

def write_file(filepath, content):
    """ This method provides capability to write a file.

        Parameters:

        :param filepath: file name to write
        :type filepath: str, required
        :param content: content to write to file
        :type content: list, required
        :return: return content of file
        :rtype: list
    """

    # type check filepath to ensure its a string, if not return None
    if not isinstance(filepath,str):
        return None

    # if content was passed as a string, let's convert to list
    if isinstance(content, str):
        content = content.splitlines(True)

    # shown below is equivalent to running 'resolve_path' but we can't invoke it since we expect this method
    # to write to a new file. resolve_path assumes filepath already exists and returns realpath otherwise returns
    # None.
    filepath = os.path.expanduser(filepath)
    filepath = os.path.expandvars(filepath)
    filepath = os.path.realpath(filepath)

    # if filepath is an actual file, let's not write to file and return None.
    # also if filepath is a directory let's also return None
    if is_file(filepath) or is_dir(filepath):
        return None
    
    fd = open(filepath, "w")
    # process each line and write to file
    for line in content:
        if line:
            fd.writelines(line)

    fd.close()