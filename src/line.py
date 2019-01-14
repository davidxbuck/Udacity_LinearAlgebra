from decimal import Decimal, getcontext

from src.vector import Vector

getcontext().prec = 15


class Line(object):
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def __round__(self, n=None):
        line = Line(normal_vector = round(self.normal_vector, n), constant_term = round(self.constant_term, n))
        return line


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __eq__(self, line2):

        if self.normal_vector.isZero():
            if not line2.normal_vector.iszero():
                return False
            else:
                diff = self.constant_term - line2.constant_term
                return MyDecimal(diff).is_near_zero()
        elif line2.normal_vector.isZero():
            return False

        if not self.isParallel(line2):
            return False
        basepoint_difference = self.basepoint - line2.basepoint
        return basepoint_difference.isParallel(self.normal_vector)

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i + 1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def isParallel(self, line2):
        return self.normal_vector.isParallel(line2.normal_vector)

    def intersection(self, line2):
        try:
            if self.isParallel(line2):
                raise Exception("Lines do not intersect")
            A, B = self.normal_vector
            C, D = line2.normal_vector
            k1 = self.constant_term
            k2 = line2.constant_term
            intersectx = (D * k1 - B * k2) / (A * D - B * C)
            intersecty = ((-C) * k1 + A * k2) / (A * D - B * C)
            return Vector([intersectx, intersecty])
        except Exception as e:
            if str(e) == "Lines do not intersect":
                if self == line2:
                    return self
                else:
                    return None


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
