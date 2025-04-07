import constants
from classes.button import Button
from scenes.scene import Scene


class MainMenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = {}
        self.place_buttons()

    def listen(self):
        data = self.app.socket.recv(1024).decode()
        if data == 'start_game':
            self.app.change_scene('game')
        if data == 'disconnect':
            self.app.running = False

    def start_game(self):
        self.app.socket.send('start_game'.encode())

    def place_buttons(self):
        self.buttons['new_game'] = (Button(self, constants.SCREEN_WIDTH // 2 - constants.TILE_SIZE,
                                           constants.SCREEN_HEIGHT // 2 - constants.TILE_SIZE // 2,
                                           constants.TILE_SIZE * 2, constants.TILE_SIZE, 'blue', 'blue3',
                                           action=self.start_game))

    def logic(self, event):
        for button in self.buttons.values():
            button.logic(event)

    def draw(self):
        self.app.screen.fill((50, 50, 50))
        for button in self.buttons.values():
            button.draw()
