
class MissingScriptsFile(OSError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidScriptsFile(TypeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidDirectory(OSError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidSavePath(OSError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)