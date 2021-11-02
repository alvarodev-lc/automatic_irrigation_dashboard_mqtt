import random


class HumiditySensor:
    humidity = None

    def read_humidity(self):
        self.humidity = round(random.uniform(30.00, 50.00), 2)
        return self.humidity
