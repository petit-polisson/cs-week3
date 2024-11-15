import pygame
import csv
from picture import Picture
from player import Player
import random
import matplotlib.pyplot as plt


def plot_comparison(player_list, best_game,number_of_game):

    if len(player_list) != len(best_game)or len(player_list)!=len(number_of_game):
        print("Error : data lists not the same length.")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(player_list, best_game, color="skyblue", edgecolor="black")


    plt.xlabel("Players", fontsize=14)
    plt.ylabel("Personal Best (Score)", fontsize=14)
    plt.title("Player Personal Best Scores", fontsize=16)
    
    
    for i, score in enumerate(best_game):
        plt.text(i, score + 0.1, f"{score:.2f}\nnb of game{number_of_game[i]}", ha='center', fontsize=10, color='darkblue')
    
    plt.tight_layout()
    plt.show()


def plot_evolution(jumps_evolution, position_evolution,player_name,average_jumps,average_position):

    if len(jumps_evolution) != len(position_evolution):
        print("Error : data lists not same length.")
        return
    

    games = list(range(1, len(jumps_evolution) + 1))

    plt.figure(figsize=(10, 6))
    

    plt.plot(games, jumps_evolution, marker='o', label="Jumps Evolution", color="blue")
    plt.plot(games, position_evolution, marker='s', label="Position Evolution", color="green")

    plt.xlabel("Game Number", fontsize=14)
    plt.ylabel("Jumps and Position(*100)", fontsize=14)
    plt.title(f'Evolution of Jumps and Position by Game for {player_name} ', fontsize=16)
    plt.xticks(games, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)

    info_text = ""
    info_text += f"Average Jumps: {average_jumps}\n"
    info_text += f"Average Position: {average_position}"
    
    if info_text:
        plt.text(
            0.95, 0.95, info_text,
            transform=plt.gca().transAxes,
            fontsize=12,
            color="darkred",
            ha="right",
            va="top",
            bbox=dict(facecolor="white", edgecolor="darkred", boxstyle="round,pad=0.5")
        )
    
    plt.tight_layout()
    plt.show()

