# -*- coding: utf-8 -*-

# 获取引擎服务端API的模块
import mod.server.extraServerApi as serverApi
# 获取引擎服务端System的基类，System都要继承于ServerSystem来调用相关函数
ServerSystem = serverApi.GetServerSystemCls()
import teachScripts.Config.config as modConfig

from teachScripts.item.swordSystem import swordSystem
from teachScripts.item.armorSystem import armorSystem
from teachScripts.magic.magicSerSystem import magicSerSystem
# from TeachItemScripts.entity.entitySystem import entitySystem



from teachScripts.MoroEngine.System.Math import Math




import math
import random

class teachServerSystem(ServerSystem):
    levelId = serverApi.GetLevelId()

    swordSystem = None
    armorSystem = None
    magicSerSystem = None
    # entitySystem = None


    delay5s=0
    delay1s=0
    delays2=0
    delays5=0
    digTime=0


    def __init__(self, namespace, systemName):
        super(teachServerSystem, self).__init__(namespace, systemName)
        self.ListenEvent()

        self.swordSystem = swordSystem(self)
        self.armorSystem = armorSystem(self)
        self.magicSerSystem = magicSerSystem(self)
        # self.entitySystem = entitySystem(self)





    def ListenEvent(self):

        self.ListenForEvent(modConfig.modName, modConfig.clientName, "GenerNotifyToServer", self,self.GenerNotifyToServer)
        # self.ListenForEvent(modConfig.modName,modConfig.clientName,"BigItemGenerNotifyToServer",self, self.BigItemGenerNotifyToServer)

        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.DamageEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self, self.tick)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnNewArmorExchangeServerEvent", self, self.OnNewArmorExchangeServerEvent)
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityRemoveEvent", self,self.EntityRemoveEvent)
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEntityServerEvent",self, self.AddEntityServerEvent)
 
    def UnListenEvent(self):

        self.UnListenForEvent(modConfig.modName, modConfig.clientName, "GenerNotifyToServer", self,self.GenerNotifyToServer)
        # self.UnListenForEvent(modConfig.modName,modConfig.clientName,"BigItemGenerNotifyToServer",self, self.BigItemGenerNotifyToServer)

        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.DamageEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ClientLoadAddonsFinishServerEvent", self, self.ClientLoadAddonsFinishServerEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self, self.tick)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnNewArmorExchangeServerEvent", self, self.OnNewArmorExchangeServerEvent)
        # self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityRemoveEvent", self,self.EntityRemoveEvent)
        # self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEntityServerEvent",self, self.AddEntityServerEvent)

    #固定组件_____________________________________________________________________________________________________________________________



    # 通用发送数据包给客户端
    def GenerNotifyToClient(self, args):
        self.NotifyToClient(args["pid"], "GenerNotifyToClient", args)

    # 通用接收数据
    def GenerNotifyToServer(self, args):

        if args["event"] == "print":
            print "server","data:",args["data"]
        elif args["event"] == "SetMagic":
            self.magicSerSystem.SetMagic(args["pid"],args["itemName"])


        # if args["event"] == "buttonMove":
        #     self.buttonMove(args)
        # elif args["event"] == "getPlayerAllItem":
        #     allItem=self.getPlayerAllItem(args["pid"])
        #     self.GenerNotifyToClient({"pid": args["pid"], "event": "getPlayerAllItem", "data":allItem})



    #巨型物品引擎通用接收数据
    playID = {}
    playIDNum = 0
    def BigItemGenerNotifyToServer(self, args):
        if args["event"]=="weapon_init":
            self.BroadcastToAllClient("BigItemGenerNotifyToClient",args)
        elif args["event"]=="weapon_discard":
            self.BroadcastToAllClient("BigItemGenerNotifyToClient",args)
        elif args["event"]=="client_loaded":
            if args['playerId'] not in self.playID:
                self.playID[args['playerId']]=str(self.playIDNum)
                self.playIDNum+=1

                playID={"event":"client_loaded","playerId":args['playerId'],"playID":self.playID}


            self.BroadcastToAllClient("BigItemGenerNotifyToClient",playID)


    # 读取数据
    def GetData(self, event):
        comp = serverApi.CreateComponent(self.levelId, "Minecraft", "extraData")
        return comp.GetExtraData(modConfig.modName + event)

    # 储存数据
    def SaveData(self, args):
        serverApi.CreateComponent(self.levelId, "Minecraft", "extraData").SetExtraData(modConfig.modName + args["event"],args["data"])

    # 通用保存数据引擎
    playerData={}
    def GenerSaveData(self, playerId=False):
        if playerId:
            self.playerData = self.GetData("playerData")
            if self.playerData == None:
                self.playerData = {}
                self.SaveData({"event": "playerData", "data": self.playerData})

            if playerId not in self.playerData:
                self.playerData[playerId] = {}
                self.SaveData({"event": "playerData", "data": self.playerData})

            if "UIpos" in self.playerData[playerId]:
                self.GenerNotifyToClient({"pid": playerId, "event": "buttonMove", "data": self.playerData[playerId]["UIpos"]})

        else:
            self.SaveData({"event": "playerData", "data": self.playerData})

    # 保存UI位置
    def buttonMove(self, args):
        if "UIpos" not in self.playerData[args["pid"]]:
            self.playerData[args["pid"]]["UIpos"] = {}

        self.playerData[args["pid"]]["UIpos"][args["path"]] = args["pos"]
        self.GenerSaveData()
        if "UIpos" in self.playerData[args["pid"]]:
            self.GenerNotifyToClient({"pid": args["pid"], "event": "buttonMove", "data": self.playerData[args["pid"]]["UIpos"]})



    #获取玩家全部物品
    def getPlayerAllItem(self,playerId):
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        allItem=[]
        for i in range(0,36):
            allItem.append(comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i))
        return allItem


    #原生事件_____________________________________________________________________________________________________________________________

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        self.UnListenEvent()


    # 客户端加载完成事件
    def ClientLoadAddonsFinishServerEvent(self, args):
        playerId=args["playerId"]
        self.GenerSaveData(playerId)
        self.OnNewArmorExchangeServerEvent({"playerId": args["playerId"]})



    # 切换盔甲
    def OnNewArmorExchangeServerEvent(self, args):
        self.armorSystem.OnNewArmorExchangeServerEvent(args)



    # 客户端加载完成事件
    def DamageEvent(self, args):



        if args["cause"]!="none":
            self.magicSerSystem.DamageEvent(args)

            #玩家攻击
            if args["srcId"] in serverApi.GetPlayerList():
                args["itemName"]=self.getPlayerCarried(args["srcId"])

                
                self.swordSystem.PlayerDamageEvent(args)
                self.armorSystem.PlayerDamageEvent(args)

            #生物攻击
            elif args["entityId"] in serverApi.GetPlayerList():
                self.armorSystem.DamageEvent(args)





    # 每秒30次
    def tick(self):
        self.magicSerSystem.tick()

        # 1秒5次tick
        if self.delays5 <= 6:
            self.delays5 += 1
        else:
            self.delays5 = 0



        # 1秒2次tick
        if self.delays2 <= 15:
            self.delays2 += 1
        else:
            self.delays2 = 1

        # 1秒1次tick
        if self.delay1s <= 30:
            self.delay1s += 1
        else:
            self.delay1s = 1

            self.swordSystem.tick1s()
            self.magicSerSystem.tick1s()




        # 5秒1次tick
        if self.delay5s <= 150:
            self.delay5s += 1
        else:
            self.delay5s = 1
            self.armorSystem.tick5s()







    #次生事件_____________________________________________________________________________________________________________________________


    #通用组件_____________________________________________________________________________________________________________________________

    # 获取手持物品名称
    def getPlayerCarried(self, playerId):
        comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        if item:
            return item["itemName"]
        else:
            return None

    def getEnDistance(self, en, enn):  # 距离计算函数,填写两个实体返回距离

        comp1 = serverApi.CreateComponent(en, "Minecraft", "pos")
        comp2 = serverApi.CreateComponent(enn, "Minecraft", "pos")
        if comp1.GetPos() and comp2.GetPos():
            Enpos1 = comp1.GetPos()
            Enpos2 = comp2.GetPos()
            Enx = Enpos1[0]
            Eny = Enpos1[1]
            Enz = Enpos1[2]

            enx = Enpos2[0]
            eny = Enpos2[1]
            enz = Enpos2[2]

            yy = Eny - eny
            xx = Enx - enx
            zz = Enz - enz
            return math.sqrt((yy * yy) + (xx * xx) + (zz * zz))
        else:
            return 99999


    # 获取实体是否能攻击
    def getEntitiesCanAttack(self, en):
        cantAttack = ["hh3:magic_stage"]
        comp = serverApi.CreateComponent(en, "Minecraft", "engineType")
        entityType = comp.GetEngineType()

        comp = serverApi.CreateComponent(en, "Minecraft", "engineType")
        entityTypestr = comp.GetEngineTypeStr()
        # 以判断是否是 Mob 为例，如果要判断是否为弹射物，找到对应的类型Projectile修改即可

        if entityType & serverApi.GetMinecraftEnum().EntityType.Mob == serverApi.GetMinecraftEnum().EntityType.Mob:
            return True
        else:
            return False

    # 获取实体是否能攻击
    def IsGoodEntity(self, en):
        GoodEntity=["minecraft:player"]

        comp = serverApi.CreateComponent(en, "Minecraft", "engineType")
        entityType = comp.GetEngineType()

        comp = serverApi.CreateComponent(en, "Minecraft", "engineType")
        entityTypestr = comp.GetEngineTypeStr()

        if entityTypestr in GoodEntity:
            return True
        if entityType & serverApi.GetMinecraftEnum().EntityType.Animal == serverApi.GetMinecraftEnum().EntityType.Animal:
            return True
        else:
            return False


    #获取方块是否不是虚体方块，不是则返回True
    def GetBlockNotVirtual(self,blockName):
        virtualBlock=[
        "minecraft:air","minecraft:water","minecraft:flowing_water","minecraft:flowing_lava",
        "minecraft:lava","minecraft:tallgrass","minecraft:double_plant","minecraft:yellow_flower",
        "minecraft:red_flower","minecraft:seagrass","minecraft:tall_seagrass"]

        if blockName[-5:]=="_door" and blockName[-6:]=="_door2":
            return False
        if blockName in virtualBlock:
            return False
        else:
            return True