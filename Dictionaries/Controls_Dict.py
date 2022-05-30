import pygame
pygame.init()

CONTROLS_DICT = {
    "SWING": pygame.K_c,
    "SWING2": pygame.K_v,
    "MOVE_LEFT": pygame.K_a,
    "MOVE_RIGHT": pygame.K_d,
    "CROUCH": pygame.K_s,
    "JUMP": pygame.K_w,
    "DIVE": pygame.K_LSHIFT,
    "AIRDASH": pygame.K_e
    }
CONTROLS_DICT_2 = {
    "SWING": pygame.K_COMMA,
    "SWING2": pygame.K_m,
    "MOVE_LEFT": pygame.K_LEFT,
    "MOVE_RIGHT": pygame.K_RIGHT,
    "CROUCH": pygame.K_DOWN,
    "JUMP": pygame.K_UP,
    "DIVE": pygame.K_RSHIFT,
    "AIRDASH": pygame.K_o
    }
