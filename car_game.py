
try:
    from ursina import *
    from ursina.prefabs.first_person_controller import FirstPersonController
    import random
    import math
    import time

    # Initialize Ursina
    app = Ursina()

    # Game settings
    window.title = "Ultimate 3D Racing Game"
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = False
    window.fps_counter.enabled = True

    # Colors and materials
    class Colors:
        TRACK = color.dark_gray
        GRASS = color.green
        BARRIERS = color.red
        PLAYER_CAR = color.blue
        AI_CAR_1 = color.red
        AI_CAR_2 = color.yellow
        AI_CAR_3 = color.orange
        SKY = color.cyan
        UI_TEXT = color.white

    class GameState:
        def __init__(self):
            self.racing = False
            self.game_over = False
            self.race_time = 0
            self.player_position = 1
            self.lap = 1
            self.total_laps = 3
            self.speed = 0
            self.nitro = 100
            self.countdown = 3

    game_state = GameState()

    # Environment setup
    def create_environment():
        """Create the racing environment"""

        # Sky
        sky = Sky(texture='sky_default')

        # Ground/Grass
        ground = Entity(model='plane', color=Colors.GRASS, scale=200, position=(0, -0.1, 0))

        # Main track (curved oval)
        track_segments = []
        num_segments = 60
        track_radius = 40
        track_width = 12

        for i in range(num_segments):
            angle = (i / num_segments) * 2 * math.pi
            x = math.cos(angle) * track_radius
            z = math.sin(angle) * track_radius

            # Track segment
            segment = Entity(
                model='cube',
                color=Colors.TRACK,
                position=(x, 0, z),
                scale=(track_width, 0.2, 4),
                rotation_y=math.degrees(angle + math.pi/2)
            )
            track_segments.append(segment)

            # Track barriers (inner and outer)
            inner_barrier = Entity(
                model='cube',
                color=Colors.BARRIERS,
                position=(x - math.cos(angle) * (track_width/2 + 2), 0.5, z - math.sin(angle) * (track_width/2 + 2)),
                scale=(0.5, 1, 2)
            )

            outer_barrier = Entity(
                model='cube',
                color=Colors.BARRIERS,
                position=(x + math.cos(angle) * (track_width/2 + 2), 0.5, z + math.sin(angle) * (track_width/2 + 2)),
                scale=(0.5, 1, 2)
            )

        return track_segments

    class Car(Entity):
        """Advanced 3D car with physics"""

        def __init__(self, position=(0, 0, 0), color=Colors.PLAYER_CAR, is_player=False):
            super().__init__(
                model='cube',
                color=color,
                position=position,
                scale=(2, 1, 4)
            )

            self.is_player = is_player
            self.velocity = Vec3(0, 0, 0)
            self.max_speed = 25 if is_player else 20
            self.acceleration = 0.5
            self.turn_speed = 80
            self.friction = 0.95
            self.nitro_boost = 1.0

            # AI specific
            self.ai_target_angle = 0
            self.ai_speed_variation = random.uniform(0.8, 1.2)
            self.lap_progress = 0

            # Visual enhancements
            self.create_car_details()

        def create_car_details(self):
            """Add visual details to the car"""
            # Windshield
            windshield = Entity(
                model='cube',
                color=color.light_gray,
                parent=self,
                position=(0, 0.3, -0.8),
                scale=(1.8, 0.6, 1.5)
            )

            # Wheels
            positions = [(-0.8, -0.3, 1.2), (0.8, -0.3, 1.2), (-0.8, -0.3, -1.2), (0.8, -0.3, -1.2)]
            for pos in positions:
                wheel = Entity(
                    model='cylinder',
                    color=color.black,
                    parent=self,
                    position=pos,
                    scale=(0.4, 0.2, 0.4),
                    rotation=(0, 0, 90)
                )

            # Headlights
            headlight_l = Entity(
                model='cube',
                color=color.white,
                parent=self,
                position=(-0.6, 0.2, 1.8),
                scale=(0.3, 0.3, 0.2)
            )
            headlight_r = Entity(
                model='cube',
                color=color.white,
                parent=self,
                position=(0.6, 0.2, 1.8),
                scale=(0.3, 0.3, 0.2)
            )

        def update_physics(self):
            """Update car physics"""
            if self.is_player:
                self.handle_player_input()
            else:
                self.handle_ai_movement()

            # Apply movement
            self.position += self.velocity * time.dt

            # Apply friction
            self.velocity *= self.friction

            # Keep cars on ground
            self.y = 0.5

            # Update game state for player
            if self.is_player:
                game_state.speed = length(self.velocity) * 10  # Convert to display speed

        def handle_player_input(self):
            """Handle player input"""
            if not game_state.racing:
                return

            # Acceleration
            if held_keys['w'] or held_keys['up arrow']:
                forward = self.forward * self.acceleration * self.nitro_boost
                self.velocity += forward

                # Limit speed
                if length(self.velocity) > self.max_speed:
                    self.velocity = normalize(self.velocity) * self.max_speed

            # Braking
            if held_keys['s'] or held_keys['down arrow']:
                self.velocity *= 0.9

            # Steering
            if held_keys['a'] or held_keys['left arrow']:
                if length(self.velocity) > 0.1:  # Only turn when moving
                    self.rotation_y += self.turn_speed * time.dt

            if held_keys['d'] or held_keys['right arrow']:
                if length(self.velocity) > 0.1:
                    self.rotation_y -= self.turn_speed * time.dt

            # Nitro
            if held_keys['space'] and game_state.nitro > 0:
                self.nitro_boost = 1.5
                game_state.nitro -= 50 * time.dt
            else:
                self.nitro_boost = 1.0
                if game_state.nitro < 100:
                    game_state.nitro += 20 * time.dt

        def handle_ai_movement(self):
            """Simple AI movement"""
            if not game_state.racing:
                return

            # Move forward
            forward = self.forward * self.acceleration * self.ai_speed_variation
            self.velocity += forward

            # Limit speed
            if length(self.velocity) > self.max_speed * self.ai_speed_variation:
                self.velocity = normalize(self.velocity) * self.max_speed * self.ai_speed_variation

            # Follow track (simple circular motion)
            center = Vec3(0, 0, 0)
            to_center = center - self.position
            to_center.y = 0  # Keep on same level

            if length(to_center) != 0:
                # Maintain distance from center (follow track)
                desired_distance = 35  # Track radius
                current_distance = length(to_center)

                if current_distance > desired_distance + 5:
                    # Too far from center, turn inward
                    self.rotation_y += self.turn_speed * time.dt * 0.5
                elif current_distance < desired_distance - 5:
                    # Too close to center, turn outward
                    self.rotation_y -= self.turn_speed * time.dt * 0.5

            # Add some randomness
            if random.random() < 0.01:
                self.rotation_y += random.uniform(-20, 20)

    # Create cars
    def create_cars():
        """Create player and AI cars"""
        # Player car
        player_car = Car(position=(35, 0.5, 0), color=Colors.PLAYER_CAR, is_player=True)

        # AI cars
        ai_cars = []
        ai_positions = [(30, 0.5, 5), (25, 0.5, -5), (40, 0.5, 3)]
        ai_colors = [Colors.AI_CAR_1, Colors.AI_CAR_2, Colors.AI_CAR_3]

        for i, (pos, col) in enumerate(zip(ai_positions, ai_colors)):
            ai_car = Car(position=pos, color=col, is_player=False)
            ai_cars.append(ai_car)

        return player_car, ai_cars

    # Camera system
    class RacingCamera(Entity):
        """Advanced racing camera"""

        def __init__(self, target):
            super().__init__()
            self.target = target
            self.offset = Vec3(0, 8, -15)  # Behind and above the car
            self.smoothness = 5
            self.camera_mode = 0  # 0: behind, 1: cockpit, 2: side

        def update_camera(self):
            """Update camera position"""
            if self.camera_mode == 0:  # Behind car
                target_pos = self.target.position + self.target.back * 15 + self.target.up * 8
                target_rotation = self.target.rotation

            elif self.camera_mode == 1:  # Cockpit view
                target_pos = self.target.position + self.target.up * 2 + self.target.forward * 1
                target_rotation = self.target.rotation

            else:  # Side view
                target_pos = self.target.position + self.target.right * 10 + self.target.up * 5
                target_rotation = (0, self.target.rotation_y - 90, 0)

            # Smooth camera movement
            camera.position = lerp(camera.position, target_pos, time.dt * self.smoothness)
            camera.rotation = lerp(camera.rotation, target_rotation, time.dt * self.smoothness)

    # UI System
    class RacingUI:
        """Advanced racing UI"""

        def __init__(self):
            self.ui_entities = []
            self.create_ui()

        def create_ui(self):
            """Create UI elements"""
            # Speed display
            self.speed_text = Text(
                "Speed: 0", 
                position=(-0.85, 0.45), 
                scale=2, 
                color=Colors.UI_TEXT
            )

            # Position display
            self.position_text = Text(
                "Position: 1/4", 
                position=(-0.85, 0.35), 
                scale=2, 
                color=Colors.UI_TEXT
            )

            # Lap display
            self.lap_text = Text(
                "Lap: 1/3", 
                position=(-0.85, 0.25), 
                scale=2, 
                color=Colors.UI_TEXT
            )

            # Nitro bar background
            self.nitro_bg = Entity(
                model='cube',
                color=color.dark_gray,
                position=(0.7, -0.4, -1),
                scale=(0.3, 0.05, 1)
            )

            # Nitro bar
            self.nitro_bar = Entity(
                model='cube',
                color=color.blue,
                position=(0.7, -0.4, -0.9),
                scale=(0.28, 0.03, 1)
            )

            # Countdown text
            self.countdown_text = Text(
                "", 
                position=(0, 0), 
                scale=5, 
                color=color.yellow,
                origin=(0, 0)
            )

            # Instructions
            instruction_texts = [
                "WASD or Arrow Keys: Drive",
                "Space: Nitro Boost",
                "C: Change Camera",
                "R: Restart Race"
            ]

            for i, text in enumerate(instruction_texts):
                Text(
                    text,
                    position=(0.3, 0.45 - i * 0.05),
                    scale=1,
                    color=color.light_gray
                )

        def update_ui(self):
            """Update UI elements"""
            # Speed
            self.speed_text.text = f"Speed: {int(game_state.speed)}"

            # Position  
            self.position_text.text = f"Position: {game_state.player_position}/4"

            # Lap
            self.lap_text.text = f"Lap: {game_state.lap}/{game_state.total_laps}"

            # Nitro bar
            nitro_ratio = max(0, min(1, game_state.nitro / 100))
            self.nitro_bar.scale_x = 0.28 * nitro_ratio

            # Countdown
            if game_state.countdown > 0:
                if game_state.countdown > 1:
                    self.countdown_text.text = str(int(game_state.countdown))
                else:
                    self.countdown_text.text = "GO!"
                self.countdown_text.enabled = True
            else:
                self.countdown_text.enabled = False

    # Game logic
    def start_countdown():
        """Start race countdown"""
        game_state.countdown = 3
        game_state.racing = False

        def countdown_update():
            if game_state.countdown > 0:
                game_state.countdown -= time.dt
                if game_state.countdown <= 0:
                    game_state.racing = True
                    game_state.race_time = 0

        return countdown_update

    def calculate_positions(player_car, ai_cars):
        """Calculate race positions"""
        all_cars = [player_car] + ai_cars

        # Simple position calculation based on lap progress
        # In a real game, you'd calculate based on track position
        positions = sorted(all_cars, key=lambda car: car.lap_progress, reverse=True)

        for i, car in enumerate(positions):
            if car.is_player:
                game_state.player_position = i + 1
                break

    # Initialize game
    def initialize_game():
        """Initialize the racing game"""
        # Create environment
        track_segments = create_environment()

        # Create cars
        player_car, ai_cars = create_cars()

        # Setup camera
        racing_camera = RacingCamera(player_car)

        # Create UI
        ui = RacingUI()

        # Start countdown
        countdown_func = start_countdown()

        return player_car, ai_cars, racing_camera, ui, countdown_func

    # Game update function
    def update():
        """Main game update function"""
        if 'player_car' in globals():
            # Update countdown
            if hasattr(update, 'countdown_func'):
                update.countdown_func()

            # Update cars
            player_car.update_physics()
            for ai_car in ai_cars:
                ai_car.update_physics()

            # Update camera
            racing_camera.update_camera()

            # Update UI
            ui.update_ui()

            # Update race time
            if game_state.racing:
                game_state.race_time += time.dt

            # Calculate positions
            calculate_positions(player_car, ai_cars)

    # Input handling
    def input(key):
        """Handle input events"""
        if key == 'c':
            # Change camera mode
            racing_camera.camera_mode = (racing_camera.camera_mode + 1) % 3

        elif key == 'r':
            # Restart race
            start_countdown()

        elif key == 'escape':
            # Quit game
            quit()

    # Initialize and start the game
    player_car, ai_cars, racing_camera, ui, countdown_func = initialize_game()

    # Store countdown function for update loop
    update.countdown_func = countdown_func

    # Run the game
    app.run()

except ImportError:
    print("Ursina engine not installed. Installing now...")
    import subprocess
    import sys

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ursina"])
        print("Ursina installed successfully!")
        print("Please run the script again to start the 3D racing game.")
    except subprocess.CalledProcessError:
        print("Failed to install Ursina. Please install manually:")
        print("pip install ursina")

except Exception as e:
    print(f"Error running 3D racing game: {e}")
    print("\nFalling back to 2D Pygame version...")

    # Fallback to the previously created 2D racing game
    exec(open('advanced_car_racing_game.py').read())
