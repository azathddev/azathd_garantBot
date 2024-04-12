import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_ids(self) -> list:
        with self.connection:
            result = []
            for room_id in self.cursor.execute("SELECT id FROM rooms").fetchall():
                result.append(room_id[0])
            return result

    def get_times(self) -> list:
        with self.connection:
            result = []
            for res in self.cursor.execute("SELECT id, time FROM rooms").fetchall():
                result.append((res[0], res[1]))
            return result

    def del_room(self, room_id: str) -> None:
        with self.connection:
            self.cursor.execute("DELETE FROM rooms WHERE id = ?", (room_id,))

    def get_room(self, room_id: str) -> list:
        with self.connection:
            return list(self.cursor.execute(f"SELECT buyer, seller FROM rooms WHERE id = ('{room_id}')").fetchone())

    def add_room(self, room_id: str, buyer: int, seller: int) -> None:
        with self.connection:
            self.cursor.execute("INSERT INTO rooms(id, buyer, seller, time) VALUES (?, ?, ?, ?)", (room_id, buyer, seller, int(time.time())))

    def update_room(self, room_id: str, buyer: int, seller: int) -> None:
        with self.connection:
            self.cursor.execute(f"UPDATE rooms SET buyer = ? WHERE id = ('{room_id}')", (buyer, ))
            self.cursor.execute(f"UPDATE rooms SET seller = ? WHERE id = ('{room_id}')", (seller, ))
