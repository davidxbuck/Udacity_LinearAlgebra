#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:40:34 2017

@author: davidxbuck
"""
class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)
        
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
                
        except TypeError:
            raise TypeError('The coordinates must be an iterable')
            
    def plus(self,v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self,v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def scalar_multiple(self,c):
        new_coordinates = [x*Decimal(c) for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        magnitude = (sum(x**Decimal(2) for x in self.coordinates))**Decimal(.5)
        return (magnitude)
    
    def normalized(self):
        try:
            direction = self.scalar_multiple(Decimal('1.0')/self.magnitude())
            return (direction)
        
        except ZeroDivisionError:
            raise Exception('cannot normalize the zero vector')
        
    def dot_product(self,v):
        return (sum([x*y for x,y in zip(self.coordinates, v.coordinates)]))
    
    def angle(self,v,in_degrees=False):
        try:
            xmag = self.magnitude()
            ymag = v.magnitude()
            angle = math.acos(self.dot_product(v)/(xmag*ymag))
            if in_degrees:
                return (math.degrees(angle))
            else:
                return (angle)
        
        except Exception as e:
            if str(e) ==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('cannot compute an angle with the zero vector')
            else:
                raise e
                
    def check_zero(self, tolerance = 1e-10):
        return(abs(sum(x for x in self.coordinates)) < tolerance)
    
    def check_parallel(self,v):
        if self.magnitude() == 0 or v.magnitude() == 0 or self.angle(v) == 0 or self.angle(v) == math.pi :
            return(True)
        else:
            return(False)

    def check_orthogonal(self, v, tolerance = 1e-10):
        if self.check_zero() or v.check_zero() or abs(self.dot_product(v)) < tolerance :
            return(True)
        else:
            return(False)
        
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
    
    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
import math
from decimal import Decimal, getcontext
    
getcontext().prec = 30

vec1a = Vector([8.218, -9.341])
vec1b = Vector([-1.129, 2.111])
vec2a = Vector([7.119, 8.215])
vec2b = Vector([-8.223, 0.878])
vec3a = Vector([1.671, -1.012, -0.318])
sca3a = 7.41

print ('1a',vec1a.plus(vec1b))
print ('2a',vec2a.minus(vec2b))
print ('3a',vec3a.scalar_multiple(sca3a))
        
vec4a = Vector([-0.221, 7.437])
vec4b = Vector([8.813, -1.331, -6.247])
vec4c = Vector([5.581, -2.136])
vec4d = Vector([1.996, 3.108, -4.554])

print('4a',vec4a.magnitude())
print('4b',vec4b.magnitude())
print('4c',vec4c.normalized())
print('4d',vec4d.normalized())
vec5a = Vector([7.887, 4.138])
vec5b = Vector([-8.802, 6.776])
vec6a = Vector([-5.955, -4.904, -1.874])
vec6b = Vector([-4.496, -8.755, 7.103])
vec7a = Vector([3.183, -7.627])
vec7b = Vector([-2.668, 5.319])
vec8a = Vector([7.35, 0.221, 5.188])
vec8b = Vector([2.751, 8.259, 3.985])
print('5a',vec5a.dot_product(vec5b))
print('6a',vec6a.dot_product(vec6b))
print('7a',vec7a.angle(vec7b))
print('8a',vec8a.angle(vec8b,in_degrees=True))

vec9a = Vector([-7.579, -7.88])
vec9b = Vector([22.737, 23.64])
vecaa = Vector([-2.029, 9.97, 4.172])
vecab = Vector([-9.231, -6.639, -7.245])
vecba = Vector([-2.328, -7.284, -1.214])
vecbb = Vector([-1.821, 1.072, -2.94])
vecca = Vector([2.118, 4.827])
veccb = Vector([0, 0])

print ('9a',vec9a.check_parallel(vec9b), vec9a.check_orthogonal(vec9b))
print ('aa',vecaa.check_parallel(vecab), vecaa.check_orthogonal(vecab))
print ('ba',vecba.check_parallel(vecbb), vecba.check_orthogonal(vecbb))
print ('ca',vecca.check_parallel(veccb), vecca.check_orthogonal(veccb))
