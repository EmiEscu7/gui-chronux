from abc import  ABC, abstractmethod


class InfoFile(ABC):
    @abstractmethod
    def extract_info(self):
        pass

    @abstractmethod
    def load_params(self):
        pass
