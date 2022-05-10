from abc import ABC, abstractmethod

from flask import Flask


app = None
external_added_modules = []

class Module(ABC):
    @abstractmethod
    def get_name(self) -> str:
        return "Main Page"

    @abstractmethod
    def get_route(self) -> str:
        pass

    @abstractmethod
    def controller(self):
        pass


class MainPage(Module):
    def get_name(self) -> str:
        return "Main Page"

    def get_route(self) -> str:
        return "/"

    def controller(self):
        return "<H1>Main Page</H1>"


def initialize():
    global app
    app = Flask(__name__)
    add_module(MainPage)


def add_module(module: Module, external=True):
    global app, external_added_modules
    instance = module()
    app.route(instance.get_route())(instance.controller)
    if external:
        external_added_modules.append(instance)


def run():
    global app
    app.run()
    

if __name__ == "__main__":
    initialize()
    run()
