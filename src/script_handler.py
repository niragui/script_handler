from typing import List

import datetime

import os

import json

from .exceptions import MissingScriptsFile, InvalidScriptsFile
from .script import Script
from .constants import PID_FIELD, ACTIVE_FIELD, LAST_DATE_FIELD

import sys

IMPORT_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
sys.path.append(IMPORT_PATH)


from Publisher.publisher import Publisher


class ScriptHandler():
    def __init__(self,
                 scripts_path: str) -> None:
        self.scripts_path = scripts_path
        self.scripts_dicts = []
        self.scripts: List[Script] = []

        self.read_scripts()

    def read_scripts(self):
        """
        Read the scripts json file and set the scripts list
        with the data
        """
        if not os.path.isfile(self.scripts_path):
            raise MissingScriptsFile(f"Must Have A Valid Scripts File Path [{self.scripts_path}]")

        try:
            with open(self.scripts_path, "r", encoding="utf-8") as f:
                self.scripts_dicts = json.load(f)
        except json.JSONDecodeError:
            raise InvalidScriptsFile(f"Scripts File Not A Valid JSON")

        if not isinstance(self.scripts_dicts, list):
            raise InvalidScriptsFile(f"Scripts File Must Be A JSON List [{type(self.scripts_dicts)}]")

        self.scripts = []

        for script_data in self.scripts_dicts:
            active = script_data.get(ACTIVE_FIELD, True)
            script = Script.from_dict(script_data)
            self.scripts.append((script, active))

    def update_scripts_dict(self):
        """
        Stored the update scripts dict in the script save path
        """
        with open(self.scripts_path, "w") as f:
            f.write(json.dumps(self.scripts_dicts, indent=4))

    def check_scripts(self):
        """
        Check if all the scripts are running. In case some it's not,
        it restarts it.
        """
        processes_updated = False
        processes_text = ""

        for i, (script, active) in enumerate(self.scripts):
            if not active:
                continue
            new_pid = script.check_script_alive()
            if new_pid is not None:
                processes_updated = True
                processes_text += f"{script.name} Has Been Restarted\n"
                self.scripts_dicts[i][PID_FIELD] = new_pid
                if script.last_time is not None:
                    self.scripts_dicts[i][LAST_DATE_FIELD] = script.last_time.isoformat()
                self.update_scripts_dict()

        print(processes_text)

        if processes_updated:
            now = datetime.datetime.now()

            topic = "Script Handler"
            subject = f"Scripts Changes [{now}]"

            publisher = Publisher(topic, subject, processes_text)
            print(vars(publisher))
            publisher.publish()
        else:
            print("Nothing Happened")
