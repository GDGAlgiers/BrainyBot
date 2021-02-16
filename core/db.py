import sqlite3
from random import randint
import os


def initialize(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'messages' ('message_id' INT, 'channel' INT,"
        " 'reactionrole_id' INT, 'guild_id' INT);"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'reactionroles' ('reactionrole_id' INT, 'reaction'"
        " NVCARCHAR, 'role_id' INT);"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS 'dbinfo' ('version' INT);")
    cursor.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS reactionrole_idx ON messages (reactionrole_id);"
    )
    conn.commit()
    cursor.close()
    conn.close()


class Database:
    def __init__(self, database):
        self.database = database
        initialize(self.database)

        self.reactionrole_creation = {}

    def add_reaction_role(self, rl_dict: dict):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            if self.exists(rl_dict["message"]["message_id"]):
                raise Exception("The message id is already in use!")
            while True:
                try:
                    reactionrole_id = randint(0, 100000)
                    cursor.execute(
                        "INSERT INTO 'messages' ('message_id', 'channel', 'reactionrole_id',"
                        " 'guild_id') values(?, ?, ?, ?);",
                        (rl_dict["message"]["message_id"], rl_dict["message"]["channel_id"], reactionrole_id, rl_dict["message"]["guild_id"]),
                    )
                    break
                except sqlite3.IntegrityError:
                    continue
            combos = [(reactionrole_id, reaction, role_id) for reaction, role_id in rl_dict["reactions"].items()]
            cursor.executemany("INSERT INTO 'reactionroles' ('reactionrole_id', 'reaction', 'role_id') values(?, ?, ?);", combos)
            conn.commit()
            cursor.close()
            conn.close()
        except sqlite3.Error as e:
            return e
    
    def exists(self, message_id):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM messages WHERE message_id = ?;", (message_id,)
            )
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result

        except sqlite3.Error as e:
            return e

    def get_reactions(self, message_id):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT reactionrole_id FROM messages WHERE message_id = ?;",
                (message_id,),
            )
            reactionrole_id = cursor.fetchall()[0][0]
            cursor.execute(
                "SELECT reaction, role_id FROM reactionroles WHERE reactionrole_id"
                " = ?;",
                (reactionrole_id,),
            )
            combos = {}
            for row in cursor:
                reaction = row[0]
                role_id = row[1]
                combos[reaction] = role_id

            cursor.close()
            conn.close()
            return combos

        except sqlite3.Error as e:
            return e

    def fetch_messages(self, channel):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT message_id FROM messages WHERE channel = ?;", (channel,)
            )
            all_messages_in_channel = []
            for row in cursor:
                message_id = int(row[0])
                all_messages_in_channel.append(message_id)

            cursor.close()
            conn.close()
            return all_messages_in_channel

        except sqlite3.Error as e:
            return e

    def fetch_all_messages(self):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages;")
            all_messages = cursor.fetchall()

            cursor.close()
            conn.close()
            return all_messages

        except sqlite3.Error as e:
            return e




        
    def delete(self, message_id, guild_id=None):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            if guild_id:
                cursor.execute(
                    "SELECT reactionrole_id FROM messages WHERE guild_id = ?;",
                    (guild_id,),
                )

            else:
                cursor.execute(
                    "SELECT reactionrole_id FROM messages WHERE message_id = ?;",
                    (message_id,),
                )

            result = cursor.fetchall()
            if result:
                reactionrole_id = result[0][0]
                cursor.execute(
                    "DELETE FROM messages WHERE reactionrole_id = ?;",
                    (reactionrole_id,),
                )
                cursor.execute(
                    "DELETE FROM reactionroles WHERE reactionrole_id = ?;",
                    (reactionrole_id,),
                )
                conn.commit()

            cursor.close()
            conn.close()

        except sqlite3.Error as e:
            return e

    def add_reaction(self, message_id, role_id, reaction):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT reactionrole_id FROM messages WHERE message_id = ?;",
                (message_id,),
            )
            reactionrole_id = cursor.fetchall()[0][0]
            cursor.execute(
                "SELECT * FROM reactionroles WHERE reactionrole_id = ? AND reaction = ?;",
                (reactionrole_id, reaction)
            )
            exists = cursor.fetchall()
            if exists:
                cursor.close()
                conn.close()
                return False

            cursor.execute(
                "INSERT INTO reactionroles ('reactionrole_id', 'reaction', 'role_id')"
                " values(?, ?, ?);",
                (reactionrole_id, reaction, role_id),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True

        except sqlite3.Error as e:
            return e

    def remove_reaction(self, message_id, reaction):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT reactionrole_id FROM messages WHERE message_id = ?;",
                (message_id,),
            )
            reactionrole_id = cursor.fetchall()[0][0]
            cursor.execute(
                "DELETE FROM reactionroles WHERE reactionrole_id = ? AND reaction = ?;",
                (reactionrole_id, reaction),
            )
            conn.commit()
            cursor.close()
            conn.close()

        except sqlite3.Error as e:
            return e

directory = os.path.dirname(os.path.realpath(__file__))
db_file = f"{directory}/db/brainy.db"
db = Database(db_file)