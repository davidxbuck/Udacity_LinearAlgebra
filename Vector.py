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
            self.coordinates = tuple(coordinates)
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
        new_coordinates = [x*c for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        magnitude = (sum(x**2 for x in self.coordinates))**.5
        return (magnitude)
    
    def normalized(self):
        try:
            direction = self.scalar_multiple(1./self.magnitude())
            return (direction)
        
    except ZeroDivisionError:
        raise Exception('cannot normalize the zero vector')
            
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
    
    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
vec1a = Vector([8.218, -9.341])
vec1b = Vector([-1.129, 2.111])
vec2a = Vector([7.119, 8.215])
vec2b = Vector([-8.223, 0.878])
vec3a = Vector([1.671, -1.012, -0.318])
sca3a = 7.41

print (vec1a.plus(vec1b))
print (vec2a.minus(vec2b))
print (vec3a.scalar_multiple(sca3a))
        
vec4a = Vector([-0.221, 7.437])
vec4b = Vector([8.813, -1.331, -6.247])
vec4c = Vector([5.581, -2.136])
vec4d = Vector([1.996, 3.108, -4.554])

print(vec4a.magnitude())
print(vec4b.magnitude())
print(vec4c.normalized())
print(vec4d.normalized())
