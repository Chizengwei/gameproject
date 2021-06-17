from super_mario.data.game import Game
from super_mario.data.level import Level
from super_mario.data.load_screen import Load_Screen, GameOver
from super_mario.data.main_menu import MainMenu

diction = {'level': Level(), 'menu': MainMenu(), 'load': Load_Screen(), 'game_over': GameOver()}
if __name__ == '__main__':
	game = Game(diction, 'menu')
	game.run()
	pass
