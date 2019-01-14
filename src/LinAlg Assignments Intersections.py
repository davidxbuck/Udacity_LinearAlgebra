from src.line import Line
from src.linsys import LinearSystem
from src.plane import Plane
from src.vector import Vector
from src.hyperplane import Hyperplane

answers = []

# Quiz1

# 1  4.046x + 2.836y = 1.21
#  10.115x + 7.09y  = 3.025
A = 4.046
B = 2.836
k1 = 1.21
line1 = Line(normal_vector=Vector([A, B]), constant_term=k1)
C = 10.115
D = 7.09
k2 = 3.025
line2 = Line(normal_vector=Vector([C, D]), constant_term=k2)
answers.append(round(line1.intersection(line2), 3))

# 2  7.204x + 3.182y = 8.68
#   8.172x + 4.114y = 9.883

A = 7.204
B = 3.182
k1 = 8.68
line1 = Line(normal_vector=Vector([A, B]), constant_term=k1)
C = 8.172
D = 4.114
k2 = 9.883
line2 = Line(normal_vector=Vector([C, D]), constant_term=k2)
answers.append(round(line1.intersection(line2), 3))

# 3  1.182x + 5.562y = 6.744
#   1.773x + 8.343y = 9.525

A = 1.182
B = 5.562
k1 = 6.744
line1 = Line(normal_vector=Vector([A, B]), constant_term=k1)
C = 1.773
D = 8.343
k2 = 9.525
line2 = Line(normal_vector=Vector([C, D]), constant_term=k2)
answers.append(line1.intersection(line2))

# Quiz2

A = -0.412
B = 3.806
C = 0.728
k1 = -3.46
plane1 = Plane(normal_vector=Vector([A, B, C]), constant_term=k1)
D = 1.03
E = -9.515
F = -1.82
k2 = 8.65
plane2 = Plane(normal_vector=Vector([D, E, F]), constant_term=k2)
answers.append([plane1 == plane2, plane1.isParallel(plane2)])

A = 2.611
B = 5.528
C = 0.283
k1 = 4.6
plane1 = Plane(normal_vector=Vector([A, B, C]), constant_term=k1)
D = 7.715
E = 8.306
F = 5.342
k2 = 3.76
plane2 = Plane(normal_vector=Vector([D, E, F]), constant_term=k2)
answers.append([plane1 == plane2, plane1.isParallel(plane2)])

A = -7.926
B = 8.625
C = -7.212
k = -7.952
plane1 = Plane(normal_vector=Vector([A, B, C]), constant_term=k1)
D = -2.642
E = 2.875
F = -2.404
k2 = -2.443
plane2 = Plane(normal_vector=Vector([D, E, F]), constant_term=k2)
answers.append([plane1 == plane2, plane1.isParallel(plane2)])

# Quiz 22

# 1
# 5.862x + 1.178y -10.366z = -8.15
# -2.931x - 0.589y + 5.183z = -4.075

p0 = Plane(normal_vector=Vector([5.862, 1.178, -10.366]), constant_term=-8.150)
p1 = Plane(normal_vector=Vector([-2.931, -0.589, 5.183]), constant_term=-4.075)
s = LinearSystem([p0, p1])
answers.append(s.gaussian_elimination())

# 2
# 8.631x + 5.112y - 1.816z = -5.113
# 4.315x + 11.132y - 5.27z = -6.775
# -2.158x + 3.01y - 1.727z = -0.831

p0 = Plane(normal_vector=Vector([8.631, 5.112, -1.816]), constant_term=-5.113)
p1 = Plane(normal_vector=Vector([4.315, 11.132, -5.270]), constant_term=-6.775)
p2 = Plane(normal_vector=Vector([-2.158, 3.01, -1.727]), constant_term=-0.831)
s = LinearSystem([p0, p1, p2])
answers.append(s.gaussian_elimination())

