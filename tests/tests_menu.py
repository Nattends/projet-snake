import unittest
from unittest.mock import patch, MagicMock
import pygame
from core.menu import Menu # Assurez-vous que le chemin d'import est correct

class TestMenu(unittest.TestCase):

    @patch("pygame.display.set_mode")
    @patch("pygame.image.load")
    @patch("utils.helpers.resize_image")
    def setUp(self, mock_resize, mock_load, mock_set_mode):
        pygame.init()
        
        self.mock_background = pygame.Surface((500, 900))  
    
        mock_surface = pygame.Surface((100, 100))
        mock_resize.return_value = mock_surface
        mock_load.return_value = mock_surface
        mock_set_mode.return_value = pygame.Surface((500, 900))
    
        self.menu = Menu(self.mock_background)

    def test_initialization(self):
        self.assertEqual(self.menu.screen_width, 500)
        self.assertEqual(self.menu.screen_height, 900)
        self.assertIsNotNone(self.menu.logo_img)
        self.assertIsNotNone(self.menu.jouer_img)
        self.assertIsNotNone(self.menu.score_img)
        self.assertIsNotNone(self.menu.options_img)

    @patch("pygame.event.get")
    @patch("sys.exit")
    @patch("pygame.quit")
    def test_quit_event(self, mock_quit, mock_exit, mock_event_get):
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]

        with self.assertRaises(SystemExit): 
            self.menu.show()

        mock_quit.assert_called_once()
        mock_exit.assert_called_once()

    @patch("pygame.event.get")
    @patch("menu.SnakeGame")
    def test_click_jouer(self, mock_snake_game, mock_event_get):
        mock_event_get.return_value = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (250, 420)}) 
        ]

        self.menu.show()
        mock_snake_game.assert_called_once_with(self.mock_background)
        mock_snake_game.return_value.run.assert_called_once()

    @patch("pygame.event.get")
    @patch("menu.ScorePage")
    def test_click_score(self, mock_score_page, mock_event_get):
        mock_event_get.return_value = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (250, 520)})  
        ]

        self.menu.show()
        mock_score_page.assert_called_once_with(self.mock_background)
        mock_score_page.return_value.show.assert_called_once()

    @patch("pygame.event.get")
    @patch("menu.OptionsPage")
    def test_click_options(self, mock_options_page, mock_event_get):
        mock_event_get.return_value = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (250, 620)})  
        ]

        self.menu.show()
        mock_options_page.assert_called_once_with(self.mock_background)
        mock_options_page.return_value.show.assert_called_once()

    def tearDown(self):
        pygame.quit() 

if __name__ == "__main__":
    unittest.main()
