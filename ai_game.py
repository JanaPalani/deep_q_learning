import pygame , random , torch 
import numpy as np 
pygame.init()
from collections import deque
from model import QTrainer, Linear_QNet
dimensions_display = (600,600)
black = (0,0,0)
red = (250,0,0)
sky_blue = (0,250,250)



player_x = 5
player_y = 295
player_width = 20
player_heigth = 10
movement_player,  score = 0,  0


# model_parameters
n_games , epsilon , gamma = 0 , 0 , 0.9
memory = deque(maxlen=100_000)  
batch_size = 600 
alpha = 0.05
model = Linear_QNet(4,10,5,3)
trainer = QTrainer(model = model , lr = alpha ,gamma = gamma)

# model.load_state_dict(torch.load("q_learning_model"))
scores = []



walls = []
walls_count = len(walls)
def add_walls():
    global wall_opening
    wall_opening =  random.randint(50,450)
    opening_length = random.randint(100,140)
    wall_x = 590 
    walls.append([wall_x,wall_opening,opening_length])
 

def get_state(player_x,player_y ,wall_x,wall_opening , wall_opening_length):
    distance = wall_x - player_x
    wall_closing = wall_opening+wall_opening_length
    state =   [wall_opening, wall_closing,distance,player_y]
    return np.array(state,dtype=int)


def get_action(state):
    global epsilon 
    epsilon = 80 - n_games
    final_move  = [0,0,0]
    if random.randint(0,200) < epsilon :
        move = random.randint(0,2)
        final_move[move] = 1
    else:
        state0 = torch.tensor(state,dtype=torch.float)
        pred = model(state0)
        move = torch.argmax(pred).item()
        final_move[move] = 1
    return final_move

def short_train(state,action,reward,new_state,done):
    trainer.train_step(state, action, reward, new_state, done)
    

def long_train():
    if len(memory) > batch_size:
        mini_sample = random.sample(memory, batch_size) # list of tuples
    else:
        mini_sample = memory

    states, actions, rewards, next_states, dones = zip(*mini_sample)
    trainer.train_step(states, actions, rewards, next_states, dones)




display = pygame.display.set_mode(dimensions_display)

run = True 
clock = pygame.time.Clock()


while run:
    clock.tick(180)
    display.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                add_walls()
            

    
        
        
 


    pygame.draw.rect(display,sky_blue,(player_x,player_y,player_width,player_heigth))
    
    if len(walls) > 0:
        for index,each in enumerate(walls):
            x,opening , length = each
            pygame.draw.rect(display,red,(x,0,5,opening))
            pygame.draw.rect(display,red,(x,opening+length,5,600))
            x -= 3
            walls[index][0] = x
            number_of_walls = len(walls)
            reward = 0
            done = False
            if number_of_walls < 2:
                if x  < 110 : 
                    add_walls()


            if x < player_x :
                score += 1
                reward = 10
                walls.pop(index)
            
            
            
            if player_y not in range(opening,opening+length-10) and x in range(player_x , player_x+20)  :
                done = True
                player_y = 295
                scores.append(score)
                movement_player, score = 0, 0
                walls=[]
                n_games += 1
                add_walls()
                long_train()
                memory = deque(maxlen=100_00)
                

                break


        state = get_state(player_x,player_y,walls[0][0],walls[0][1],walls[0][2])
        action = get_action(state)
        to_take = action.index(max(action))
        
        if to_take == 1 and player_y > 10:
            player_y -= 5
        elif to_take ==  2 and player_y < 580 :
            player_y += 5
        else:
            player_y += 0
        new_state = get_state(player_x,player_y,walls[0][0],walls[0][1],walls[0][2])
        reward = reward
        memory.append([state,action,reward,new_state,done])
        # short_train(state,action,reward,new_state,done)
        if reward == 10 :
            print([state,action,reward,new_state,done])
        
    
    pygame.display.flip()

    if n_games >= 500 :
        run = False

print(max(scores))
model.save("q_learning_model")