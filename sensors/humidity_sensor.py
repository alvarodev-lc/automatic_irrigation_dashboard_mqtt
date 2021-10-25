import random


class HumiditySensor:
    humidity = None

    def read_humidity(self):
        self.humidity = random.randint(30, 50)
        return self.humidity
