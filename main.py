from machine import Pin
from models import PswdDb
from setting import TOKENS, EXPIRE
import utime

"""
<combinazione_numerica + "A" aggiungi una nuova password>
    per poterlo fare, bisogna disporre del token:
        <digita il token> + "D"
        Avrai a dispozizione 30 secondi per inserire il nuovo codice

<"C"> cancell cio che hai digitato

<"B"> stampa il database delle password 

"""


class Rasp(PswdDb):
    expired_time: int = 0

    def __init__(self):
        super().__init__()
        self.red = Pin(11, Pin.OUT)
        self.green = Pin(10, Pin.OUT)
        self.blue = Pin(12, Pin.OUT)
        led = Pin(15, Pin.OUT)
        self.led = Pin(25, Pin.OUT)
        self.matrix_keys = [['1', '2', '3', 'A'],
                            ['4', '5', '6', 'B'],
                            ['7', '8', '9', 'C'],
                            ['*', '0', '#', 'D']]
        self.keypad_columns = [6, 7, 8, 9]
        self.keypad_rows = [2, 3, 4, 5]
        self.col_pins = []
        self.row_pins = []
        for x in range(0, 4):
            self.row_pins.append(Pin(self.keypad_rows[x], Pin.OUT))
            self.row_pins[x].value(1)
            self.col_pins.append(Pin(self.keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
            self.col_pins[x].value(0)

    def rgb_flash(self, n_iter: int, interval, color: str = 'b') -> None:
        for i in range(n_iter):
            ld = None
            if color == 'g':
                ld = self.green
            elif color == 'r':
                ld = self.red
            else:
                ld = self.blue
            ld.value(1)
            utime.sleep(interval)
            ld.value(0)
            if n_iter - i == 1:
                interval = 0.03
            utime.sleep(interval)

    def flashing_led(self, n: int, interval: float) -> None:
        for i in range(n):

            self.led.value(1)
            utime.sleep(interval)
            self.led.value(0)
            if n - i == 1:
                interval = 0.03
            utime.sleep(interval)

    def scan_keys(self) -> str:
        key_press = None
        for row in range(4):
            for col in range(4):
                self.row_pins[row].high()
                if self.col_pins[col].value() == 1:
                    key_press = self.matrix_keys[row][col]
                    self.led.value(1)
                    utime.sleep(0.06)
                    self.led.value(0)
                    utime.sleep(0.2)
                    if key_press.isdigit() or (key_press == '*') or (key_press == '#'):
                        print(key_press, end='')
                    break
            self.row_pins[row].low()
            if key_press:
                return key_press
        return key_press

    @staticmethod
    def open_the_door() -> None:
        print("the door is openning!")

    def check_status_permission(self):
        if self.write_permission:
            if self.expired_time <= utime.time():
                self.write_permission = False

    def run(self) -> None:

        my_str = ''
        while True:
            self.check_status_permission()
            character = self.scan_keys()
            if character:
                if character.isdigit() or (character == '*') or (character == '#'):
                    my_str += character
                else:
                    if character.lower() == 'a':
                        if my_str:
                            dt = self.push_db(my_str)
                            print('\n\ndt!!', dt)
                            if dt:
                                print('\nAdded new data to db')
                                self.rgb_flash(4, 0.02, 'g')
                            else:
                                print('\nPermission denied!')
                                self.rgb_flash(4, 0.02, 'r')
                        my_str = ''
                        print()

                    elif character.lower() == 'b':
                        print(my_str)
                        self.show_db()
                    elif character.lower() == 'c':
                        my_str = ''
                        self.flashing_led(2, 0.3)
                        self.rgb_flash(4, 0.02, 'r')
                        self.rgb_flash(4, 0.02, 'g')
                        self.rgb_flash(12, 0.02, 'b')
                    elif character.lower() == 'd':
                        if my_str in TOKENS:
                            self.write_permission = True
                            self.expired_time = utime.time() + EXPIRE
                            print('\nYou have 30 seconds for change the pssword')
                            self.rgb_flash(1, 1, 'b')
                            continue
                        if self.pass_exists(my_str):
                            self.open_the_door()
                            self.rgb_flash(6, 0.02, 'b')
                            my_str = ''
                        else:
                            self.rgb_flash(6, 0.02, 'r')
                            my_str = ''


if __name__ == '__main__':
    hdw = Rasp()

    hdw.rgb_flash(4, 0.05, 'r')
    hdw.rgb_flash(4, 0.05, 'g')
    hdw.rgb_flash(4, 0.05, 'b')
    hdw.run()






