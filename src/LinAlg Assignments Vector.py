from src.vector import Vector
x1 = Vector([8.218, -9.341])
y1 = Vector([-1.129, 2.111])
x2 = Vector([7.119, 8.215])
y2 = Vector([-8.223, 0.878])
x3 = Vector([1.671, -1.012, -0.318])
y3 = 7.41
x4 = Vector([-0.221, 7.437])
x5 = Vector([8.813, -1.331, -6.247])
x6 = Vector([5.581, -2.136])
x7 = Vector([1.996, 3.108, -4.554])
x8 = Vector([7.887, 4.138])
y8 = Vector([-8.802, 6.776])
x9 = Vector([-5.955, -4.904, -1.874])
y9 = Vector([-4.496, -8.755, 7.103])
x10 = Vector([3.183, -7.627])
y10 = Vector([-2.668, 5.319])
x11 = Vector([7.35, 0.221, 5.188])
y11 = Vector([2.751, 8.259, 3.985])
x12 = Vector([-7.579, -7.88])
y12 = Vector([22.737, 23.64])
x13 = Vector([-2.029, 9.97, 4.172])
y13 = Vector([-9.231, -6.639, -7.245])
x14 = Vector([-2.328, -7.284, -1.214])
y14 = Vector([-1.821, 1.072, -2.94])
x15 = Vector([2.118, 4.4827])
y15 = Vector([0, 0])
v1  = Vector([3.039, 1.879])
b1  = Vector([0.825, 2.036])
v2  = Vector([-9.88, -3.264, -8.159])
b2  = Vector([-2.155, -9.353, -9.473])
v3  = Vector([3.009, -6.173, 3.692, -2.51])
b3  = Vector([6.404, -9.144, 2.759, 8.718])
v4  = Vector([8.462, 7.893, -8.187])
w4  = Vector([6.984, -5.975, 4.778])
v5  = Vector([-8.987, -9.838, 5.031])
w5  = Vector([-4.268, -1.861, -8.866])
v6  = Vector([1.5, 9.547, 3.691])
w6  = Vector([-6.007, 0.124, 5.772])

answers = []
answers.append(round(x1 + y1,3))
answers.append(round(x2 - y2,3))
answers.append(round(x3.scalarMultiple(y3),3))
answers.append(round(x4.magnitude(),3))
answers.append(round(x5.magnitude(),3))
answers.append(round(x6.normalise(),3))
answers.append(round(x7.normalise(),3))
answers.append(round(x8.dotProduct(y8),3))
answers.append(round(x9.dotProduct(y9),3))
answers.append(round(x10.angle(y10),3))
answers.append(round((x11.angle(y11,in_degrees=True)),3))
answers.append("Q1 Is parallel " + str(x12.isParallel(y12)) + " : Is orthogonal " + str(x12.isOrthogonal(y12)))
answers.append("Q2 Is parallel " + str(x13.isParallel(y13)) + " : Is orthogonal " + str(x13.isOrthogonal(y13)))
answers.append("Q3 Is parallel " + str(x14.isParallel(y14)) + " : Is orthogonal " + str(x14.isOrthogonal(y14)))
answers.append("Q4 Is parallel " + str(x15.isParallel(y15)) + " : Is orthogonal " + str(x15.isOrthogonal(y15)))
answers.append(round(v1.vProjected(b1),3))
answers.append(round(v2.vOrthogonal(b2),3))
answers.append(str(round(v3.vProjected(b3),3)) + "  " + str(round(v3.vOrthogonal(b3),3)))
answers.append(round(v4.crossProduct(w4),3))
v5w5 = v5.crossProduct(w5)
answers.append(round(v5w5.magnitude(),3))
v6w6 = v6.crossProduct(w6)
answers.append(round(v6w6.magnitude()/2,3))



for i in answers:
    print(i)

