import math

ACCELERATION_FACTOR = 2
TORPEDO_RADIUS = 4
LIFE_SPAN = 200


class Torpedo:
    """
    This class represents the torpedos in an asteroids game.
    if a torpedo hits an asteroid - then it damages it.
    """

    def __init__(self, ship):
        """ A constructor for a Torpedo object
        :param ship = the ship in the game
        """

        self._pos = ship._pos
        self._direction = ship.get_direction()

        radian_heading = math.radians(self._direction)
        self._x_velocity = ship.get_x_velocity() + ACCELERATION_FACTOR\
                                             * math.cos(radian_heading)
        self._y_velocity = ship.get_y_velocity() + ACCELERATION_FACTOR *\
                                             math.sin(radian_heading)
        self._life = 0

    def set_pos(self, update_pos):
        """ This method updates the torpedo's position """
        self._pos = update_pos

    def get_pos(self):
        """ This method returns the torpedo's position """
        return self._pos

    def x(self):
        """ This method returns the x value of the torpedo """
        x = self._pos[0]
        return x

    def y(self):
        """ This method returns the y value of the torpedo """
        y = self._pos[1]
        return y

    def get_x_velocity(self):
        """  method returns the velocity of x coordinate of the torpedo """
        return self._x_velocity

    def get_y_velocity(self):
        """ This method returns the velocity of y coordinate of the torpedo"""
        return self._y_velocity

    def get_direction(self):
        """ This method returns the torpedo's direction """
        return self._direction

    def radius(self):
        """ This method returns the torpedo's radius """
        return TORPEDO_RADIUS

    def update_life(self):
        """ This method updates the torpedo's life """
        self._life += 1

    def dead_torpedo(self):
        """
        This method returns True if the torpedo is dead and False if the
        torpedo is alive.
        """
        return self._life >= LIFE_SPAN

    def alive_torpedo(self):
        """
        This method returns True if the torpedo is alive and False
        if the torpedo is dead."""
        return not self.dead_torpedo()



