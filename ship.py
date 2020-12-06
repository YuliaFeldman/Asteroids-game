from random import randint
import math

SHIP_RADIUS = 1
SHIP_START_LIFE = 3
CHANGE_DIR_DEGREE = 7


class Ship:
    """
    This class represents a spaceship in the game.
    The ship can move in all direction, accelerate and shoot torpedos.
    if the ship is hit by an asteroid - then the game ends.
    """

    def __init__(self):
        """ A constructor for a Ship object. """

        x = randint(-500, 500)
        y = randint(-500, 500)
        self._pos = (x, y)

        self._x_velocity = 0
        self._y_velocity = 0

        self._direction = 0

        self.life = SHIP_START_LIFE

    def set_pos(self, update_pos):
        """ This method updates the ship's position """
        self._pos = update_pos

    def get_pos(self):
        """ This method returns the ship's position """
        return self._pos

    def x(self):
        """ This method returns the x value of the ship """
        x = self._pos[0]
        return x

    def y(self):
        """ This method returns the y value of the ship """
        y = self._pos[1]
        return y

    def get_x_velocity(self):
        """ This method returns the velocity of x coordinate of the ship """
        return self._x_velocity

    def get_y_velocity(self):
        """ This method returns the velocity of y coordinate of the ship """
        return self._y_velocity

    def set_x_velocity(self, update):
        """ This method sets the velocity of x coordinate of the ship """
        self._x_velocity = update

    def set_y_velocity(self, update):
        """ This method sets the velocity of y coordinate of the ship """
        self._y_velocity = update

    def get_direction(self):
        """ This method returns the ship's direction """
        return self._direction

    def change_direction(self, direction):
        """ This method changes the direction of the ship """
        if direction == "left":
            self._direction += CHANGE_DIR_DEGREE
        else:
            self._direction -= CHANGE_DIR_DEGREE

    def accelerate(self):
        """ This method accelerates the ship's velocity """
        radian_heading = math.radians(self._direction)
        self._x_velocity += math.cos(radian_heading)
        self._y_velocity += math.sin(radian_heading)

    def radius(self):
        """ This method returns the ship's radius """
        return SHIP_RADIUS