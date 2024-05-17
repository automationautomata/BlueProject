import os.path
from abc import ABC, abstractmethod

class HardwareConnection(ABC):
    @abstractmethod
    def EstablishConnection() -> None: pass
    @abstractmethod
    def send(data) -> bool: pass
    @abstractmethod
    def recieve() -> str: pass

class CardChecker(HardwareConnection):
    def EstablishConnection() -> None: pass
    def send(data) -> bool: pass
    def recieve() -> str: pass