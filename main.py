import pygame
import sys
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS
from src.utils.renderer import Renderer
from src.data_manager import DataManager
from src.game_state_manager import GameStateManager
from src.states.menu_state import MenuState
from src.states.hub_state import HubState
from src.states.battle_state import BattleState
from src.states.admin_state import AdminState

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Initialize Core Systems
    renderer = Renderer(screen)
    data_manager = DataManager()
    state_manager = GameStateManager(renderer, data_manager)

    # Register States
    state_manager.register_state("menu", MenuState(renderer))
    state_manager.register_state("hub", HubState(renderer))
    state_manager.register_state("battle", BattleState(renderer))
    state_manager.register_state("admin", AdminState(renderer))

    # Start Game
    state_manager.change_state("menu")

    running = True
    while running:
        dt = clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        state_manager.update(dt, events)
        state_manager.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
