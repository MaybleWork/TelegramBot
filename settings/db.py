import sqlite3
from sqlite3 import Error


USER_CREATION_QUERY = """ 
    CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, user_id text NOT NULL, 
    name text NOT NULL, last_name text NOT NULL, surname text NOT NULL, email text UNIQUE, 
    token text NOT NULL , user_type text NOT NULL); 
"""


class BotDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

        self.create_table(USER_CREATION_QUERY)

    def create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def exist_user(self, user_id):
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,)
        )
        return bool(len(result.fetchall()))

    def exist_user_teacher(self, user_id):
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ? AND user_type = 'teacher'",
            (user_id,),
        )
        return bool(len(result.fetchall()))

    def exist_user_student(self, user_id):
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ? AND user_type = 'student'",
            (user_id,),
        )
        return bool(len(result.fetchall()))

    def update_user_info(self, email, name, last_name, surname, user_id):
        qs = """
        UPDATE `users`
        SET `email` = CASE WHEN ? IS NOT NULL THEN ? ELSE `email` END,
            `name` = CASE WHEN ? IS NOT NULL THEN ? ELSE `name` END,
            `last_name` = CASE WHEN ? IS NOT NULL THEN ? ELSE `last_name` END,
            `surname` = CASE WHEN ? IS NOT NULL THEN ? ELSE `surname` END
        WHERE `user_id` = ?
        """

        self.cursor.execute(
            qs,
            (
                email,
                email,
                name,
                name,
                last_name,
                last_name,
                surname,
                surname,
                user_id,
            ),
        )
        self.conn.commit()

    def get_full_name_user(self, user_id):
        result = self.cursor.execute(
            "SELECT `name`, `last_name`, `surname` FROM `users` WHERE `user_id` = ?",
            (user_id,),
        )
        return result.fetchone()[0]

    def get_email_user(self, user_id):
        result = self.cursor.execute(
            "SELECT `email` FROM `users` WHERE `user_id` = ?",
            (user_id,),
        )
        return result.fetchone()[0]

    def add_user(self, user_id, name, last_name, surname, email, token, user_type):
        self.cursor.execute(
            "INSERT INTO `users` (`user_id`, `name`, `last_name`, `surname`, `email`, `token`, `user_type`) VALUES (?,?,?,?,?,?,?)",
            (user_id, name, last_name, surname, email, token, user_type),
        )
        return self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute(
            "DELETE FROM `users` WHERE `user_id` = ?",
            (user_id,),
        )

        return self.conn.commit()

    def close(self):
        """DB connection close"""
        self.connection.close()
