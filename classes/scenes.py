from classes.game import Game


class Scene:
    def __init__(self, app):
        self.app = app

    def logic(self, event):
        pass


class MainMenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)

    def logic(self, event):
        pass

    def draw(self):
        pass


class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game(self)

    def logic(self, event):
        if not self.game.game_over:
            if not self.game.promotion_window.promotion:
                self.game.selected_piece_logic(event)
            else:
                self.game.promotion_window.logic(event)
            for button in self.game.buttons:
                button.logic(event)
        else:
            self.app.switch_scene(MainMenuScene)

    def draw(self):
        self.app.screen.fill((50, 50, 50))
        self.game.draw_board()
        self.game.draw_highlighted_tiles()
        self.game.draw_buttons()
        self.game.draw_pieces()
        self.game.draw_promotion_window()
