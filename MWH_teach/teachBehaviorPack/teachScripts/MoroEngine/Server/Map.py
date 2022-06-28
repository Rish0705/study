# coding=utf-8

# ================================================================================
# * Map
# --------------------------------------------------------------------------------
# - Version : 1.0.0
# - Last Update : 2021/05/06
# ================================================================================

# ================================================================================
# * Import
# --------------------------------------------------------------------------------
import mod.server.extraServerApi as serverApi
from .. import Server
from ..System.Math import Math
from ..System.Error import InstanceError
# ================================================================================


class Map(object):

    def __init__(self):
        raise InstanceError()

    # 在指定位置生成爆炸
    @classmethod
    def SetExplodeByPlace(cls, attackerId, position, radius, sourceId, breaks=False, fire=False):
        """
        在指定位置生成爆炸

        :param attackerId: 爆炸创造实体Id (str)
        :param position: 爆炸位置 tuple(float,float,float)
        :param radius: 爆炸威力，具体含义可参考 wiki 对爆炸的解释 (int)
        :param sourceId: 爆炸伤害源实体Id (str)
        :param breaks: 是否破坏方块，可缺省，默认为 False (bool)
        :param fire: 是否带火，可缺省，默认为 False (bool)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.GetEngineCompFactory().CreateExplosion(serverApi.GetLevelId())
        comp.CreateExplosion(position, radius, fire, breaks, sourceId, attackerId)

    # 在指定实体位置生成爆炸
    @classmethod
    def SetExplodeByEntity(cls, attackerId, entityId, radius, sourceId, breaks=False, fire=False):
        """
        在指定实体位置生成爆炸

        :param attackerId: 爆炸创造实体Id (str)
        :param entityId: 爆炸位置实体Id (str)
        :param radius: 爆炸威力，具体含义可参考 wiki 对爆炸的解释 (int)
        :param sourceId: 爆炸伤害源实体Id (str)
        :param breaks: 是否破坏方块，可缺省，默认为 False (bool)
        :param fire: 是否带火，可缺省，默认为 False (bool)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        position = comp.GetPos()
        if position:
            return cls.SetExplodeByPlace(attackerId, position, radius, sourceId, breaks, fire)
        return False

    # 在位置处掉落物品
    @classmethod
    def SpawnItemByPlace(cls, entityId, itemDict, position):
        """
        在位置处掉落物品

        :param entityId: 实体Id (str)
        :param itemDict: 物品信息词典 (dict)
        :param position: 指定位置 tuple(int, int, int)
        :return: 是否设置成功 (bool)
        """
        comp_dimension = serverApi.CreateComponent(entityId, 'Minecraft', 'dimension')
        dimension_id = comp_dimension.GetEntityDimensionId()
        comp_item = serverApi.CreateComponent(serverApi.GetLevelId(), 'Minecraft', 'item')
        return comp_item.SpawnItemToLevel(itemDict, dimension_id, position)

    # 在实体处掉落物品
    @classmethod
    def SpawnItemByEntity(cls, entityId, itemDict):
        """
        在实体处掉落物品

        :param entityId: 实体Id (str)
        :param itemDict: 物品信息词典 (dict)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        position = comp.GetPos()
        if position:
            return cls.SpawnItemByPlace(entityId, itemDict, position)
        return False

    # 从指定位置起，应用射线检测碰撞实体
    @classmethod
    def GetPointedEntities(cls, position, rotation, distance, radius, angle_offset, entity_list):
        """
        从指定位置起，应用射线检测碰撞实体

        :param position: 起始位置 (x, y, z) tuple(int, int, int)
        :param rotation: 起始旋转 (yaw, pitch) tuple(int, int)
        :param distance: 距离范围，起始距离和终止距离，例如(0, 60)，可以为负数但是第一个一定要小 tuple(int, int)
        :param radius: 射线碰撞半径
        :param angle_offset: yaw（横向）/ pitch（俯仰）偏移 tuple(int, int)
        :param entity_list: 要检测的实体列表 list
        :return: 检测到的实体列表（无序） list
        """
        yaw = rotation[1] + angle_offset[0]
        pitch = rotation[0] + angle_offset[1]

        direction_vector = serverApi.GetDirFromRot((pitch, yaw))
        radial_start = Math.getVectorEndPosition(position, Math.getVectorMultiply(direction_vector, distance[0]))
        radial_vector = Math.getVectorMultiply(direction_vector, distance[1] - distance[0])
        capsule_radial = (radial_start, radial_vector, radius)

        deny_list = ['None', 'minecraft:Undefined', 'minecraft:ItemEntity', 'minecraft:PrimedTnt', 'minecraft:FallingBlock',
                     'minecraft:MovingBlock', 'minecraft:Experience', 'minecraft:EnderCrystal', 'minecraft:FireworksRocket',
                     'minecraft:FishingHook', 'minecraft:Chalkboard', 'minecraft:Painting', 'minecraft:LeashKnot',
                     'minecraft:BoatRideable', 'minecraft:LightningBolt', 'minecraft:AreaEffectCloud', 'minecraft:Balloon',
                     'minecraft:Shield', 'minecraft:Lectern', 'minecraft:ArmorStand', 'minecraft:Agent',
                     'minecraft:TripodCamera', 'minecraft:Minecart', 'minecraft:MinecartRideable', 'minecraft:MinecartHopper',
                     'minecraft:MinecartTNT', 'minecraft:MinecartChest', 'minecraft:MinecartFurnace',
                     'minecraft:MinecartCommandBlock', 'minecraft:Projectile', 'minecraft:DragonFireball',
                     'minecraft:ThrownEgg', 'minecraft:Snowball', 'minecraft:ThrownPotion', 'minecraft:SmallFireball',
                     'minecraft:LingeringPotion', 'minecraft:AbstractArrow', 'minecraft:Trident']

        return_list = []
        for entity in entity_list:
            comp_entity = serverApi.CreateComponent(entity, 'Minecraft', 'engineType')
            entity_type = str(comp_entity.GetEngineTypeStr())
            if entity_type not in deny_list:
                capsule_entity = Server.Entity.Entity.GetCapsule(entity)
                if Math.isCapsuleCollideCapsule(capsule_radial, capsule_entity) >= 0:
                    return_list.append(entity)

        return return_list
