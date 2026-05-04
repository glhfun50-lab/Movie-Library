"""Unit tests for Movie Library validation functions."""
import unittest
from main import MovieLibrary
import tkinter as tk


class TestMovieLibrary(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = MovieLibrary(self.root)
        self.root.withdraw()  # Hide window during tests

    def tearDown(self):
        self.root.destroy()

    def test_validate_year_valid(self):
        """Valid year should return integer."""
        self.assertEqual(self.app.validate_year("2020"), 2020)
        self.assertEqual(self.app.validate_year("1994"), 1994)
        self.assertEqual(self.app.validate_year("1888"), 1888)  # First film

    def test_validate_year_invalid(self):
        """Invalid year should raise ValueError."""
        with self.assertRaises(ValueError):
            self.app.validate_year("abc")
        with self.assertRaises(ValueError):
            self.app.validate_year("")
        with self.assertRaises(ValueError):
            self.app.validate_year("1800")  # Too early
        with self.assertRaises(ValueError):
            self.app.validate_year("3000")  # Too far in future

    def test_validate_rating_valid(self):
        """Valid rating should return float."""
        self.assertEqual(self.app.validate_rating("7.5"), 7.5)
        self.assertEqual(self.app.validate_rating("0"), 0.0)
        self.assertEqual(self.app.validate_rating("10"), 10.0)
        self.assertEqual(self.app.validate_rating("5.5"), 5.5)
        self.assertEqual(self.app.validate_rating("5,5"), 5.5)  # Comma as decimal

    def test_validate_rating_invalid(self):
        """Invalid rating should raise ValueError."""
        with self.assertRaises(ValueError):
            self.app.validate_rating("abc")
        with self.assertRaises(ValueError):
            self.app.validate_rating("-1")
        with self.assertRaises(ValueError):
            self.app.validate_rating("11")
        with self.assertRaises(ValueError):
            self.app.validate_rating("")

    def test_get_filtered_no_filters(self):
        """Filtering with no filters should return all movies."""
        self.app.movies = [
            {"title": "Film A", "genre": "Драма", "year": 2020, "rating": 7.5},
            {"title": "Film B", "genre": "Комедия", "year": 2019, "rating": 8.0},
        ]
        filtered = self.app.get_filtered()
        self.assertEqual(len(filtered), 2)

    def test_get_filtered_by_genre(self):
        """Filtering by genre should return matching movies."""
        self.app.movies = [
            {"title": "Film A", "genre": "Драма", "year": 2020, "rating": 7.5},
            {"title": "Film B", "genre": "Комедия", "year": 2019, "rating": 8.0},
        ]
        self.app.filter_genre_var.set("Драма")
        filtered = self.app.get_filtered()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Film A")

    def test_get_filtered_by_year_range(self):
        """Filtering by year range should return matching movies."""
        self.app.movies = [
            {"title": "Film A", "genre": "Драма", "year": 2020, "rating": 7.5},
            {"title": "Film B", "genre": "Комедия", "year": 2019, "rating": 8.0},
            {"title": "Film C", "genre": "Драма", "year": 2018, "rating": 6.5},
        ]
        self.app.filter_year_from_var.set("2019")
        self.app.filter_year_to_var.set("2020")
        filtered = self.app.get_filtered()
        self.assertEqual(len(filtered), 2)
        self.assertEqual({f["title"] for f in filtered}, {"Film A", "Film B"})


if __name__ == "__main__":
    unittest.main()
