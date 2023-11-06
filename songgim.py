import sys
import pygame
import random
from pygame.locals import KEYDOWN, QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((1000,1000))
FPS = pygame.time.Clock()

infection_percent = 50
no_mask = 0
dental_mask = 50 # percentage of infection decrease
kf80 = 80
kf94 = 94
people_map=[]
row_and_column = 200
infected = 0

class person():
    def __init__(self, x, y, mask):
        self.is_infected = False
        self.mask = mask
        self.x = x
        self.y = y
    def cough(self):
        global infected
        for y in range(-1, 2): # spread infection to nearby people
            for x in range(-1, 2):
                person_x = self.x + x
                person_y = self.y + y
                person_x = min(max(0, person_x), row_and_column -1)
                person_y = min(max(0, person_y), row_and_column -1)
                if people_map[person_y][person_x].is_infected:
                    continue
                else:
                    infection_chance = random.randint(1,100) 
                    if infection_chance > infection_percent* (100+self.mask)/100:
                        people_map[person_y][person_x].is_infected = True
                        infected += 1

def spread_virus():
    infected_list=[]
    for people in people_map:
        for person in people:
            if person.is_infected:
                infected_list.append(person)
    for person in infected_list: 
        person.cough()

def move_people():
   list_of_people = []
   for people in people_map:
      list_of_people.extend(people)
   random.shuffle(list_of_people)
   list_return = [list_of_people[row * row_and_column : (row+1) * row_and_column]
                       for row in range(row_and_column)]
   return list_return

def position_reset():
    for y in range(row_and_column):
        for x in range(row_and_column):
            person = people_map[y][x]
            person.x = x
            person.y = y

def draw_people():
    for people in people_map:
        for person in people:
            if person.is_infected:
                person_rect = (person.x * 5, person.y * 5, 5, 5)
                pygame.draw.rect(SURFACE, (255,0,0), person_rect)

def draw_line():
    for index in range(row_and_column):
        pygame.draw.line(SURFACE, (0,0,0), (index * 5, 0), (index * 5, 1000))
        pygame.draw.line(SURFACE, (0,0,0), (0, index * 5), (1000, index * 5))

def simulate_by_days(mask, people_move):
    global people_map
    people_map = [[person(x, y, mask) for x in range(row_and_column)] for y in range(row_and_column)]
    people_map[random.randrange(row_and_column)][random.randrange(row_and_column)].is_infected = True
    days = 0
    font = pygame.font.SysFont(None, 70)
    days_font = font.render('DAY : 0', True, (0,255,255))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if people_move:
                    people_map = move_people()
                    position_reset()
                    spread_virus()
                else:
                    spread_virus()
                days += 1
                days_font = font.render('DAY : {}'.format(days), True, (0,255,255))
        SURFACE.fill((255, 255, 255))
        draw_people()
        draw_line()
        SURFACE.blit(days_font, (20,20))
        pygame.display.update()
        FPS.tick(20)

def get_data(mask, people_move, simulation_hour):
    global people_map
    global infected
    people_map = [[person(x, y, mask) for x in range(row_and_column)] for y in range(row_and_column)]
    people_map[random.randrange(row_and_column)][random.randrange(row_and_column)].is_infected = True
    hours = 0
    infected = 0
    data = []
    while hours < simulation_hour:
        if people_move:
            people_map = move_people()
            position_reset()
            spread_virus()
        else:
            spread_virus()
        hours += 1
        data.append((hours, infected))
    return data

if __name__== '__main__':
    simulate_by_days(kf94, True)



conditions = ((no_mask,False), (no_mask,True), (dental_mask,True), (kf80,True), (kf94,True))
for condition in conditions:
    datas = []
    average = []
    for x in range(10):
        datas.append(get_data(condition[0], condition[1],10))
    for x in range(10):
        num = 0
        for data in datas:
            num += data[x][1]
        average.append(num / 10)
    print(average)