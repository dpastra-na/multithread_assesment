import sqlite3

from service.repository.repository import (
    FileRepository,
    ConnectionPool,
    DatabaseRepository,
)
from service.model.message import Message


class TestFileRepository:
    def test_save_message_to_file_with_valid_data(self, tmp_path):
        file_path = tmp_path / "temp_test_data.txt"
        message = Message(
            id="12345", sensor_name="temperature", value=25, timestamp=1627894567.0
        )
        repo = FileRepository(file_path=file_path)
        repo.save(message)
        with open(file_path, "r") as file:
            assert (
                file.read()
                == f"{message.id},{message.timestamp},{message.sensor_name},{message.value}\n"
            )


class TestConnectionPool:
    def test_get_connection(self, tmp_path):
        conn_pool = ConnectionPool(2)
        db_name = tmp_path / "test.db"
        conn = conn_pool.get_connection(db_name)
        assert isinstance(conn, sqlite3.Connection)

    def test_release_connection(self, tmp_path):
        conn_pool = ConnectionPool(2)
        db_name = tmp_path / "test.db"
        conn = conn_pool.get_connection(db_name)
        conn_pool.release_connection(conn)
        assert conn_pool.connections.qsize() == 1

    def test_get_connection_edge(self, tmp_path):
        conn_pool = ConnectionPool(0)
        db_name = tmp_path / "test.db"
        conn = conn_pool.get_connection(db_name)
        assert conn is None

        conn_pool = ConnectionPool(1)
        conn1 = conn_pool.get_connection(db_name)
        conn2 = conn_pool.get_connection(db_name)
        assert conn1 is not None
        assert conn2 is None


class TestDatabaseRepository:
    def test_initialize_database_existing_db(self, tmp_path):
        db_name = tmp_path / "test.db"
        repo = DatabaseRepository(db_name=db_name)

        repo.initialize_database()

        with repo.connection_pool.get_connection(repo.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='sensors_data';"
            )
            result = cursor.fetchone()
            assert result[0] == "sensors_data"

    def test_save_single_message(self, tmp_path):
        db_name = tmp_path / "test.db"
        repo = DatabaseRepository(db_name=db_name)
        message = Message(
            id="12345", sensor_name="sensor1", value=10, timestamp=123456789
        )

        repo.save(message)

        with repo.connection_pool.get_connection(repo.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sensors_data WHERE id=?", (str(message.id),))
            result = cursor.fetchone()
            assert result[0] == str(message.id)
            assert result[1] == message.timestamp
            assert result[2] == message.sensor_name
            assert result[3] == message.value

    def test_save_multiple_messages(self, tmp_path):
        db_name = tmp_path / "test.db"
        repo = DatabaseRepository(db_name=db_name)
        messages = [
            Message(sensor_name="sensor1", value=10, timestamp=123456789, id="123"),
            Message(sensor_name="sensor2", value=20, timestamp=123456790, id="456"),
            Message(sensor_name="sensor3", value=30, timestamp=123456791, id="789"),
        ]

        for message in messages:
            repo.save(message)

        with repo.connection_pool.get_connection(repo.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sensors_data")
            result = cursor.fetchone()
            assert result[0] == len(messages)
