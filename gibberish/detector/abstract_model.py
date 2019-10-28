from abc import ABCMeta, abstractmethod


class AbstractGibberishDetector(metaclass=ABCMeta):
    @abstractmethod
    def is_gibberish(self, text):
        pass


class AbstractTrainableGibberishDetector(AbstractGibberishDetector):
    @abstractmethod
    def save(self, model_path):
        pass

    @abstractmethod
    def load(self, model_path):
        pass

    @abstractmethod
    def train(self, data_path):
        pass
