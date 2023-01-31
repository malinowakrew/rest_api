class Error(Exception):
    pass


class RecordNotExist(Error):
    def __init__(self, message="Record doesn't exist") -> None:
        self.message = message
        super().__init__(self.message)
