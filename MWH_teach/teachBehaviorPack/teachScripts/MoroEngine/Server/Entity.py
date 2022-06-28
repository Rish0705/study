# coding=utf-8

# ================================================================================
# * Entity
# --------------------------------------------------------------------------------
# - Version : 1.0.0
# - Last Update : 2021/05/06
# ================================================================================

# ================================================================================
# * Import
# --------------------------------------------------------------------------------
import mod.server.extraServerApi as serverApi
from Map import Map
from ..System.Math import Math
from ..System.Error import InstanceError
# ================================================================================


class Entity(object):

    def __init__(self):
        raise InstanceError()

    @classmethod
    def InportText(cls):
        print "___________suc___________"

    # 获取实体手持物品名称
    @classmethod
    def GetCarriedItemName(cls, entityId):
        """
        获取实体手持物品名称

        :param entityId: 实体Id (str)
        :return: 手持物品的 itemName，没有则返回 None (str)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'item')
        item_dict = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if item_dict:
            return item_dict["itemName"]
        return None

    # 获取实体是否能攻击
    @classmethod
    def CanAttack(cls, entityId):
        """
        获取实体是否能攻击

        :param entityId: 实体Id (str)
        :return: 实体是否能攻击 (bool)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'engineType')
        entity_type = comp.GetEngineType()
        # 以判断是否是 Mob 为例，如果要判断是否为弹射物，找到对应的类型Projectile修改即可
        if entity_type & serverApi.GetMinecraftEnum().EntityType.Mob == serverApi.GetMinecraftEnum().EntityType.Mob:
            return True
        return False

    # 获取实体与实体的距离
    @classmethod
    def GetDistanceFromEntity(cls, entityId1, entityId2):
        """
        获取实体与实体的距离

        :param entityId1: 实体Id 1 (str)
        :param entityId2: 实体Id 2 (str)
        :return: 二者距离，如果二者有一个为空则返回 sys.maxsize (int)
        """
        comp1 = serverApi.CreateComponent(entityId1, 'Minecraft', 'pos')
        comp2 = serverApi.CreateComponent(entityId2, 'Minecraft', 'pos')
        return Math.distance3D(comp1.GetPos(), comp2.GetPos())

    # 获取实体与坐标的距离
    @classmethod
    def GetDistanceFromPosition(cls, entityId, position):
        """
        获取实体与坐标的距离

        :param entityId: 实体Id (str)
        :param position: 三维坐标 tuple(int, int, int)
        :return: 二者距离，如果二者有一个为空则返回 sys.maxsize (int)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        return Math.distance3D(comp.GetPos(), position)

    # 为实体添加药水效果
    @classmethod
    def AddEffect(cls, entityId, effectName, duration, amplifier, showParticles=False):
        """
        为实体添加指定状态效果，如果添加的状态已存在则有以下集中情况：
        1、等级大于已存在则更新状态等级及持续时间；
        2、状态等级相等且剩余时间 duration 大于已存在则刷新剩余时间；
        3、等级小于已存在则不做修改；
        4、粒子效果以新的为准

        :param entityId: 实体Id (str)
        :param effectName: 状态效果名称字符串，包括自定义状态效果和原版状态效果，原版状态效果可在wiki查询 (str)
        :param duration: 状态效果持续时间，单位秒 (int)
        :param amplifier: 状态效果的额外等级。必须在0至255之间（含）。若未指定，默认为0。注意，状态效果的第一级（如生命恢复I）对应为0，因此第二级状态效果，如生命回复II，应指定强度为1。部分效果及自定义状态效果没有强度之分，如夜视 (int)
        :param showParticles: 是否显示粒子效果，可缺省，默认为 True (bool)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.GetEngineCompFactory().CreateEffect(entityId)
        return comp.AddEffectToEntity(effectName, duration, amplifier, showParticles)

    # 增加实体最大生命
    @classmethod
    def AddMaxHealth(cls, entityId, value):
        """
        增加实体最大生命

        :param entityId: 实体Id (str)
        :param value: 增加的最大生命值，为负数就是减少 (int)
        :return: 设置后的最大生命值，失败返回0 (int)
        """
        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
        max_health = comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        success = comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, max(1, max_health + value))
        return max(1, max_health + value) if success else 0

    # 设置实体最大生命
    @classmethod
    def SetMaxHealth(cls, entityId, value):
        """
        设置实体最大生命

        :param entityId: 实体Id (str)
        :param value: 设置的生命值 (int)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
        return comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, max(1, value))

    # 获取实体生命值
    @classmethod
    def GetHealth(cls, entityId):
        """
        获取实体生命值

        :param entityId: 实体Id (str)
        :return: 实体生命值 (int)
        """
        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
        return comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)

    # 获取实体生命值百分比
    @classmethod
    def GetHealthPercent(cls, entityId):
        """
        获取实体生命值百分比

        :param entityId: 实体Id (str)
        :return: 实体生命值百分比 (float)
        """
        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
        max_health = comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        current_health = comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        return float(current_health) / max_health

    # 增加实体生命值
    @classmethod
    def AddHealth(cls, entityId, value):
        """
        增加实体的生命，如果超过上限则设置为上限。

        :param entityId: 实体Id (str)
        :param value: 增加的生命值，为负数就是减少 (int)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
        max_health = comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        current_health = comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        return comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,
                                 max(0, min(current_health + value, max_health)))

    # 设置实体伤害
    @classmethod
    def SetEntityHurt(cls, entityId, damage, attackerId=None, cause='override', childAttackerId=None, knocked=True):
        """
        设置实体伤害

        :param entityId: 实体Id (str)
        :param damage: 伤害值 (int)
        :param attackerId: 伤害来源的实体Id，可缺省，默认为 None (str)
        :param cause: 伤害来源，详见 Minecraft 枚举值文档的 ActorDamageCause 枚举，可缺省，默认为 override (str)
        :param childAttackerId: 伤害来源的子实体Id，默认为 None，比如玩家使用抛射物对实体造成伤害，该值应为抛射物Id (str)
        :param knocked: 实体是否被击退，可缺省，默认为 True (bool)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.GetEngineCompFactory().CreateHurt(entityId)
        comp.Hurt(damage, cause, attackerId, childAttackerId, knocked)

    # 移除生物（通过移动到虚空）
    @classmethod
    def RemoveEntity(cls, entityId):
        """
        移除生物（通过移动到虚空）

        :param entityId: 实体Id (str)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        position = comp.GetPos()
        if position:
            return comp.SetPos((position[0], -20, position[2]))
        return False

    # 获取实体周围随机位置 (3D)
    @classmethod
    def GetAroundRandomPosition3D(cls, entityId, radius):
        """
        获取实体周围球体内随机位置

        :param entityId: 实体Id (str)
        :param radius: 随机半径大小 (int)
        :return: pos(x, y, z) tuple(float, float, float)
        """
        comp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        return Math.randomPosition3D(comp.GetPos(), radius)

    # 获取实体周围随机位置 (2D)
    @classmethod
    def GetAroundRandomPosition2D(cls, entityId, radius):
        """
        获取实体周围圆内随机位置

        :param entityId: 实体Id (str)
        :param radius: 随机半径大小 (int)
        :return: pos(x, z) tuple(float, float)
        """
        comp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        position = comp.GetPos()
        return Math.randomPosition2D((position[0], position[2]), radius)

    # 获取实体周围随机位置 (2.5D)
    @classmethod
    def GetAroundRandomPosition25D(cls, entityId, radius, height):
        """
        获取实体周围圆柱体内随机位置

        :param entityId: 实体Id (str)
        :param radius: 随机半径大小 (int)
        :param height: 高度（以实体为中心，上下） (int)
        :return: pos(x, y, z) tuple(float, float, float)
        """
        comp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        return Math.randomPosition25D(comp.GetPos(), radius, height)

    # 获取实体手持物品特殊值
    @classmethod
    def GetCarriedItemAuxValue(cls, entityId):
        """
        获取实体手持物品特殊值

        :param entityId: 实体Id (str)
        :return: 手持物品的 auxValue，没有则返回 None (int)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'item')
        item = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if item:
            return item["auxValue"]
        return None

    # 获取实体手持物品耐久
    @classmethod
    def GetCarriedItemDurability(cls, entityId):
        """
        获取实体手持物品耐久

        :param entityId: 实体Id (str)
        :return: 耐久值 (int)
        """
        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
        item_dict = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if not item_dict:
            return 0
        return item_dict['durability']

    # 获取实体手持物品耐久百分比
    @classmethod
    def GetCarriedItemDurabilityPercent(cls, entityId):
        """
        获取实体手持物品耐久百分比

        :param entityId: 实体Id (str)
        :return: 耐久值百分比 (float)
        """
        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
        item_dict = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if not item_dict:
            return 0
        current_durability = item_dict['durability']
        comp_item = serverApi.GetEngineCompFactory().CreateItem(serverApi.GetLevelId())
        max_durability = comp_item.GetItemBasicInfo(item_dict['itemName'])['maxDurability']
        if max_durability == 0:
            return 0
        return float(current_durability) / max_durability

    # 设置实体手持物品耐久
    @classmethod
    def SetCarriedItemDurability(cls, entityId, value):
        """
        设置实体手持物品耐久

        :param entityId: 实体Id (str)
        :param value: 设置值 (int)
        :return: 设置后的耐久值，物品无耐久返回-1，物品碎裂返回0，超出上限返回 max (int)
        """
        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
        item_dict = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        comp_item = serverApi.GetEngineCompFactory().CreateItem(serverApi.GetLevelId())
        max_durability = comp_item.GetItemBasicInfo(item_dict['itemName'])['maxDurability']
        if max_durability == 0:
            return -1
        if value <= 0:
            comp.SetInvItemNum(comp.GetSelectSlotId(), 0)
            return 0
        elif value >= max_durability:
            comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, max_durability)
            return max_durability
        else:
            comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, value)
            return value

    # 增加实体手持物品耐久
    @classmethod
    def AddCarriedItemDurability(cls, entityId, value):
        """
        增加实体手持物品耐久

        :param entityId: 实体Id (str)
        :param value: 增加值，负数为减少 (int)
        :return: 设置后的耐久值，物品无耐久返回-1，物品碎裂返回0，超出上限返回 max (int)
        """
        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
        current_durability = comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        real_durability = current_durability + value
        return cls.SetCarriedItemDurability(entityId, real_durability)

    # 修复实体手持物品
    @classmethod
    def FixCarriedItem(cls, entityId):
        """
        修复实体手持物品

        :param entityId: 实体Id (str)
        :return: 修复后的耐久值 max，物品无耐久返回-1 (int)
        """
        comp = serverApi.GetEngineCompFactory().CreateItem(entityId)
        item_dict = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        comp_item = serverApi.GetEngineCompFactory().CreateItem(serverApi.GetLevelId())
        max_durability = comp_item.GetItemBasicInfo(item_dict['itemName'])['maxDurability']
        if max_durability == 0:
            return -1
        comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, max_durability)
        return max_durability

        # 获取实体是否在水里

    @classmethod
    def IsInWater(cls, entityId):
        """
        获取实体是否在水里

        :param entityId: 实体Id (str)
        :return: 是否在水里 (bool)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        position = comp.GetPos()
        if position:
            comp_block = serverApi.GetEngineCompFactory().CreateBlockInfo(entityId)
            block_name = comp_block.GetBlockNew((position[0], position[1] - 1.2, position[2]))['name']
            return block_name == 'minecraft:water' or block_name == 'minecraft:flowing_water'
        return False

    # 获取箭是否在水里
    @classmethod
    def IsArrowInWater(cls, entityId):
        """
        获取箭是否在水里

        :param entityId: 实体Id (str)
        :return: 是否在水里 (bool)
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        position = comp.GetPos()
        if position:
            comp_block = serverApi.GetEngineCompFactory().CreateBlockInfo(entityId)
            block_name = comp_block.GetBlockNew(position)['name']
            return block_name == 'minecraft:water' or block_name == 'minecraft:flowing_water'
        return False

    # 获取距离实体一定范围内的实体列表
    @classmethod
    def GetEntitiesAround(cls, entityId, radius, filter_dict={}):
        """
        # 获取距离实体一定范围内的实体列表

        :param entityId: 实体Id (str)
        :param radius: 半径 (int)
        :param filter_dict: 过滤器词典，可缺省，默认为{} (dict)
        :return: 实体列表 (list<str>)
        """
        comp = serverApi.GetEngineCompFactory().CreateGame(entityId)
        return comp.GetEntitiesAround(entityId, radius, filter_dict)

    # 将列表中实体按照离实体的距离排序（升序）
    @classmethod
    def GetSortedEntityList(cls, entityId, entity_list):
        """
        将列表中实体按照离实体的距离排序（升序）

        :param entityId: 实体Id (str)
        :param entity_list: 实体列表 (list<str>)
        :return: 实体列表（升序） (list<str>)
        """
        distance_dict = {}
        return_list = []
        for entity in entity_list:
            distance = cls.GetDistanceFromEntity(entityId, entity)
            for i in range(0, len(return_list)):
                if distance_dict[return_list[i]] > distance:
                    return_list.insert(i, entity)
                    distance_dict[entity] = distance
                    break
            if entity not in distance_dict:
                return_list.append(entity)
                distance_dict[entity] = distance
        return return_list

    # 获取实体的胶囊碰撞体
    @classmethod
    def GetCapsule(cls, entityId):
        """
        获取实体的胶囊碰撞体

        :param entityId: 实体Id (str)
        :return: 胶囊碰撞体 tuple(pos<tuple(int, int, int)>, vector<tuple(int, int, int)>, radius<int>)
        """
        comp_position = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        position = comp_position.GetFootPos()
        comp_collision = serverApi.CreateComponent(entityId, "Minecraft", "collisionBox")
        collision_box = comp_collision.GetSize()

        radius = collision_box[0] / 2
        start = (position[0], position[1] + radius, position[2])
        vector = (0, max(0.1, collision_box[1] - collision_box[0]), 0)
        return start, vector, radius

    # 获取两个实体的碰撞距离
    @classmethod
    def GetCollideDistance(cls, entityId1, entityId2):
        """
        获取两个实体的碰撞距离

        :param entityId1: 实体Id 1 (str)
        :param entityId2: 实体Id 2 (str)
        :return: 碰撞距离，-1为不碰撞 (float)
        """
        capsule1 = cls.GetCapsule(entityId1)
        capsule2 = cls.GetCapsule(entityId2)
        return Math.isCapsuleCollideCapsule(capsule1, capsule2)

    # 从实体发射射线检测碰撞实体
    @classmethod
    def GetPointedEntities(cls, entityId, distance, radius, angle_offset, entity_list):
        """
        从实体发射射线检测碰撞实体

        :param entityId: 发起检测实体Id (str)
        :param distance: 距离范围，起始距离和终止距离，例如(0, 60)，可以为负数但是第一个一定要小 tuple(int, int)
        :param radius: 射线碰撞半径
        :param angle_offset: yaw（横向）/ pitch（俯仰）偏移 tuple(int, int)
        :param entity_list: 要检测的实体列表 list
        :return: 检测到的实体列表（无序） list
        """
        comp = serverApi.CreateComponent(entityId, 'Minecraft', 'pos')
        origin = list(comp.GetPos())

        comp_type = serverApi.CreateComponent(entityId, 'Minecraft', 'engineType')
        entity_type = comp_type.GetEngineTypeStr()
        if entity_type != "minecraft:player":
            comp_collision = serverApi.CreateComponent(entityId, 'Minecraft', 'collisionBox')
            collision_box = comp_collision.GetSize()
            origin[1] += collision_box[1] * 0.725
        comp_rotation = serverApi.CreateComponent(entityId, 'Minecraft', 'rot')
        rotation = list(comp_rotation.GetRot())
        yaw = rotation[1]
        pitch = rotation[0]
        if entity_type == 'minecraft:phantom':
            pitch -= -36
            origin[1] -= 0.5
        
        # if angle_offset==None:
        #     angle_offset=(0,0)
        # if entity_list==None:
        #     entity_list=serverApi.GetEngineActor().keys()
            #self.SerSystem.pmobs


        return Map.GetPointedEntities(tuple(origin), (pitch, yaw), distance, radius, angle_offset, entity_list)

    # 从实体发射射线检测碰撞实体，并升序排序
    @classmethod
    def GetPointedEntitiesSorted(cls, entityId, distance, radius, angle_offset, entity_list):
        """
        从实体发射射线检测碰撞实体，并升序排序

        :param entityId: 发起检测实体Id (str)
        :param distance: 距离范围，起始距离和终止距离，例如(0, 60)，可以为负数但是第一个一定要小 tuple(int, int)
        :param radius: 射线碰撞半径
        :param angle_offset: yaw（横向）/ pitch（俯仰）偏移 tuple(int, int)
        :param entity_list: 要检测的实体列表 list
        :return: 检测到的实体列表（升序） list
        """
        return_list = cls.GetPointedEntities(entityId, distance, radius, angle_offset, entity_list)
        return cls.GetSortedEntityList(entityId, return_list)
