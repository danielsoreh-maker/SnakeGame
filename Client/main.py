"""The Big O-Block - Snake Game Client."""
import requests
import pygame
import time
from Game.logic import SnakeGame

username = input("Ievadi savu lietotājvārdu: ")
print(f"Sveiks, {username}! Spēle tiek lādēta...")
time.sleep(2)

# Krāsas
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
GOLD = pygame.Color(255, 215, 0)
BLUE = pygame.Color(0, 0, 255)
GRID_COLOR = pygame.Color(35, 45, 55)  # Tumši zilganpelēka rūtiņu krāsa

# Iestatījumi
BLOCK_SIZE = 50  # Čūskas un ābola izmērs
WINDOW_SIZE = 750  # Laukuma izmērs (jābūt dalāmam ar BLOCK_SIZE)

pygame.init()
pygame.display.set_caption("The Big O-Block")
game_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
fps = pygame.time.Clock()

game = SnakeGame(WINDOW_SIZE, BLOCK_SIZE)
# Fonts rezultātam (jādefinē vienu reizi pirms cikla)
score_font = pygame.font.SysFont("Courier New", 25)

def draw_grid():
  for x in range(0, WINDOW_SIZE, BLOCK_SIZE):
    pygame.draw.line(game_window, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
  for y in range(0, WINDOW_SIZE, BLOCK_SIZE):
    pygame.draw.line(game_window, GRID_COLOR, (0, y), (WINDOW_SIZE, y))

# --- SĀKUMA EKRĀNS (MAIN MENU) ---
in_menu = True
while in_menu:
    game_window.fill(BLACK)
    draw_grid()

    # Spēles nosaukums
    title_font = pygame.font.SysFont("Courier New", 42, bold=True)
    title_surface = title_font.render("THE BIG O-BLOCK", True, BLUE)
    title_rect = title_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 160))
    game_window.blit(title_surface, title_rect)

    # Sveicens ar ievadīto vārdu
    user_font = pygame.font.SysFont("Courier New", 22,bold=True)
    user_surface = user_font.render(f"Spēlētājs: {username}", True, GOLD)
    user_rect = user_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 50))
    game_window.blit(user_surface, user_rect)

    # "Press ENTER to start" uzraksts
    start_font = pygame.font.SysFont("Courier New", 20, bold=True)
    start_surface = start_font.render("Press ENTER to start", True, WHITE)
    start_rect = start_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 50))
    game_window.blit(start_surface, start_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter taustiņš sākt spēli
                in_menu = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
paused = False # Pauzes ekrānam
running = True # Dzīve ciklam

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False  # ESC aizver spēli
      elif event.key == pygame.K_p:
        paused = not paused # Pauze spelei ar "P"
      elif not paused:
        if event.key == pygame.K_UP or event.key == pygame.K_w:
          game.change_to = "UP"
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          game.change_to = "DOWN"
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
          game.change_to = "LEFT"
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          game.change_to = "RIGHT"
        elif event.key == pygame.K_SPACE:
          game.activate_matrix_effect() # Palaist laika palēnināšanu vai aktivizēt mehāniku
  if paused:
    game_window.fill(BLACK)
    pause_font = pygame.font.SysFont("Courier New", 45, bold=True)
    pause_surface = pause_font.render("PAUZE (Nospied P)",True, BLUE)
    pause_rect = pause_surface.get_rect(
      center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 100)
    )
    game_window.blit(pause_surface, pause_rect)
    pygame.display.update()
    fps.tick(10)
    continue    

      
   # Loģikas atjaunināšana
  is_alive = game.update()
  if not is_alive:
    # --- "GAME OVER" EKRĀNS ---
    game_window.fill(BLACK)

    # 1. Lielais virsraksts
    game_over_font = pygame.font.SysFont("Trebuchet MS", 60, bold=True)
    go_surface = game_over_font.render("SPĒLE BEIGUSIES!", True, RED)
    go_rect = go_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 130))
    game_window.blit(go_surface, go_rect)

    # 2. Score parāde
    score_over_font = pygame.font.SysFont("Courier New", 35, bold=True)
    score_over_surface = score_over_font.render(
        f"Gala rezultāts: {game.score}", True, BLUE
    )
    score_over_rect = score_over_surface.get_rect(
        center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 30)
    )
    game_window.blit(score_over_surface, score_over_rect)

    # 3. Mazākā rindiņa apakšā
    sub_font = pygame.font.SysFont("Consolas", 30)
    sub_surface = sub_font.render("R - Restartēt, ESC - Iziet", True, WHITE)
    sub_rect = sub_surface.get_rect(
        center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 45)
    )
    game_window.blit(sub_surface, sub_rect)

    pygame.display.update()

    # --- NOSŪTĀM REZULTĀTU UZ SERVERI ---
    try:
        url = "http://127.0.0.1:8000/scores"  # Tavs API servera adrese
        payload = {
            "username": username,
            "score": game.score
        }
        # Ja serveris prasa tokenu, to varēs pievienot headers, bet pagaidām sūtām JSON
        response = requests.post(url, json=payload, timeout=3)
        
        if response.status_code in [200, 201]:
            print("Rezultāts veiksmīgi saglabāts serverī!")
        else:
            print(f"Serveris atgrieza kļūdu: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Uzmanību: Neizdevās savienoties ar serveri! (Serveris nav ieslēgts)")

    # Gaidām lietotāja izvēli
    waiting = True
    while waiting:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          waiting = False
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            waiting = False
            running = False
          elif event.key == pygame.K_r:
            # Izveidojam jaunu spēles objektu un turpinām ciklu!
            game = SnakeGame(WINDOW_SIZE, BLOCK_SIZE)
            waiting = False

  # Vizuālā daļa
  game_window.fill(BLACK)
  draw_grid()

  # 1. Čūskas zīmēšana(uzlabotais ver)... beta still
  for i, pos in enumerate(game.snake_body):
    # Uzzīmējam ķermeņa posmu ar nedaudz noapaļotiem stūriem un atstarpēm, lai redzētu blokus
    rect = pygame.Rect(
        pos[0] + 2, pos[1] + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4
    )
    pygame.draw.rect(game_window, GREEN, rect, border_radius=8)

    # Ja šis ir pirmais posms (galva - i == 0), uzzīmējam acis atkarībā no virziena
    if i == 0:
      eye_color = BLACK  # Melnas acis
      if game.direction == "RIGHT":
        eye1 = (pos[0] + 35, pos[1] + 12)
        eye2 = (pos[0] + 35, pos[1] + 38)
      elif game.direction == "LEFT":
        eye1 = (pos[0] + 15, pos[1] + 12)
        eye2 = (pos[0] + 15, pos[1] + 38)
      elif game.direction == "UP":
        eye1 = (pos[0] + 12, pos[1] + 15)
        eye2 = (pos[0] + 38, pos[1] + 15)
      else:  # DOWN
        eye1 = (pos[0] + 12, pos[1] + 35)
        eye2 = (pos[0] + 38, pos[1] + 35)

      pygame.draw.circle(game_window, eye_color, eye1, 5)
      pygame.draw.circle(game_window, eye_color, eye2, 5)


  # 2. Ābola zīmēšana (Noapaļots ar kātiņu un lapiņu)...Beta
  apple_color = GOLD if game.is_super_fruit else RED
  apple_rect = pygame.Rect(
        game.fruit_position[0] + 8,
        game.fruit_position[1] + 12,
        BLOCK_SIZE - 16,
        BLOCK_SIZE - 16,
    )
  # Ābola ķermenis ar noapaļotiem stūriem
  pygame.draw.rect(game_window, apple_color, apple_rect, border_radius=14)

  # Brūns kātiņš
  stem_color = (139, 69, 19)
  stem_rect = pygame.Rect(
        game.fruit_position[0] + BLOCK_SIZE // 2 - 3,
        game.fruit_position[1] + 1,
        7,   # Kātiņa platums
        13,  # Kātiņa garums
    )
  pygame.draw.rect(game_window, stem_color, stem_rect, border_radius=3)

  # Zaļa lapiņa blakus kātiņam
  leaf_color = (0, 220, 0)
  pygame.draw.ellipse(
      game_window,
      leaf_color,
      pygame.Rect(
          game.fruit_position[0] + BLOCK_SIZE // 2 - 2,
          game.fruit_position[1] + 2,
          16,
          10,
      ),
  )
  # 3. Punktu skaitītāja zīmēšana
  score_surface = score_font.render(f"Punkti: {game.score}", True, WHITE)
  game_window.blit(score_surface, (10, 10))

  # --- MATRIX EFEKTS UN ENERĢIJAS LĪNIJa ---
  # Ja Matrix ir aktīvs, palēninām kadru nomaiņu (laika palēnināšana)
  actual_speed = game.current_speed // 2 if game.is_matrix_active else game.current_speed
  
  bar_width = 200
  bar_height = 15
  bar_x = WINDOW_SIZE - 220
  bar_y = 15
  
  # Fons stienītim
  pygame.draw.rect(game_window, (30, 41, 59), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
  # Aktīvā enerģija
  current_bar_width = int(bar_width * (game.energy / 100))
  energy_color = (0, 255, 200) if not game.is_matrix_active else (250, 204, 21)
  pygame.draw.rect(game_window, energy_color, (bar_x, bar_y, current_bar_width, bar_height), border_radius=4)

  pygame.display.update()
  fps.tick(actual_speed)

pygame.quit()