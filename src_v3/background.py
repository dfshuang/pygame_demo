"""
迪润完成
可自行拆分为多个文件
"""

import pygame as pg
from pygame.sprite import Group
from pygame.sprite import Sprite

class Background():
	def __init__(self,sett):
		self.fullimage=pg.image.load('../image/bg/sky.png')
		self.images=[0,0]
		self.rects=[0,0]
		self.images[0]=self.fullimage.subsurface(pg.Rect((0,0),(1200,800)))
		self.images[1]=pg.image.load('../image/bg/land.png')
		for i in range(2):
			self.rects[i]=self.images[i].get_rect()
		self.rects[1].bottom=sett.screen_height
		self.time=0.0
		self.clock=pg.time.Clock()
		self.T=(4033-1200)*30.0

	def update(self):
		self.time+=self.clock.tick()
		if self.time>self.T:
			self.time=0
		i=int(self.time//30)
		self.images[0]=self.fullimage.subsurface(pg.Rect((i,0),(1200,800)))

	def drawme(self,screen):
		for i in range(2):
			screen.blit(self.images[i],self.rects[i])
		


