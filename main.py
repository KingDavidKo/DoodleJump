###############################
### Name: David Kofman
### Date: 6/21/2022
### Description: Final Project! A re-creation of the classic game Doodle Jump. Move the doodle from left to right, keep on the look out for rockets, and avoid monsters and blackholes. Don't fall, and try to get the highest score possible!
###############################

import pygame
pygame.init()
from random import randint
from replit import db

#Initialize global game variables
HEIGHT = 800
WIDTH  = 600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREEN = (106, 186, 23)
WHITE = (255,255,255)
BLUE = (7, 150, 199)
BLACK = (0,0,0)
PEACH = (245, 231, 210)
HONEY = (212, 154, 66)
BURGUNDY = (172, 0, 0)
font = pygame.font.Font("COMIC.TTF",30)
highScore = 0

#Initialize images
background = pygame.image.load("background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
introbackground = pygame.image.load("introbackground.jpg").convert_alpha()
introbackground = pygame.transform.scale(introbackground, (WIDTH,HEIGHT))
doodleRight = pygame.image.load("doodle.webp").convert_alpha()
doodleRight = pygame.transform.scale(doodleRight, (60,60))
doodleLeft = pygame.transform.flip(doodleRight,True,False)
gameOver = pygame.image.load("gameOver.png").convert_alpha()
doodleRocketRight = pygame.image.load("doodleRocket.png")
doodleRocketRight = pygame.transform.scale(doodleRocketRight, (60,60))
doodleRocketLeft = pygame.transform.flip(doodleRocketRight,True,False)
rocketImage = pygame.image.load("rocket.png")
rocketImage = pygame.transform.scale(rocketImage, (60,60))
blackholeImage = pygame.image.load("blackhole.png")
blackholeImage = pygame.transform.scale(blackholeImage, (100,100))
monsterImages = []
for i in range(1,11):
  monsterImages.append(pygame.image.load("Monster"+str(i)+".png"))

#Initialize Sounds
jumpSound=pygame.mixer.Sound("Jump-Sound.mp3")
rocketSound = pygame.mixer.Sound("Rocket-Sound.mp3")
gameOverSound = pygame.mixer.Sound("Sad-Trombone.ogg")
monsterSound = pygame.mixer.Sound("MonsterSound.mp3")
vanishSound = pygame.mixer.Sound("Vanish.ogg")

#Defining Classes
class Doodle():
  def __init__(self):
    self.bodySize = 60
    self.x = 285
    self.y = 400
    self.xSpeed = 0
    self.ySpeed = 20
    self.gravity = 1
    self.image = doodleRight
    self.score = 0
    self.rocketBoost = False

  def drawPlayer(self):
    screen.blit(self.image,(self.x,self.y))

  def moveRight(self):
    if self.rocketBoost:
      self.image = doodleRocketRight
    else:
      self.image = doodleRight
    self.xSpeed = 15

  def moveLeft(self):
    if self.rocketBoost:
      self.image = doodleRocketLeft
    else:
      self.image = doodleLeft
    self.xSpeed = -15

  def jump(self): 
    self.ySpeed = 20
    jumpSound.play(loops=0)
  
  def move(self):
    self.y -= self.ySpeed
    self.ySpeed -= self.gravity
    self.x += self.xSpeed
  
  def collisionPlatform(self, platformList):
    for i in platformList:
      if i.y - (self.y+60)<=10 and i.y-(self.y+60)>=-30 and self.x+40-i.x>=0 and self.x-i.x <=50 and self.ySpeed<0:  
        self.jump()

  def collisionTemporaryPlatform(self, i):
    if i.y -(self.y+60)<=10 and i.y-(self.y+60)>=-30 and self.x+40-i.x>=0 and self.x-i.x <=50 and self.ySpeed<0 and i.visible:   
        vanishSound.play(loops=0)
        self.jump()
        i.visible = False

  def collisionOutside(self):
    #If the doodle crosses either side, it spawns on the opposite side (teleports through)
    if self.x < 0:
      self.x = 600
    elif self.x>600:
      self.x = 0 

  def collisionRocket(self,rocket):
    if self.x+30>rocket.x and self.x<rocket.x+30 and self.y+30>rocket.y and self.y<rocket.y+30 and rocket.visible:
      rocketSound.play(loops=0)
      self.ySpeed=40
      rocket.visible = False
      self.rocketBoost = True
      if doodle.image == doodleRight: 
        doodle.image = doodleRocketRight
      if doodle.image == doodleLeft: 
        doodle.image = doodleRocketLeft

  def collisionBlackhole(self,blackhole):
    if self.x+30>blackhole.x and self.x<blackhole.x+50 and self.y+30>blackhole.y and self.y<blackhole.y+50:
      return True

  def collisionMonster(self,monster):
    if self.x+30>monster.x and self.x<monster.x+monster.bodySizeX-20 and self.y+30>monster.y and self.y<monster.y+monster.bodySizeY-10:
      return True

class Platform():
  def __init__(self,position):
    self.sizeX = 70
    self.sizeY = 10
    self.x = randint(0,530)
    self.y = 100*position
    self.xSpeed = 0
    self.CLR = GREEN

  def drawPlatform(self):
    pygame.draw.rect(screen, self.CLR, (self.x, self.y, self.sizeX,self.sizeY),0,3)

  def shiftPlatform(self,doodle):
    if doodle.y<250 and doodle.ySpeed>0:
      self.y += doodle.ySpeed

    if self.y>800:
      self.x = randint(0,530)
      self.y = -10
      doodle.score += 1

    if self.x<0 or self.x>530:
      self.xSpeed = -self.xSpeed
    self.x += self.xSpeed

class TemporaryPlatform():
  def __init__(self):
    self.sizeX = 70
    self.sizeY = 10
    self.x = randint(0,530)
    self.y = -80
    self.xSpeed = 0
    self.visible = False

  def drawPlatform(self):
    pygame.draw.rect(screen, WHITE, (self.x, self.y, self.sizeX,self.sizeY),0,3)
    pygame.draw.rect(screen, BLACK, (self.x, self.y, self.sizeX,self.sizeY),1,3)

  def shiftPlatform(self,doodle):
    if doodle.y<250 and doodle.ySpeed>0:
      self.y += doodle.ySpeed

    if self.y>800:
      self.x = randint(0,530)
      self.y = -10
      doodle.score += 1

    if self.x<0 or self.x>530:
      self.xSpeed = -self.xSpeed
    self.x += self.xSpeed

class Rocket():
  def __init__(self,x,y,i):
    self.bodySize = 60
    self.x = x
    self.y = y-60
    self.image = rocketImage
    self.visible = False
    self.platform = i
  def drawRocket(self):
    screen.blit(self.image,(self.x,self.y))
  def shiftRocket(self,doodle,platformList):
    if doodle.y<250 and doodle.ySpeed>0:
      self.y+= doodle.ySpeed
    if self.visible:
      self.x = platformList[self.platform].x
    
class Blackhole():
  def __init__(self):
    self.bodySize = 100
    self.x = randint(0,500)
    self.y = -30
    self.image = blackholeImage
  def drawBlackhole(self):
    screen.blit(self.image,(self.x,self.y))
  def shiftBlackhole(self,doodle):
    if doodle.y<250 and doodle.ySpeed>0:
      self.y+= doodle.ySpeed

class Monster():
  def __init__(self):
    self.image = monsterImages[randint(0,9)]
    self.bodySizeX = self.image.get_width()
    self.bodySizeY = self.image.get_height()
    self.x = randint(0,400)
    self.y = -300
    self.xSpeed = 3
  def drawMonster(self):
    screen.blit(self.image,(self.x,self.y))
  def shiftMonster(self,doodle):
    #Shift the monster relative to the doodle, and move it right and left
    if doodle.y<250 and doodle.ySpeed>0:
      self.y += doodle.ySpeed
    if self.x<=0 or self.x+self.bodySizeX>=600:
      self.xSpeed = -self.xSpeed
    self.x += self.xSpeed
    #Makes sure that the sound is only playing one at a time, while the monster has not passed
    sound = pygame.mixer.Channel(5)
    if not sound.get_busy() and self.y<800:
      sound.play(monsterSound)

def redrawScreen(doodle, platformList,highScore,blackhole,rocket,monster,temporaryPlatform):
  #Display game information
  screen.blit(background,(0,0))
  scoreText = font.render("Score: " + str(doodle.score),0,0)
  screen.blit(scoreText,(0,0))
  highScoreText = font.render("High Score: " + str(highScore),0,0)
  screen.blit(highScoreText,(0,30))
  screen.blit(scoreText,(0,0))
  #Checks for collisions and draws and shifts all of objects
  doodle.collisionRocket(rocket)
  for i in platformList:
    i.drawPlatform()
    i.shiftPlatform(doodle)
  if temporaryPlatform.visible:
    temporaryPlatform.drawPlatform()
    temporaryPlatform.shiftPlatform(doodle)
  blackhole.drawBlackhole()
  blackhole.shiftBlackhole(doodle)
  monster.drawMonster()
  monster.shiftMonster(doodle)
  if rocket.visible:  
    rocket.drawRocket()
  rocket.shiftRocket(doodle,platformList)
  if doodle.ySpeed<=0 and doodle.rocketBoost:
    doodle.rocketBoost = False
    if doodle.image == doodleRocketRight: 
      doodle.image = doodleRight
    if doodle.image == doodleRocketLeft: 
       doodle.image = doodleLeft
  doodle.collisionOutside()
  doodle.drawPlayer()
  doodle.move()
  doodle.collisionPlatform(platformList)
  doodle.collisionTemporaryPlatform(temporaryPlatform)
  #Checks if the doodle fell, collided with a Blackhole, or collided with a Monster
  if doodle.y > HEIGHT or doodle.collisionBlackhole(blackhole) or doodle.collisionMonster(monster):
    pygame.mixer.stop()
    return False
  else:
    return True
  
def startGameScreen(y,CLR=PEACH):
  #Displays all of the designs of the intro screen
  screen.blit(introbackground,(0,0))
  screen.blit(monsterImages[5],(450,60))
  screen.blit(doodleRight,(60,y))
  pygame.draw.rect(screen, GREEN, (50,620,70,10),0,3)
  pygame.draw.ellipse(screen, CLR, (175,200,150,60), 0)
  pygame.draw.ellipse(screen, HONEY, (175,200,150,60), 5)
  play = font.render("Play",0,0)
  screen.blit(play,(225,205))

def endGameScreen(allTimeHighScore, CLR=PEACH):
  #Displays all of the end game information (Score, Highscore, and All Time Highscore)
  font = pygame.font.Font("COMIC.TTF",40)
  screen.blit(background,(0,0))
  screen.blit(gameOver,(100,25))
  scoreText = font.render("Score: " + str(doodle.score),0,0)
  screen.blit(scoreText,(100,200))
  highScoreText = font.render("High Score: " + str(highScore),0,0)
  screen.blit(highScoreText,(100,275))
  AllTimeHighScoreText = font.render("All Time High Score: " + str(allTimeHighScore),0,0)
  screen.blit(AllTimeHighScoreText,(100,350))
  #Displays the button
  pygame.draw.ellipse(screen, CLR, (215,480,175,80), 0)
  pygame.draw.ellipse(screen, HONEY, (215,480,175,80), 5)
  font = pygame.font.Font("COMIC.TTF",30)
  playAgain = font.render("Play Again",0,0)
  screen.blit(playAgain,(235,495))

exitFlag = False
introScreen = True
while not exitFlag:
  #Initializes/resets all of the objects
  platformList = []
  for i in range(7):
    platformList.append(Platform(i))
  doodle = Doodle()
  blackhole = Blackhole()
  blackhole.y = 800
  monster = Monster()
  monster.y = 800
  rocket = Rocket(0,850,0)
  temporaryPlatform = TemporaryPlatform()
  temporaryPlatform.y = 800
  for event in pygame.event.get():         # check for any events
    if event.type == pygame.QUIT:
       exitFlag = False
  gravity = 0.003
  ySpeed = 1
  y = 570
  while introScreen:
    #Control the jumping Doodle in the intro screen
    y -= ySpeed
    ySpeed -= gravity
    if y>570:
      ySpeed=1
      #Displays the screen
    startGameScreen(y)
    for event in pygame.event.get():    
      if event.type == pygame.QUIT:    
        introScreen = False
    #Checks if the mouse is hovering over the button. Changes colour if it does
    mouseX,mouseY = pygame.mouse.get_pos()
    if mouseY>200 and mouseY<260 and mouseX>175 and mouseX<325:
      startGameScreen(y,BURGUNDY)
      #Checks if the mouse clicks on the button. Starts the game
      if event.type == pygame.MOUSEBUTTONDOWN:
        introScreen = False
    pygame.display.update()
  
  pygame.mixer.stop()
  gameOn = True
  while gameOn:
    for event in pygame.event.get():         # check for any events 
      if event.type == pygame.QUIT:    
        gameOn=False
      if event.type == pygame.KEYDOWN:  #checks if any keys have been pressed
        if event.key == pygame.K_RIGHT:
          doodle.moveRight()
        if event.key == pygame.K_LEFT:
          doodle.moveLeft()
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
          doodle.xSpeed = 0
        if event.key == pygame.K_LEFT:
          doodle.xSpeed = 0 
    #Spawns a new Blackhole every 9 points
    if doodle.score%9 == 0 and blackhole.y > 800 and doodle.score!=0:
      blackhole = Blackhole()
    #Spawns a new Temporary Platform every 12 points
    if doodle.score%12 == 0  and not temporaryPlatform.visible and doodle.score!=0:
      temporaryPlatform = TemporaryPlatform()
      temporaryPlatform.visible = True
    #Spawns a new Monster every 12 points
    if doodle.score%15 == 0 and monster.y>800 and doodle.score!=0:
      monster = Monster()      
    #Spawns a new Rocket every 26 points. The Rocket's position is linked to the platform it spawns on
    if doodle.score%18 == 0 and not rocket.visible and doodle.score!=0:
      i = -doodle.score%7
      rocket = Rocket(platformList[i].x,platformList[i].y,i)
      rocket.visible = True
    #Every score of 15, a stationary platform turns into a moving platform.
    if doodle.score%14 == 0 and doodle.score!=0 and platformList[-doodle.score%7].CLR == GREEN:
      platformList[-doodle.score%7].CLR = BLUE
      platformList[-doodle.score%7].xSpeed = randint(2,4) * randint(-1,1)
      while platformList[-doodle.score%7].xSpeed == 0:
        platformList[-doodle.score%7].xSpeed = randint(2,4) * randint(-1,1)
    #Resets unused rockets
    if rocket.y>800:
      rocket.visible = False
    gameOn = redrawScreen(doodle,platformList,highScore,blackhole,rocket,monster,temporaryPlatform)
    #Updates highscore
    if doodle.score>highScore:
      highScore = doodle.score
    #Keeps the doodle in the frame
    if doodle.y<-5:
      doodle.y = -5
    pygame.time.delay(60)
    pygame.display.update()

  #Once the game is done, checks if the highscore beats the all-time highscore (stored in Replit databasee)
  if highScore>db["AllTimeHighScore"]:
    db["AllTimeHighScore"] = highScore
  allTimeHighScore = db["AllTimeHighScore"]
  gameOverScreen = True
  gameOverSound.play(loops=0)
  while gameOverScreen:
    endGameScreen(allTimeHighScore)
    for event in pygame.event.get():    
      if event.type == pygame.QUIT:    
        gameOverScreen = False
    #Checks if mouse is hovering over hte button
    mouseX,mouseY = pygame.mouse.get_pos()
    if mouseY>480 and mouseY<560 and mouseX>215 and mouseX<400:
      endGameScreen(allTimeHighScore,BURGUNDY)
      #Checks if user ends the game
      if event.type == pygame.MOUSEBUTTONDOWN:
        gameOverScreen = False
    else:
      endGameScreen(allTimeHighScore) 
    pygame.display.update()

pygame.quit()