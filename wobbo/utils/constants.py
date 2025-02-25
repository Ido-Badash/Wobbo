from .helpers import path_exists

#* --- Admin ---
# admin
RUN_AS_ADMIN = True

#* --- Player ---
# x pos
X_VELOCITY = 5

# y pos
Y_VELOCITY = 5
JUMP_HEIGHT = 10
GRAVITY = 0.5

# size
PLAYER_SIZE = (50, 50)

#* --- Game ---
# font
GAME_FONT = path_exists("wobbo/assets/fonts/game_font.ttf")