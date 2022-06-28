# coding=utf-8

# ================================================================================
# * Player
# --------------------------------------------------------------------------------
# - Version : 1.0.0
# - Last Update : 2021/05/06
# ================================================================================

# ================================================================================
# * Import
# --------------------------------------------------------------------------------
import mod.server.extraServerApi as serverApi
from ..System.Math import Math
from ..System.Error import InstanceError
# ================================================================================


class Player(object):

    def __init__(self):
        raise InstanceError()

    # 使用物品
    @classmethod
    def UseItem(cls, playerId, itemName, count=1):
        """
        使用物品

        :param playerId: 玩家Id (str)
        :param itemName: 物品的 ItemName (str)
        :param count: 使用数量，可缺省，默认为 1 (int)
        :return: 是否使用成功 (bool)
        """
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        temp_array = []
        have_count = 0
        for i in range(0, 36):
            item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i)
            if item and item['itemName'] == itemName:
                have_count += item['count']
                if have_count > count:
                    for j in temp_array:
                        comp.SetInvItemNum(j, 0)
                    comp.SetInvItemNum(i, have_count - count)
                    return True
                temp_array.append(i)
        return False

    # 设置玩家手持物品特殊值
    @classmethod
    def SetCarriedItemAuxValue(cls, playerId, auxValue):
        """
        设置玩家手持物品特殊值

        :param playerId: 玩家Id (str)
        :param auxValue: 手持物品的 auxValue (int)
        :return: 是否设置成功 (bool)
        """
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if item:
            item["auxValue"] = auxValue
            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            return comp.SpawnItemToPlayerCarried(item, playerId)
        return None
