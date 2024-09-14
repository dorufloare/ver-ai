from lib.ai import AIController
from lib.utils import *

def main():
    window, game_map = initialize_pygame()
    
    config_file = "./config.txt"
    ai_controller = AIController(config_file, game_map, window)
    
    ai_controller.run()

if __name__ == "__main__":
    main()
