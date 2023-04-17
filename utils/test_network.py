import threading
import pytest

from utils.network import Network


class TestNetwork:
    def test_send_and_receive_message_successfully(self):
        network = Network()
        message = "Hello World!"
        network.send_message(message)
        received_message = network.receive_message()
        assert received_message == message

    def test_send_more_messages_than_max_limit(self):
        network = Network(max_messages=1)
        message1 = "Message 1"
        message2 = "Message 2"
        message3 = "Message 3"
        with pytest.raises(threading.BrokenBarrierError):
            network.send_message(message1)
            network.send_message(message2)
            network.send_message(message3)
