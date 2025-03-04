from .helpers import path_exists

#* --- Admin ---
# admin
RUN_AS_ADMIN = True

#* --- Player ---
# x pos
X_VELOCITY = 5

# y pos
GRAVITY = 0.5

# size
PLAYER_SIZE = (50, 50)

#* ------- Game -------
# -~-~- font and text -~-~-
# ~~~ font ~~~
GAME_FONT = path_exists("wobbo/assets/fonts/game_font.ttf")

# ~~~ text ~~~
# - titles -~
# title sizes
LEVEL_TITLE_SIZE_FACTOR = 0.05
SPECS_TEXT_SIZE_FACTOR = 0.04

# title effects
LEVEL_TITLE_FADE_TIME = 500
LEVEL_TITLE_FADE_SPEED = 1