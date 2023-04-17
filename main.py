from sensors.base_sensor import SameSensorFactory, SensorType, DifferentSensorsFactory
from utils.network import Network
from logging_service.logging import Logging
from service.repository.repository import FileRepository

import concurrent.futures


"""
This program is a multithreaded application that creates different types of sensors and logs their
data usinga network and a diferent types of repositories.
The program starts by initializing a Network object with a maximum number of messages, the requirement
is 5 and a RepositoryStrategy object. It then creates a Logging object with the previously created
Network and RepositoryStrategy objects.
The program then creates a list of sensors using the SensorsFactory class (SameSensorFactory and
DifferentSensorsFactory are implemnted).
The program then uses a ThreadPoolExecutor to start the logging and sensor threads concurrently.
"""


if __name__ == "__main__":
    network = Network(max_messages=5)
    repository = FileRepository()
    logging = Logging(repository=repository, network=network)

    # sensors = SameSensorFactory().create_sensors(
    #     network=network,
    #     sensor_type=SensorType.SensorB,
    #     number_of_sensors=5,
    # )

    sensors = DifferentSensorsFactory().create_sensors(
        network=network,
        sensor_type={
            SensorType.SensorA: 2,
            SensorType.SensorB: 1,
            SensorType.SensorC: 2,
        },
    )

    with concurrent.futures.ThreadPoolExecutor(6) as executor:
        executor.submit(logging.start)
        for sensor in sensors:
            executor.submit(sensor.start)
