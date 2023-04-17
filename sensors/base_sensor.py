import random
import time
from typing import Protocol
from enum import Enum
import threading

from utils.network import Network


class BaseSensor(Protocol):
    """
    The BaseSensor class is a protocol that defines the basic functionalities of a sensor.
    It provides a blueprint for other sensor classes to follow, ensuring that they have the
    necessary methods to start and stop the sensor, retrieve and send sensor data.
    """

    def run(self) -> None:
        """Starts the sensor"""

    def stop_sensor(self) -> None:
        """Stops the sensor"""

    def get_sensor_data(self) -> None:
        """Gets the sensor data"""

    def send_sensor_data(self) -> None:
        """Sends the sensor data"""


class SensorFactory(Protocol):
    """
    The SensorFactory class is a protocol that defines the main functionality of a
    factory for creating sensors. It provides a blueprint for other factory classes to follow,
    ensuring that they have the necessary methods to create sensors.
    """

    def create_sensors(self, network: Network) -> list[BaseSensor]:
        """Creates a sensor"""


class SensorTypeA(threading.Thread):
    """
    The SensorTypeA class is a subclass of the threading.Thread class and represents a sensor of type A.
    It generates random values between -100 and 100 and sends them to a with a deley of 5 seconds
    network using the Network class. It runs indefinitely until the stop_sensor method is called.
    """

    def __init__(
        self,
        network: Network,
        name: str = "sensor_type_A",
    ):
        super().__init__()
        self.timestamp: float = 0
        self.name: str = name
        self.value: int = 0
        self.network: Network = network
        self.delay: int = 5
        self.runing: bool = True

    def _generate_value(self) -> int:
        return random.randint(-100, 100)

    def run(self) -> None:
        print("Sensor A starting...")
        time.sleep(random.randint(1, 11))
        while True:
            self.read_sensor_data()
            self.send_sensor_data()
            time.sleep(self.delay)

    def stop_sensor(self) -> None:
        print("Sensor A stopped")
        self.runing = False

    def read_sensor_data(self) -> None:
        self.timestamp = time.time()
        self.value = self._generate_value()

    def send_sensor_data(self) -> None:
        encoded_message = f"{self.name} {self.value} {self.timestamp}"
        self.network.send_message(encoded_message=encoded_message)

    def __str__(self) -> str:
        return f"SensorTypeA(name={self.name}, value={self.value}, timestamp={self.timestamp}, delay={self.delay})"


class SensorTypeB(threading.Thread):
    """
    The SensorTypeB class is a subclass of the threading.Thread class and represents a sensor of type B.
    Its main functionalities are to generate random sensor data between 0 and 75, read and send sensor data to a network
    with a delasy of 1 second using the Network class, and run continuously until stopped.
    """

    def __init__(
        self,
        network: Network,
        name: str = "sensor_type_B",
    ):
        super().__init__()
        self.timestamp: int = 0
        self.name: str = name
        self.value: int = 0
        self.network: Network = network
        self.delay: int = 1
        self.runing: bool = True

    def _generate_value(self) -> int:
        return random.randint(0, 75)

    def run(self) -> None:
        print("Sensor B starting...")
        time.sleep(random.randint(1, 11))
        while True:
            self.read_sensor_data()
            self.send_sensor_data()
            time.sleep(self.delay)

    def stop_sensor(self) -> None:
        print("Sensor B stopped")
        self.runing = False

    def read_sensor_data(self) -> None:
        self.timestamp = time.time()
        self.value = self._generate_value()

    def send_sensor_data(self) -> None:
        encoded_message = f"{self.name} {self.value} {self.timestamp}"
        self.network.send_message(encoded_message=encoded_message)

    def __str__(self) -> str:
        return f"SensorTypeA(name={self.name}, value={self.value}, timestamp={self.timestamp}, delay={self.delay})"


class SensorTypeC(threading.Thread):
    """
    The SensorTypeC class is a subclass of the threading.Thread class and represents a sensor of type C.
    It generates random values within a range between -12 and 50, reads the sensor data, and sends it to
    a network using the Network class with a deley of 10 seconds. It runs on a separate thread and can be
    stopped using the stop_sensor() method.
    """

    def __init__(
        self,
        network: Network,
        name: str = "sensor_type_C",
    ):
        super().__init__()
        self.timestamp: float = 0
        self.name: str = name
        self.value: int = 0
        self.network: Network = network
        self.delay: int = 10
        self.runing: bool = True

    def _generate_value(self) -> int:
        return random.randint(-12, 50)

    def run(self) -> None:
        print("Sensor C starting...")
        time.sleep(random.randint(1, 11))
        while True:
            self.read_sensor_data()
            self.send_sensor_data()
            time.sleep(self.delay)

    def stop_sensor(self) -> None:
        print("Sensor C stopped")
        self.runing = False

    def read_sensor_data(self) -> None:
        self.timestamp = time.time()
        self.value = self._generate_value()

    def send_sensor_data(self) -> None:
        encoded_message = f"{self.name} {self.value} {self.timestamp}"
        self.network.send_message(encoded_message=encoded_message)

    def __str__(self) -> str:
        return f"SensorTypeA(name={self.name}, value={self.value}, timestamp={self.timestamp}, delay={self.delay})"


class SensorType(Enum):
    SensorA = SensorTypeA
    SensorB = SensorTypeB
    SensorC = SensorTypeC


class SameSensorFactory:
    """
    The SameSensorFactory class is responsible for creating a list of sensors of the same type,
    based on the specified sensor type and number of sensors. It uses the SensorType enum to
    determine the type of sensor to create and the number_of_sensors parameter to determine
    how many sensors to create. It returns a list of BaseSensor objects that can be used
    to start, stop, retrieve and send sensor data.
    """

    def create_sensors(
        self,
        network: Network,
        sensor_type: SensorType,
        number_of_sensors: int,
    ) -> list[BaseSensor]:
        return [
            sensor_type.value(
                network=network,
                name=f"{sensor_type.name}_{i}",
            )
            for i in range(number_of_sensors)
        ]


class DifferentSensorsFactory:
    """
    The DifferentSensorsFactory class is responsible for creating different types of sensors
    based on the SensorType enum and the number of sensors required for each type.
    It returns a list of BaseSensor objects that can be used to start, stop, retrieve and send sensor data.
    """

    def create_sensors(
        self, network: Network, sensor_type: dict[SensorType, int]
    ) -> list[BaseSensor]:
        sensors: list[BaseSensor] = []
        for k, v in sensor_type.items():
            for i in range(v):
                sensors.append(k.value(network, name=f"{k.name}_{i}"))
        return sensors
