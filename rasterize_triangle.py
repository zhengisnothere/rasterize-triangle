import sys
from random import randint as ri

import pygame
from pygame.locals import QUIT

pygame.init()
screen_w,screen_h=400,300
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('rasterize triangle')
clock=pygame.time.Clock()
font=pygame.font.SysFont('Arial',10)
res=1

def show_fps():
  fps=str(int(clock.get_fps()))
  text=font.render(fps,True,'white')
  screen.blit(text,(0,0))

class Triangle:
  def __init__(self,p1,p2,p3,color):
    self.p1=p1
    self.p2=p2
    self.p3=p3
    self.color=color

  def sort_points_by_y(self):
    return sorted((self.p1,self.p2,self.p3),key=lambda p:p[1])

  def rasterize(self):
    up,mid,down=self.sort_points_by_y()
    x1,y1=up
    x2,y2=mid
    x3,y3=down
    k1=(x1-x3)/(y1-y3) if y1!=y3 else 0.001
    k2=(x2-x1)/(y2-y1) if y2!=y1 else 0.001
    k3=(x3-x2)/(y3-y2) if y3!=y2 else 0.001
    sx,ex=x1,x1
    for y in range(y1,y3,res):
      ry=int(y/res)*res
      sx+=k1*res
      ex+=k2*res if y<y2 else k3*res
      dir=1 if sx<ex else -1
      rsx=int(sx/res)*res
      rex=int(ex/res)*res
      for x in range(rsx,rex,dir*res):
        pygame.draw.rect(screen,self.color,(x,ry,res,res))
    pygame.draw.polygon(screen,(255,255,255),(up,mid,down),width=1)
    pygame.draw.circle(screen,(255,0,0),up,2)
    pygame.draw.circle(screen,(0,255,0),mid,2)
    pygame.draw.circle(screen,(0,0,255),down,2)

def generate_random_triangle():
  p1=(ri(0,screen_w),ri(0,screen_h))
  p2=(ri(0,screen_w),ri(0,screen_h))
  p3=(ri(0,screen_w),ri(0,screen_h))
  c=(ri(0,255),ri(0,255),ri(0,255))
  return Triangle(p1,p2,p3,c)

triangles=[generate_random_triangle() for i in range(20)]

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  screen.fill((0,0,0))
  for t in triangles:
    t.rasterize()
  show_fps()
  pygame.display.flip()
  clock.tick(30)
