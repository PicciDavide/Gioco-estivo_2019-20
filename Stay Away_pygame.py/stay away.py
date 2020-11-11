import pygame, sys
from pygame.math import Vector2
from pygame.locals import *
import math
import random

pygame.init()
pygame.font.init()

#schermo
SCREEN_SIZE = (500, 500)
screen = pygame.display.set_mode(SCREEN_SIZE)


#clock
FPS = 60
CLOCK = pygame.time.Clock()

#colori
BIANCO = (255, 255, 255)
ROSSO = (255, 0, 0)
GIALLO = (255, 255, 0)
VERDE = (0, 255, 0)
BLU = (0, 0, 255)
NERO = (0, 0, 0)

#game_exit
GAME_EXIT = False

def is_between(numero1, numero2, numero_controllo):
	a = min(numero1, numero2)
	b = max(numero1, numero2)
	if numero_controllo < b and numero_controllo > a:
		return True
	else:
		return False


class Pers:
	def __init__(self, screen, colore_pers, x, y, w, h, speed):
		self.screen = screen
		self.colore_pers = colore_pers
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.speed = speed
		self.vel_change_pers_x = 0
		self.vel_change_pers_y = 0

		self.PERSONAGGIO_HITBOX = Rect(int(self.x), int(self.y), self.w, self.h)
	
	def stampa(self):
		pygame.draw.rect(self.screen, self.colore_pers, (self.PERSONAGGIO_HITBOX))

		self.PERSONAGGIO_HITBOX = Rect(int(self.x), int(self.y), self.w, self.h)

	def move(self):
		self.vel_change_pers_y = 0
		self.vel_change_pers_x = 0

		TASTO_PREMUTO = pygame.key.get_pressed()
		if TASTO_PREMUTO[pygame.K_a]:
			self.vel_change_pers_x = self.speed * -1
		if TASTO_PREMUTO[pygame.K_d]:
			self.vel_change_pers_x = abs(self.speed)
		if TASTO_PREMUTO[pygame.K_w]:
			self.vel_change_pers_y = self.speed * -1
		if TASTO_PREMUTO[pygame.K_s]:
			self.vel_change_pers_y = abs(self.speed)

		self.x += self.vel_change_pers_x
		self.y += self.vel_change_pers_y

		if self.x <= 0:
			self.x += self.speed
		elif self.x + self.w >= SCREEN_SIZE[0]:
			self.x -= self.speed
		if self.y <= 0:
			self.y += self.speed
		elif self.y + self.h >= SCREEN_SIZE[1]:
			self.y -= self.speed

'''class Laser:
	def __init__(self, screen, colore, w):
		self.screen = screen
		self.colore = colore
		self.w = w
		self.x_1, self.y_1 = 0, 0
		self.x_2, self.y_2 = 0, 0
		self.laser_sparato = False
	
	def stampa(self):
		if self.laser_sparato:
			self.x_1, self.y_1 = PERSONAGGIO.main_x + PERSONAGGIO.w//2, PERSONAGGIO.y + PERSONAGGIO.h//2
			self.x_2, self.y_2 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
			self.start = (self.x_1, self.y_1)
			self.end = (self.x_2, self.y_2)

			pygame.draw.line(self.screen, self.colore, self.start, self.end, self.w)

	def gestore_laser(self):
		if self.laser_sparato:
			if is_between(self.x_1, self.x_2, NEMICO.x) and is_between(self.y_1, self.y_2, NEMICO.y):
				print("oof")
			elif is_between(self.x_1, self.x_2, NEMICO.x + NEMICO.w) and is_between(self.y_1, self.y_2, NEMICO.y + NEMICO.h):
				print("oof")
		
def spara_laser():
	if event.type == MOUSEBUTTONDOWN:
		if event.button == 3:
			if LASER.laser_sparato == False:
				LASER.laser_sparato = True
			else:
				LASER.laser_sparato = False'''

class Proiettile:
	def __init__(self, screen, colore_proiettile, proiettile_w, proiettile_h, proiettile_speed):
		self.screen = screen
		self.colore = colore_proiettile
		self.x, self.y = PERSONAGGIO.x, PERSONAGGIO.y
		self.w, self.h = proiettile_w, proiettile_h
		self.speed = proiettile_speed
		self.x_stop, self.y_stop = pygame.mouse.get_pos()

		self.d = 100

		self.radianti = math.atan2(self.y_stop - self.y, self.x_stop - self.x)

		#self.d = math.hypot(self.x_stop - self.x, self.y_stop - self.y)
		#self.d = int((self.d) / self.speed)

		self.x_d = math.cos(self.radianti) * self.speed
		self.y_d = math.sin(self.radianti) * self.speed

		self.proiettile_sparato = True

	def stampa(self):
		if self.proiettile_sparato:
			self.immagine = pygame.image.load("shuriken.png")
			self.screen.blit(self.immagine, (self.x,self.y))
	
	def move(self):
		if self.proiettile_sparato:
			if self.d:
				self.d -= 1
				self.x += self.x_d
				self.y += self.y_d

				self.PROIETTILE_HITBOX = Rect(int(self.x), int(self.y), self.w, self.h)             
			else:
				self.proiettile_sparato = False

