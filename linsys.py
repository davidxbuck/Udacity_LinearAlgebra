from copy import deepcopy
from decimal import Decimal, getcontext

from plane import Plane
from hyperplane import Hyperplane
from vector import Vector

getcontext().prec = 15


class LinearSystem(object):
    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):

        temp = self[row1]
        self[row1] = self[row2]
        self[row2] = temp
        return

    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector.scalarMultiple(coefficient)
        k = self[row].constant_term * coefficient
        self[row] = Hyperplane(normal_vector = n, constant_term=k)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        plane_to_be_added = Hyperplane(normal_vector=self[row_to_add].normal_vector.scalarMultiple(coefficient),
                                  constant_term=self[row_to_add].constant_term * coefficient)
        new_vector = self[row_to_be_added_to].normal_vector + plane_to_be_added.normal_vector
        new_constant = self[row_to_be_added_to].constant_term + plane_to_be_added.constant_term
        self[row_to_be_added_to] = Hyperplane(normal_vector=new_vector, constant_term=new_constant)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Hyperplane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def compute_triangular_form(self):
        system = deepcopy(self)
        num_equations = len(system)
        num_variables = system.dimension
        variable = 0
        for row in range(0, num_equations):
            while variable < num_variables:
                c = MyDecimal(system.planes[row].normal_vector[variable])
                if c.is_near_zero():
                    swap_success = system.swap_successful(row, variable)
                    if not swap_success:
                        variable += 1
                        continue

                system.clear_terms_below(row, variable)
                variable += 1
                break
        return system

    def compute_rref(self):
        tf = self.compute_triangular_form()
        num_equations = len(tf)
        pivots = tf.indices_of_first_nonzero_terms_in_each_row()
        for i in range(num_equations - 1, -1, -1):
            variable = pivots[i]
            if variable < 0:
                continue
            alpha = tf[i].normal_vector[variable]
            tf.multiply_coefficient_and_row(Decimal('1.0') / alpha, i)
            tf.clear_terms_above(i, variable)
        return tf

    def clear_terms_above(self, row, variable):

        for r in range(row - 1, -1, -1):
            s = self[r].normal_vector[variable]
            self.add_multiple_times_row_to_row(-s, row, r)

    def swap_successful(self, row, variable):

        num_equations = len(self)

        for k in range(row + 1, num_equations):
            coefficient = MyDecimal(self.planes[k].normal_vector[variable])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True
        return False

    def clear_terms_below(self, row, variable):

        num_equations = len(self)

        q = self[row].normal_vector[variable]
        for r in range(row + 1, num_equations):
            s = self[r].normal_vector[variable]
            self.add_multiple_times_row_to_row(-s / q, row, r)
        variable += 1

    def gaussian_elimination(self):
        rref = self.compute_rref()
        try:
            rref.check_for_exceptions()
        except Exception as e:
            if str(e) == self.NO_SOLUTIONS_MSG:
                return str(e)
            if str(e) == self.INF_SOLUTIONS_MSG:
                return Parametrization(rref.extract_basepoint_for_parametrization(),
                                       rref.extract_direction_vectors_for_parametrization())
            else:
                raise e

        num_variables = rref.dimension
        solution_coordinates = [rref.planes[i].constant_term for i in range(num_variables)]
        return Vector(solution_coordinates)


    def extract_direction_vectors_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        free_variable_indices = set(range(num_variables)) - set(pivot_indices)

        direction_vectors = []

        for free_var in free_variable_indices:
            vector_coords = [0] * num_variables
            vector_coords[free_var] = 1
            for index, plane in enumerate(self.planes):
                pivot_var = pivot_indices[index]
                if pivot_var < 0:
                    break
                vector_coords[pivot_var] = -plane.normal_vector[free_var]

            direction_vectors.append(Vector(vector_coords))

        return direction_vectors


    def extract_basepoint_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()

        basepoint_coords = [0] * num_variables

        for index, plane in enumerate(self.planes):
            pivot_var = pivot_indices[index]
            if pivot_var < 0:
                break
            basepoint_coords[pivot_var] = plane.constant_term

        return Vector(basepoint_coords)

    def check_for_exceptions(self):
        for plane in self.planes:
            try:
                plane.first_nonzero_index(plane.normal_vector)
            except Exception as e:
                if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                    if not MyDecimal(plane.constant_term).is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                else:
                    raise e

        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension
        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)


    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i + 1, p) for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret

class Parametrization(object):

    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM = (
        'The basepoint and direction vectors should all live in the same '
        'dimension')

    def __init__(self, basepoint, direction_vectors):

        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension

        except AssertionError:
            raise Exception(self.BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM)

    def __str__(self):

        output = ''
        for coord in range(self.dimension):
            output += 'x_{} = {} '.format(coord + 1,
                                          round(self.basepoint[coord], 3))
            for free_var, vector in enumerate(self.direction_vectors):
                output += '+ {} t_{}'.format(round(vector[coord], 3),
                                             free_var + 1)
            output += '\n'
        return output


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

# p0 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
# p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
# p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
# p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

# s = LinearSystem([p0,p1,p2,p3])
#
# print (s.indices_of_first_nonzero_terms_in_each_row())
# print ('{},{},{},{}'.format(s[0],s[1],s[2],s[3]))
# print (len(s))
# print (s)
#
# s[0] = p1
# print (s)
#
# print (MyDecimal('1e-9').is_near_zero())
# print (MyDecimal('1e-11').is_near_zero())
