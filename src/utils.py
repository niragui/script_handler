import psutil


def is_process_alive(pid: int):
    """
    Check if a given pid represents a working process

    Parameters:
        - pid: PID process to check
    """
    try:
        process = psutil.Process(pid)

        is_running = process.is_running()
        is_zombie = process.status() == psutil.STATUS_ZOMBIE

        return is_running and not is_zombie
    except psutil.NoSuchProcess:
        return False