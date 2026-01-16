
import pygame
import random
import math
import time
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 120

# Modern Color Palette
class Colors:
    # Background gradients
    BG_PRIMARY = (12, 15, 25)
    BG_SECONDARY = (18, 22, 35)
    BG_ACCENT = (25, 30, 45)

    # UI Elements
    UI_PRIMARY = (255, 255, 255)
    UI_SECONDARY = (180, 190, 210)
    UI_ACCENT = (120, 140, 180)
    UI_MUTED = (80, 90, 110)

    # Game Elements
    PADDLE_PRIMARY = (64, 123, 255)
    PADDLE_GLOW = (100, 150, 255)
    BALL_PRIMARY = (255, 255, 255)
    BALL_TRAIL = (180, 200, 255)

    # Brick Colors (Modern flat design)
    BRICK_TIER_1 = (46, 204, 113)    # Emerald
    BRICK_TIER_2 = (52, 152, 219)    # Peter River
    BRICK_TIER_3 = (155, 89, 182)    # Amethyst
    BRICK_TIER_4 = (241, 196, 15)    # Sun Flower
    BRICK_TIER_5 = (231, 76, 60)     # Alizarin
    BRICK_SPECIAL = (230, 126, 34)   # Carrot

    # Power-ups
    POWERUP_SPEED = (231, 76, 60)
    POWERUP_MULTI = (46, 204, 113)
    POWERUP_PADDLE = (52, 152, 219)
    POWERUP_LASER = (241, 196, 15)
    POWERUP_SHIELD = (155, 89, 182)
    POWERUP_LIFE = (26, 188, 156)

    # Status colors
    SUCCESS = (46, 204, 113)
    WARNING = (241, 196, 15)
    DANGER = (231, 76, 60)
    INFO = (52, 152, 219)

@dataclass
class GameSettings:
    """Game configuration settings"""
    paddle_speed: float = 600.0
    ball_speed: float = 400.0
    brick_rows: int = 8
    brick_cols: int = 12
    powerup_chance: float = 0.2
    lives: int = 3
    enable_particles: bool = True
    enable_sounds: bool = True
    enable_screen_shake: bool = True

class PowerUpType(Enum):
    SPEED_BOOST = ("Speed Boost", "⚡", Colors.POWERUP_SPEED)
    MULTI_BALL = ("Multi Ball", "●", Colors.POWERUP_MULTI)
    WIDE_PADDLE = ("Wide Paddle", "━", Colors.POWERUP_PADDLE)
    LASER_PADDLE = ("Laser Paddle", "▲", Colors.POWERUP_LASER)
    SHIELD = ("Shield", "◐", Colors.POWERUP_SHIELD)
    EXTRA_LIFE = ("Extra Life", "♥", Colors.POWERUP_LIFE)

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"
    SETTINGS = "settings"

class UIElement:
    """Base class for UI elements with animations"""

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target_x = x
        self.target_y = y
        self.alpha = 255
        self.target_alpha = 255
        self.scale = 1.0
        self.target_scale = 1.0
        self.hover = False

    def animate_to(self, x: float, y: float, duration: float = 0.3):
        """Animate to new position"""
        self.target_x = x
        self.target_y = y

    def update(self, dt: float):
        """Update animations"""
        # Smooth position interpolation
        self.x += (self.target_x - self.x) * dt * 8
        self.y += (self.target_y - self.y) * dt * 8

        # Alpha animation
        self.alpha += (self.target_alpha - self.alpha) * dt * 10

        # Scale animation
        self.scale += (self.target_scale - self.scale) * dt * 12

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width * self.scale, self.height * self.scale)

