import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_room(self, room_id):
        with self.connection:
            return self.cursor.execute(f"SELECT buyer, seller FROM posts WHERE id = ({room_id})").fetchone()[0]

    def add_room(self, room_id, buyer, seller):
        with self.connection:
            return self.cursor.execute("INSERT INTO rooms(id, buyer, seller) VALUES (?, ?, ?)", (room_id, buyer, seller))
