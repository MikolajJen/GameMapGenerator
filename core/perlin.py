import random
import math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, other):
        return self.x * other.x + self.y * other.y


def setSeed(seed=None):
    global permutation
    permutation = makePermutation(seed)


def shuffle(array):
    for i in reversed(array):
        index = round(random.random()*(i-1))
        temp = array[i]

        array[i] = array[index]
        array[index] = temp


def makePermutation(seed=None):
    rng = random.Random(seed)
    permutation = list(range(256))
    rng.shuffle(permutation)
    return permutation + permutation



# def makePermutation():
#     permutation = []
#
#     for i in range(256):
#         permutation.append(i)
#
#     shuffle(permutation)
#
#     for i in range(256):
#         permutation.append(permutation[i])
#
#     return permutation



def getConstantVector(v):

    h = v & 3

    if(h == 0):
        return Vector2(1.0, 1.0)
    elif(h == 1):
        return Vector2(-1.0, 1.0)
    elif(h == 2):
        return Vector2(-1.0, -1.0)
    else:
        return Vector2(1.0, -1.0)



def lerp(t, a1, a2):
    return a1 + t*(a2-a1)

def fade(t):
    return ((6*t - 15)*t + 10)*t*t*t

def noise2D(x, y):
    X = math.floor(x) & 255
    Y = math.floor(y) & 255

    xf = x-math.floor(x)
    yf = y-math.floor(y)



    topRight = Vector2(xf-1.0, yf - 1.0)
    topLeft = Vector2(xf, yf-1.0)
    bottomRight = Vector2(xf-1.0, yf)
    bottomLeft = Vector2(xf, yf)

    valueTopRight = permutation[permutation[X+1]+Y+1]
    valueTopLeft = permutation[permutation[X]+Y+1]
    valueBottomRight = permutation[permutation[X+1]+Y]
    valueBottomLeft = permutation[permutation[X]+Y]

    dotTopRight = topRight.dot(getConstantVector(valueTopRight))
    dotTopLeft = topLeft.dot(getConstantVector(valueTopLeft))
    dotBottomRight = bottomRight.dot(getConstantVector(valueBottomRight))
    dotBottomLeft = bottomLeft.dot(getConstantVector(valueBottomLeft))

    u = fade(xf)
    v = fade(yf)

    return(lerp(u, lerp(v, dotBottomLeft, dotTopLeft), lerp(v, dotBottomRight, dotTopRight)))




def perlinNoise(x, y):

    n = noise2D(x, y)

    n += 1.0
    n /= 2.0

    c = round(255*n)
    return (c, c, c)

def fractalBrownianMotion(x, y, numOctaves):
    result = 0.0
    amplitude = 1.0
    frequency = 0.005

    for octave in range(numOctaves):
        n = amplitude * noise2D(x * frequency, y * frequency)
        result += n

        amplitude *= 0.5
        frequency *= 2.0

    return result

    #c = round(255*result)


    #return (c, c, c)