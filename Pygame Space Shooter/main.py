from data.modules.game.game import Game

if __name__ == '__main__':
	game = Game()

	while game.is_running:
		game.handle_events()
		game.update()
		game.draw()
