import pytest
import os

from src.script import Script
from src.exceptions import ProcessException, InvalidDirectory

THIS_FOLDER = os.path.dirname(__file__)

VALID_DATE = "2025-01-01"
VALID_FILE = os.path.join(THIS_FOLDER, "file_test.py")

def test_invalid_file_path():
    with pytest.raises(ProcessException):
        script = Script("Test",
                        "test_file.py")


def test_invalid_timeout():
    with pytest.raises(ValueError):
        script = Script("Test",
                        VALID_FILE,
                        -1)


def test_invalid_last_time():
    invalid_date = "invalid"

    with pytest.raises(ValueError):
        script = Script("Test",
                        VALID_FILE,
                        None,
                        invalid_date)


def test_negative_pid():
    invalid_date = "invalid"

    with pytest.raises(ValueError):
        script = Script("Test",
                        VALID_FILE,
                        None,
                        VALID_DATE,
                        -1)


def test_non_int_pid():
    with pytest.raises(TypeError):
        script = Script("Test",
                        VALID_FILE,
                        None,
                        VALID_DATE,
                        "2")


def test_invalid_directory():
    with pytest.raises(InvalidDirectory):
        script = Script("Test",
                        VALID_FILE,
                        None,
                        VALID_DATE,
                        None,
                        "/invalid/directory")


def test_no_str_directory():
    with pytest.raises(InvalidDirectory):
        script = Script("Test",
                        VALID_FILE,
                        None,
                        VALID_DATE,
                        None,
                        1)



def test_invalid_exec_path():
    with pytest.raises(TypeError):
        script = Script("Test",
                        VALID_FILE,
                        None,
                        VALID_DATE,
                        None,
                        None,
                        3)

