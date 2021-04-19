import sqlite3


class DBManager:
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect('telegram.db')

    def set_clients(self,phone_number, client_session, used_before):
        self.conn.execute("""INSERT INTO telegram_clients (phone_number, client_session, used_before) \
                        VALUES ( '{}', '{}', '{}');""".format(phone_number,client_session,used_before))
        self.conn.commit()
    def get_clients(self):
        clients = self.conn.execute("""SELECT * FROM telegram_clients WHERE used_before = 0""")
        clients = clients.fetchall()
        self.conn.commit()
        return clients

    def update_client(self,client_session):
        self.conn.execute("""UPDATE telegram_clients SET used_before=1 WHERE client_session = '{}';""".format(client_session))
        self.conn.commit()
        return True


db_service = DBManager()
db_service.get_clients()
