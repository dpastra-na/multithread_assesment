import threading


class Network:
    """
    The Network class provides a thread-safe way to send and receive messages between different
    parts of a program. It uses a semaphore to limit the number of messages that can be sent at once,
    and a buffer queue to store messages until they are received. The class also uses a condition
    variable to allow threads to wait for new messages to arrive.
    """

    def __init__(self, max_messages: int = 5) -> None:
        self.encoded_message: str = None
        self.lock: threading.Lock = threading.Lock()
        self.semaphore: threading.Semaphore = threading.Semaphore(max_messages)
        self.condition: threading.Condition = threading.Condition(self.lock)
        self.buffer_queue: list[str] = []

    def send_message(self, encoded_message: str) -> None:
        with self.condition:
            if self.semaphore._value == 0:
                raise threading.BrokenBarrierError(
                    "The maximum number of messages has been reached."
                )
            self.semaphore.acquire()
            print(f"Sending message: {encoded_message}")
            self.new_mesasge: bool = True
            self.encoded_message: str = encoded_message
            self.buffer_queue: List[str] = [encoded_message]
            self.condition.notify_all()  # Notify waiting consumers

    def receive_message(self) -> str:
        with self.condition:
            while not self.buffer_queue:
                self.condition.wait()  # Wait for notification from the producer
            for message in self.buffer_queue:
                # print(f"Receiving message: {message}")
                self.buffer_queue.remove(message)
                self.semaphore.release()
                return self.encoded_message
