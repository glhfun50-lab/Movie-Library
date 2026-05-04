import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "movies.json"


def load_movies():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_movies(movies):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library — Личная кинотека")
        self.root.resizable(False, False)

        self.movies = load_movies()

        self._build_input_frame()
        self._build_filter_frame()
        self._build_table()
        self._build_summary_frame()

        self.refresh_table()

    # ── Input form ──────────────────────────────────────────────────────────

    def _build_input_frame(self):
        frame = ttk.LabelFrame(self.root, text="Добавить фильм", padding=10)
        frame.grid(row=0, column=0, padx=10, pady=8, sticky="ew")

        ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.title_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Жанр:").grid(row=0, column=2, sticky="w")
        self.genre_var = tk.StringVar()
        genres = ["Драма", "Комедия", "Боевик", "Фантастика", "Ужасы", "Мультфильм", "Детектив", "Романтика", "Документальный", "Другое"]
        ttk.Combobox(frame, textvariable=self.genre_var, values=genres, width=15,
                     state="readonly").grid(row=0, column=3, padx=5)
        self.genre_var.set(genres[0])

        ttk.Label(frame, text="Год:").grid(row=0, column=4, sticky="w")
        self.year_var = tk.StringVar(value=str(datetime.today().year))
        ttk.Entry(frame, textvariable=self.year_var, width=10).grid(row=0, column=5, padx=5)

        ttk.Label(frame, text="Рейтинг (0-10):").grid(row=0, column=6, sticky="w")
        self.rating_var = tk.StringVar(value="7.5")
        ttk.Entry(frame, textvariable=self.rating_var, width=8).grid(row=0, column=7, padx=5)

        ttk.Button(frame, text="Добавить фильм", command=self.add_movie).grid(
            row=0, column=8, padx=10)

    # ── Filter form ─────────────────────────────────────────────────────────

    def _build_filter_frame(self):
        frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        frame.grid(row=1, column=0, padx=10, pady=4, sticky="ew")

        ttk.Label(frame, text="Жанр:").grid(row=0, column=0, sticky="w")
        self.filter_genre_var = tk.StringVar(value="Все")
        genres = ["Все"] + ["Драма", "Комедия", "Боевик", "Фантастика", "Ужасы", "Мультфильм", "Детектив", "Романтика", "Документальный", "Другое"]
        ttk.Combobox(frame, textvariable=self.filter_genre_var, values=genres, width=15,
                     state="readonly").grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Год от:").grid(row=0, column=2, sticky="w")
        self.filter_year_from_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.filter_year_from_var, width=8).grid(row=0, column=3, padx=5)

        ttk.Label(frame, text="Год до:").grid(row=0, column=4, sticky="w")
        self.filter_year_to_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.filter_year_to_var, width=8).grid(row=0, column=5, padx=5)

        ttk.Button(frame, text="Применить фильтр", command=self.refresh_table).grid(
            row=0, column=6, padx=5)
        ttk.Button(frame, text="Сбросить", command=self.reset_filters).grid(
            row=0, column=7, padx=5)

    # ── Table ────────────────────────────────────────────────────────────────

    def _build_table(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=2, column=0, padx=10, pady=4, sticky="nsew")

        columns = ("id", "title", "genre", "year", "rating")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)

        self.tree.heading("id", text="№")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=250, anchor="w")
        self.tree.column("genre", width=120, anchor="center")
        self.tree.column("year", width=70, anchor="center")
        self.tree.column("rating", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Button(self.root, text="Удалить выбранное", command=self.delete_selected).grid(
            row=3, column=0, pady=4)

    # ── Summary ──────────────────────────────────────────────────────────────

    def _build_summary_frame(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=4, column=0, padx=10, pady=6, sticky="ew")

        ttk.Label(frame, text="Всего фильмов:").grid(row=0, column=0, sticky="w")
        self.count_var = tk.StringVar(value="0")
        ttk.Label(frame, textvariable=self.count_var, font=("Arial", 11, "bold")).grid(
            row=0, column=1, padx=10)

        ttk.Label(frame, text="Средний рейтинг:").grid(row=0, column=2, sticky="w")
        self.avg_var = tk.StringVar(value="0.0")
        ttk.Label(frame, textvariable=self.avg_var, font=("Arial", 11, "bold")).grid(
            row=0, column=3, padx=10)

    # ── Logic ────────────────────────────────────────────────────────────────

    def validate_year(self, value: str) -> int:
        """Raises ValueError if year is invalid."""
        value = value.strip()
        if not value.isdigit():
            raise ValueError("Год должен быть числом.")
        year = int(value)
        current_year = datetime.today().year
        if year < 1888 or year > current_year + 5:  # 1888 = first film
            raise ValueError(f"Год должен быть в диапазоне 1888-{current_year + 5}.")
        return year

    def validate_rating(self, value: str) -> float:
        """Raises ValueError if rating is invalid."""
        value = value.strip().replace(",", ".")
        try:
            rating = float(value)
        except ValueError:
            raise ValueError("Рейтинг должен быть числом.")
        if rating < 0 or rating > 10:
            raise ValueError("Рейтинг должен быть от 0 до 10.")
        return rating

    def add_movie(self):
        # Validate title
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Ошибка", "Введите название фильма.")
            return

        # Validate year
        try:
            year = self.validate_year(self.year_var.get())
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный год: {e}")
            return

        # Validate rating
        try:
            rating = self.validate_rating(self.rating_var.get())
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный рейтинг: {e}")
            return

        genre = self.genre_var.get().strip()
        if not genre:
            messagebox.showerror("Ошибка", "Выберите жанр.")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": round(rating, 1),
        }
        self.movies.append(movie)
        save_movies(self.movies)

        self.title_var.set("")
        self.year_var.set(str(datetime.today().year))
        self.rating_var.set("7.5")
        self.refresh_table()

    def get_filtered(self):
        genre_filter = self.filter_genre_var.get()
        from_str = self.filter_year_from_var.get().strip()
        to_str = self.filter_year_to_var.get().strip()

        from_year = None
        to_year = None

        if from_str:
            try:
                from_year = self.validate_year(from_str)
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректный год «от»: {e}")
                return None

        if to_str:
            try:
                to_year = self.validate_year(to_str)
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректный год «до»: {e}")
                return None

        result = []
        for movie in self.movies:
            if genre_filter != "Все" and movie["genre"] != genre_filter:
                continue
            if from_year and movie["year"] < from_year:
                continue
            if to_year and movie["year"] > to_year:
                continue
            result.append(movie)

        return result

    def refresh_table(self):
        filtered = self.get_filtered()
        if filtered is None:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        total_rating = 0.0
        for i, movie in enumerate(filtered, start=1):
            self.tree.insert("", "end", values=(
                i,
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))
            total_rating += movie["rating"]

        self.count_var.set(str(len(filtered)))
        if filtered:
            self.avg_var.set(f"{total_rating / len(filtered):.1f}")
        else:
            self.avg_var.set("0.0")

    def reset_filters(self):
        self.filter_genre_var.set("Все")
        self.filter_year_from_var.set("")
        self.filter_year_to_var.set("")
        self.refresh_table()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Удаление", "Выберите строку для удаления.")
            return

        filtered = self.get_filtered()
        if filtered is None:
            return

        # Build mapping of displayed rows to actual movies
        indices_to_delete = set()
        for item in selected:
            row_num = int(self.tree.item(item, "values")[0]) - 1
            if 0 <= row_num < len(filtered):
                movie = filtered[row_num]
                # Find actual index in self.movies
                for idx, m in enumerate(self.movies):
                    if m is movie:
                        indices_to_delete.add(idx)
                        break

        self.movies = [m for i, m in enumerate(self.movies) if i not in indices_to_delete]
        save_movies(self.movies)
        self.refresh_table()


def main():
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()


if __name__ == "__main__":
    main()
