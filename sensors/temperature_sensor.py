import random


class TemperatureSensor:
    temp = None

    def read_temperature(self):
        self.temp = random.randint(20, 40)
        return self.temp
