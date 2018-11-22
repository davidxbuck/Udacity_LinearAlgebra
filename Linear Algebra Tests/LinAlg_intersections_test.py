from decimal import Decimal, getcontext
import pytest
from line import Line
from linsys import LinearSystem, Parametrization
from plane import Plane
from vector import Vector
from hyperplane import Hyperplane

getcontext().prec = 15


def test_null_Line():
    line1 = Line()
    assert isinstance(line1, Line)
    assert line1.normal_vector == Vector([0, 0])
    assert line1.constant_term == 0


def test_Line_init_nolabels():
    line1 = Line(Vector([1, 1]), 4)
    assert isinstance(line1, Line)
    assert line1.normal_vector == Vector([1, 1])
    assert line1.constant_term == 4


def test_Line_init_labels():
    line1 = Line(normal_vector=Vector([2, 2]), constant_term=3)
    assert isinstance(line1, Line)
    assert line1.normal_vector == Vector([2, 2])
    assert line1.constant_term == 3


def test_Line_eq():
    line1 = Line(Vector([1, 1]), 1)
    line2 = Line(Vector([-3, -3]), -3)
    assert line1 == line2


def test_Line_ne():
    line1 = Line(Vector([1, 1]), 1)
    line2 = Line(Vector([-3, -3]), 3)
    assert line1 != line2


def test_Line_parallel():
    line1 = Line(Vector([1, 1]), 1)
    line2 = Line(Vector([1, 1]), 2)
    assert line1 != line2
    assert line1.isParallel(line2)


def test_Line_not_parallel():
    line1 = Line(Vector([1, 1.1]), 1)
    line2 = Line(Vector([1, 1]), 2)
    assert line1 != line2
    assert not line1.isParallel(line2)


def test_intersect_parallel():
    line1 = Line(Vector([2, 2]), 1)
    line2 = Line(Vector([1, 1]), 2)
    assert line1.intersection(line2) == None


def test_intersect_parallel_identical():
    line1 = Line(Vector([2, 2]), 2)
    line2 = Line(Vector([1, 1]), 1)
    assert str(line1.intersection(line2)) == "2x_1 + 2x_2 = 2"


def test_intersect():
    line1 = Line(Vector([1, 1]), 2)
    line2 = Line(Vector([1, -1]), 2)
    intersect = line1.intersection(line2)
    assert intersect.coordinates[0] == pytest.approx(2, abs=1e-3)
    assert intersect.coordinates[1] == pytest.approx(0, abs=1e-3)


def test_null_Plane():
    plane1 = Plane()
    assert isinstance(plane1, Plane)
    assert plane1.normal_vector == Vector([0, 0, 0])
    assert plane1.constant_term == 0


def test_Plane_init_nolabels():
    plane1 = Plane(normal_vector=Vector([1, 1, 1]), constant_term=5)
    assert isinstance(plane1, Plane)
    assert plane1.normal_vector == Vector([1, 1, 1])
    assert plane1.constant_term == 5


def test_Plane_init_labels():
    plane1 = Plane(normal_vector=Vector([2, 2, 2]), constant_term=3)
    assert isinstance(plane1, Plane)
    assert plane1.normal_vector == Vector([2, 2, 2])
    assert plane1.constant_term == 3


def test_Plane_parallel():
    plane1 = Plane(Vector([1, 1, 1]), 1)
    plane2 = Plane(Vector([1, 1, 1]), 2)
    assert plane1 != plane2
    assert plane1.isParallel(plane2)


def test_Plane_not_parallel():
    plane1 = Plane(Vector([1, 1, 1.1]), 1)
    plane2 = Plane(Vector([1, 1, 1]), 2)
    assert plane1 != plane2
    assert not plane1.isParallel(plane2)


def test_Plane_parallel_identical():
    plane1 = Plane(Vector([1, 1, 1]), 1)
    plane2 = Plane(Vector([1, 1, 1]), 1)
    assert plane1 == plane2
    assert plane1.isParallel(plane2)


def test_linsys_init():
    p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

    s = LinearSystem([p0, p1, p2, p3])
    assert s.planes[0] == Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    assert s.planes[1] == Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    assert s.planes[2] == Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    assert s.planes[3] == Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')


# def test_linsys_all_same_dimension():
#     with pytest.raises(Exception, message='All planes in the system should live in the same dimension'):
#         p0 = Plane(normal_vector=Vector(['1','1']), constant_term='1')
#         p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
#         p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
#         p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
#
#         s = LinearSystem([p0,p1,p2,p3])
#         assert s == s
#
# Plane class currently sets all dimensions to 3.


def test_linsys_swap_rows():
    p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p0, p1, p2, p3])
    s.swap_rows(0, 1)
    assert s[0] == p1
    assert s[1] == p0
    assert s[2] == p2
    assert s[3] == p3

    s.swap_rows(1, 3)

    assert s[0] == p1
    assert s[1] == p3
    assert s[2] == p2
    assert s[3] == p0

    s.swap_rows(3, 1)

    assert s[0] == p1
    assert s[1] == p0
    assert s[2] == p2
    assert s[3] == p3


