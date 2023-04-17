import uuid
import threading

from service.repository.repository import Repository
from utils.network import Network
from service.model.message import Message


class Logging(threading.Thread):
    """
    The Logging class is a subclass of the threading.Thread class and is responsible
    for receiving messages from the Network class, parsing them into Message objects,
    and saving them to a repository using the Repository protocol. It runs in an
    infinite loop, continuously receiving messages and saving them to the repository.
    """

    def __init__(
        self,
        repository: Repository,
        network: Network,
    ):
        super().__init__()
        self.repository: Repository = repository
        self.network: Network = network
        self.message: Message = None

    def run(self) -> None:
        while True:
            message = self.network.receive_message()
            print(f"Receiving message: {message}")
            message = message.split(" ")
            message = Message(
                id=uuid.uuid4(),
                sensor_name=message[0],
                value=int(message[1]),
                timestamp=float(message[2]),
            )
            self.repository.save(message=message)
