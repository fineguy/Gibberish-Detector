from abc import ABCMeta, abstractmethod


class AbstractGibberishDetector(metaclass=ABCMeta):
    @abstractmethod
    def is_gibberish(self, text):
        """
        Detects whether the given text is gibberish or not.

        :param text: str
        :return: `True` if the provided text is considered as gibberish and `False` otherwise.
        """
        pass


class AbstractTrainableGibberishDetector(AbstractGibberishDetector):
    @abstractmethod
    def save(self, model_path):
        pass

    @abstractmethod
    def load(self, model_path):
        pass

    @abstractmethod
    def train(self, *args, **kwargs):
        pass