class ModernButton(UIElement):
    """Modern flat design button with hover effects"""

    def __init__(self, x: float, y: float, width: float, height: float, 
                 text: str, font: pygame.font.Font, 
                 bg_color: Tuple[int, int, int] = Colors.UI_ACCENT,
                 text_color: Tuple[int, int, int] = Colors.UI_PRIMARY):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_scale = 1.05
        self.click_scale = 0.95
        self.pressed = False

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> bool:
        """Handle mouse events"""
        rect = self.get_rect()
        mouse_over = rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEMOTION:
            if mouse_over and not self.hover:
                self.hover = True
                self.target_scale = self.hover_scale
            elif not mouse_over and self.hover:
                self.hover = False
                self.target_scale = 1.0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_over and event.button == 1:
                self.pressed = True
                self.target_scale = self.click_scale
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.pressed = False
                self.target_scale = self.hover_scale if self.hover else 1.0

        return False

    def draw(self, screen: pygame.Surface):
        """Draw button with modern design"""
        rect = self.get_rect()

        # Draw shadow
        shadow_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width, rect.height)
        shadow_color = (*Colors.BG_PRIMARY, 100)
        pygame.draw.rect(screen, shadow_color[:3], shadow_rect, border_radius=8)

        # Draw button background
        color_intensity = 0.8 if self.pressed else (1.1 if self.hover else 1.0)
        bg_color = tuple(min(255, int(c * color_intensity)) for c in self.bg_color)
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)

        # Draw border
        border_color = tuple(min(255, int(c * 1.2)) for c in self.bg_color)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

