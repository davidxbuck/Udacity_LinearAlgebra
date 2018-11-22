from decimal import Decimal, getcontext
from math import acos, degrees, sqrt, pi

getcontext().prec = 15

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError ('The coordinates must be nonempty')

        except TypeError:
            raise TypeError ('The coordinates must be an iterable')

    def __iter__(self):
            return iter(self.coordinates)

    def __getitem__(self,index):
            return self.coordinates[index]

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__ (self, a):
        if self.dimension is not a.dimension:
            raise ValueError ('The dimensions of the vectors must be equal')
        return Vector(tuple(map(sum, zip(self.coordinates, a.coordinates))))

    def __sub__ (self, a):
        if self.dimension is not a.dimension:
            raise ValueError ('The dimensions of the vectors must be equal')
        return Vector([i - j for i, j in zip(self.coordinates, a.coordinates)])

    def __round__(self, n=None):
        return Vector([round(x, n) for x in self])

    def scalarMultiple(self, a):
        if isinstance(a, int) or isinstance(a, float) or isinstance(a, Decimal):
            a = Decimal(a)
        else:
            raise ValueError ('Can only multiply by a single, numeric value')
        return Vector([i * a for i in self.coordinates])

    def magnitude(self):
        return Decimal(sqrt(sum([i**2 for i in self.coordinates])))

    def normalise(self):
        try:
            return self.scalarMultiple(1 / self.magnitude())
        except ZeroDivisionError:
            raise Exception('Cannot normalise the zero vector')

    def dotProduct(self, a):
        return Decimal(sum([i*j for i, j in zip(self.coordinates, a.coordinates)]))

    def angle(self, a, in_degrees = False):
        try:
            ratio = self.dotProduct(a)/(Decimal(self.magnitude()) * Decimal(a.magnitude()))
            if ratio > 1:
                ratio = 1
            if ratio < -1:
                ratio = -1
            theta = acos(ratio)
            if in_degrees:
                theta = degrees(theta)
            return theta
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot compute an angle with the zero vector')

    def isParallel(self, a):
        if self.isZero() or a.isZero() or self.angle(a) == 0 or self.angle(a) == pi:
            return True
        else:
            return False

    def isOrthogonal(self, a):
        if self.isZero() or a.isZero() or abs(self.dotProduct(a)) < 1e-10:
            return True
        else:
            return False

    def isZero(self, tolerance = 1e-10):
        if self.magnitude() < tolerance:
            return True
        else:
            return False

    def vProjected(self, b):
        bnorm = b.normalise()
        dot = self.dotProduct(bnorm)
        return bnorm.scalarMultiple(dot)

    def vOrthogonal(self, b):
        return self - self.vProjected(b)

    def crossProduct(self, b):
        try:
            if self.dimension != 3 or b.dimension != 3:
                raise ValueError
            return Vector([
                self.coordinates[1] * b.coordinates[2] - b.coordinates[1] * self.coordinates[2],
                -(self.coordinates[0] * b.coordinates[2] - b.coordinates[0] * self.coordinates[2]),
                self.coordinates[0] * b.coordinates[1] - b.coordinates[0] * self.coordinates[1]
                ])
        except ValueError:
            raise ValueError('Cross product can only work for 3D vectors')

