import arcade
import time

# Constants
TILE_SIZE = 32  # px
SCREEN_TITLE = "BreakEm"
TICK = 0.0  # second between frames

# Constants used to scale our sprites from their original size
PADDLE_SCALING = 0.25
BALL_SCALING = 0.5
BLOCK_SCALING = 0.25


class Game13(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, computer):

        # Call the parent class and set up the window
        super().__init__((width + 1) * TILE_SIZE, (height + 1) * TILE_SIZE, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        self.width = (width + 1) * TILE_SIZE
        self.height = (height + 1) * TILE_SIZE
        self.computer = GameComputer(computer)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.block_list = None
        self.paddle_list = None
        self.ball_list = None
        self.wall_list = None

        # Separate variable that holds the player sprite
        self.paddle_sprite = None
        self.ball_sprite = None

        # update time
        self.update_time = 0

    def tile_x(self, x):
        return x * TILE_SIZE  # x + 1 ?

    def tile_y(self, y):
        return self.height - y * TILE_SIZE

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.computer.update_state(initial=True)
        self.draw_scene()

    def draw_scene(self):
        # Create the Sprite lists
        self.block_list = arcade.SpriteList()
        self.paddle_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the paddle, specifically placing it at these coordinates.
        self.paddle_sprite = arcade.Sprite(":resources:images/tiles/bridgeA.png", PADDLE_SCALING)
        self.paddle_sprite.left = self.tile_x(self.computer.paddle[0])
        self.paddle_sprite.top = self.tile_y(self.computer.paddle[1])
        self.paddle_list.append(self.paddle_sprite)

        # Set up the ball, specifically placing it at these coordinates.
        self.ball_sprite = arcade.Sprite(":resources:images/pinball/pool_cue_ball.png", BALL_SCALING)
        self.ball_sprite.left = self.tile_x(self.computer.ball[0])
        self.ball_sprite.top = self.tile_y(self.computer.ball[1])
        self.ball_list.append(self.ball_sprite)

        # Set up the walls
        for wall in self.computer.walls:
            wall_sprite = arcade.Sprite(":resources:images/tiles/brickGrey.png", BLOCK_SCALING)
            wall_sprite.left = self.tile_x(wall[0])
            wall_sprite.top = self.tile_y(wall[1])
            self.wall_list.append(wall_sprite)

        # Set up the blocks
        for block in self.computer.blocks:
            block_sprite = arcade.Sprite(":resources:images/tiles/brickBrown.png", BLOCK_SCALING)
            block_sprite.left = self.tile_x(block[0])
            block_sprite.top = self.tile_y(block[1])
            self.block_list.append(block_sprite)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        # Draw sprites
        self.wall_list.draw()
        self.block_list.draw()
        self.paddle_list.draw()
        self.ball_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.computer.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.BLACK, 38)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.LEFT:
            self.computer.add_input([-1])
        elif key == arcade.key.RIGHT:
            self.computer.add_input([1])
        else:
            self.computer.add_input([0])

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass

    def on_update(self, delta_time):
        """ Movement and game logic """

        if time.time() - self.update_time > TICK:
            self.update_time = time.time()

            self.computer.update_state()
            self.draw_scene()


class GameComputer:

    def __init__(self, computer):
        self.computer = computer
        self.accumulated_input = []

        # Game state
        self.walls = []
        self.blocks = []
        self.paddle = None
        self.ball = None
        self.score = None

    def add_input(self, input):
        self.accumulated_input = self.accumulated_input + input

    def update_state(self, initial=False):
        if self.computer.is_running():
            # if len(self.accumulated_input) == 0:
            #     self.computer.run([0])
            # else:
            self.computer.run(self.accumulated_input)

            self.accumulated_input.clear()

            for i in range(0, len(self.computer.output_list), 3):
                if self.computer.output_list[i] == -1:  # score
                    self.score = self.computer.output_list[i + 2]
                if not initial and self.computer.output_list[i + 2] == 0:  # empty
                    if tuple(self.computer.output_list[i:i + 2]) in self.blocks:
                        self.blocks.remove(tuple(self.computer.output_list[i:i + 2]))
                elif self.computer.output_list[i + 2] == 1:  # wall
                    self.walls.append(tuple(self.computer.output_list[i:i + 2]))
                elif self.computer.output_list[i + 2] == 2:  # block
                    self.blocks.append(tuple(self.computer.output_list[i:i + 2]))
                elif self.computer.output_list[i + 2] == 3:  # paddle
                    self.paddle = tuple(self.computer.output_list[i:i + 2])
                elif self.computer.output_list[i + 2] == 4:  # ball
                    self.ball = tuple(self.computer.output_list[i:i + 2])
                    if not initial and not (self.ball[0] == self.paddle[0]):
                        self.accumulated_input.append((self.ball[0] - self.paddle[0]) // abs(self.ball[0] - self.paddle[0]))

            self.computer.output_list.clear()


def main():
    """ Main method """
    window = Game13()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
