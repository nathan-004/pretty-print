def loading_cars(*args, cars=["|", "/", "-", "\\", "|", "/", "-", "\\"], steps = 10):
    s = 0
    for idx in range(*args):
        if s % steps == 0:
            print(cars[idx % (len(cars) - 1)], end="\r")
        yield idx
        s += 1
                 
def main():
    for i in loading_cars(10000):
        pass