from screen import Screen
import ship
import asteroid
import sys
import torpedo

DEFAULT_ASTEROIDS_NUM = 5
AXIS_MAX_COORD = 500
AXIS_MIN_COORD = -500
DELTA_AXIS = AXIS_MAX_COORD - AXIS_MIN_COORD
HIT_TITLE = "Ship hit!"
HIT_MSG = "Ohoh, You have hit an asteroid! =O"
WIN_GAME_TITLE = "Congratulations!!! You destroyed all asteroids!!!"
WIN_GAME_MSG = "You have won the game!"
LOST_GAME_TITLE = "Game Over!!!"
LOST_GAME_MSG = "You have lost all your lives and lost the game!!!"
QUIT_TITLE = "You have chosen to quit the game! )-:"
QUIT_MSG = "Bye Bye!!! The game ends now"
MAX_TORPEDO_NUMBER = 15
BIG_ASTEROID_SIZE = 3
MEDIUM_ASTEROID_SIZE = 2
HIT_BIG_AST_POINTS = 20
HIT_MEDIUM_AST_POINTS = 50
HIT_SMALL_AST_POINTS = 100



class GameRunner:
    """A class representing a spaceship asteroids game.
    the game is composed of a spaceship that moves according to the player's
    commands. the goal is to destroy all the asteroids by hitting them with
    the spaceship's torpedo. if the spaceship is hit by an asteroid for
    three times then the player loses. if the player pushes on the q button
    than he quits the game and it stops. if the player succeeds destroying
    all asteroids then he wins the game."""

    def __init__(self, asteroids_amnt):
        """
        A constructor for a gamerunner object
        :param asteroids_amnt = the amount of asteroids the game will start
        with.
        """
        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y

        self._ship = ship.Ship()
        self._screen.draw_ship(self._ship.x(), self._ship.y(),
                               self._ship.get_direction())

        self.asteroid_list = []
        for i in range(asteroids_amnt):
            self.asteroid_list.append(asteroid.Asteroid(self._ship))
        registered_asteroid_list = []
        for an_asteroid in self.asteroid_list:
            self._screen.register_asteroid(an_asteroid, an_asteroid.size)
            self._screen.draw_asteroid(an_asteroid, an_asteroid.x(),
                                       an_asteroid.y())

        self.torpedo_list = []

        self.score = 0

    def move(self, pos, x_velocity, y_velocity):
        """ a function that moves all objects according to the following
        equation: new cord = (speed + old coord - axis minimum coord) %
        (axis max coor - axis min coord) + axis min coord. (for each
         axis separately)
        :param pos: the current position of the object
        :param x_velocity: the current x velocity of the object
        :param y_velocity: the current y velocity of the object
        :return: the new (x, y) coor
        """
        x = pos[0]
        y = pos[1]
        new_x = (x_velocity + x - AXIS_MIN_COORD) % DELTA_AXIS + AXIS_MIN_COORD
        new_y = (y_velocity + y - AXIS_MIN_COORD) % DELTA_AXIS + AXIS_MIN_COORD

        return new_x, new_y

    def split_asteroid(self, index, an_asteroid, a_torpedo, a_ship):
        """ if an asteroid is hit with a torpedo it splits to two
        smaller asteroids. this function creates two new smaller asteroids and
        removes the one that got hit.
        :param an_asteroid: a asteroid that was hit by a torpedo
        :param a_torpedo: the torpedo that hit the asteroid
        :param a_ship: the game's ship
        """
        size = an_asteroid.get_size()
        self._screen.unregister_asteroid(an_asteroid)
        self.asteroid_list[index] = None
        if size != 1:
            # the new astroids are smaller than the original, by one:
            new_asteroids = [asteroid.Asteroid(a_ship, size - 1),
                         asteroid.Asteroid(a_ship, size - 1)]

            # calculating the new velocity according to
            #  the following function (for each axis separately:
            # (torpedo velocity + the old asteroid's velocity)
            #  / ((the old asteroid's velocity in the x axis)**2) +
            # (the old asteroid's velocity in the y axis)**2)) ** (1/2)
            new_x_velocity_o = (a_torpedo.get_x_velocity() +
                                an_asteroid.get_x_velocity())/ \
                               (an_asteroid.get_x_velocity()**2 +
                                            an_asteroid.get_y_velocity()**2)\
                               **(1/2)
            new_asteroids[0].set_x_velocity(new_x_velocity_o)
            new_x_velocity_1 = -new_x_velocity_o
            new_asteroids[1].set_x_velocity(new_x_velocity_1)
            new_y_velocity_o = (a_torpedo.get_y_velocity() +
                                an_asteroid.get_y_velocity()) \
                                         / (an_asteroid.get_x_velocity()**2 +
                                            an_asteroid.get_y_velocity()**2)\
                                              ** (1/2)
            new_asteroids[0].set_y_velocity(new_y_velocity_o)
            new_y_velocity_1 = -new_y_velocity_o
            new_asteroids[1].set_y_velocity(new_y_velocity_1)

            for a_new_asteroid in new_asteroids:
                a_new_asteroid.set_pos(an_asteroid.get_pos())
                self._screen.register_asteroid(a_new_asteroid,
                                               a_new_asteroid.get_size())
                self.asteroid_list.append(a_new_asteroid)



    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def set_score(self, an_asteroid):
        """ This function is called if a torpedo hit an asteroid.
        the score is set as following:
        20 points for a 3 sized asteroid
        50 points for a 2 sized asteroid
        100 points for a 1 sized asteroid
        """
        if an_asteroid.size == BIG_ASTEROID_SIZE:
            self.score += HIT_BIG_AST_POINTS
        elif an_asteroid.size == MEDIUM_ASTEROID_SIZE:
            self.score += HIT_MEDIUM_AST_POINTS
        else:
            self.score += HIT_SMALL_AST_POINTS
        # show new score on screen
        self._screen.set_score(self.score)

    def push_the_button(self):
        """ checks if the user pushed any buttons and
        responds accordingly.
        """
        # update ship status according to user's steps:
        if self._screen.is_left_pressed():
            self._ship.change_direction("left")

        if self._screen.is_right_pressed():
            self._ship.change_direction("right")

        if self._screen.is_up_pressed():
            self._ship.accelerate()

        if self._screen.is_space_pressed():
            if len(self.torpedo_list) < MAX_TORPEDO_NUMBER:
                a_torpedo = torpedo.Torpedo(self._ship)
                self._screen.register_torpedo(a_torpedo)
                self.torpedo_list.append(a_torpedo)
            else:
                pass

    def should_game_continue(self):
        """ a function that checks if the game should continue or not.
        the game should end if the ship has no more lives, there are no
        more asteroids or if the user pressed 'quit'.
        """
        win = True
        for an_asteroid in self.asteroid_list:
            if an_asteroid is not None:
                win = False
                break
        if win:
            self._screen.show_message(WIN_GAME_TITLE, WIN_GAME_MSG)
            self._screen.end_game()
            sys.exit()

        elif self._ship.life == 0:
            self._screen.show_message(LOST_GAME_TITLE, LOST_GAME_MSG)
            self._screen.end_game()
            sys.exit()
        elif self._screen.should_end():
            self._screen.show_message(QUIT_TITLE, QUIT_MSG)
            self._screen.end_game()
            sys.exit()

    def _game_loop(self):
        """this method runs one round of the game."""
        # move ship:
        update_ship_pos = self.move(self._ship.get_pos(),
                                    self._ship.get_x_velocity(),
                                    self._ship.get_y_velocity())
        self._ship.set_pos(update_ship_pos)
        self._screen.draw_ship(self._ship.x(), self._ship.y(),
                               self._ship.get_direction())

        # check user's commands
        self.push_the_button()

        # update torpedo
        for a_torpedo in self.torpedo_list:
            a_torpedo.update_life()

        for a_torpedo in filter(torpedo.Torpedo.dead_torpedo,
                                self.torpedo_list):
            self._screen.unregister_torpedo(a_torpedo)

        self.torpedo_list = list(filter(torpedo.Torpedo.alive_torpedo,
                                        self.torpedo_list))

        # move all torpedos
        for a_torpedo in self.torpedo_list:
            update_torpedo_pos = self.move(a_torpedo.get_pos(),
                                           a_torpedo.get_x_velocity(),
                                           a_torpedo.get_y_velocity())
            a_torpedo.set_pos(update_torpedo_pos)
            self._screen.draw_torpedo(a_torpedo, a_torpedo.x(), a_torpedo.y(),
                                      a_torpedo.get_direction())

        # move all asteroids and check if asteroids hit the ship or a torpedo
        for (index, an_asteroid) in enumerate(self.asteroid_list):
            if an_asteroid is not None:
                update_asteroid_pos = self.move(
                    an_asteroid.get_pos(), an_asteroid.get_x_velocity(),
                    an_asteroid.get_y_velocity())
                an_asteroid.set_pos(update_asteroid_pos)
                self._screen.draw_asteroid(
                    an_asteroid, an_asteroid.x(), an_asteroid.y())

                # check if the asteroid hit the ship:
                if an_asteroid.has_intersection(self._ship):
                    self._ship.life -= 1
                    self._screen.remove_life()
                    self._screen.unregister_asteroid(an_asteroid)
                    self.asteroid_list[index] = None
                    self._screen.show_message(HIT_TITLE, HIT_MSG)

            # check if the game should end:
            self.should_game_continue()

        # check if a torpedo hit an asteroid:
        # if it has the score will change and the
        # asteroid will split (or disappear if it's
        # size was one
        for (index, an_asteroid) in enumerate(self.asteroid_list):
            if an_asteroid is not None:
                for a_torpedo in self.torpedo_list:
                    if an_asteroid.has_intersection(a_torpedo):
                        self.set_score(an_asteroid)
                        self.split_asteroid(index, an_asteroid,
                                            a_torpedo, self._ship)
                        self.torpedo_list.remove(a_torpedo)
                        self._screen.unregister_torpedo(a_torpedo)
                        break

        # check if the game should end:
        self.should_game_continue()



def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )


