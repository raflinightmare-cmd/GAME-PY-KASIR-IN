
import random
import sys

try:
  import pygame
except ModuleNotFoundError as exc:
  raise SystemExit(
      "Pygame belum terinstal. Jalankan 'pip install pygame' lalu coba lagi."
  ) from exc

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasir in Ribut in 🛒💥")
clock = pygame.time.Clock()

# Palet Warna (Eksentrik & Colorful)
BACKGROUND = (44, 62, 80)
WHITE = (255, 255, 255)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)

# Font game
font = pygame.font.SysFont("Arial", 18, bold=True)
font_large = pygame.font.SysFont("Arial", 28, bold=True)


class Player:

  def __init__(self):
    self.x = 400
    self.y = 450
    self.width = 40
    self.height = 50
    self.speed = 5
    self.is_punching = False
    self.punch_timer = 0

  def move(self, keys):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.x -= self.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.x += self.speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
      self.y -= self.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
      self.y += self.speed

    # Batas area kasir
    self.x = max(50, min(WIDTH - 90, self.x))
    self.y = max(250, min(HEIGHT - 80, self.y))

  def draw(self, surface):
    # Badan Kasir
    pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))
    # Kepala & Topi Kasir
    pygame.draw.circle(surface, YELLOW, (self.x + 20, self.y - 10), 14)
    pygame.draw.rect(surface, RED, (self.x + 8, self.y - 24, 24, 10))

    # Efek Pukulan
    if self.is_punching:
      pygame.draw.circle(
          surface, WHITE, (self.x + 45, self.y + 20), 15, width=3
      )
      self.punch_timer -= 1
      if self.punch_timer <= 0:
        self.is_punching = False


class NPC:

  def __init__(self):
    self.x = random.choice([0, WIDTH - 40])
    self.y = random.randint(300, 500)
    self.width = 35
    self.height = 45
    self.speed = 2
    self.state = "SHOPPING"  # SHOPPING, STEALING, RETURNING, FLEEING
    self.has_item = False
    self.timer = 0
    self.dialogue = "Mau beli jajan..."
    self.color = random.choice([PURPLE, GREEN, ORANGE])

  def update(self):
    if self.state == "SHOPPING":
      self.y -= self.speed
      if self.y <= 210:
        self.state = "STEALING"
        self.has_item = True
        self.dialogue = "Comot barang dulu ah! 😼"
        self.timer = 120
    elif self.state == "STEALING":
      # Berjalan mondar-mandir mencoba kabur
      self.x += self.speed if self.x < WIDTH / 2 else -self.speed
      self.dialogue = "Lari ada kasir galak! 🏃💨"
    elif self.state == "RETURNING":
      self.dialogue = "Aduh! Ampun Pak/Bu Kasir! 😭"
      self.timer -= 1
      if self.timer <= 0:
        self.has_item = False
        self.state = "FLEED"
    elif self.state == "FLEED":
      self.y += self.speed * 2
      self.dialogue = "Kapok maling di sini! 💀"

  def draw(self, surface):
    pygame.draw.rect(
        surface, self.color, (self.x, self.y, self.width, self.height)
    )
    pygame.draw.circle(surface, YELLOW, (self.x + 17, self.y - 8), 12)

    if self.has_item:
      # Indikator barang curian di atas kepala NPC
      pygame.draw.rect(surface, RED, (self.x + 10, self.y - 32, 16, 16))

    # Balon teks dialog NPC
    txt = font.render(self.dialogue, True, WHITE)
    surface.blit(txt, (self.x - 25, self.y - 55))


def main():
  player = Player()
  npcs = []
  spawn_timer = 0
  score = 0
  stolen_returned = 0

  running = True
  while running:
    screen.fill(BACKGROUND)

    # Visual Toko (Rak Supermarket & Meja Kasir)
    pygame.draw.rect(
        surface=screen, color=(127, 140, 141), rect=(50, 90, 700, 20)
    )
    txt_shelf = font.render(
        "📦 RAK SUPERMARKET (AWAS BARANG DICURI!)", True, WHITE
    )
    screen.blit(txt_shelf, (60, 60))

    pygame.draw.rect(
        surface=screen, color=(189, 195, 199), rect=(50, 180, 700, 35)
    )
    txt_counter = font_large.render("🏪 MEJA KASIR IN", True, (44, 62, 80))
    screen.blit(txt_counter, (270, 182))

    # Event handling
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          player.is_punching = True
          player.punch_timer = 15
          # Cek jarak pukul ke NPC
          for npc in npcs:
            dist = ((player.x - npc.x) ** 2 + (player.y - npc.y) ** 2) ** 0.5
            if dist < 65:  # Jangkauan pukul
              if npc.has_item:
                npc.state = "RETURNING"
                npc.timer = 50
                score += 100
                stolen_returned += 1
              else:
                npc.dialogue = "Kenapa pukul saya bos?! 🤬"

    # Update & Gambar Player
    player.move(keys)
    player.draw(screen)

    # Spawn NPC secara berkala
    spawn_timer += 1
    if spawn_timer > 80 and len(npcs) < 5:
      npcs.append(NPC())
      spawn_timer = 0

    # Update & Gambar NPC
    for npc in npcs[:]:
      npc.update()
      npc.draw(screen)
      if npc.y > HEIGHT + 60 or npc.y < -60:
        npcs.remove(npc)

    # UI / HUD Permainan
    score_txt = font_large.render(f"Skor: {score}", True, GREEN)
    returned_txt = font.render(
        f"Barang Diselamatkan: {stolen_returned}", True, YELLOW
    )
    controls_txt = font.render(
        "Kontrol: [WASD / Tombol Panah] Gerak  |  [SPASI] Pukul Maling!",
        True,
        WHITE,
    )

    screen.blit(score_txt, (20, 15))
    screen.blit(returned_txt, (20, 50))
    screen.blit(controls_txt, (20, HEIGHT - 35))

    pygame.display.flip()
    clock.tick(FPS)


if __name__ == "__main__":
  main()