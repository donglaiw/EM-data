#!/usr/bin/env python
__doc__ = """
3D Vector class.
Modified from the vec3d class on the pygame wiki site.
http://pygame.org/wiki/3DVectorClass
Kisuk Lee <kisuklee@mit.edu>, 2015-2016
"""

import math
import operator

class Vec3d(object):
    """
    3d vector class, supports vector and scalar operators,
    and also provides a bunch of high level functions.
    reproduced from the vec2d class on the pygame wiki site.
    """
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x_or_triple, y = None, z = None):
        if y == None:
            self.x = x_or_triple[0]
            self.y = x_or_triple[1]
            self.z = x_or_triple[2]
        else:
            self.x = x_or_triple
            self.y = y
            self.z = z

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec3d")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec3d")

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec3d(%s, %s, %s)' % (self.x, self.y, self.z)

    # Comparison
    def __eq__(self, v):
        if hasattr(v, "__getitem__") and len(v) == 3:
            return self.x == v[0] and self.y == v[1] and self.z == v[2]
        else:
            return False

    def __ne__(self, v):
        if hasattr(v, "__getitem__") and len(v) == 3:
            return self.x != v[0] or self.y != v[1] or self.z != v[2]
        else:
            return True

    def __nonzero__(self):
        return self.x or self.y or self.z

    # Generic operator handlers
    def _o2(self, v, f):
        "Any two-operator operation where the left operand is a Vec3d"
        if isinstance(v, Vec3d):
            return Vec3d(f(self.x, v.x),
                         f(self.y, v.y),
                         f(self.z, v.z))
        elif (hasattr(v, "__getitem__")):
            return Vec3d(f(self.x, v[0]),
                         f(self.y, v[1]),
                         f(self.z, v[2]))
        else:
            return Vec3d(f(self.x, v),
                         f(self.y, v),
                         f(self.z, v))

    def _r_o2(self, v, f):
        "Any two-operator operation where the right operand is a Vec3d"
        if (hasattr(v, "__getitem__")):
            return Vec3d(f(v[0], self.x),
                         f(v[1], self.y),
                         f(v[2], self.z))
        else:
            return Vec3d(f(v, self.x),
                         f(v, self.y),
                         f(v, self.z))

    def _io(self, v, f):
        "inplace operator"
        if (hasattr(v, "__getitem__")):
            self.x = f(self.x, v[0])
            self.y = f(self.y, v[1])
            self.z = f(self.z, v[2])
        else:
            self.x = f(self.x, v)
            self.y = f(self.y, v)
            self.z = f(self.z, v)
        return self

    # Addition
    def __add__(self, v):
        if isinstance(v, Vec3d):
            return Vec3d(self.x + v.x, self.y + v.y, self.z + v.z)
        elif hasattr(v, "__getitem__"):
            return Vec3d(self.x + v[0], self.y + v[1], self.z + v[2])
        else:
            return Vec3d(self.x + v, self.y + v, self.z + v)
    __radd__ = __add__

    def __iadd__(self, v):
        if isinstance(v, Vec3d):
            self.x += v.x
            self.y += v.y
            self.z += v.z
        elif hasattr(v, "__getitem__"):
            self.x += v[0]
            self.y += v[1]
            self.z += v[2]
        else:
            self.x += v
            self.y += v
            self.z += v
        return self

    # Subtraction
    def __sub__(self, v):
        if isinstance(v, Vec3d):
            return Vec3d(self.x - v.x, self.y - v.y, self.z - v.z)
        elif (hasattr(v, "__getitem__")):
            return Vec3d(self.x - v[0], self.y - v[1], self.z - v[2])
        else:
            return Vec3d(self.x - v, self.y - v, self.z - v)
    def __rsub__(self, v):
        if isinstance(v, Vec3d):
            return Vec3d(v.x - self.x, v.y - self.y, v.z - self.z)
        if (hasattr(v, "__getitem__")):
            return Vec3d(v[0] - self.x, v[1] - self.y, v[2] - self.z)
        else:
            return Vec3d(v - self.x, v - self.y, v - self.z)
    def __isub__(self, v):
        if isinstance(v, Vec3d):
            self.x -= v.x
            self.y -= v.y
            self.z -= v.z
        elif (hasattr(v, "__getitem__")):
            self.x -= v[0]
            self.y -= v[1]
            self.z -= v[2]
        else:
            self.x -= v
            self.y -= v
            self.z -= v
        return self

    # Multiplication
    def __mul__(self, v):
        if isinstance(v, Vec3d):
            return Vec3d(self.x*v.x, self.y*v.y, self.z*v.z)
        if (hasattr(v, "__getitem__")):
            return Vec3d(self.x*v[0], self.y*v[1], self.z*v[2])
        else:
            return Vec3d(self.x*v, self.y*v, self.z*v)
    __rmul__ = __mul__

    def __imul__(self, v):
        if isinstance(v, Vec3d):
            self.x *= v.x
            self.y *= v.y
            self.z *= v.z
        elif (hasattr(v, "__getitem__")):
            self.x *= v[0]
            self.y *= v[1]
            self.z *= v[2]
        else:
            self.x *= v
            self.y *= v
            self.z *= v
        return self

    # Division
    def __div__(self, v):
        return self._o2(v, operator.div)
    def __rdiv__(self, v):
        return self._r_o2(v, operator.div)
    def __idiv__(self, v):
        return self._io(v, operator.div)

    def __floordiv__(self, v):
        return self._o2(v, operator.floordiv)
    def __rfloordiv__(self, v):
        return self._r_o2(v, operator.floordiv)
    def __ifloordiv__(self, v):
        return self._io(v, operator.floordiv)

    def __truediv__(self, v):
        return self._o2(v, operator.truediv)
    def __rtruediv__(self, v):
        return self._r_o2(v, operator.truediv)
    def __itruediv__(self, v):
        return self._io(v, operator.floordiv)

    # Modulo
    def __mod__(self, v):
        return self._o2(v, operator.mod)
    def __rmod__(self, v):
        return self._r_o2(v, operator.mod)

    def __divmod__(self, v):
        return self._o2(v, operator.divmod)
    def __rdivmod__(self, v):
        return self._r_o2(v, operator.divmod)

    # Exponentation
    def __pow__(self, v):
        return self._o2(v, operator.pow)
    def __rpow__(self, v):
        return self._r_o2(v, operator.pow)

    # Bitwise operators
    def __lshift__(self, v):
        return self._o2(v, operator.lshift)
    def __rlshift__(self, v):
        return self._r_o2(v, operator.lshift)

    def __rshift__(self, v):
        return self._o2(v, operator.rshift)
    def __rrshift__(self, v):
        return self._r_o2(v, operator.rshift)

    def __and__(self, v):
        return self._o2(v, operator.and_)
    __rand__ = __and__

    def __or__(self, v):
        return self._o2(v, operator.or_)
    __ror__ = __or__

    def __xor__(self, v):
        return self._o2(v, operator.xor)
    __rxor__ = __xor__

    # Unary operations
    def __neg__(self):
        return Vec3d(operator.neg(self.x),
                     operator.neg(self.y),
                     operator.neg(self.z))

    def __pos__(self):
        return Vec3d(operator.pos(self.x),
                     operator.pos(self.y),
                     operator.pos(self.z))

    def __abs__(self):
        return Vec3d(abs(self.x), abs(self.y), abs(self.z))

    def __invert__(self):
        return Vec3d(-self.x, -self.y, -self.z)

    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2 + self.z**2

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
        self.z *= value/length
    length = property(get_length, __setlength, None,
                      "gets or sets the magnitude of the vector")

    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec3d(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return length

    def dot(self, v):
        return float(self.x*v[0] + self.y*v[1] + self.z*v[2])

    def get_distance(self, v):
        return math.sqrt((self.x - v[0])**2 +
                         (self.y - v[1])**2 +
                         (self.z - v[2])**2)

    def get_dist_sqrd(self, v):
        return (self.x - v[0])**2 + (self.y - v[1])**2 + (self.z - v[2])**2

    def projection(self, v):
        v_length_sqrd = v[0]*v[0] + v[1]*v[1] + v[2]*v[2]
        projected_length_times_v_length = self.dot(v)
        return v*(projected_length_times_v_length/v_length_sqrd)

    def cross(self, v):
        return Vec3d(self.y*v[2] - self.z*v[1],
                     self.z*v[0] - self.x*v[2],
                     self.x*v[1] - self.y*v[0])

    def interpolate_to(self, v, range):
        return Vec3d(self.x + (v[0] - self.x)*range,
                     self.y + (v[1] - self.y)*range,
                     self.z + (v[2] - self.z)*range)

    def convert_to_basis(self, x_vector, y_vector, z_vector):
        return Vec3d(self.dot(x_vector)/x_vector.get_length_sqrd(),
                     self.dot(y_vector)/y_vector.get_length_sqrd(),
                     self.dot(z_vector)/z_vector.get_length_sqrd())

    def __getstate__(self):
        return [self.x, self.y, self.z]

    def __setstate__(self, dict):
        self.x, self.y, self.z = dict


########################################################################
## Helper vector functions
########################################################################
def minimum(v1, v2):
    v1 = Vec3d(v1)
    v2 = Vec3d(v2)

    xmin = min(v1.x, v2.x)
    ymin = min(v1.y, v2.y)
    zmin = min(v1.z, v2.z)

    return Vec3d(xmin, ymin, zmin)


def maximum(v1, v2):
    v1 = Vec3d(v1)
    v2 = Vec3d(v2)

    xmax = max(v1.x, v2.x)
    ymax = max(v1.y, v2.y)
    zmax = max(v1.z, v2.z)

    return Vec3d(xmax, ymax, zmax)
