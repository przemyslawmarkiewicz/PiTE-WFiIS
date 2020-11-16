from abc import ABC, abstractmethod
import random
import time
import logging
import multiprocessing


logging.basicConfig(filename='simulation.log', level=logging.DEBUG)


class Event(ABC):
    def __init__(self, rate=1):
        self.rate = rate

    @abstractmethod
    def flight_impact(self):
        pass


class Turbulence(Event):
    def flight_impact(self):
        return random.gauss(0, 2*self.rate)


class Correctioin(Event):
    def flight_impact(self):
        return self.rate


class Plane:
    def __init__(self, name, starting_tilt=0, rate_of_correction=1):
        self.name = name
        self.tilt = starting_tilt
        self.correction = Correctioin(rate_of_correction)

    def get_tilt(self):
        return f'tilt of plane {self.name} is {self.tilt}'

    def correct_right(self):
        self.tilt += self.correction.flight_impact()

    def correct_left(self):
        self.tilt -= self.correction.flight_impact()

    def correct(self):
        if self.tilt == 0:
            pass
        elif self.tilt < 0:
            logging.debug("Left tilt, turning right to correct")
            self.correct_right()
        elif self.tilt > 0:
            logging.debug("Right tilt, turning left to correct")
            self.correct_left()


class Environment:
    def __init__(self, plane, rate_of_turbulence=1):
        self.plane = plane
        self.turbulence = Turbulence(rate_of_turbulence)

    def affect_plane_with_turbulence(self):
        self.plane.tilt += self.turbulence.flight_impact()


def simulate_flight_step(plane):
    step = 0
    try:
        environment = Environment(plane)
        while True:
            environment.affect_plane_with_turbulence()
            logging.info(plane.get_tilt())
            print(plane.get_tilt())
            plane.correct()
            time.sleep(0.5)
            step += 1
            yield step

    except KeyboardInterrupt:
        print(f"Simulation for plane {plane.name} interrupted")
        logging.debug(f"Simulation interrupted for plane {plane.name}")


def simulate_flight(plane):
    for step in simulate_flight_step(plane):
        pass


if __name__ == "__main__":
    plane_1 = Plane("RYA-167", rate_of_correction=2)
    plane_2 = Plane("MS-180")

    try:
        p1 = multiprocessing.Process(target=simulate_flight, args=[plane_1])
        p2 = multiprocessing.Process(target=simulate_flight, args=[plane_1])

        p1.start()
        p2.start()

        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("Flight simulator interrupted")
