import unittest
import pygame
import os
import random
from Laki_laki import KarakterLaki_laki, Drum_Bergerak, Drum_Diam, Pesawat

class TestKarakterLaki_laki(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.Laki_laki = KarakterLaki_laki()

    def test_initial_state(self):
        self.assertFalse(self.Laki_laki.Laki_laki_duck)
        self.assertTrue(self.Laki_laki.Laki_laki_run)
        self.assertFalse(self.Laki_laki.Laki_laki_jump)
        self.assertEqual(self.Laki_laki.k_rect.x, 80)
        self.assertEqual(self.Laki_laki.k_rect.y, 390)

    def test_duck(self):
        self.Laki_laki.duck()
        self.assertEqual(self.Laki_laki.k_rect.y, 410)

    def test_run(self):
        self.Laki_laki.run()
        self.assertEqual(self.Laki_laki.k_rect.y, 390)

    def test_jump(self):
        self.Laki_laki.Laki_laki_jump = True
        self.Laki_laki.jump()
        self.assertLess(self.Laki_laki.k_rect.y, 390)

class TestObstacles(unittest.TestCase):
    def setUp(self):
        self.drum_bergerak = Drum_Bergerak(pygame.image.load(os.path.join("Assets/Design", "drum_gerak.png")))
        self.drum_diam = Drum_Diam(pygame.image.load(os.path.join("Assets/Design", "drum_diam.png")))
        self.pesawat = Pesawat(pygame.image.load(os.path.join("Assets/Design", "pesawat.png")))

    def test_drum_bergerak_position(self):
        self.assertEqual(self.drum_bergerak.rect.y, 445)

    def test_drum_diam_position(self):
        self.assertEqual(self.drum_diam.rect.y, 420)

    def test_pesawat_position(self):
        self.assertEqual(self.pesawat.rect.y, 350)

if __name__ == "__main__":
    unittest.main()
