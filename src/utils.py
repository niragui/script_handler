import psutil

import os
import signal

from .exceptions import ProcessException


def check_valid_pid(pid: int):
    """
    Raise an Exception In Case The PID provided is not valid

    Parameters:
        - pid: PID number to check
    """
    if not isinstance(pid, int):
        raise TypeError(f"Pid Must Be An Int [{type(pid)}]")

    if pid <= 0:
        raise ValueError(f"Pid Mst Be A Positive Integer")


def is_process_alive(pid: int):
    """
    Check if a given pid represents a working process

    Parameters:
        - pid: PID process to check
    """
    check_valid_pid(pid)

    try:
        process = psutil.Process(pid)

        is_running = process.is_running()
        is_zombie = process.status() == psutil.STATUS_ZOMBIE

        return is_running and not is_zombie
    except psutil.NoSuchProcess:
        return False


def kill_process(pid: int):
    """
    Given a PID, it stops the given process
    """
    check_valid_pid(pid)

    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        raise ProcessException(f"Could Not Finish Process [{pid}]")