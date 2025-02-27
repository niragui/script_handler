from src.script_handler import ScriptHandler

import traceback
import os

THIS_FOLDER = os.path.dirname(__file__)
LOG_FILE = os.path.join(THIS_FOLDER, "log.txt")


if __name__ == "__main__":
    try:
        scripts_file = os.path.join(THIS_FOLDER, "scripts.json")
        handler = ScriptHandler(scripts_file)
        handler.check_scripts()
    except:
        error = traceback.format_exc()
        with open(LOG_FILE, "w") as f:
            f.write(error)