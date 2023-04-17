from sensors.base_sensor import SameSensorFactory, SensorType, DifferentSensorsFactory
from utils.network import Network
from logging_service.logging import Logging
from service.repository.repository import FileRepository

import concurrent.futures

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
