import pygame as pg
from pygame import Vector2
from settings import *

class CameraGroup(pg.sprite.Group):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.display_surface = self.game.screen

		# camera offset 
		self.offset = pg.math.Vector2()
		self.half_w = WIDTH // 2
		self.half_h = HEIGHT // 2

		# zoom 
		self.zoom_scale = 1
		self.curr_zoom = self.zoom_scale
		self.internal_surf_size = (2500,2500)
		self.internal_surf = pg.Surface(self.internal_surf_size, pg.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pg.math.Vector2(self.internal_surf_size)
		self.internal_offset = pg.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def custom_draw(self, player):
		self.center_target_camera(player)

		self.internal_surf.fill(BGCOLOR)

		# active elements
		for sprite in self.game.all_sprites.sprites():
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image, offset_pos)
		
		if self.curr_zoom != self.zoom_scale:
			self.curr_zoom += (self.zoom_scale - self.curr_zoom) * 0.1
		scaled_surf = pg.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.curr_zoom)
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

		self.display_surface.blit(scaled_surf,scaled_rect)
		
		pg.draw.rect(self.display_surface, LIGHTGREY, pg.Rect(30, 30, 100, 20))
		pg.draw.rect(self.display_surface, RED, pg.Rect(30, 30, self.game.player.lives/1000*100, 20))