def test_linsys_multiply_coefficient():
    p0 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p0, p1, p2, p3])

    assert s[0] == p0
    assert s[1] == p1
    assert s[2] == p2
    assert s[3] == p3

    s.multiply_coefficient_and_row(1, 0)

    assert s[0] == p0
    assert s[1] == p1
    assert s[2] == p2
    assert s[3] == p3

    s.multiply_coefficient_and_row(-1, 2)

    assert s[0] == p0
    assert s[1] == p1
    assert s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3')
    assert s[3] == p3

    s.multiply_coefficient_and_row(10, 1)

    assert s[0] == p0
    assert s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10')
    assert s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3')
    assert s[3] == p3


def test_linsys_multiply_times_row():
    p0 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p1 = Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10')
    p2 = Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p0, p1, p2, p3])

    assert s[0] == p0
    assert s[1] == p1
    assert s[2] == p2
    assert s[3] == p3

    s.add_multiple_times_row_to_row(0, 0, 1)

    assert s[0] == p0
    assert s[1] == p1
    assert s[2] == p2
    assert s[3] == p3

    s.add_multiple_times_row_to_row(1, 0, 1)

    assert s[0] == p0
    assert s[1].normal_vector == Vector(['10', '11', '10'])
    assert s[1].constant_term == 12
    assert s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12')
    assert s[2] == p2
    assert s[3] == p3

    s.add_multiple_times_row_to_row(-1, 1, 0)

    assert s[0] == Plane(normal_vector=Vector(['-10', '-10', '-10']), constant_term='-10')
    assert s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12')
    assert s[2] == p2
    assert s[3] == p3


def test_linsys_triangular_form1():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    assert t[0] == p1
    assert t[1] == p2


def test_linsys_triangular_form2():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    assert t[0] == p1
    assert t[1] == Plane(constant_term='1')


def test_linsys_triangular_form3():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p1, p2, p3, p4])
    t = s.compute_triangular_form()
    assert t[0] == p1
    assert t[1] == p2
    assert t[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2')
    assert t[3] == Plane()


def test_linsys_triangular_form4():
    p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    s = LinearSystem([p1, p2, p3])
    t = s.compute_triangular_form()
    assert t[0] == Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    assert t[1] == Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    assert t[2] == Plane(normal_vector=Vector(['0', '0', '-9']), constant_term='-2')


def test_linsys_rref1():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    r = s.compute_rref()
    assert r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='-1')
    assert r[1] == p2


def test_linsys_rref2():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    r = s.compute_rref()
    assert r[0] == p1
    assert r[1] == Plane(constant_term='1')


def test_linsys_rref3():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p1, p2, p3, p4])
    r = s.compute_rref()
    assert r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='0')
    assert r[1] == p2
    assert r[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2')
    assert r[3] == Plane()


def test_linsys_rref4():
    p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    s = LinearSystem([p1, p2, p3])
    r = s.compute_rref()
    assert r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term=Decimal('23') / Decimal('9'))
    assert r[1] == Plane(normal_vector=Vector(['0', '1', '0']), constant_term=Decimal('7') / Decimal('9'))
    assert r[2] == Plane(normal_vector=Vector(['0', '0', '1']), constant_term=Decimal('2') / Decimal('9'))


def test_gaussian_elimination_init():
    p1 = Plane(normal_vector=Vector(['0', '0', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '-1', '0']), constant_term='-2')
    p3 = Plane(normal_vector=Vector(['5', '0', '0']), constant_term='15')
    s = LinearSystem([p1, p2, p3])
    r = s.gaussian_elimination()
    assert r == Vector(['3', '2', '1'])

def test_gaussian_elimination_infinite_solutions():
    p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '-1', '-1']), constant_term='-1')
    s = LinearSystem([p1, p2])
    r = s.gaussian_elimination()
#    assert r == 'Infinitely many solutions'

def test_gaussian_elimination_no_solution():
    p1 = Plane(normal_vector=Vector(['1', '2', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '-1', '0']), constant_term='-2')
    p3 = Plane(normal_vector=Vector(['2', '4', '2']), constant_term='-4')
    s = LinearSystem([p1, p2, p3])
    r = s.gaussian_elimination()
    assert r == 'No solutions'

def test_hyperplane_gaussian_elimination_init():
    p1 = Hyperplane(normal_vector=Vector(['0', '0', '1']), constant_term='1')
    p2 = Hyperplane(normal_vector=Vector(['0', '-1', '0']), constant_term='-2')
    p3 = Hyperplane(normal_vector=Vector(['5', '0', '0']), constant_term='15')
    s = LinearSystem([p1, p2, p3])
    r = s.gaussian_elimination()
    assert r == Vector(['3', '2', '1'])

def test_hyperplane_gaussian_elimination_infinite_solutions():
    p1 = Hyperplane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Hyperplane(normal_vector=Vector(['0', '-1', '-1']), constant_term='-1')
    s = LinearSystem([p1, p2])
    r = s.gaussian_elimination()

#    assert r == 'Infinitely many solutions'

def test_hyperplane_gaussian_elimination_no_solution():
    p1 = Hyperplane(normal_vector=Vector(['1', '2', '1', '2']), constant_term='1')
    p2 = Hyperplane(normal_vector=Vector(['0', '-1', '0', '7']), constant_term='-2')
    p3 = Hyperplane(normal_vector=Vector(['2', '4', '2', '4']), constant_term='-4')
    s = LinearSystem([p1, p2, p3])
    r = s.gaussian_elimination()
    assert r == 'No solutions'