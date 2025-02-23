import pytest
import subprocess

from time import sleep

from src.utils import is_process_alive, check_valid_pid

import os


def test_current_process():
    """
    Test that the is_process_alive function
    returns True with the current process
    """
    assert is_process_alive(os.getpid())


def test_invalid_pid_type():
    """
    Test that the is_process_alive function
    raises an Execption When Not an int
    """

    with pytest.raises(TypeError):
        check_valid_pid("10")

    with pytest.raises(TypeError):
        check_valid_pid(12.0)


def test_invalid_pid_value():
    """
    Test that the check_valid_pid function
    raises an Exception when negative or 0
    """

    with pytest.raises(ValueError):
        check_valid_pid(-10)

    with pytest.raises(ValueError):
        check_valid_pid(0)


def test_dead_pid():
    """
    Test that the is_process_alive function
    returns True with the current process
    """
    process = subprocess.Popen(['echo', "Test"], shell=True)
    pid = process.pid

    assert is_process_alive(pid)

    process.wait()
    sleep(0.1)

    assert not is_process_alive(pid)
