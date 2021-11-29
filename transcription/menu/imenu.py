from abc import ABCMeta, abstractmethod


class MenuOption(metaclass=ABCMeta):
    def __init__(self, next_option):
        self.next_option = next_option

    @abstractmethod
    def execute(self, option: str):
        pass


class NullOption(MenuOption):
    def __init__(self):
        super().__init__(None)

    def execute(self, option: str):
        pass
