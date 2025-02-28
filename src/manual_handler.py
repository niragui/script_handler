import json
import os

from .script import Script
from .utils import kill_process

from .exceptions import InvalidScriptsFile
from .constants import NAME_FIELD, ACTIVE_FIELD, PID_FIELD, LAST_DATE_FIELD

THIS_FOLDER = os.path.dirname(__file__)
SCRIPTS_FILE_NAME = "scripts.json"
SCRIPTS_FILE = os.path.join(THIS_FOLDER, os.pardir, SCRIPTS_FILE_NAME)


def read_scripts(scripts_file: str = SCRIPTS_FILE):
    """
    Given a scripts file, it returns the list of the scripts

    Parameters:
        - scripts_file: Path where the scripts are saved
    """
    if not os.path.isfile(scripts_file):
        raise InvalidScriptsFile(f"The Given Script File Doesn't Exist [{scripts_file}]")

    try:
        with open(scripts_file, "r") as f:
            scripts = json.load(f)
    except json.JSONDecodeError:
        raise InvalidScriptsFile(f"The Given Script File Doesn't Have A Valid Json Format [{scripts_file}]")

    return scripts


def list_scripts(scripts_file: str = SCRIPTS_FILE):
    """
    Given a scripts file, it returns a list of the saved scripts

    Parameters:
        - scripts_file: Path where the scripts are saved
    """
    scripts = read_scripts(scripts_file)

    script_list = []

    for script in scripts:
        script_name = script[NAME_FIELD]
        script_active = script[ACTIVE_FIELD]

        new_script = {}
        new_script[NAME_FIELD] = script_name
        new_script[ACTIVE_FIELD] = script_active

        script_list.append(new_script)

    return script_list


def restart_script(name: str,
                   scripts_file: str = SCRIPTS_FILE):
    """
    Given a script, it stops its process and restarts it.

    Parameters:
        - name: Name of the script to stop
        - scripts_file: Path where the scripts are saved
    """
    scripts = read_scripts(scripts_file)

    script_found = False
    changed_scripts = []

    for i, script in enumerate(scripts):
        script_name = script[NAME_FIELD]

        if script_name == name:
            script_found = True
            script_item = Script.from_dict(script)

            script_item.restart_process()

            script[PID_FIELD] = script_item.last_pid
            script[LAST_DATE_FIELD] = script_item.last_time

        changed_scripts.append(script)

    if not script_found:
        raise KeyError(f"Script Name Not Found [{name}]")

    with open(scripts_file, "w") as f:
        f.write(json.dumps(changed_scripts, indent=4))


def deactivate_script(name: str,
                      scripts_file: str = SCRIPTS_FILE):
    """
    Given a script, it stops its process and restarts it.

    Parameters:
        - name: Name of the script to stop
        - scripts_file: Path where the scripts are saved
    """
    scripts = read_scripts(scripts_file)

    script_found = False
    changed_scripts = []

    for i, script in enumerate(scripts):
        script_name = script[NAME_FIELD]

        if script_name == name:
            script_found = True
            script_item = Script.from_dict(script)

            if script_item.is_running():
                kill_process(script_item.last_pid)

            script[PID_FIELD] = None
            script[LAST_DATE_FIELD] = None
            script[ACTIVE_FIELD] = False

        changed_scripts.append(script)

    if not script_found:
        raise KeyError(f"Script Name Not Found [{name}]")

    with open(scripts_file, "w") as f:
        f.write(json.dumps(changed_scripts, indent=4))


def activate_script(name: str,
                    scripts_file: str = SCRIPTS_FILE):
    """
    Given a script, it sets it as active.

    Parameters:
        - name: Name of the script to stop
        - scripts_file: Path where the scripts are saved
    """
    scripts = read_scripts(scripts_file)

    script_found = False
    changed_scripts = []

    for i, script in enumerate(scripts):
        script_name = script[NAME_FIELD]

        if script_name == name:
            script_found = True
            script[ACTIVE_FIELD] = True

        changed_scripts.append(script)

    if not script_found:
        raise KeyError(f"Script Name Not Found [{name}]")

    with open(scripts_file, "w") as f:
        f.write(json.dumps(changed_scripts, indent=4))