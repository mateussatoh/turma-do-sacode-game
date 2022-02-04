import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI

class Game:
	def __init__(self):
		self.max_level = 2
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')
		self.overworld = Overworld(0,self.max_level,screen,self.criaLevel)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)
		self.ui = UI(screen)

	def criaLevel(self,current_level):
		self.level = Level(current_level,screen,self.criaMapa,self.mudaMoedas,self.mudaVida)
		self.status = 'level'
		self.overworld_bg_music.stop()
		self.level_bg_music.play(loops = -1)

	def criaMapa(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.criaLevel)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)
		self.level_bg_music.stop()

	def mudaMoedas(self,amount):
		self.coins += amount

	def mudaVida(self,amount):
		self.cur_health += amount

	def isGameOver(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.criaLevel)
			self.status = 'overworld'
			self.level_bg_music.stop()
			self.overworld_bg_music.play(loops = -1)

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.isGameOver()

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
game.criaLevel(0)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	screen.fill('grey')
	game.run()
	pygame.display.update()
	clock.tick(60)