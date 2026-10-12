"""The Big O-Block - Snake Game Client."""
import pygame
from Game.logic import SnakeGame

# Krāsas
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
GOLD = pygame.Color(255, 215, 0)
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


running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False  # ESC aizver spēli
      elif event.key == pygame.K_UP or event.key == pygame.K_w:
        game.change_to = "UP"
      elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        game.change_to = "DOWN"
      elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        game.change_to = "LEFT"
      elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        game.change_to = "RIGHT"
      elif event.key == pygame.K_SPACE:
        # Palaist laika palēnināšanu vai aktivizēt mehāniku
        game.activate_matrix_effect()
        
   # Loģikas atjaunināšana
  is_alive = game.update()
  if not is_alive:
    # --- "GAME OVER" EKRĀNS ---
    game_window.fill(BLACK)

    # 1. Lielais virsraksts
    game_over_font = pygame.font.SysFont("arial", 50, bold=True)
    go_surface = game_over_font.render("SPĒLE BEIGUSIES!", True, RED)
    go_rect = go_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 40))
    game_window.blit(go_surface, go_rect)

    # 2. Mazākā rindiņa apakšā
    sub_font = pygame.font.SysFont("arial", 25)
    sub_surface = sub_font.render("R - Restartēt, ESC - Iziet", True, WHITE)
    sub_rect = sub_surface.get_rect(
        center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 20)
    )
    game_window.blit(sub_surface, sub_rect)

    pygame.display.update()

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

  # 1. Čūskas zīmēšana
  for pos in game.snake_body:
    pygame.draw.rect(
        game_window,
        GREEN,
        pygame.Rect(pos[0], pos[1], BLOCK_SIZE - 1, BLOCK_SIZE - 1),
    )

  # 2. Ābola zīmēšana
  apple_color = GOLD if game.is_super_fruit else RED
  pygame.draw.rect(
      game_window,
      apple_color,
      pygame.Rect(
          game.fruit_position[0],
          game.fruit_position[1],
          BLOCK_SIZE - 1,
          BLOCK_SIZE - 1,
      ),
  )

  # 3. Punktu skaitītāja zīmēšana
  score_surface = score_font.render(f"Punkti: {game.score}", True, WHITE)
  game_window.blit(score_surface, (10, 10))

  pygame.display.update()
  fps.tick(game.current_speed)

pygame.quit()