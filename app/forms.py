from fastapi import Request
from typing import List


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: str = ""
        self.password: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Valid Email is mandatory")
        if not self.password or not len(self.password) >= 1:
            self.errors.append("Password needs to be > 6 chars")

        if not self.errors:
            return True
        return False


class CreatePost:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: str = ""
        self.content: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("email")
        self.content = form.get("password")

    async def is_valid(self):
        if not self.title:
            self.errors.append("Your Post doesn't have title.")
        if not self.content:
            self.errors.append("Content is empty.")

        if not self.errors:
            return True
        return False
