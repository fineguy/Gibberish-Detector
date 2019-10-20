from abc import ABCMeta, abstractmethod


class AbstractGibberishDetector(metaclass=ABCMeta):
    @abstractmethod
    def is_gibberish(self, text):
        pass
