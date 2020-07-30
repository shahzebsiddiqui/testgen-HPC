import os
from buildtest.defaults import BUILDTEST_SETTINGS_FILE
from buildtest.config import (
    load_settings,
    check_settings,
    get_default_settings,
    init,
)
from buildtest.utils.file import is_file, is_dir


def test_load_and_check_settings():

    init(BUILDTEST_SETTINGS_FILE)
    print(f"Checking if file: {BUILDTEST_SETTINGS_FILE} is valid")
    assert is_file(BUILDTEST_SETTINGS_FILE)

    recipe = load_settings(BUILDTEST_SETTINGS_FILE)
    assert isinstance(recipe, dict)

    check_settings(executor_check=False)


def test_get_default_settings():

    loaded_settings = get_default_settings()
    assert isinstance(loaded_settings, dict)

    assert "config" in loaded_settings.keys()
    assert "executors" in loaded_settings.keys()


def test_init_creation_of_buildtest_dir(tmp_path):

    settings = os.path.join(tmp_path, "config.yml")
    init(settings)
    print(f"Checking buildtest settings file: {settings}")
    print(f"Checking if 'site' sub-directory: {os.path.join(tmp_path,'site')} exists")
    assert is_file(settings)
    assert is_dir(os.path.join(tmp_path, "site"))
