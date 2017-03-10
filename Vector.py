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
    
    def cross_product(self,v):
        try:
            x = self.coordinates[1]*v.coordinates[2] - v.coordinates[1]*self.coordinates[2]
            y = self.coordinates[2]*v.coordinates[0] - v.coordinates[2]*self.coordinates[0]
            z = self.coordinates[0]*v.coordinates[1] - v.coordinates[0]*self.coordinates[1]
            return (Vector([x, y, z]))
        
        except ValueError as e:
            msg=str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise (e)
    
    def area_parallelogram(self,v):
        xp = v.cross_product(self)
        return (xp.magnitude())
    
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
        return(self.magnitude() < tolerance)
    
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
        
    def component_parallel_to (self, basis):
        try:
            ub = basis.normalized()
            weight = self.dot_product(ub)
            return (ub.scalar_multiple(weight))
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
                
    def component_orthogonal_to (self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return (self.minus(projection))
        
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e      
        
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
print ('\n2a',vec2a.minus(vec2b))
print ('\n3a',vec3a.scalar_multiple(sca3a))
        
vec4a = Vector([-0.221, 7.437])
vec4b = Vector([8.813, -1.331, -6.247])
vec4c = Vector([5.581, -2.136])
vec4d = Vector([1.996, 3.108, -4.554])

print('\n4a',vec4a.magnitude())
print('\n4b',vec4b.magnitude())
print('\n4c',vec4c.normalized())
print('\n4d',vec4d.normalized())
vec5a = Vector([7.887, 4.138])
vec5b = Vector([-8.802, 6.776])
vec6a = Vector([-5.955, -4.904, -1.874])
vec6b = Vector([-4.496, -8.755, 7.103])
vec7a = Vector([3.183, -7.627])
vec7b = Vector([-2.668, 5.319])
vec8a = Vector([7.35, 0.221, 5.188])
vec8b = Vector([2.751, 8.259, 3.985])
print('\n5a',vec5a.dot_product(vec5b))
print('\n6a',vec6a.dot_product(vec6b))
print('\n7a',vec7a.angle(vec7b))
print('\n8a',vec8a.angle(vec8b,in_degrees=True))

vec9a = Vector([-7.579, -7.88])
vec9b = Vector([22.737, 23.64])
vecaa = Vector([-2.029, 9.97, 4.172])
vecab = Vector([-9.231, -6.639, -7.245])
vecba = Vector([-2.328, -7.284, -1.214])
vecbb = Vector([-1.821, 1.072, -2.94])
vecca = Vector([2.118, 4.827])
veccb = Vector([0, 0])

print ('\n9a',vec9a.check_parallel(vec9b), vec9a.check_orthogonal(vec9b))
print ('\naa',vecaa.check_parallel(vecab), vecaa.check_orthogonal(vecab))
print ('\nba',vecba.check_parallel(vecbb), vecba.check_orthogonal(vecbb))
print ('\nca',vecca.check_parallel(veccb), vecca.check_orthogonal(veccb))

vecdv = Vector([3.039, 1.879])
vecdb = Vector([0.825, 2.036])
vecev = Vector([-9.88, -3.264, -8.159])
veceb = Vector([-2.155, -9.353, -9.473])
vecfv = Vector([3.009, -6.172, 3.692, -2.51])
vecfb = Vector([6.404, -9.144, 2.759, 8.718])

print ('\nd',vecdv.component_parallel_to(vecdb))
vecee = vecev.component_parallel_to(veceb)
print ('\ne',vecev.component_orthogonal_to(vecee))
vecfe = vecfv.component_parallel_to(vecfb)
print ('\nfp',vecfe)
print ('\nfo',vecfv.component_orthogonal_to(vecfe))

vecgv = Vector([8.462, 7.893, -8.187])
vecgw = Vector([6.984, -5.975, 4.778])
vechv = Vector([-8.987, -9.838, 5.031])
vechw = Vector([-4.268, -1.861, -8.866])
veciv = Vector([1.5, 9.547, 3.691])
veciw = Vector([-6.007, 0.124, 5.772])

print ('\ng',vecgv.cross_product(vecgw))
print ('\nh',vechv.area_parallelogram(vechw))
print ('\ni',veciv.area_parallelogram(veciw)/Decimal('2'))