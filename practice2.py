import math


class Point3d:
    _total_points_count = 0

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        Point3d._total_points_count += 1

    def __str__(self) -> str:
        return f"({round(self.x, 2)}, {round(self.y, 2)}, {round(self.z, 2)})"

    def __repr__(self) -> str:
        return f"Point3d(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"

    def distance_to(self, other: 'Point3d') -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    @classmethod
    def origin(cls) -> 'Point3d':
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def clone(cls, point: 'Point3d') -> 'Point3d':
        return cls(point.x, point.y, point.z)

    @classmethod
    def from_polar(cls, r: float, theta_degrees: float, z: float = 0.0) -> 'Point3d':
        # Перевод из цилиндрических координат (полярные + высота z)
        rad = math.radians(theta_degrees)
        x = r * math.cos(rad)
        y = r * math.sin(rad)
        return cls(x, y, z)

    @staticmethod
    def distance_between(p1: tuple, p2: tuple) -> float:
        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2 +
            (p1[2] - p2[2]) ** 2
        )


class Vector3d:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self) -> str:
        return f"({round(self.x, 2)}, {round(self.y, 2)}, {round(self.z, 2)})"

    def __repr__(self) -> str:
        return f"Vector3d(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"

    @classmethod
    def from_points(cls, start: Point3d, end: Point3d) -> 'Vector3d':
        return cls(end.x - start.x, end.y - start.y, end.z - start.z)

    # Вспомогательный метод для вычисления точной длины (модуля) вектора
    def _magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # Операции сравнения (равенство по координатам, больше/меньше по длине)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3d):
            return False
        return (
            math.isclose(self.x, other.x) and
            math.isclose(self.y, other.y) and
            math.isclose(self.z, other.z)
        )

    def __gt__(self, other: 'Vector3d') -> bool:
        return self._magnitude() > other._magnitude()

    def __lt__(self, other: 'Vector3d') -> bool:
        return self._magnitude() < other._magnitude()

    # Вспомогательный метод для приведения числа к кортежу (n, n, n)
    @staticmethod
    def _unpack_operand(other):
        if isinstance(other, Vector3d):
            return other.x, other.y, other.z
        elif isinstance(other, (int, float)):
            return float(other), float(other), float(other)
        raise TypeError("Операнд должен быть Vector3d или числом (int, float)")

    # Арифметические операции (слева и справа)
    def __add__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        return Vector3d(self.x + ox, self.y + oy, self.z + oz)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        return Vector3d(self.x - ox, self.y - oy, self.z - oz)

    def __rsub__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        return Vector3d(ox - self.x, oy - self.y, oz - self.z)

    def __mul__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        return Vector3d(self.x * ox, self.y * oy, self.z * oz)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        if ox == 0 or oy == 0 or oz == 0:
            raise ZeroDivisionError("Деление на ноль запрещено")
        return Vector3d(self.x / ox, self.y / oy, self.z / oz)

    def __rtruediv__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        if self.x == 0 or self.y == 0 or self.z == 0:
            raise ZeroDivisionError("Деление на ноль запрещено")
        return Vector3d(ox / self.x, oy / self.y, oz / self.z)

    # Инкрементальные операции (in-place, без создания нового объекта)
    def __iadd__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        self.x += ox
        self.y += oy
        self.z += oz
        return self

    def __isub__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        self.x -= ox
        self.y -= oy
        self.z -= oz
        return self

    def __imul__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        self.x *= ox
        self.y *= oy
        self.z *= oz
        return self

    def __itruediv__(self, other):
        ox, oy, oz = self._unpack_operand(other)
        if ox == 0 or oy == 0 or oz == 0:
            raise ZeroDivisionError("Деление на ноль запрещено")
        self.x /= ox
        self.y /= oy
        self.z /= oz
        return self

    # Векторное произведение (@)
    def __matmul__(self, other: 'Vector3d') -> 'Vector3d':
        if not isinstance(other, Vector3d):
            raise TypeError("Векторное произведение определено только для двух Vector3d")
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vector3d(cx, cy, cz)

    # Статические методы проверки коллинеарности и компланарности
    @staticmethod
    def is_collinear(a: 'Vector3d', b: 'Vector3d') -> bool:
        # Векторы коллинеарны, если их векторное произведение равно нулевому вектору
        cross = a @ b
        return (
            math.isclose(cross.x, 0.0, abs_tol=1e-9) and
            math.isclose(cross.y, 0.0, abs_tol=1e-9) and
            math.isclose(cross.z, 0.0, abs_tol=1e-9)
        )

    @staticmethod
    def is_complanar(a: 'Vector3d', b: 'Vector3d', c: 'Vector3d') -> bool:
        # Векторы компланарны, если их смешанное произведение (a · (b × c)) равно 0
        cross = b @ c
        scalar_triple = a.x * cross.x + a.y * cross.y + a.z * cross.z
        return math.isclose(scalar_triple, 0.0, abs_tol=1e-9)

    # Длина вектора (Python требует, чтобы __len__ возвращал целое число int >= 0)
    def __len__(self) -> int:
        return int(round(self._magnitude()))

    # Доступ по индексу и имени компоненты
    def __getitem__(self, key):
        if key in (0, 'x'):
            return self.x
        elif key in (1, 'y'):
            return self.y
        elif key in (2, 'z'):
            return self.z
        raise KeyError(f"Недопустимый индекс или ключ: {key}")

    # Итерация по компонентам в цикле for
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


