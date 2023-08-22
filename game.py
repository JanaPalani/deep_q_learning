import pygame , random 
pygame.init()
dimensions_display = (600,600)
black = (0,0,0)
red = (250,0,0)
sky_blue = (0,250,250)



player_x = 5
player_y = 295
movement_player, key_pressed , score = 0, False , 0


walls = []
walls_count = len(walls)
def add_walls():
    global wall_opening
    wall_opening =  random.randint(0,500)
    opening_length = random.randint(80,100)
    wall_x = 590 
    walls.append([wall_x,wall_opening,opening_length])

    
    
    



display = pygame.display.set_mode(dimensions_display)

run = True 
clock = pygame.time.Clock()


while run:
    clock.tick(60)
    display.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            key_pressed = True
            if event.key == pygame.K_SPACE:
                print('started flying')
                add_walls()
            
            if event.key == pygame.K_DOWN:
                movement_player = 5

            if event.key == pygame.K_UP:
                movement_player = -5 
            
        if event.type == pygame.KEYUP:
            key_pressed = False
    if key_pressed:
        if movement_player == -5:
            if player_y > 10 :
                player_y += movement_player
        if movement_player == 5:
            if player_y <580:
                player_y += movement_player 

            


    pygame.draw.rect(display,sky_blue,(player_x,player_y,20,10))

    for index,each in enumerate(walls):
        print(each)
        x,opening , length = each
        pygame.draw.rect(display,red,(x,0,5,opening))
        pygame.draw.rect(display,red,(x,opening+length,5,600))
        x -= 3
        walls[index][0] = x
        number_of_walls = len(walls)

        if number_of_walls < 2:
            if x  < 310 : 
                add_walls()


        if x < player_x :
            score += 1
            walls.pop(index)
        
        
        if player_y not in range(opening,opening+length-10) and x in range(player_x , player_x+20)  :
            run = False

    pygame.display.flip()

print(score)