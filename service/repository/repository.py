import os
import threading
from typing import Protocol
from dataclasses import dataclass, field
import sqlite3
from queue import Queue

from service.model.message import Message


class Repository(Protocol):
    """
    The Repository class is a protocol that defines the interface for saving data to a repository.
    It ensures that any class that implements this protocol has a save method that takes a
    Message object as input and returns None.
    """

    def save(self, message: Message) -> None:
        """Saves the data to the repository"""


@dataclass
class FileRepository:
    """
    The FileRepository class is responsible for saving Message objects to a text file format.
    """

    file_path: str = "./sonsor_data.csv"

    def save(self, message: Message) -> None:
        if not message.sensor_name or not message.value or not message.timestamp:
            print("Message data is invalid")
            # raise ValueError("Message data is invalid")
        with open(self.file_path, "a") as file:
            file.write(
                f"{message.id},{message.timestamp},{message.sensor_name},{message.value}\n"
            )


@dataclass
class InMemoryRepository:
    """
    The InMemoryRepository class is responsible for storing Message objects in an in-memory list.
    It provides a save method to add new messages to the list.
    """

    data: list[Message] = field(default_factory=list)

    def save(self, message: Message) -> None:
        self.data.append(message)


class ConnectionPool:
    """
    The ConnectionPool class provides a way to manage a pool of SQLite database connections.
    It limits the number of connections that can be created and allows for reusing connections
    to improve performance.
    """

    def __init__(self, max_connections: int):
        self.max_connections = max_connections
        self.connections: Queue[sqlite3.Connection] = Queue(maxsize=max_connections)
        self.number_of_connections = 0

    def get_connection(self, db_name: str) -> sqlite3.Connection:
        if self.number_of_connections == self.max_connections:
            return None
        if self.number_of_connections < self.max_connections:
            self.number_of_connections += 1
            self.connections.put(sqlite3.connect(db_name))
        return self.connections.get()

    def release_connection(self, conn: sqlite3.Connection) -> None:
        self.number_of_connections -= 1
        self.connections.put(conn)

    def __str__(self) -> str:
        return f"ConnectionPool(max_connections={self.max_connections}, connections={self.number_of_connections})"


@dataclass
class DatabaseRepository:
    """
    The DatabaseRepository class provides a way to save sensor data to an SQLite database.
    It uses a ConnectionPool to manage a pool of database connections and limit the number of
    connections that can be created. It also initializes the database if it does not exist.
    NOTE: I have not properly test this class yet.
    """

    db_name: str = "./sensors_data.db"
    connection_pool: ConnectionPool = field(default_factory=lambda: ConnectionPool(5))
    db_exists: bool = os.path.exists(db_name)

    def initialize_database(self) -> None:
        try:
            with self.connection_pool.get_connection(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sensors_data (
                        id TEXT PRIMARY KEY,
                        timestamp REAL,
                        sensor_name TEXT,
                        value INTEGER
                    )
                """
                )
                conn.commit()
            self.connection_pool.release_connection(conn)
        except sqlite3.Error as e:
            print(f"Error while initializing database: {e}")

    def save(self, message: Message) -> None:
        if not self.db_exists:
            self.initialize_database()
            self.db_exists = True
        with self.connection_pool.get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO sensors_data (id, timestamp, sensor_name, value)
                VALUES (?, ?, ?, ?)
            """,
                (
                    str(message.id),
                    message.timestamp,
                    message.sensor_name,
                    message.value,
                ),
            )
            conn.commit()