# ==================== ДЕМОНСТРАЦИЯ РАБОТЫ ====================
if __name__ == "__main__":
    print("=== 1. Работа с Point3d ===")
    p1 = Point3d(1.234, 2.567, 3.891)
    p2 = Point3d(4.0, 6.0, 3.891)
    p_origin = Point3d.origin()
    p_clone = Point3d.clone(p1)
    p_polar = Point3d.from_polar(5, 90, 2)

    print("str(p1):", str(p1))
    print("repr(p1):", repr(p1))
    print("Начало координат:", p_origin)
    print("Клон p1:", p_clone)
    print("Из полярных (r=5, 90°, z=2):", p_polar)
    print("Расстояние p1 -> p2:", round(p1.distance_to(p2), 2))
    print("Статическое расстояние:", Point3d.distance_between((0, 0, 0), (0, 3, 4)))
    print("Всего создано точек:", Point3d._total_points_count)

    print("\n=== 2. Создание и вывод Vector3d ===")
    v1 = Vector3d(3.1415, 4.9876, 5.0)
    v2 = Vector3d.from_points(Point3d(1, 2, 3), Point3d(4, 6, 8))
    print("str(v1):", str(v1))
    print("repr(v1):", repr(v1))
    print("v2 из точек:", repr(v2))

    print("\n=== 3. Сравнение векторов ===")
    v_same = Vector3d(3, 4, 5)
    print("v2 == v_same:", v2 == v_same)
    print("v1 > v2:", v1 > v2)
    print("v2 < v1:", v2 < v1)

    print("\n=== 4. Арифметические операции ===")
    a = Vector3d(3, 4, 5)
    b = Vector3d(1, 2, 3)
    print("a + 3 =", a + 3)
    print("3 + a =", 3 + a)
    print("10 - a =", 10 - a)
    print("a * b =", a * b)
    print("2 * a =", 2 * a)
    print("a / 2 =", a / 2)

    print("\n=== 5. Инкрементальные операции (без создания нового объекта) ===")
    old_id = id(a)
    a += 2
    print("a += 2 ->", a, "| Тот же объект в памяти:", id(a) == old_id)
    a *= b
    print("a *= b ->", a, "| Тот же объект в памяти:", id(a) == old_id)

    print("\n=== 6. Векторное произведение, коллинеарность и компланарность ===")
    i = Vector3d(1, 0, 0)
    j = Vector3d(0, 1, 0)
    k = i @ j
    print("i @ j =", k)

    v_col1 = Vector3d(2, 4, 6)
    v_col2 = Vector3d(-1, -2, -3)
    print("Коллинеарны (2,4,6) и (-1,-2,-3):", Vector3d.is_collinear(v_col1, v_col2))
    print("Коллинеарны i и j:", Vector3d.is_collinear(i, j))

    v_comp = Vector3d(5, 7, 0)  # лежит в плоскости XY вместе с i и j
    print("Компланарны i, j и (5,7,0):", Vector3d.is_complanar(i, j, v_comp))
    print("Компланарны i, j и k:", Vector3d.is_complanar(i, j, k))

    print("\n=== 7. Длина, индексация и итерация ===")
    v_test = Vector3d(3, 4, 12)  # точная длина = 13
    print("len(v_test):", len(v_test))
    print("По индексу v_test[0], v_test[1], v_test[2]:", v_test[0], v_test[1], v_test[2])
    print("По ключу v_test['x'], v_test['y'], v_test['z']:", v_test['x'], v_test['y'], v_test['z'])
    print("Перебор через for:", [coord for coord in v_test])