def spara_proiettile():
	if event.type == MOUSEBUTTONDOWN:
		if event.button == 1:
			proiettile_sparati.append(Proiettile(screen, ROSSO, 10, 10, 10))			

class Nemico:
	def __init__(self, screen, colore1, colore2, colore3, stato):
		self.screen = screen
		self.colore = random.choice([colore1, colore2, colore3])
		self.w, self.h = 30, 30
		self.x = random.randrange(0, SCREEN_SIZE[0] - self.w)
		self.y = random.randrange(0, SCREEN_SIZE[1] - self.h)
		self.NEMICO_HITBOX = Rect(int(self.x), int(self.y), self.w, self.h)
		self.stato = stato

		self.speed = 1

	def stampa(self):
		self.immagine = pygame.image.load('robber-mask.png')
		self.screen.blit(self.immagine, (self.x,self.y))
		

	def path_finder(self):
		self.bersaglio_x, self.bersaglio_y = PERSONAGGIO.x, PERSONAGGIO.y
		self.radianti = math.atan2(self.bersaglio_y - self.y, self.bersaglio_x - self.x)
		self.d = math.hypot(self.bersaglio_x - self.x, self.bersaglio_y - self.y)
		self.d = int((self.d) / self.speed)
		self.x_d = math.cos(self.radianti) * self.speed
		self.y_d = math.sin(self.radianti) * self.speed
	
	def move(self):
		if self.d:
			self.d -= 1
			self.x += self.x_d
			self.y += self.y_d 
			self.NEMICO_HITBOX = Rect(int(self.x), int(self.y), self.w, self.h)

def spawner_nemico():
	global timer_spawner_nemico
	timer = -50 * nemico_uccisi + 3000
	if len(nemico_spawned) < 5:
		if pygame.time.get_ticks() - timer_spawner_nemico > timer:
			nemico_spawned.append(Nemico(screen, BIANCO, ROSSO, BLU, "normale"))
			timer_spawner_nemico = pygame.time.get_ticks()

def gestore():
	global nemico_spawned
	global nemico_uccisi
	global Stato_gioco
	global GAME_EXIT

	for proiettile in proiettile_sparati:
			proiettile.move()
			proiettile.stampa()
			if not proiettile.proiettile_sparato:
				proiettile_sparati.remove(proiettile)
			for nemico in nemico_spawned: # collisione proitettile - nemico
				if proiettile.PROIETTILE_HITBOX.colliderect(nemico.NEMICO_HITBOX):
					nemico.stato = "colpito"
					nemico_spawned.remove(nemico)
					proiettile.proiettile_sparato = False
					nemico_uccisi += 1
					if nemico_uccisi >= 40:
						Stato_gioco = "vinto"

	for nemico in nemico_spawned:
		nemico.path_finder()
		nemico.move()
		nemico.stampa()
		if nemico.NEMICO_HITBOX.colliderect(PERSONAGGIO.PERSONAGGIO_HITBOX):
			PERSONAGGIO.w += 1
			PERSONAGGIO.h += 1
			if PERSONAGGIO.w > 200:
				Stato_gioco = "perso"
				if PERSONAGGIO.w > 400:
					GAME_EXIT = True


def fine_gioco():
	global GAME_EXIT
	font = pygame.font.SysFont('Arial Black', 72)
	font2 = pygame.font.SysFont("Arial Black", 68)
	font_screen = font.render("GAME OVER", True, (0, 0, 0))
	font_screen2 = font2.render("GAME OVER", True, (255, 255, 255))
	if Stato_gioco == "perso":
		screen.blit(font_screen2,
		(250 - font_screen2.get_width() // 2, 250 - font_screen2.get_height() // 2))
		screen.blit(font_screen,
		(250 - font_screen.get_width() // 2, 250 - font_screen.get_height() // 2))

	font_screen_vinto1 = font.render("HAI VINTO!", True, (0, 0, 0))
	font_screen_vinto2 = font2.render("HAI VINTO!", True, (255, 255, 255))

	if Stato_gioco == "vinto":
		screen.blit(font_screen_vinto2,
		(250 - font_screen_vinto2.get_width() // 2, 250 - font_screen_vinto2.get_height() // 2))
		screen.blit(font_screen_vinto1,
		(250 - font_screen_vinto1.get_width() // 2, 250 - font_screen_vinto1.get_height() // 2))
		GAME_EXIT = True



PERSONAGGIO = Pers(screen, (31, 25, 33), 50, 50, 20, 20, 5)
#LASER = Laser(screen, GIALLO, 5)
proiettile_sparati = []
nemico_spawned = []
nemico_uccisi = 0
timer_spawner_nemico = pygame.time.get_ticks()
Stato_gioco = "neutro"



while GAME_EXIT == False:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: #Quit
			GAME_EXIT = True
		spara_proiettile()

	PERSONAGGIO.move()

	immagine_screen = pygame.image.load('sfondo_mattoni_pietra.png')
	screen.blit(immagine_screen, (0,0))

	spawner_nemico()
	gestore()
	fine_gioco()
	
	PERSONAGGIO.stampa()

	pygame.display.flip()
	CLOCK.tick(FPS)

pygame.quit()
