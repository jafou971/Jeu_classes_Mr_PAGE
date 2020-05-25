import pygame, os,time
import random as rd
from pygame.locals import*


from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

pygame.init()

size = width, height = 1920, 1080
fenetre = pygame.display.set_mode((size), FULLSCREEN)
pygame.display.set_caption('NewDarkSpace')
fps = pygame.time.Clock()
font = pygame.font.Font("street cred.ttf", 64)

class ElementGraphique():
	# Le constructeur basique
	def __init__(self, img, x = 0, y = 0):
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height

	def afficher(self, window, img = None) :
		if img is None:
			img = self.image
		window.blit(img, self.rect)

class Perso(ElementGraphique):
	def __init__(self, img, x = 0, y = 0):
		super(Perso, self).__init__(img, x, y)
		self.vie = 4
		self.v = 7

	def deplacement(self, touches):

		self.image = vmilieu.copy()

		if touches[pygame.K_w] and self.rect.y > 0:
			self.rect.y -= self.v

		if touches[pygame.K_a] and self.rect.x > 0:
			self.image = vgauche.copy()
			self.rect.x -= self.v

		if touches[pygame.K_s] and self.rect.y < height - self.rect.h :
			self.rect.y += self.v

		if touches[pygame.K_d] and self.rect.x < width - self.rect.w :
			self.image = vdroite.copy()
			self.rect.x += self.v

		if invincible:
			self.image.fill([255,255,255,128], None, pygame.BLEND_RGBA_MULT)
				
		
class Balles(ElementGraphique):
	def __init__(self, img, x = 0, y = 0):
		super(Balles, self).__init__(img, x , y)
		self.vx = rd.randint(-7, 7)
		self.vy = rd.randint(-7, 7)

	def deplacement(self):
		self.rect.x += self.vx
		if self.rect.x > self.width - self.rect.w:
			 self.vx = -abs(self.vx)
		if self.rect.x < 0:
			self.vx = abs(self.vx)

		self.rect.y += self.vy
		if self.rect.y > self.height - self.rect.h:
			 self.vy = -abs(self.vy)
		if self.rect.y < 0:
			self.vy = abs(self.vy)

class Bonus(Balles):
	def __init__(self, img, x = 0, y = 0):
		super(Bonus, self).__init__(img, x , y)

class Bombes(Balles):
	def __init__(self, img, x = 0, y = 0):
		super(Bombes, self).__init__(img, x , y)

class Life(Balles):
	def __init__(self, img, x = 0, y = 0):
		super(Life, self).__init__(img, x , y)
		
		
imageFond = pygame.image.load("images/fond.jpg").convert_alpha()
fond = ElementGraphique(imageFond)

imageCoeur = pygame.image.load("images/coeur.png").convert_alpha()

vmilieu = pygame.image.load("images/vaisseau1.png").convert_alpha()
vgauche = pygame.image.load("images/vaisseau_gauche.png").convert_alpha()
vdroite = pygame.image.load("images/vaisseau_droite.png").convert_alpha()


perso = Perso(vmilieu, width/2, height/2)

imageBombes = pygame.image.load("images/astéroide.png").convert_alpha()
bombes = Bombes(imageBombes, rd.randint(900,1900),rd.randint(100,1000))

imageBonus = pygame.image.load("images/star (1).png").convert_alpha()
bonus = Bonus(imageBonus, rd.randint(900,1900),rd.randint(100,1000))

continuer = True
invincible = 0
i = 0
score = 0
liste_bombes = []
liste_bonus = []
liste_life = []

while continuer:
	i += 1

	if i % 144 == 0:
		score += 1

	if invincible : 
		invincible -= 1
		
	fps.tick(144)
	touches = pygame.key.get_pressed()
	
	if touches[pygame.K_ESCAPE]:
		continuer = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			continuer = False

	fond.afficher(fenetre)
	
	perso.deplacement(touches)
	perso.afficher(fenetre)

	if i % (144*4) == 0 and len(liste_bombes) < 9:
		liste_bombes.append(Bombes(imageBombes, rd.randint(100,1900),rd.randint(100,1000)))

	for bombes in liste_bombes:
		bombes.afficher(fenetre)
		bombes.deplacement()
		if perso.rect.colliderect(bombes.rect) and not invincible:
			liste_bombes.remove(bombes)
			perso.vie -= 1
	
	for life in liste_life:
		life.afficher(fenetre)
		life.deplacement()
		if perso.rect.colliderect(life.rect):
			liste_life.remove(life)
			perso.vie += 1
	
	if i % (144*20) == 0 and len(liste_life) < 2:
		liste_life.append(Life(pygame.transform.scale(imageCoeur, [64,64]), rd.randint(100,1900),rd.randint(100,1000)))

	if i % (144*12) == 0 and len(liste_bonus) < 2:
		liste_bonus.append(Bonus(imageBonus, rd.randint(100,1900),rd.randint(100,1000)))

	for bonus in liste_bonus:
		bonus.afficher(fenetre)
		bonus.deplacement()
		if perso.rect.colliderect(bonus.rect):
			liste_bonus.remove(bonus)
			invincible += 144*4

	for n in range(perso.vie):
		fenetre.blit(imageCoeur,[int(n*36),0])
	
	fenetre.blit(font.render(str(score), True, [255, 255, 255]), [width - 128, 64])
	

	if perso.vie == 0 :
		continuer = 0
	pygame.display.update()