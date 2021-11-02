import random


class TemperatureSensor:
    temp = None

    def read_temperature(self):
        self.temp = round(random.uniform(20.00, 40.00), 2)
        return self.temp
