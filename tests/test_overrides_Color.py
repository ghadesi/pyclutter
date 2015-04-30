import unittest
import warnings

import gi.overrides

try:
    from gi.repository import Clutter
    Clutter # pyflakes
except ImportError as err:
    print(err)
    Clutter = None

@unittest.skipUnless(Clutter, 'Clutter not available')
class TestClutterColor(unittest.TestCase):
    def test_color_empty(self):
        color = Clutter.Color()
        self.assertEqual(color.red, 0)
        self.assertEqual(color.green, 0)
        self.assertEqual(color.blue, 0)
        self.assertEqual(color.alpha, 0)

    def test_color_init_flat(self):
        color = Clutter.Color(32, 64, 128, 255)
        self.assertEqual(color.red, 32)
        self.assertEqual(color.green, 64)
        self.assertEqual(color.blue, 128)
        self.assertEqual(color.alpha, 255)

    def test_color_init_named(self):
        color = Clutter.Color(red=64, alpha=128)
        self.assertEqual(color.red, 64)
        self.assertEqual(color.green, 0)
        self.assertEqual(color.blue, 0)
        self.assertEqual(color.alpha, 128)