# 3
# 5.262x + 2.739y - 9.878z = -3.441
# 5.111x + 6.358y + 7.638z = -2.152
# 2.016x - 9.924y - 1.367z = -9.278
# 2.167x - 13.543y -18.883z = -10.567

p0 = Plane(normal_vector=Vector([5.262, 2.739, -9.878]), constant_term=-3.441)
p1 = Plane(normal_vector=Vector([5.111, 6.358, 7.638]), constant_term=-2.152)
p2 = Plane(normal_vector=Vector([2.016, -9.924, -1.367]), constant_term=-9.278)
p3 = Plane(normal_vector=Vector([2.167, -13.543, -18.883]), constant_term=-10.567)
s = LinearSystem([p0, p1, p2, p3])
answers.append(round(s.gaussian_elimination(), 3))

# Quiz 23

p0 = Plane(normal_vector=Vector([0.786, 0.786, 0.588]), constant_term=-0.714)
p1 = Plane(normal_vector=Vector([-0.131, -0.131, 0.244]), constant_term=0.319)

s = LinearSystem([p0, p1])
answers.append(s.gaussian_elimination())

p0 = Plane(Vector([8.631, 5.112, -1.816]), -5.113)
p1 = Plane(Vector([4.315, 11.132, -5.27]), -6.775)
p2 = Plane(Vector([-2.158, 3.01, -1.727]), -0.831)

s = LinearSystem([p0, p1, p2])
answers.append(s.gaussian_elimination())

p0 = Plane(Vector([0.935, 1.76, -9.365]), -9.955)
p1 = Plane(Vector([0.187, 0.352, -1.873]), -1.991)
p2 = Plane(Vector([0.374, 0.704, -3.746]), -3.982)
p3 = Plane(Vector([-0.561, -1.056, 5.619]), 5.973)

s = LinearSystem([p0, p1, p2, p3])
answers.append(s.gaussian_elimination())

p1 = Hyperplane(normal_vector=Vector([0.786, 0.786]), constant_term=-0.714)
p2 = Hyperplane(normal_vector=Vector([-0.131, -0.131]), constant_term=-0.319)

s = LinearSystem([p1, p2])
answers.append(s.gaussian_elimination())

p1 = Hyperplane(normal_vector=Vector([2.102, 7.489, -0.786]),
                constant_term=-5.113)
p2 = Hyperplane(normal_vector=Vector([-1.131, 8.318, 1.209]),
                constant_term=-6.775)
p3 = Hyperplane(normal_vector=Vector([9.015, -5.873, 1.105]),
                constant_term=-0.831)

s = LinearSystem([p1, p2, p3])
x = s.gaussian_elimination()
answers.append(s.gaussian_elimination())
#
p1 = Hyperplane(normal_vector=Vector([0.786, 0.786, 8.123, 1.111, -8.363]),
                constant_term=-0.714423)
# constant_term = -3.982)
p2 = Hyperplane(normal_vector=Vector([-0.131, 0.131, 7.05, -2.813, 1.19]),
                constant_term=0.318940)
# constant_term = -3.982)
p3 = Hyperplane(normal_vector=Vector([9.015, -5.873, -1.105, 2.013, -2.802]),
                constant_term=-0.004671)
# constant_term = -3.982)
s = LinearSystem([p1, p2, p3])
x = s.gaussian_elimination()
answers.append(s.gaussian_elimination())
#
# # p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
# # p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
# # s = LinearSystem([p1, p2])
# # r = s.compute_rref()
# # print('xx')
# # print(Plane(normal_vector=Vector(['1', '0', '0']), constant_term='-1'))
# # print(r[0])
# # print('yy')
# # print(r[1])
# # print(p2)
# # print('zz')
# #
# # xx = Vector(['1.2345', '0.443441234124321', '3456.78890123'])
# # print (xx)
# # print (round(xx,3))
#
#
for n, i in enumerate(answers):
    print("Answer to problem: {}\n{}\n".format(n + 1, i))
