
#功能方块系统

from mod.server.system.serverSystem import ServerSystem
# import AoA3_Scripts.Config.config as modConfig
import mod.server.extraServerApi as serverApi
import math
import random
# import attack_speeds

from teachScripts.MoroEngine.System.Math import Math


class swordSystem(object):
    SerSystem = None
    swordUtil=None
    LevelId=serverApi.GetLevelId()
    creeperList=[]
    ControlAi=[]
    NegativeEff=["slowness","mining_fatigue","instant_damage","hunger","weakness",
    "poison","wither","levitation","fatal_poison","bad_omen","bad_omen","blindness","nausea"]

    allEff=["empty","speed", "slowness", "haste", "mining_fatigue", "strength", "instant_health", "instant_damage"
    , "jump_boost", "nausea", "regeneration", "resistance", "fire_resistance", "water_breathing", "invisibility"
    ,"blindness", "night_vision", "hunger", "weakness", "poison", "wither", "health_boost", "absorption", "saturation"
    , "levitation", "fatal_poison", "conduit_power", "slow_falling", "bad_omen", "village_hero"]

    candyList=[
    "mwh_aoa3:food_candy_corn",
    "mwh_aoa3:food_peppermint_candy",
    "mwh_aoa3:food_spearmint_candy",
    "mwh_aoa3:food_sour_candy",
    "mwh_aoa3:food_sour_gummy",
    "mwh_aoa3:food_sour_pop",
    "mwh_aoa3:food_eye_candy"]

    attackCooling={}
    Eatcandy_bladeList=[]
    flyEnList=[]
    ControlAiEntity={}

    def __init__(self, SerSystem):
        self.SerSystem = SerSystem
        self.swordUtil = self


#原生事件_______________________________________________________________________________________________

    # 客户端加载完成事件
    def PlayerDamageEvent(self, args):
        itemName=args["itemName"]
        playerId=args["srcId"]
        entityId=args["entityId"]
        print "PlayerDamageEvent","itemName:",itemName,"cause:",args["cause"]


        if args["cause"]=="entity_attack":
            #钻石剑
            if itemName=="minecraft:diamond_sword":
                
                entityList=[]
                for eid in serverApi.GetEngineActor().keys():               
                    if self.SerSystem.getEnDistance(entityId,eid)<=10:
                        entityList.append(eid)

                if entityList:
                    level=(len(entityList)-1)/2
                    print level
                    for eid in entityList:
                        self.AddEffectToEntity(eid,"slowness",3,level,True)


            #金剑
            elif itemName=="minecraft:golden_sword":
                comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
                effectDictList = comp.GetAllEffects()
                if effectDictList:
                    for i in effectDictList:
                        if i["effectName"] in self.NegativeEff:
                            self.AddEffectToEntity(entityId,i["effectName"],i["duration"],i["amplifier"],False)
                            comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
                            res = comp.RemoveEffectFromEntity(i["effectName"])

            #木剑
            elif itemName=="minecraft:wooden_sword":
                pass
                # comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
                # allDefense=0
                # for slot in range(0,4):
                #     Armor=comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, slot)
                #     if Armor:
                #         Defense=self.GetMinecraftArmorDefense(Armor["itemName"])
                #         if Defense:
                #             allDefense+=Defense

                # addDamage=(20-allDefense)/3
                # args["damage"]+=addDamage





            #大便剑
            elif itemName=="minecraft:dabian":
                if random.randint(0,100)<25:
                    args["damage"]=0


            #铁剑
            elif itemName=="minecraft:iron_sword":
                rotComp = serverApi.CreateComponent(playerId, "Minecraft", "rot")
                rot = rotComp.GetRot()
                velX, velY, velZ = serverApi.GetDirFromRot(rot)

                for eid in serverApi.GetEngineActor().keys():               
                    if self.SerSystem.getEnDistance(entityId,eid)<=8:
                        comp = serverApi.CreateComponent(eid, "Minecraft", "action")
                        comp.SetMobKnockback(velX,velZ,6,velY,4)#击退


        
        if args["projectileId"]:
            projectileId=args["projectileId"]
            comp = serverApi.GetEngineCompFactory().CreateEngineType(projectileId)
            EngineType=comp.GetEngineTypeStr()

            if EngineType=="minecraft:snowball":
                if itemName=="minecraft:golden_sword":

                    comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
                    comp.SetEntityOnFire(3, 1)





    # 每秒1次
    def tick1s(self):
        if self.ControlAiEntity:
            popKey=[]
            for entityId in self.ControlAiEntity:
                if self.ControlAiEntity[entityId]>0:
                    self.ControlAiEntity[entityId]-=1
                else:
                    comp = serverApi.GetEngineCompFactory().CreateControlAi(entityId)
                    comp.SetBlockControlAi(True)
                    popKey.append(entityId)
            
            if popKey:
                for key in popKey:
                    self.ControlAiEntity.pop(key)










