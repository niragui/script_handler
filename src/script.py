import os

from time import time
import datetime

from typing import Optional, List

from .constants import DEFAULT_PYTHON_PATH
from .constants import NAME_FIELD, FILE_FIELD, PID_FIELD, ARG_FIELD
from .constants import DIRECTORY_FIELD, EXECUTE_FIELD, LOG_FIELD
from .constants import TIMEOUT_FIELD, LAST_DATE_FIELD
from .exceptions import InvalidDirectory, InvalidSavePath, ProcessException
from .utils import is_process_alive, kill_process, check_valid_pid

import subprocess

SEPARATED_PROCESS = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP


class Script():
    def __init__(self,
                 name: str,
                 file_path: str,
                 timeout: Optional[int] = None,
                 last_time: Optional[str] = None,
                 last_pid: Optional[int] = None,
                 operating_directory: Optional[str] = None,
                 executing_path: str = DEFAULT_PYTHON_PATH,
                 save_path: Optional[str] = None,
                 arguments: Optional[List[str]] = None):
        self.name = name

        if last_pid is not None:
            check_valid_pid(last_pid)
        self.last_pid = last_pid

        if timeout is None:
            self.timeout = None
        elif timeout == 0:
            self.timeout = None
        elif timeout < 0:
            raise ValueError(f"Timeout Value Must Be A Positive Integer or None. [{timeout}]")
        else:
            self.timeout = timeout

        if last_time is None:
            self.last_time = None
        else:
            try:
                self.last_time = datetime.datetime.fromisoformat(last_time)
            except ValueError:
                raise ValueError(f"Invalid Last Execution Date [{last_time}]")

        if operating_directory is None:
            operating_directory = os.getcwd()
        elif not isinstance(operating_directory, str):
            raise InvalidDirectory(f"{self.name} Operating Directory Must Be A String [{operating_directory}]")

        if not os.path.isdir(operating_directory):
            raise InvalidDirectory(f"{self.name} Must Have A Valid Operating Directory [{operating_directory}]")

        self.directory = operating_directory

        full_path = os.path.join(self.directory, file_path)

        if not os.path.isfile(full_path):
            raise ProcessException(f"File Path Must Be An Existing File [{full_path}]")

        self.file_path = file_path

        if not isinstance(executing_path, str):
            raise TypeError(f"Invalid Executing Path For {self.name} [{executing_path}]")

        self.executing_path = executing_path

        if save_path is None:
            logs_folder = os.path.join(operating_directory, "logs")
            os.makedirs(logs_folder, exist_ok=True)
            save_path = os.path.join(logs_folder, f"{name}.txt")
            print(save_path)

        save_filename = os.path.basename(save_path)
        save_filename = f"{time()}_{save_filename}"
        save_path = os.path.join(os.path.dirname(save_path), save_filename)

        if not isinstance(save_path, str):
            raise InvalidSavePath(f"Saving Path Must Be A str For {self.name} [{save_path}]")

        save_dir = os.path.dirname(save_path)
        if not os.path.isdir(save_dir):
            raise InvalidSavePath(f"Invalid Saving Path Directory For {self.name} [{save_path}]")

        self.save_path = save_path

        if arguments is None:
            arguments = []
        elif not isinstance(arguments, list):
            raise TypeError(f"Arguments Must Be A List [{type(arguments)}]")

        self.arguments = arguments

    def create_script_path(self):
        """
        Create the string to run the script
        """
        script_path = self.executing_path
        script_path += f" -u {self.file_path}"
        for argument in self.arguments:
            script_path += f" {argument}"

        return script_path

    def start_script(self):
        """
        Run the script and stores the last saved pid.
        """
        script_str = self.create_script_path()

        script_args = script_str.split(" ")

        save_path = open(self.save_path, "w")

        try:
            script_process = subprocess.Popen(script_args,
                                              stdout=save_path,
                                              stderr=save_path,
                                              creationflags=SEPARATED_PROCESS,
                                              cwd=self.directory)
        except Exception as e:
            raise ProcessException(f"Issue With Process [{e}]")

        self.last_pid = script_process.pid
        self.last_time = datetime.datetime.now()

    def is_running(self):
        """
        Returns a bool indicating if the process is
        being run right now
        """
        if self.last_pid is None:
            return False

        return is_process_alive(self.last_pid)

    def should_restart(self):
        """
        Returns a bool indicating if the process should
        be restarted in case it has a timeout
        """
        if self.timeout is None:
            return False

        if self.last_pid is None:
            return False

        current_time = datetime.datetime.now()

        if self.last_time is None:
            self.last_time = current_time
            return False

        gap = current_time - self.last_time
        if gap.total_seconds() >= self.timeout:
            return True

    def restart_process(self):
        """
        Restarts the current process
        """
        is_running = self.is_running()

        if is_running:
            kill_process(self.last_pid)

        self.start_script()

    def check_script_alive(self):
        """
        Check if the scripts are alive or if it should be restarted.
        If restart is needed, it'll invoke the process.
        """
        should_restart = self.should_restart()
        is_running = self.is_running()

        if is_running and not should_restart:
            return None

        if is_running and should_restart:
            kill_process(self.last_pid)

        self.start_script()

        return self.last_pid

    def create_dict(self):
        """
        Return the dictionary representing the script
        """
        script_dict = {}

        script_dict[NAME_FIELD] = self.name
        script_dict[FILE_FIELD] = self.file_path
        script_dict[PID_FIELD] = self.last_pid
        script_dict[DIRECTORY_FIELD] = self.directory
        script_dict[EXECUTE_FIELD] = self.executing_path
        script_dict[LOG_FIELD] = self.save_path
        script_dict[ARG_FIELD] = self.arguments
        script_dict[TIMEOUT_FIELD] = self.timeout
        script_dict[LAST_DATE_FIELD] = self.last_time

        return script_dict

    @classmethod
    def from_dict(cls,
                  script_dict: dict):
        """
        Create a Script instance given the information of it
        in a dictionary format

        Parameters:
            - script_dict: Dictionary with the script information
        """
        script_name = script_dict.get(NAME_FIELD, None)
        if script_name is None:
            raise KeyError(f"Script MUST provide a name")

        script_file = script_dict.get(FILE_FIELD, None)
        if script_file is None:
            raise KeyError(f"Script MUST provide a file path")

        script_pid = script_dict.get(PID_FIELD, None)
        script_directory = script_dict.get(DIRECTORY_FIELD, None)
        script_exec_path = script_dict.get(EXECUTE_FIELD, DEFAULT_PYTHON_PATH)
        script_save_path = script_dict.get(LOG_FIELD, None)
        script_arguments = script_dict.get(ARG_FIELD, None)
        script_timeout = script_dict.get(TIMEOUT_FIELD, None)
        script_last_time = script_dict.get(LAST_DATE_FIELD, None)

        return Script(script_name,
                      script_file,
                      script_timeout,
                      script_last_time,
                      script_pid,
                      script_directory,
                      script_exec_path,
                      script_save_path,
                      script_arguments,)
