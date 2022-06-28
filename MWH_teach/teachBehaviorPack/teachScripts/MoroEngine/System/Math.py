# coding=utf-8

# ================================================================================
# * Math
# --------------------------------------------------------------------------------
# - Version : 1.0.0
# - Last Update : 2021/04/15
# ================================================================================

# ================================================================================
# * Import
# --------------------------------------------------------------------------------
import math
import random
import sys
# ================================================================================


class Math(object):

    ESCAPE = 0.000001

    # 二维坐标距离
    @classmethod
    def distance2D(cls, position1, position2):
        if not position1 or not position2:
            return sys.maxsize
        dx = position1[0] - position2[0]
        dy = position1[1] - position2[1]
        return (dx * dx + dy * dy) ** 0.5

    # 三维坐标距离
    @classmethod
    def distance3D(cls, position1, position2):
        if not position1 or not position2:
            return sys.maxsize
        dx = position1[0] - position2[0]
        dy = position1[1] - position2[1]
        dz = position1[2] - position2[2]
        return (dx * dx + dy * dy + dz * dz) ** 0.5

    # 获取圆形中随机位置
    @classmethod
    def randomPosition2D(cls, origin, radius):
        real_radius = random.uniform(0, radius)
        real_angle = random.uniform(0, math.pi * 2)

        delta_x = real_radius * math.sin(real_angle)
        delta_z = real_radius * math.cos(real_angle)

        real_x = origin[0] + delta_x
        real_z = origin[1] + delta_z

        return real_x, real_z

    # 获取圆柱中随机位置
    @classmethod
    def randomPosition25D(cls, origin, radius, height):
        delta_x, delta_z = cls.randomPosition2D((0, 0), radius)
        delta_y = random.uniform(-height, height)

        real_x = origin[0] + delta_x
        real_y = origin[1] + delta_y
        real_z = origin[2] + delta_z

        return real_x, real_y, real_z

    # 获取球体中随机位置
    @classmethod
    def randomPosition3D(cls, origin, radius):
        real_radius = random.uniform(0, radius)
        real_angle_y = random.uniform(- math.pi / 2, math.pi / 2)

        delta_y = real_radius * math.sin(real_angle_y)
        real_radius_xz = (real_radius * real_radius - delta_y * delta_y) ** 0.5

        delta_x, delta_z = cls.randomPosition2D((0, 0), real_radius_xz)

        real_x = origin[0] + delta_x
        real_y = origin[1] + delta_y
        real_z = origin[2] + delta_z

        return real_x, real_y, real_z

    # 获取坐标是否在球体中
    @classmethod
    def isPositionInSphere(cls, sphere, position):
        distance = cls.distance3D(sphere[0], position)
        return distance <= sphere[1]

    # 获取数字是否在两数之间
    @classmethod
    def isNumberInRange(cls, range_tuple, number):
        distance = abs(range_tuple[0] - range_tuple[1]) / 2
        middle = (range_tuple[0] + range_tuple[1]) / 2
        return abs(number - middle) <= distance

    # 获取坐标是否在长方体中
    @classmethod
    def isPositionInCuboid(cls, cuboid, position):
        for i in range(0, len(position)):
            if not cls.isNumberInRange((cuboid[0][i], cuboid[1][i]), position[i]):
                return False
        return True

    # 获取坐标是否在长方形中
    @classmethod
    def isPositionInRectangle(cls, rectangle, position):
        return cls.isPositionInCuboid(rectangle, position)

    # 获取球体是否碰撞球体
    @classmethod
    def isSphereCollideSphere(cls, sphere1, sphere2):
        distance = cls.distance3D(sphere1[0], sphere2[0])
        collide_distance = abs(sphere1[1] - sphere2[1])
        return distance <= collide_distance

    # 获取向量模长
    @classmethod
    def getVectorNorm(cls, vector):
        return (vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2]) ** 0.5

    # 通过两点获取向量
    @classmethod
    def getVectorByPositions(cls, position1, position2):
        return position2[0] - position1[0], position2[1] - position1[1], position2[2] - position1[2]

    # 向量翻倍
    @classmethod
    def getVectorMultiply(cls, vector, value):
        return vector[0] * value, vector[1] * value, vector[2] * value,

    # 获取向量终点
    @classmethod
    def getVectorEndPosition(cls, position, vector):
        return position[0] + vector[0], position[1] + vector[1], position[2] + vector[2]

    # 向量叉乘
    @classmethod
    def vectorCrossMultiply(cls, vector1, vector2):
        x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
        y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
        z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
        return x, y, z

    # 向量点乘
    @classmethod
    def vectorDotMultiply(cls, vector1, vector2):
        return vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]

    # 向量是否垂直
    @classmethod
    def isVectorVertical(cls, vector1, vector2):
        return abs(cls.vectorDotMultiply(vector1, vector2)) <= cls.ESCAPE

    # 向量是否平行
    @classmethod
    def isVectorParallel(cls, vector1, vector2):
        return cls.getVectorNorm(cls.vectorCrossMultiply(vector1, vector2)) <= cls.ESCAPE

    # 向量单位化
    @classmethod
    def getUnitVector(cls, vector):
        norm = cls.getVectorNorm(vector)
        return vector[0] / norm, vector[1] / norm, vector[2] / norm

    # 获取平行向量距离
    @classmethod
    def getParallelVectorDistance(cls, start1, start2, vector):
        base_vector = cls.getVectorByPositions(start1, start2)
        return cls.getParallelVectorDistanceByBaseVector(base_vector, vector)

    # 获取平行向量距离
    @classmethod
    def getParallelVectorDistanceByBaseVector(cls, base_vector, vector):
        return cls.getVectorNorm(cls.vectorCrossMultiply(base_vector, vector)) / cls.getVectorNorm(vector)

    # 扩展 position
    @classmethod
    def PositionMove(cls, position, value):
        return position[0] + value, position[1] + value, position[2] + value

    # 二阶行列式
    @classmethod
    def Determinant2(cls, a, b, c, d):
        return a * d - b * c

    # 三阶行列式
    @classmethod
    def Determinant3(cls, v1, v2, v3):
        a = v1[0] * v2[1] * v3[2] + v1[1] * v2[2] * v3[0] + v1[2] * v2[0] * v3[1]
        b = v1[0] * v2[2] * v3[1] + v1[1] * v2[0] * v3[2] + v1[2] * v2[1] * v3[0]
        return a - b

    # 解析垂足坐标
    @classmethod
    def phraseVerticalFoot(cls, start, vector, length, amt, direction):
        g0 = start[0] - direction * vector[0] * amt[2] / length
        g1 = start[1] - direction * vector[1] * amt[2] / length
        g2 = start[2] + direction * (amt[0] * vector[0] + amt[1] * vector[1]) / length
        return g0, g1, g2

    # 求空间两直线公垂线交点坐标
    @classmethod
    def getVerticalFoot(cls, start1, vector1, start2, vector2):

        a0 = cls.Determinant2(vector1[1], vector1[2], vector2[1], vector2[2])
        a1 = cls.Determinant2(vector1[2], vector1[0], vector2[2], vector2[0])
        a2 = cls.Determinant2(vector1[0], vector1[1], vector2[0], vector2[1])

        b0 = cls.Determinant2(vector2[1], a1, vector2[2], a2)
        b1 = cls.Determinant2(vector2[2], a2, vector2[0], a0)
        b2 = cls.Determinant2(vector2[0], a0, vector2[1], a1)

        w1 = cls.Determinant3((a0, a1, a2), (b0, b1, b2), (vector1[1], -vector1[0], 0))
        d1 = b0 * (start2[0] - start1[0]) + b1 * (start2[1] - start1[1]) + b2 * (start2[2] - start1[2])

        foot1 = cls.phraseVerticalFoot(start1, vector1, w1, (a0, a1, a2), d1)

        c0 = vector1[1] * (vector1[0] * vector2[1] - vector2[0] * vector1[1]) + vector1[2] * (vector1[0] * vector2[2] - vector1[2] * vector2[0])
        c1 = vector1[2] * (vector1[1] * vector2[2] - vector2[1] * vector1[2]) + vector1[0] * (vector1[1] * vector2[0] - vector2[1] * vector1[0])
        c2 = vector1[0] * (vector1[2] * vector2[0] - vector2[2] * vector1[0]) + vector1[1] * (vector1[2] * vector2[1] - vector2[2] * vector1[1])

        w2 = vector2[1] * (a1 * c2 - c1 * a2) + vector2[0] * (a0 * c2 - c0 * a2)
        d2 = c0 * (start1[0] - start2[0]) + c1 * (start1[1] - start2[1]) + c2 * (start1[2] - start2[2])

        foot2 = cls.phraseVerticalFoot(start2, vector2, w2, (a0, a1, a2), d2)

        return foot1, foot2

    # 获取胶囊体是否碰撞另一个胶囊体，返回碰撞距离，不碰撞返回-1
    @classmethod
    def isCapsuleCollideCapsule(cls, capsule1, capsule2):
        start1 = capsule1[0]
        vector1 = cls.getUnitVector(capsule1[1])
        radius1 = capsule1[2]
        start2 = capsule2[0]
        vector2 = cls.getUnitVector(capsule2[1])
        radius2 = capsule2[2]

        end1 = cls.getVectorEndPosition(start1, capsule1[1])
        end2 = cls.getVectorEndPosition(start2, capsule2[1])
        distance = radius2 + radius1

        # 平行
        if cls.isVectorParallel(vector1, vector2):
            base_vector = cls.getVectorByPositions(start1, start2)
            vector_distance = cls.getParallelVectorDistanceByBaseVector(base_vector, vector1)
            if vector_distance > distance:
                return -1
            # 共线
            if cls.isVectorParallel(base_vector, vector1) and cls.isVectorParallel(base_vector, vector2):
                start1_inline = cls.isPositionInCuboid((start2, end2), start1)
                end1_inline = cls.isPositionInCuboid((start2, end2), end1)
                start2_inline = cls.isPositionInCuboid((start1, end1), start2)
                end2_inline = cls.isPositionInCuboid((start1, end1), end2)
                if start1_inline or end1_inline or start2_inline or end2_inline:
                    return vector_distance

                min_distance = min(cls.distance3D(start1, start2), cls.distance3D(end1, end2),
                                   cls.distance3D(start1, end2), cls.distance3D(end1, start2))
                return min_distance if min_distance <= distance else -1

            # 不共线
            matrix_vector = cls.vectorCrossMultiply(base_vector, vector1)
            vertical_matrix_vector = cls.vectorCrossMultiply(vector1, matrix_vector)
            vertical_matrix_uni_vector = cls.getUnitVector(vertical_matrix_vector)
            move_vector = cls.getVectorMultiply(vertical_matrix_uni_vector, vector_distance)
            reverse_move_vector = cls.getVectorMultiply(move_vector, -1)

            start1_inline = cls.isPositionInCuboid((start2, end2), cls.getVectorEndPosition(start1, move_vector))
            end1_inline = cls.isPositionInCuboid((start2, end2), cls.getVectorEndPosition(end1, move_vector))
            start2_inline = cls.isPositionInCuboid((start1, end1), cls.getVectorEndPosition(start2, reverse_move_vector))
            end2_inline = cls.isPositionInCuboid((start1, end1), cls.getVectorEndPosition(end2, reverse_move_vector))
            if start1_inline or end1_inline or start2_inline or end2_inline:
                return vector_distance

            min_distance = min(cls.distance3D(start1, start2), cls.distance3D(end1, end2),
                               cls.distance3D(start1, end2), cls.distance3D(end1, start2))
            return min_distance if min_distance <= distance else -1

        # 不平行
        foot = cls.getVerticalFoot(start1, vector1, start2, vector2)

        position1 = foot[0]
        position2 = foot[1]

        real_distance = cls.distance3D(position1, position2)

        position1_inline = cls.isPositionInCuboid((start1, end1), position1)
        position2_inline = cls.isPositionInCuboid((start2, end2), position2)

        if position1_inline and position2_inline:
            min_distance = cls.distance3D(position1, position2)
            return real_distance if min_distance <= distance else -1
        if position1_inline:
            min_distance = min(cls.distance3D(position1, start2), cls.distance3D(position1, end2))
            return real_distance if min_distance <= distance else -1
        if position2_inline:
            min_distance = min(cls.distance3D(position2, start1), cls.distance3D(position2, end1))
            return real_distance if min_distance <= distance else -1

        min_distance = min(cls.distance3D(start1, start2), cls.distance3D(end1, end2),
                           cls.distance3D(start1, end2), cls.distance3D(end1, start2))
        return min_distance if min_distance <= distance else -1
