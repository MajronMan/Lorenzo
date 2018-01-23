from abc import ABC, abstractmethod


class ImageFilter(ABC):
    @abstractmethod
    def filter(self, frame):
        pass
