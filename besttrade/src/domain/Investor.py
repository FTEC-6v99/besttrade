import typing as t


class Investor():
    def __init__(self, username: str = None, status: int = 1, id: int = -1):
        self.id = id
        self.username = username
        self.status = status

    def __str__(self):
        return f'(id: {self.id}, username: {self.username}, status: {self.status})'
