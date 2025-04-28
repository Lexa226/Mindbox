"""
Библиотека для вычисления площадей геометрических фигур.
Содержит реализации Circle и Triangle с методами area и __str__,
а также утилиту compute_area и набор юнит-тестов.
"""
from abc import ABC, abstractmethod
import math

class Figura(ABC):
    """
    Абстрактный класс для геометрических фигур.
    """
    @abstractmethod
    def area(self) -> float:
        """
        Вычислить и вернуть площадь фигуры.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Вернуть строковое представление фигуры с указанием площади.
        """
        pass

class Circle(Figura):
    """
    Класс для круга, задаётся радиусом.
    """
    def __init__(self, radius: int | float) -> None:
        """
        Инициализация круга.

        Args:
            radius (int | float): Радиус круга, должен быть положительным.

        Raises:
            ValueError: Если radius <= 0.
        """
        if radius <= 0:
            raise ValueError("Радиус не может быть меньше или равен 0")
        self.radius = radius

    def area(self) -> float:
        """
        Вычислить и вернуть площадь круга: π * r².
        """
        return math.pi * (self.radius ** 2)

    def __str__(self) -> str:
        """
        Вернуть описание круга с площадью.
        """
        return f"Круг(радиус={self.radius}) → площадь={self.area()}"

class Triangle(Figura):
    """
    Класс для треугольника по длинам трёх сторон.
    Поддерживает вычисление площади по формуле Герона и проверку прямого угла.
    """
    def __init__(self, a: int | float, b: int | float, c: int | float) -> None:
        """
        Инициализация треугольника.

        Args:
            a (int | float): Длина стороны a, должно быть > 0.
            b (int | float): Длина стороны b, должно быть > 0.
            c (int | float): Длина стороны c, должно быть > 0.

        Raises:
            ValueError: Если стороны <= 0 или нарушено неравенство треугольника.
        """
        if any(side <= 0 for side in (a, b, c)):
            raise ValueError("Стороны треугольника должны быть положительными")
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            raise ValueError("Нарушено неравенство треугольника")
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        """
        Вычислить и вернуть площадь по формуле Герона.
        """
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right(self) -> bool:
        """
        Проверить, является ли треугольник прямоугольным.
        """
        sides = sorted((self.a, self.b, self.c))
        return math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2)

    def __str__(self) -> str:
        """
        Вернуть описание треугольника с площадью.
        """
        return f"Треугольник(стороны={self.a}, {self.b}, {self.c}) → площадь={self.area()}"

def compute_area(shape: Figura) -> float:
    """
    Вычислить площадь произвольной фигуры.

    Args:
        shape (Figura): Объект фигуры.

    Returns:
        float: Площадь фигуры.
    """
    return shape.area()


if __name__ == "__main__":
    import unittest

    class TestShapes(unittest.TestCase):
        def test_circle_area(self):
            c = Circle(1)
            self.assertAlmostEqual(c.area(), math.pi)

        def test_triangle_area(self):
            t = Triangle(3, 4, 5)
            self.assertAlmostEqual(t.area(), 6.0)

        def test_triangle_right(self):
            t = Triangle(3, 4, 5)
            self.assertTrue(t.is_right())
            t2 = Triangle(2, 2, 3)
            self.assertFalse(t2.is_right())

        def test_invalid_circle(self):
            with self.assertRaises(ValueError):
                Circle(0)

        def test_invalid_triangle_sides(self):
            with self.assertRaises(ValueError):
                Triangle(1, 2, 3)

        def test_dynamic_area(self):
            shapes = [Circle(2), Triangle(5, 5, 6)]
            areas = [compute_area(s) for s in shapes]
            self.assertEqual(len(areas), 2)

    unittest.main()