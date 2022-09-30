import random


def generate_color():
    rand = lambda: random.randint(100, 255)
    return '#%02X%02X%02X' % (rand(), rand(), rand())
