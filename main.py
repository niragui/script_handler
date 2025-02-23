from src.script_handler import ScriptHandler


if __name__ == "__main__":
    handler = ScriptHandler("scripts.json")
    handler.check_scripts()