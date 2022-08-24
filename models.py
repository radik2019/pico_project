import os
import json
import random
from setting import DB_FILE


class PswdDb:
    """       Database    """
    write_permission = False

    def __init__(self):
        self.db_file = DB_FILE

    def str_generator(self, str_length: int = 10) -> str:
        alfa = 'qazwsxedcrfvtgbyhnujmikolp'
        digits = '1234567890'
        gen_str = ''
        for i in range(str_length):
            gen_str += random.choice(alfa + digits)
        return gen_str

    def load_db(self) -> dict:
        with open(self.db_file, 'r') as file:
            data = json.load(file)
        return data

    def dump_data(self, data: dict) -> None:
        with open(self.db_file, 'w') as db:
            json.dump(data, db)

    def push_db(self, my_str) -> bool:
        if self.write_permission:
            dct: dict = self.load_db()
            dct.update({self.str_generator(): my_str})
            self.dump_data(dct)
            return True
        return False

    def init_db(self) -> None:
        if not (self.db_file in os.listdir()):
            self.dump_data({'initial': None})

    def show_db(self) -> None:
        df: dict = self.load_db()
        sjson = json.dumps(df)

        print(f"\ndb size: {os.stat(self.db_file)[6]} bytes")
        print(sjson)

    def pass_exists(self, cod: str) -> bool:
        db = self.load_db()
        return cod in db


