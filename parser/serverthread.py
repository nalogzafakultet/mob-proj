import threading, pymongo
from datetime import datetime
from datetime import timedelta

MSGLEN = 5000
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

DB_HOST = '167.99.39.202'
DB_PORT = 5055

DB_NAME = 'weather_db'
COLLECTION_NAME = 'weathers'


class ServerThread(threading.Thread):

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def run(self):
        data = self.sock.recv(2048)
        data = data.decode('utf-8').split(',')
        print('Konektovao se klijent')
        print('Data primljena:', data)
        # temp, vlaz, vetar, osv
        obj = {}
        obj['temperatura'] = float(data[0])
        obj['vlaznost'] = float(data[1])
        obj['pritisak'] = float(data[2])
        obj['osvetljenje'] = int(data[3])
        obj['vreme'] = str(datetime.now()) + timedelta(hours=2)

        client = pymongo.MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print(client)
        print(db)
        print(collection)
        print('Objekat:', obj)
        str_id = collection.insert_one(obj)
        print('Inserted:', str_id)

