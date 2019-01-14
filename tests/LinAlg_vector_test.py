from decimal import Decimal, getcontext
import pytest
from src.vector import Vector

getcontext().prec = 15


def test_Vector_init():
    vec = Vector([1, 2, 3])
    assert isinstance(vec, Vector)
    assert vec.dimension == 3
    assert vec.coordinates == (1, 2, 3)


def test_Vector_init_failvalue():
    with pytest.raises(ValueError, message="The coordinates must be nonempty"):
        vec = Vector("")


def test_Vector_str():
    vec = Vector([1, 2, 3])
    assert str(vec) == "Vector: (Decimal('1'), Decimal('2'), Decimal('3'))"


def test_Vector_eq():
    vec = Vector([1, 2, 3])
    assert vec == Vector([1, 2, 3])


def test_vector_add_dimension_check():
    with pytest.raises(ValueError, message="The dimensions of the vectors must be equal"):
        vec1 = Vector([1, 2, 3])
        vec2 = Vector([1, 2, 3, 4])
        vec3 = vec1 + vec2


def test_vector_add():
    vec1 = Vector([1, 2, 3])
    vec2 = Vector([7, 8, 9])
    vec3 = vec1 + vec2
    assert vec3.coordinates == (8, 10, 12)
    assert vec3.dimension == 3


def test_vector_sub_dimension_check():
    with pytest.raises(ValueError, message="The dimensions of the vectors must be equal"):
        vec1 = Vector([1, 2, 3])
        vec2 = Vector([1, 2, 3, 4])
        vec3 = vec1 - vec2


def test_vector_sub():
    vec1 = Vector([1, 2, 3])
    vec2 = Vector([7, 8, 9])
    vec3 = vec1 - vec2
    assert vec3.coordinates == (-6, -6, -6)
    assert vec3.dimension == 3


def test_vector_scalar_mult_multiplier_check1():
    with pytest.raises(ValueError, message="Can only multiply by a single, numeric value"):
        vec1 = Vector([1, 2, 3])
        vec1.scalarMultiple([1, 2])


def test_vector_scalar_mult_multiplier_check2():
    with pytest.raises(ValueError, message="Can only multiply by a single, numeric value"):
        vec1 = Vector([1, 2, 3])
        vec1.scalarMultiple("x")


def test_vector_scalar_multiplier():
    vec1 = Vector([1, 2, 3])
    vec2 = vec1.scalarMultiple(3)
    assert vec2.coordinates == (3, 6, 9)
    assert vec2.dimension == 3


def test_vector_magnitude():
    vec1 = Vector([2 ** .5, 2 ** .5])
    assert vec1.magnitude() == pytest.approx(2, 0.001)


def test_vector_normalise():
    vec1 = Vector([2 ** 0.5, 2 ** 0.5])
    vectest = tuple([Decimal(x / 2) for x in vec1])
    vec1_direction = vec1.normalise()
    assert vec1_direction.coordinates == pytest.approx(vectest, 0.001)


def test_vector_normalise_fail():
    with pytest.raises(Exception, message="Cannot normalise the zero vector"):
        vec1 = Vector([0, 0])
        vec1_direction = vec1.normalise()


def test_vector_dotproduct():
    vec1 = Vector([2, 2])
    vec2 = Vector([2, 2])
    dotp = vec1.dotProduct(vec2)
    assert dotp == 8


def test_angle_div_zero():
    with pytest.raises(Exception, message="Cannot compute an angle with the zero vector"):
        vec1 = Vector([0, 0])
        vec2 = Vector([1, 1])
        angle = vec1.angle(vec2)


def test_angle():
    vec1 = Vector([1, 1])
    vec2 = Vector([1, 1])
    angle = vec1.angle(vec2)
    assert angle == pytest.approx(0, abs=1e-3)


def test_angle_radians():
    vec1 = Vector([0, 1])
    vec2 = Vector([1, 1])
    angle = vec1.angle(vec2)
    assert angle == pytest.approx(0.7854, abs=1e-3)


def test_angle_degrees():
    vec1 = Vector([0, 1])
    vec2 = Vector([1, 1])
    angle = vec1.angle(vec2, in_degrees=True)
    assert angle == pytest.approx(45, abs=1e-3)


def test_parallel():
    vec1 = Vector([1, 1])
    vec2 = Vector([3, 3])
    assert vec1.isParallel(vec2) == True


def test_not_parallel():
    vec1 = Vector([3, 1])
    vec2 = Vector([3, 3])
    assert vec1.isParallel(vec2) == False


def test_zero_parallelx():
    vec1 = Vector([0, 0])
    vec2 = Vector([3, 3])
    assert vec1.isParallel(vec2) == True


def test_zero_parallely():
    vec1 = Vector([1, 1])
    vec2 = Vector([0, 0])
    assert vec1.isParallel(vec2) == True


def test_orthogonal():
    vec1 = Vector([-3, 3])
    vec2 = Vector([3, 3])
    assert vec1.isOrthogonal(vec2) == True


def test_not_orthogonal_pos():
    vec1 = Vector([3, 1])
    vec2 = Vector([3, 3])
    assert vec1.isOrthogonal(vec2) == False


def test_not_orthogonal_neg():
    vec1 = Vector([3, 3])
    vec2 = Vector([-1, -3])
    assert vec1.isOrthogonal(vec2) == False


def test_zero_orthogonalx():
    vec1 = Vector([0, 0])
    vec2 = Vector([3, 3])
    assert vec1.isOrthogonal(vec2) == True


def test_zero_orthogonaly():
    vec1 = Vector([1, 1])
    vec2 = Vector([0, 0])
    assert vec1.isOrthogonal(vec2) == True


def test_V_parallel():
    vec1 = Vector([1, 1])


def test_cross_product_dimension_check_v():
    with pytest.raises(ValueError, message="Cross product can only work for 3D vectors"):
        vec1 = Vector([1, 2, 3, 4])
        vec2 = Vector([1, 2, 3])
        vec3 = vec1.crossProduct(vec2)


def test_cross_product_dimension_check_w():
    with pytest.raises(ValueError, message="Cross product can only work for 3D vectors"):
        vec1 = Vector([1, 2, 3])
        vec2 = Vector([1, 2, 3, 4])
        vec3 = vec1.crossProduct(vec2)


def test_cross_product():
    vec1 = Vector([1, 2, 3])
    vec2 = Vector([4, 5, 6])
    vec3 = vec1.crossProduct(vec2)
    assert vec3 == Vector([-3, 6, -3])
    assert vec1.dotProduct(vec3) == 0
    assert vec2.dotProduct(vec3) == 0


def test_cross_product_anti_commutative():
    vec1 = Vector([1, 2, 3])
    vec2 = Vector([4, 5, 6])
    vec3 = vec2.crossProduct(vec1)
    assert vec3 == Vector([3, -6, 3])
    assert vec1.dotProduct(vec3) == 0
    assert vec2.dotProduct(vec3) == 0
