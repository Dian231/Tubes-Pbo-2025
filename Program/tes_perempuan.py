import unittest
import pygame
import random
import os
from Perempuan import KarakterPerempuan, Drum_Bergerak, Drum_Diam, Pesawat

class TestKarakterPerempuan(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.Perempuan = KarakterPerempuan()

    def test_initial_state(self):
        self.assertFalse(self.Perempuan.k_duck)
        self.assertTrue(self.Perempuan.k_run)
        self.assertFalse(self.Perempuan.k_jump)
        self.assertEqual(self.Perempuan.k_rect.x, 80)
        self.assertEqual(self.Perempuan.k_rect.y, 390)

    def test_duck(self):
        self.Perempuan.k_duck = True
        self.Perempuan.k_run = False
        self.Perempuan.k_jump = False
        self.Perempuan.duck()
        self.assertEqual(self.Perempuan.k_rect.y, 410)

    def test_run(self):
        self.Perempuan.k_duck = False
        self.Perempuan.k_run = True
        self.Perempuan.k_jump = False
        self.Perempuan.run()
        self.assertEqual(self.Perempuan.k_rect.y, 390)

    def test_jump(self):
        self.Perempuan.k_jump = True
        initial_y = self.Perempuan.k_rect.y
        self.Perempuan.jump()
        self.assertLess(self.Perempuan.k_rect.y, initial_y)

class TestObstacles(unittest.TestCase):
    def setUp(self):
        self.drum_bergerak = Drum_Bergerak(pygame.image.load(os.path.join("Assets/Design", "drum_gerak.png")).convert_alpha())
        self.drum_diam = Drum_Diam(pygame.image.load(os.path.join("Assets/Design", "drum_diam.png")).convert_alpha())
        self.pesawat = Pesawat(pygame.image.load(os.path.join("Assets/Design", "pesawat.png")).convert_alpha())

    def test_drum_bergerak_position(self):
        self.assertEqual(self.drum_bergerak.rect.y, 445)

    def test_drum_diam_position(self):
        self.assertEqual(self.drum_diam.rect.y, 420)

    def test_pesawat_position(self):
        self.assertEqual(self.pesawat.rect.y, 350)

if __name__ == "__main__":
    unittest.main()