class Particle:
    """Advanced particle system with multiple types"""

    def __init__(self, x: float, y: float, particle_type: str = "default"):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.life = 1.0
        self.max_life = 1.0

        if particle_type == "explosion":
            self.vx = random.uniform(-300, 300)
            self.vy = random.uniform(-400, -100)
            self.size = random.uniform(3, 8)
            self.color = random.choice([Colors.BRICK_TIER_1, Colors.BRICK_TIER_2, Colors.BRICK_TIER_3])
            self.max_life = 1.5
        elif particle_type == "trail":
            self.vx = random.uniform(-50, 50)
            self.vy = random.uniform(-100, 100)
            self.size = random.uniform(1, 3)
            self.color = Colors.BALL_TRAIL
            self.max_life = 0.5
        elif particle_type == "sparkle":
            self.vx = random.uniform(-100, 100)
            self.vy = random.uniform(-200, -50)
            self.size = random.uniform(2, 5)
            self.color = Colors.UI_PRIMARY
            self.max_life = 1.0

        self.life = self.max_life

    def update(self, dt: float):
        """Update particle"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 500 * dt  # Gravity
        self.life -= dt

        # Fade and shrink
        life_ratio = self.life / self.max_life
        self.alpha = int(255 * life_ratio)
        self.current_size = self.size * life_ratio

    def draw(self, screen: pygame.Surface):
        """Draw particle"""
        if self.life > 0 and self.current_size > 0:
            color = (*self.color, max(0, min(255, self.alpha)))
            pygame.draw.circle(screen, color[:3], (int(self.x), int(self.y)), 
                             max(1, int(self.current_size)))

    def is_alive(self) -> bool:
        return self.life > 0

class ModernBrick:
    """Modern brick with clean design and animations"""

    def __init__(self, x: float, y: float, width: float, height: float, tier: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tier = tier
        self.max_health = tier
        self.health = tier
        self.destroyed = False

        # Animation properties
        self.scale = 1.0
        self.target_scale = 1.0
        self.alpha = 255
        self.hit_flash = 0.0
        self.shake_x = 0.0
        self.shake_y = 0.0

        # Color mapping
        self.colors = {
            1: Colors.BRICK_TIER_1,
            2: Colors.BRICK_TIER_2,
            3: Colors.BRICK_TIER_3,
            4: Colors.BRICK_TIER_4,
            5: Colors.BRICK_TIER_5
        }

    def hit(self) -> bool:
        """Handle brick being hit"""
        self.health -= 1
        self.hit_flash = 0.3
        self.target_scale = 1.1

        # Shake effect
        self.shake_x = random.uniform(-3, 3)
        self.shake_y = random.uniform(-3, 3)

        if self.health <= 0:
            self.destroyed = True
            self.target_scale = 0.0
            return True
        return False

    def update(self, dt: float):
        """Update brick animations"""
        # Scale animation
        self.scale += (self.target_scale - self.scale) * dt * 8
        if not self.destroyed:
            self.target_scale = 1.0

        # Hit flash
        if self.hit_flash > 0:
            self.hit_flash -= dt * 3

        # Shake decay
        self.shake_x *= 0.9
        self.shake_y *= 0.9

        # Alpha for destruction
        if self.destroyed:
            self.alpha = max(0, self.alpha - dt * 500)

    def draw(self, screen: pygame.Surface):
        """Draw brick with modern design"""
        if self.alpha <= 0:
            return

        # Calculate position with shake
        draw_x = self.x + self.shake_x
        draw_y = self.y + self.shake_y

        # Scale rectangle
        scaled_width = self.width * self.scale
        scaled_height = self.height * self.scale
        offset_x = (self.width - scaled_width) / 2
        offset_y = (self.height - scaled_height) / 2

        rect = pygame.Rect(draw_x + offset_x, draw_y + offset_y, scaled_width, scaled_height)

        # Get base color
        base_color = self.colors.get(self.health, Colors.BRICK_TIER_1)

        # Apply hit flash
        if self.hit_flash > 0:
            flash_intensity = self.hit_flash / 0.3
            base_color = tuple(min(255, int(c + (255 - c) * flash_intensity)) for c in base_color)

        # Apply alpha
        if self.alpha < 255:
            base_color = (*base_color, int(self.alpha))

        # Draw shadow
        if self.scale > 0.5:
            shadow_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width, rect.height)
            pygame.draw.rect(screen, (*Colors.BG_PRIMARY, 50), shadow_rect, border_radius=6)

        # Draw brick
        pygame.draw.rect(screen, base_color[:3], rect, border_radius=6)

        # Draw subtle border
        border_color = tuple(min(255, int(c * 1.2)) for c in base_color[:3])
        pygame.draw.rect(screen, border_color, rect, 1, border_radius=6)

        # Draw health indicator
        if self.health > 1:
            font = pygame.font.Font(None, 16)
            health_text = font.render(str(self.health), True, Colors.UI_PRIMARY)
            text_rect = health_text.get_rect(center=rect.center)
            screen.blit(health_text, text_rect)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

class ModernBall:
    """Modern ball with trail effects and smooth physics"""

    def __init__(self, x: float, y: float, radius: float = 10):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = random.choice([-300, 300])
        self.vy = -400
        self.active = True

        # Visual effects
        self.trail_points = []
        self.glow_size = radius * 2
        self.pulse_timer = 0

    def update(self, dt: float):
        """Update ball physics and effects"""
        if not self.active:
            return

        # Update trail
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > 15:
            self.trail_points.pop(0)

        # Move ball
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Wall collisions
        if self.x <= self.radius:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x >= WINDOW_WIDTH - self.radius:
            self.x = WINDOW_WIDTH - self.radius
            self.vx = -abs(self.vx)

        if self.y <= self.radius:
            self.y = self.radius
            self.vy = abs(self.vy)

        # Check if ball fell off screen
        if self.y > WINDOW_HEIGHT + 50:
            self.active = False

        # Update pulse effect
        self.pulse_timer += dt * 8
        self.glow_size = self.radius * 2 + math.sin(self.pulse_timer) * 3

    def draw(self, screen: pygame.Surface):
        """Draw ball with modern effects"""
        if not self.active:
            return

        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail_points):
            alpha_ratio = (i + 1) / len(self.trail_points)
            trail_radius = int(self.radius * alpha_ratio * 0.6)
            if trail_radius > 0:
                trail_color = (*Colors.BALL_TRAIL, int(alpha_ratio * 100))
                pygame.draw.circle(screen, trail_color[:3], 
                                 (int(trail_x), int(trail_y)), trail_radius)

        # Draw glow
        glow_surface = pygame.Surface((self.glow_size * 2, self.glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*Colors.BALL_PRIMARY, 20), 
                          (int(self.glow_size), int(self.glow_size)), int(self.glow_size))
        screen.blit(glow_surface, (self.x - self.glow_size, self.y - self.glow_size))

        # Draw ball
        pygame.draw.circle(screen, Colors.BALL_PRIMARY, (int(self.x), int(self.y)), int(self.radius))

        # Draw highlight
        highlight_pos = (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3))
        pygame.draw.circle(screen, (*Colors.UI_PRIMARY, 150), highlight_pos, int(self.radius * 0.4))

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class ModernPaddle:
    """Modern paddle with smooth animations and effects"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 16
        self.base_width = 120
        self.speed = 600

        # Visual effects
        self.glow_intensity = 1.0
        self.pulse_timer = 0

        # Power-ups
        self.wide_paddle_timer = 0
        self.laser_timer = 0
        self.shield_timer = 0
        self.lasers = []

    def update(self, dt: float, keys):
        """Update paddle"""
        # Handle input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * dt

        # Keep on screen
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))

        # Update power-up timers
        if self.wide_paddle_timer > 0:
            self.wide_paddle_timer -= dt
            self.width = self.base_width * 1.6
        else:
            self.width = self.base_width

        if self.laser_timer > 0:
            self.laser_timer -= dt

        if self.shield_timer > 0:
            self.shield_timer -= dt

        # Update lasers
        for laser in self.lasers[:]:
            laser['y'] -= 800 * dt
            if laser['y'] < 0:
                self.lasers.remove(laser)

        # Update visual effects
        self.pulse_timer += dt * 6
        self.glow_intensity = 0.8 + 0.2 * math.sin(self.pulse_timer)

    def shoot_laser(self):
        """Shoot laser if available"""
        if self.laser_timer > 0:
            self.lasers.append({
                'x': self.x + self.width / 2,
                'y': self.y,
                'width': 4,
                'height': 20
            })

    def apply_powerup(self, powerup_type: PowerUpType):
        """Apply power-up effect"""
        if powerup_type == PowerUpType.WIDE_PADDLE:
            self.wide_paddle_timer = 12.0
        elif powerup_type == PowerUpType.LASER_PADDLE:
            self.laser_timer = 15.0
        elif powerup_type == PowerUpType.SHIELD:
            self.shield_timer = 20.0

    def draw(self, screen: pygame.Surface):
        """Draw paddle with modern design"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Draw glow
        glow_alpha = int(50 * self.glow_intensity)
        glow_rect = pygame.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
        pygame.draw.rect(screen, (*Colors.PADDLE_GLOW, glow_alpha), glow_rect, border_radius=10)

        # Draw paddle
        pygame.draw.rect(screen, Colors.PADDLE_PRIMARY, rect, border_radius=8)

        # Draw highlight
        highlight_rect = pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height // 2)
        pygame.draw.rect(screen, (*Colors.UI_PRIMARY, 100), highlight_rect, border_radius=6)

        # Draw shield effect
        if self.shield_timer > 0:
            shield_alpha = int(100 * (self.shield_timer / 20.0))
            shield_rect = pygame.Rect(self.x - 8, self.y - 8, self.width + 16, self.height + 16)
            pygame.draw.rect(screen, (*Colors.POWERUP_SHIELD, shield_alpha), shield_rect, 
                           3, border_radius=12)

        # Draw lasers
        for laser in self.lasers:
            laser_rect = pygame.Rect(laser['x'] - laser['width'] // 2, laser['y'], 
                                   laser['width'], laser['height'])
            pygame.draw.rect(screen, Colors.POWERUP_LASER, laser_rect, border_radius=2)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

class UltimateBrickBreaker:
    """Ultimate Brick Breaker game with clean modern UI"""

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ultimate Brick Breaker - Clean UI Edition")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.lives = 3
        self.level = 1
        self.high_score = self.load_high_score()
        self.combo_multiplier = 1.0
        self.combo_timer = 0

        # Game objects
        self.paddle = ModernPaddle(WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT - 80)
        self.balls = []
        self.bricks = []
        self.powerups = []
        self.particles = []

        # UI elements
        self.buttons = {}
        self.create_ui_elements()

        # Effects
        self.screen_shake = 0
        self.background_particles = []
        self.create_background_particles()

        # Initialize first level
        self.reset_level()

    def create_ui_elements(self):
        """Create modern UI elements"""
        button_width = 200
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2

        self.buttons = {
            'play': ModernButton(center_x, 400, button_width, button_height, 
                               "PLAY", self.font_medium, Colors.SUCCESS),
            'settings': ModernButton(center_x, 470, button_width, button_height, 
                                   "SETTINGS", self.font_medium, Colors.INFO),
            'quit': ModernButton(center_x, 540, button_width, button_height, 
                               "QUIT", self.font_medium, Colors.DANGER),
            'back': ModernButton(50, WINDOW_HEIGHT - 100, 120, 40, 
                               "BACK", self.font_small, Colors.UI_ACCENT),
            'restart': ModernButton(center_x, 450, button_width, button_height, 
                                  "RESTART", self.font_medium, Colors.WARNING),
            'menu': ModernButton(center_x, 520, button_width, button_height, 
                               "MAIN MENU", self.font_medium, Colors.UI_ACCENT)
        }

    def create_background_particles(self):
        """Create ambient background particles"""
        for _ in range(20):
            particle = {
                'x': random.uniform(0, WINDOW_WIDTH),
                'y': random.uniform(0, WINDOW_HEIGHT),
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-20, 20),
                'size': random.uniform(1, 3),
                'alpha': random.uniform(30, 80),
                'pulse_speed': random.uniform(1, 3)
            }
            self.background_particles.append(particle)

    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            with open('ultimate_brick_breaker_score.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0

    def save_high_score(self):
        """Save high score and statistics"""
        try:
            data = {
                'high_score': self.high_score,
                'games_played': getattr(self, 'games_played', 1),
                'total_bricks_destroyed': getattr(self, 'total_bricks_destroyed', 0)
            }
            with open('ultimate_brick_breaker_score.json', 'w') as f:
                json.dump(data, f)
        except:
            pass

    def reset_level(self):
        """Reset level with new layout"""
        self.balls = [ModernBall(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)]
        self.powerups = []
        self.particles = []
        self.combo_multiplier = 1.0
        self.combo_timer = 0

        self.create_brick_layout()

    def create_brick_layout(self):
        """Create modern brick layout"""
        self.bricks = []
        brick_width = 80
        brick_height = 25
        margin = 8
        start_y = 120

        # Calculate grid
        total_width = WINDOW_WIDTH - 2 * margin
        cols = (total_width + margin) // (brick_width + margin)
        start_x = (WINDOW_WIDTH - (cols * (brick_width + margin) - margin)) // 2

        rows = min(10, 4 + self.level)

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + margin)
                y = start_y + row * (brick_height + margin)

                # Create tier pattern
                tier = min(5, (row // 2) + 1)

                # Skip some bricks for interesting patterns
                if random.random() < 0.05 and row > 2:
                    continue

                brick = ModernBrick(x, y, brick_width, brick_height, tier)
                self.bricks.append(brick)

    def handle_collisions(self):
        """Handle all game collisions with modern physics"""
        for ball in self.balls[:]:
            if not ball.active:
                continue

            ball_rect = ball.get_rect()

            # Paddle collision with improved physics
            if ball_rect.colliderect(self.paddle.get_rect()) and ball.vy > 0:
                # Calculate hit position for angle variation
                hit_pos = (ball.x - self.paddle.x) / self.paddle.width
                hit_pos = max(0, min(1, hit_pos))

                # Convert to angle (-60 to 60 degrees)
                angle = (hit_pos - 0.5) * 120 * math.pi / 180
                speed = math.sqrt(ball.vx**2 + ball.vy**2)

                ball.vx = speed * math.sin(angle)
                ball.vy = -abs(speed * math.cos(angle))

                # Ensure minimum upward velocity
                if ball.vy > -200:
                    ball.vy = -200

                self.screen_shake = 8

                # Create impact particles
                for _ in range(8):
                    particle = Particle(ball.x, ball.y, "sparkle")
                    self.particles.append(particle)

            # Brick collisions
            for brick in self.bricks[:]:
                if brick.destroyed or brick.alpha <= 0:
                    continue

                if ball_rect.colliderect(brick.get_rect()):
                    # Improved collision detection
                    dx = ball.x - (brick.x + brick.width / 2)
                    dy = ball.y - (brick.y + brick.height / 2)

                    if abs(dx) / brick.width > abs(dy) / brick.height:
                        ball.vx = -ball.vx
                    else:
                        ball.vy = -ball.vy

                    # Hit brick
                    destroyed = brick.hit()

                    if destroyed:
                        # Score with combo multiplier
                        points = brick.tier * 50 * int(self.combo_multiplier)
                        self.score += points

                        # Update combo
                        self.combo_multiplier = min(5.0, self.combo_multiplier + 0.2)
                        self.combo_timer = 3.0

                        # Create destruction particles
                        for _ in range(15):
                            particle = Particle(brick.x + brick.width/2, 
                                               brick.y + brick.height/2, "explosion")
                            self.particles.append(particle)

                        # Powerup chance
                        if random.random() < 0.25:
                            # Create powerup (implementation would go here)
                            pass

                        self.screen_shake = 6

                    break

    def update_background_particles(self, dt: float):
        """Update ambient background particles"""
        for particle in self.background_particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt

            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = WINDOW_WIDTH
            elif particle['x'] > WINDOW_WIDTH:
                particle['x'] = 0

            if particle['y'] < 0:
                particle['y'] = WINDOW_HEIGHT
            elif particle['y'] > WINDOW_HEIGHT:
                particle['y'] = 0

            # Pulse effect
            particle['alpha'] = 30 + 50 * abs(math.sin(time.time() * particle['pulse_speed']))

    def draw_background(self):
        """Draw modern gradient background"""
        # Create gradient
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(Colors.BG_PRIMARY[0] + (Colors.BG_SECONDARY[0] - Colors.BG_PRIMARY[0]) * ratio)
            g = int(Colors.BG_PRIMARY[1] + (Colors.BG_SECONDARY[1] - Colors.BG_PRIMARY[1]) * ratio)
            b = int(Colors.BG_PRIMARY[2] + (Colors.BG_SECONDARY[2] - Colors.BG_PRIMARY[2]) * ratio)

            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        # Draw background particles
        for particle in self.background_particles:
            color = (*Colors.UI_ACCENT, int(particle['alpha']))
            pygame.draw.circle(self.screen, color[:3], 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))

    def draw_modern_ui(self):
        """Draw clean modern UI"""
        # Top panel
        panel_height = 100
        panel_surface = pygame.Surface((WINDOW_WIDTH, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*Colors.BG_ACCENT, 200))
        self.screen.blit(panel_surface, (0, 0))

        # Score
        score_text = self.font_large.render(f"{self.score:,}", True, Colors.UI_PRIMARY)
        self.screen.blit(score_text, (30, 25))

        score_label = self.font_small.render("SCORE", True, Colors.UI_SECONDARY)
        self.screen.blit(score_label, (30, 65))

        # High Score
        high_score_text = self.font_medium.render(f"BEST: {self.high_score:,}", True, Colors.UI_ACCENT)
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 35))
        self.screen.blit(high_score_text, high_score_rect)

        # Lives
        lives_x = WINDOW_WIDTH - 150
        lives_text = self.font_large.render(str(self.lives), True, Colors.UI_PRIMARY)
        self.screen.blit(lives_text, (lives_x, 25))

        lives_label = self.font_small.render("LIVES", True, Colors.UI_SECONDARY)
        self.screen.blit(lives_label, (lives_x, 65))

        # Level
        level_text = self.font_medium.render(f"LEVEL {self.level}", True, Colors.UI_SECONDARY)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 70))
        self.screen.blit(level_text, level_rect)

        # Combo multiplier
        if self.combo_multiplier > 1.1:
            combo_text = self.font_medium.render(f"×{self.combo_multiplier:.1f}", True, Colors.WARNING)
            combo_rect = combo_text.get_rect(center=(WINDOW_WIDTH - 80, 70))
            self.screen.blit(combo_text, combo_rect)

    def draw_menu(self):
        """Draw modern main menu"""
        self.draw_background()

        # Title
        title_text = self.font_title.render("BRICK BREAKER", True, Colors.UI_PRIMARY)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = self.font_medium.render("Ultimate Clean Edition", True, Colors.UI_ACCENT)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(subtitle_text, subtitle_rect)

        # High score display
        if self.high_score > 0:
            high_score_text = self.font_small.render(f"Best Score: {self.high_score:,}", True, Colors.UI_SECONDARY)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 320))
            self.screen.blit(high_score_text, high_score_rect)

        # Draw buttons
        for button_name in ['play', 'settings', 'quit']:
            if button_name in self.buttons:
                self.buttons[button_name].draw(self.screen)

    def update(self, dt: float):
        """Update game state"""
        if self.state != GameState.PLAYING:
            return

        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= dt
        else:
            self.combo_multiplier = max(1.0, self.combo_multiplier - dt * 0.5)

        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= dt * 20

        # Update game objects
        keys = pygame.key.get_pressed()
        self.paddle.update(dt, keys)

        for ball in self.balls[:]:
            ball.update(dt)
            if not ball.active:
                self.balls.remove(ball)

        for brick in self.bricks:
            brick.update(dt)

        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)

        # Update UI elements
        for button in self.buttons.values():
            button.update(dt)

        # Handle collisions
        self.handle_collisions()

        # Check game conditions
        if not self.balls:
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
            else:
                self.balls = [ModernBall(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)]

        # Check level complete
        if not any(not brick.destroyed for brick in self.bricks):
            self.level += 1
            self.state = GameState.LEVEL_COMPLETE

    def draw(self):
        """Main draw function"""
        self.draw_background()
        self.update_background_particles(1/60)  # Assume 60 FPS for background

        if self.state == GameState.MENU:
            self.draw_menu()

        elif self.state == GameState.PLAYING:
            # Draw game objects
            for brick in self.bricks:
                brick.draw(self.screen)

            self.paddle.draw(self.screen)

            for ball in self.balls:
                ball.draw(self.screen)

            for particle in self.particles:
                particle.draw(self.screen)

            self.draw_modern_ui()

        elif self.state == GameState.GAME_OVER:
            # Draw game state
            for brick in self.bricks:
                brick.draw(self.screen)
            self.paddle.draw(self.screen)
            for ball in self.balls:
                ball.draw(self.screen)
            self.draw_modern_ui()

            # Game over overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((*Colors.BG_PRIMARY, 180))
            self.screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = self.font_title.render("GAME OVER", True, Colors.DANGER)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
            self.screen.blit(game_over_text, game_over_rect)

            # Final score
            final_score_text = self.font_large.render(f"Final Score: {self.score:,}", True, Colors.UI_PRIMARY)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, 360))
            self.screen.blit(final_score_text, final_score_rect)

            # Draw restart and menu buttons
            self.buttons['restart'].draw(self.screen)
            self.buttons['menu'].draw(self.screen)

    def handle_events(self):
        """Handle events with modern UI"""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle button events
            for button_name, button in self.buttons.items():
                if button.handle_event(event, mouse_pos):
                    if button_name == 'play' and self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                        self.score = 0
                        self.lives = 3
                        self.level = 1
                        self.reset_level()
                    elif button_name == 'quit':
                        return False
                    elif button_name == 'restart' and self.state == GameState.GAME_OVER:
                        self.state = GameState.PLAYING
                        self.score = 0
                        self.lives = 3
                        self.level = 1
                        self.reset_level()
                    elif button_name == 'menu':
                        self.state = GameState.MENU

            # Game-specific events
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.paddle.shoot_laser()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

        return True

    def run(self):
        """Main game loop"""
        running = True
        last_time = time.time()

        while running:
            current_time = time.time()
            dt = min(current_time - last_time, 1/30)  # Cap delta time
            last_time = current_time

            running = self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = UltimateBrickBreaker()
    game.run()
