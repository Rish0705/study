# -*- coding: utf-8 -*-

# 获取引擎服务端API的模块
import mod.server.extraServerApi as serverApi
# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
ServerSystem = serverApi.GetServerSystemCls()

# 在modMain中注册的Server System类
class TutorialServerSystem(ServerSystem):


    # ServerSystem的初始化函数
    def __init__(self, namespace, systemName):
        # 首先调用父类的初始化函数
        super(TutorialServerSystem, self).__init__(namespace, systemName)
        print "===== TutorialServerSystem init ====="
        # 初始时调用监听函数监听事件
        self.ListenEvent()

    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        # 在自定义的ServerSystem中监听引擎的事件ServerChatEvent，回调函数为OnServerChat
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.DamageEvent)





    # 反监听函数，用于反监听事件，在代码中有创建注册就对应了销毁反注册是一个好的编程习惯，不要依赖引擎来做这些事。
    def UnListenEvent(self):
        # self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.DamageEvent)







    # 监听ServerChatEvent的回调函数
    # def OnServerChat(self, args):
    #     print "==== OnServerChat ==== ", args
        # # 生成掉落物品
        # # 当我们输入的信息等于右边这个值时，创建相应的物品
        # # 创建Component，用来完成特定的功能，这里是为了创建Item物品
        # playerId = args["playerId"]
        # comp = serverApi.CreateComponent(playerId, "Minecraft", "item")
        # if args["message"] == "钻石剑":                      
        #     # 调用SpawnItemToPlayerInv接口生成物品到玩家背包，参数参考《MODSDK文档》
        #     comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_sword", "count":1, 'auxValue': 0}, playerId)
        # elif args["message"] == "钻石镐":
        #     comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_pickaxe", "count":1, 'auxValue': 0}, playerId)
        # elif args["message"] == "钻石头盔":
        #     comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_helmet", "count":1, 'auxValue': 0}, playerId)
        # elif args["message"] == "钻石胸甲":
        #     comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_chestplate", "count":1, 'auxValue': 0}, playerId)
        # elif args["message"] == "钻石护腿":
        #     comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_leggings", "count":1, 'auxValue': 0}, playerId)
        # elif args["message"] == "钻石靴子":
        #     comp.SpawnItemToPlayerInv({"itemName":"minecraft:diamond_boots", "count":1, 'auxValue': 0}, playerId)
        # else:
        #     print "==== Sorry man ===="


    # 在实体ID处生成爆炸
    def CreateExplosionByEntityId(self, playerId,entityId,Range):
        comp = serverApi.GetEngineCompFactory().CreatePos(entityId) 
        pos=comp.GetPos()

        comp = serverApi.GetEngineCompFactory().CreateExplosion(serverApi.GetLevelId())
        comp.CreateExplosion(pos,Range,True,True,entityId,playerId)

    # 在实体ID自杀
    def CreateKillEntity(self,entityId):
        comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        comp.KillEntity(entityId)

    # 实体受到伤害时触发

    def DamageEvent(self, args):
        print "DamageEvent"
        playerId=args["srcId"]
        entityId=args["entityId"]
        
        if playerId in serverApi.GetPlayerList():

            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
            if item:
                itemName=item["itemName"]
                if itemName == "minecraft:diamond_sword":

                    if args["cause"] not in ["block_explosion","entity_explosion"]:
                        self.CreateExplosionByEntityId(playerId,entityId,3)
                elif itemName == "minecraft:golden_sword":
                        self.CreateKillEntity(entityId)









    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        print "===== TutorialServerSystem Destroy ====="
        # 调用上面的反监听函数来销毁
        self.UnListenEvent()