def play(filename):
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def save_data(jump_counter, player_name,position):
    with open("csv_files/data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([player_name, jump_counter,position])

def sort_data():
    with open("csv_files/data.csv", mode="r") as file:
        reader = csv.reader(file)
        data = list(reader)  
    data_sorted = sorted(data, key=lambda x: int(x[2]), reverse=True)

    with open("csv_files/sorted_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data_sorted)

def leaderboard_data(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < 5:  
                data.append(row)
            else:
                break 
    return data

def set_timer():
    stop_music()
    pygame.time.set_timer(OPEN_EVENT, 1000)
    pygame.time.wait(250)
    play("sound/son.mp3")
    pygame.time.wait(250)
    pygame.time.set_timer(CLOSE_EVENT, 1000)


def player_data(player_name):
    total_jumps = 0
    total_position = 0
    number_of_game = 0
    jumps_evolution = []
    position_evolution = []
    
    try:
        with open("csv_files/data.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            
            for row in reader:
                if len(row) < 3:
                    continue
                
                if row[0] == player_name:
                    jump_counter = int(row[1])
                    position = int(row[2])  
                    
                    total_jumps += jump_counter
                    total_position += position
                    jumps_evolution.append(jump_counter)
                    position_evolution.append(position/100)
                    number_of_game += 1
                    
        if number_of_game > 0:
            average_jumps = total_jumps / number_of_game
            average_position = total_position / number_of_game
            return int(average_jumps), int(average_position), number_of_game, jumps_evolution, position_evolution
        else:
          
            return None, None, 0, [], []
    except FileNotFoundError:
        print("Erreur : le fichier data.csv est introuvable.")
        return None, None, 0, [], []
    except ValueError:
        print("Erreur : données incorrectes dans le fichier CSV.")
        return None, None, 0, [], []
    
def player_comparison():

    player_list = []
    best_game = []
    number_of_game=[]
    
    try:
        with open("csv_files/data.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            
            for row in reader:
                if len(row) < 3:  
                    continue
                
                player_name = row[0]
                position = int(row[2]) 
                
                
              
                if player_name in player_list:
                    index = player_list.index(player_name)
                    best_game[index] = max(best_game[index], position)
                    number_of_game[index]+=1
                else:
                    player_list.append(player_name)
                    best_game.append(position)
                    number_of_game.append(1)
    
        return player_list, best_game, number_of_game
    
    except FileNotFoundError:
        print("Erreur : le fichier data.csv est introuvable.")
        return [], []
    except ValueError:
        print("Erreur : données incorrectes dans le fichier CSV.")
        return [], []

# Initialisation of pygame
pygame.init()

# Variables & constants
leaderboard=[]
ground_level = 120
screen_height = 720
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Boy")
OPEN_EVENT = pygame.USEREVENT + 1
CLOSE_EVENT = pygame.USEREVENT +2
open_event_active = False
paused=False
menu=True
running = True
dt = 0
jump_counter = 0

# picture loading
earth = Picture("graphics/earth.png", 2, 300, -800)
spaceship3_2 = Picture("graphics/spaceship3.2.png", 3, 300, 550)
spaceship3_1 = Picture("graphics/spaceship3.1.png", 3, 300, 550)
spaceship2 = Picture("graphics/spaceship2.png", 3, 0, -350)
spaceship = Picture("graphics/spaceship.png", 2.5, 0, 100)
star2 = Picture("graphics/stars2.png", 3, 740, -500)
star1 = Picture("graphics/stars.png", 3, 240, 0)
moon = Picture("graphics/moon.png", 1, 140, -80)
alien = Player("graphics/alien-vf.png", 2.5, 600, 540)



# Boucle principale du jeu
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == OPEN_EVENT:
            open_event_active = True
        elif event.type == CLOSE_EVENT:
            open_event_active = False
        if event.type == pygame.KEYDOWN and open_event_active:
            if event.key == pygame.K_SPACE:
                alien.jump()
                jump_counter += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not menu:
                    stop_music()
                    play("sound/menu.mp3")
                else:
                    set_timer()
                menu=not menu   
            elif event.key == pygame.K_p:
                paused=not paused


    if menu:

        screen.fill((0,0,0))
        font = pygame.font.Font(None, 200)
        menu_text = font.render(f"Menu", True, (255, 255, 255))
        screen.blit(menu_text, (430, 100))
        font = pygame.font.Font(None, 80)
        enter_text = font.render(f"press m to enter", True, (255, 255, 255))
        screen.blit(enter_text, (130, 250))
        leaderboard=leaderboard_data("csv_files/sorted_data.csv")
        for i, item in enumerate(leaderboard):
            print(i, item)
            font = pygame.font.Font(None, 50)
            u=font.render(f'Name: {item[0]}  Jump Counter: {item[1]} Position: {item[2]}', True, (255, 255, 255))
            screen.blit(u, (100, 350+50*i))

        

        pygame.display.flip()
        print(f"menu",alien.relative_position)
        continue

    if paused:
        font = pygame.font.Font(None, 200)
        paused_text = font.render(f"PAUSED", True, (255, 0, 0))
        screen.blit(paused_text, (380, 300))
        pygame.display.flip()
        print(f"paused",alien.relative_position)
        continue



    alien.isOutOfScreen()
    if alien.isOutOfScreen1 == True:
        running = False
        print("oos floor")
    if alien.isOutOfScreen2==True:
        alien.relative_position=alien.rel_position(moon.position())
        alien.isOutOfScreen2=False
        print("oos top")
    screen.fill((0, 0, 0))

    # Mises à jour des objets et des positions
    if jump_counter > 7:
        earth.update(dt, screen_width, 10, "d")
        spaceship.update(dt, screen_width, 70, "d")
        spaceship2.update(dt, screen_width, 70, "d")
        moon.update(dt, screen_width, 100, "d")
        ground_level -= 100 + 1 * dt / 1000
        star1.update(dt, screen_width, 10, "d")
        star2.update(dt, screen_width, 10, "d")
        spaceship3_2.update(dt, screen_width, 2500 * dt, "u")
    spaceship.update(dt, screen_width, 250, "r")
    spaceship2.update(dt, screen_width, 20, "r")
    spaceship.update(dt, screen_width, 250, "r")
    spaceship2.update(dt, screen_width, 20, "r")

    # Dessiner les images
    earth.draw(screen)
    star1.draw(screen)
    star2.draw(screen)
    moon.draw(screen)
    spaceship.draw(screen)
    spaceship2.draw(screen)
    if jump_counter > 7:
        spaceship3_2.draw(screen)
    else:
        spaceship3_1.draw(screen)
    spaceship.draw(screen)
    spaceship2.draw(screen)
    
    # Mettre à jour et dessiner le joueur avec gravité
    alien.update(dt, screen_height, ground_level)
    alien.draw(screen)

    # Affichage du score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Jump Counter: {jump_counter}", True, (255, 255, 255))
    height_text = font.render(f"Your Height: {alien.rel_position(moon.position())-alien.relative_position}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(height_text, (10, 40))


    # Mise à jour de l'écran
    pygame.display.flip()

player_name = ""
entering_name = True
r=random.randint(0, 255)
g=random.randint(0, 255)
b=random.randint(0, 255)
timer=0
stop_music()
play("sound/Dumaya.mp3")

while entering_name:
    timer+=1
    if timer>1000:
        timer=0
        r=random.randint(0, 255)
        g=random.randint(0, 255)
        b=random.randint(0, 255)
    screen.fill((r,g,b))
    font = pygame.font.Font(None, 48)
    name_text = font.render(f'Enter your name:', True, (0,0,0))
    screen.blit(name_text, (screen_width // 2 - 100, screen_height // 2 - 50))
    
    player_name_text = font.render(player_name, True, (0,0,0))
    screen.blit(player_name_text, (screen_width // 2 - 100, screen_height // 2))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            entering_name = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                save_data(jump_counter, player_name,alien.rel_position(moon.position())-alien.relative_position)
                sort_data()
                average_jumps, average_position, number_of_game,jumps_evolution,position_evolution=player_data(player_name)
                plot_evolution(jumps_evolution,position_evolution,player_name,average_jumps,average_position)
                player_list,best_game,number_of_game =player_comparison()
                plot_comparison(player_list,best_game,number_of_game)
                entering_name = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += event.unicode

pygame.quit()