#通用组件_______________________________________________________________________________________________

    #添加药水
    def AddEffectToEntity(self,pid,eff,time,level,par):
        comp = serverApi.CreateComponent(pid, "Minecraft", "effect")
        res = comp.AddEffectToEntity(eff,time, level, True)


    #增加生命
    def AddHealth(self,pid,HEALTH):
        comp = serverApi.GetEngineCompFactory().CreateAttr(pid)
        maxH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)

        nowH=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        if nowH+HEALTH<=maxH:
            comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, nowH+HEALTH)
        else:
            comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, maxH)


    #获取生命
    def getHealth(self,pid):
        comp = serverApi.GetEngineCompFactory().CreateAttr(pid)
        return comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)


    #攻击
    def SetHurt(self,pid,eid,hurt):
        comp = serverApi.GetEngineCompFactory().CreateHurt(eid)
        comp.Hurt(hurt,"none", pid, None, True)

    #获取背包是否有某物品如果有就减少1个
    def useItem(self,pid,itemName):
        comp = serverApi.CreateComponent(pid, 'Minecraft', 'item')
        for i in range(0,36):
            item=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i)
            if item!=None:
                if item["itemName"]==itemName:
                    comp = serverApi.GetEngineCompFactory().CreateItem(pid)
                    comp.SetInvItemNum(i, item["count"]-1)
                    return True
                    break
        return False

    #获取手持物品特殊值
    def getCarriedAuxValue(self,pid):
        comp = serverApi.CreateComponent(pid, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED,0)
        if item:
            return item["newAuxValue"]
        else:
            return None


    #设置手持物品特殊值
    def setCarriedAuxValue(self,pid,auxValue):
        comp = serverApi.CreateComponent(pid, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED,0)
        if item:
            item["newAuxValue"]=auxValue
            comp = serverApi.GetEngineCompFactory().CreateItem(pid)
            comp.SpawnItemToPlayerCarried(item,pid)





    #在实体处掉落物品
    def SpawnItemByEntity(self,en,item):
        pos=serverApi.CreateComponent(en, "Minecraft", "pos").GetPos()
        if pos:
            compw = serverApi.CreateComponent(en, "Minecraft", "dimension")
            comp = serverApi.CreateComponent(serverApi.GetLevelId(), 'Minecraft', 'item')
            comp.SpawnItemToLevel(item, compw.GetEntityDimensionId(),pos)


    #减少手持物品耐久
    def SetCarriedDurability(self,playerId,Num):
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        nj=comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0, nj-Num)
        if nj-Num<=0:
            comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
            comp.SetInvItemNum(comp.GetSelectSlotId(),0)
            return True
        else:
            return False


    #在生物位置爆炸
    def SetExplodeByEntityId(self,playerId,entityId,Range):
        compp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        pos=compp.GetPos()
        if pos:
            comp = serverApi.GetEngineCompFactory().CreateExplosion(self.LevelId)
            comp.CreateExplosion(pos,Range,False,False,entityId,playerId)


    def GetMinecraftArmorDefense(self,itemName):
        MinecraftArmorDefense={
        "minecraft:leather_helmet":1,
        "minecraft:leather_chestplate":3,
        "minecraft:leather_leggings":2,
        "minecraft:leather_boots":1,

        "minecraft:chainmail_helmet":2,
        "minecraft:chainmail_chestplate":5,
        "minecraft:chainmail_leggings":4,
        "minecraft:chainmail_boots":1,

        "minecraft:iron_helmet":2,
        "minecraft:iron_chestplate":6,
        "minecraft:iron_leggings":5,
        "minecraft:iron_boots":2,

        "minecraft:diamond_helmet":3,
        "minecraft:diamond_chestplate":8,
        "minecraft:diamond_leggings":6,
        "minecraft:diamond_boots":3,

        "minecraft:golden_helmet":2,
        "minecraft:gold_chestplate":5,
        "minecraft:golden_leggings":3,
        "minecraft:golden_boots":1,

        "minecraft:turtle_helmet":2,

        "minecraft:netherite_helmet":3,
        "minecraft:netherite_chestplate":8,
        "minecraft:netherite_leggings":6,
        "minecraft:netherite_boots":3}
        if itemName in MinecraftArmorDefense:
            return MinecraftArmorDefense[itemName]
        else:
            return False