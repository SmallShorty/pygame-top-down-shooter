import sqlite3


class ScoreBoard:
    def __init__(self, db_name="scores.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL
                )
            """
            )
            conn.commit()

    def save_score(self, name, score):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score)
            )
            conn.commit()

    def get_top_scores(self, limit=5):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT ?",
                (limit,),
            )
            return cursor.fetchall()
