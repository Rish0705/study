
#盔甲系统

from mod.server.system.serverSystem import ServerSystem
import mod.server.extraServerApi as serverApi
import math
import random





class armorSystem(object):
    SerSystem = None
    armorUtil=None
    LevelId=serverApi.GetLevelId()
    cut=[-7,-11,-9,-6]
    ghastly={}
    NegativeEff=["slowness","mining_fatigue","hunger","weakness",
    "levitation","bad_omen","nausea"]


    def __init__(self, SerSystem):
        self.SerSystem = SerSystem
        self.armorUtil = self



#原生事件_______________________________________________________________________________________________

    #切换盔甲事件
    def OnNewArmorExchangeServerEvent(self, args):

        playerId=args["playerId"]
        armor=self.getAllArmor(playerId)
        
        if "slot" in args:
            s=str(args["slot"])
            if args["newArmorDict"]!=None:
                armor[s]=args["newArmorDict"]["itemName"]
            else:
                armor[s]=None

        armorEff=self.getAllArmorCount(armor)

        if playerId in self.SerSystem.playerData:
            self.SerSystem.playerData[playerId]["armor"]=armorEff
        else:
            self.SerSystem.playerData[playerId]={}
            self.SerSystem.playerData[playerId]["armor"]=armorEff

        self.ArmorChange(playerId,armorEff)

        print armorEff


    #玩家被攻击事件
    def DamageEvent(self,args):
        self.ArmorSkill(args)

    #玩家攻击事件
    def PlayerDamageEvent(self,args):
        self.ArmorAttackSkill(args)
        



    def tick5s(self):
        for playerId in self.SerSystem.playerData.keys():
            if "armor" in self.SerSystem.playerData[playerId]:
                armor=self.SerSystem.playerData[playerId]["armor"]

                #钻石
                if "diamond" in armor:
                    Num=self.getArmorNum(armor,"diamond")
                    if Num>=4:

                        if self.isPlayerInWater(playerId):
                            self.AddEffectToEntity(playerId,"night_vision",16,0,False)
                            self.AddEffectToEntity(playerId,"water_breathing",16,0,False)
                        
                        continue


                #金
                if "golden" in armor:
                    Num=self.getArmorNum(armor,"golden")
                    compp = serverApi.CreateComponent(playerId, "Minecraft", "pos")
                    pos=compp.GetPos()
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(playerId)
                    lightlevel = comp.GetBlockLightLevel(pos)
                    print lightlevel
                    if lightlevel<=2+Num:
                        self.AddEffectToEntity(playerId,"resistance",16,0,False)

                    if Num>=4:
                        continue



                #锁链
                if "chainmail" in armor:
                    Num=self.getArmorNum(armor,"chainmail")
                    if Num>=4:

                        if self.isPlayerInWater(playerId):
                            time=Num/2
                            self.AddEffectToEntity(playerId,"regeneration",time,0,False)

                        
                        continue

#次生事件_______________________________________________________________________________________________






    #盔甲切换触发技能
    def ArmorChange(self,playerId,armorEff):

        if "knight" in self.SerSystem.playerData[playerId].keys():
            if "knight" in armorEff:
                Num=self.getArmorNum(armorEff,"knight")
                if Num>self.SerSystem.playerData[playerId]["knight"]:
                    self.SerSystem.playerData[playerId]["knight"]=Num
                    self.AddMaxHealth(playerId,1)
                    self.SerSystem.GenerSaveData()
                elif Num<self.SerSystem.playerData[playerId]["knight"]:
                    self.SerSystem.playerData[playerId]["knight"]=Num
                    self.ReduceMaxHealth(playerId,1)
                    self.SerSystem.GenerSaveData()
            else:
                self.ReduceMaxHealth(playerId,self.SerSystem.playerData[playerId]["knight"])
                self.SerSystem.playerData[playerId].pop("knight")
                self.SerSystem.GenerSaveData()





    #盔甲技能(被攻击)
    def ArmorSkill(self,args):
        playerId=args["entityId"]
        entityId=args["srcId"]
        cause=args["cause"]
        #damage,knock,ignite

        print self.SerSystem.playerData
        armor=self.SerSystem.playerData[playerId]["armor"]
        
        #铁
        if "iron" in armor:
            Num=self.getArmorNum(armor,"iron")
            if cause=="fall":
                Redu=(4-Num)*0.25
                args["damage"]=int(args["damage"]*Redu)


            if Num>=4:
                return True


        #钻石
        if "diamond" in armor:
            Num=self.getArmorNum(armor,"diamond")

            level=Num/2
            time=args["damage"]/2+1

            self.AddEffectToEntity(entityId,"slowness",time,level,True)

            if Num>=4:
                return True


        #下界合金
        if "netherite" in armor:
            Num=self.getArmorNum(armor,"netherite")
            causeList=["entity_attack"]

            if Num>=4:
                causeList.append("projectile")

            if cause in causeList:
                Redu=Num*0.25
                damage=int(args["damage"]*Redu)
                self.SetHurt(playerId,entityId,damage)

            if Num>=4:
                return True


        #锁链
        if "chainmail" in armor:
            Num=self.getArmorNum(armor,"chainmail")

            if Num>=4:
                if self.isPlayerInWater(playerId):
                    args["damage"]=int(args["damage"]*0.8)
                return True


                        





    #盔甲技能(攻击)
    def ArmorAttackSkill(self,args):
        entityId=args["entityId"]
        playerId=args["srcId"]
        cause=args["cause"]
        #damage,knock,ignite
        armor=self.SerSystem.playerData[playerId]["armor"]


        #古代
        if "archaic" in armor:
            Num=self.getArmorNum(armor,"archaic")

            Redu=1+(1-self.getHealthPer(playerId))*0.25*Num
            args["damage"]=int(args["damage"]*Redu)

            if Num>=4:
                return True




    #添加效果
    def AddEffectServerEvent(self, args):
        playerId=args["entityId"]
        eff=args["effectName"]

        armor=self.SerSystem.playerData[playerId]["armor"]

        if eff in self.NegativeEff:
            #纯净
            if "purity" in armor:
                Num=self.getArmorNum(armor,"purity")
                if Num>=4:
                    for i in self.NegativeEff:
                        comp = serverApi.GetEngineCompFactory().CreateEffect(playerId)
                        res = comp.RemoveEffectFromEntity(i)
                    return True




#通用组件_______________________________________________________________________________________________

    speArmor=[
    "achelos_diving",
    "oceanus_diving",
    "sealord_diving",
    "fa",
    "night-vision_"]
    #获取盔甲数量
    def getArmorNum(self,armor,path):
        Num=armor[path]
        if Num==3:
            if len(armor)==2:
                for i in armor.keys():
                    if i!=path:
                        if i in self.speArmor:
                            Num=4

        return Num




    #增加盔甲耐久
    def addArmorDurability(self,playerId,slot,Num):
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        nj=comp.GetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.ARMOR , slot)
        comp.SetItemDurability(serverApi.GetMinecraftEnum().ItemPosType.ARMOR , slot, nj+Num)






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
    def getHealth(self,playerId):
        comp = serverApi.GetEngineCompFactory().CreateAttr(playerId)
        return comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)

    #获取生命百分比
    def getHealthPer(self,playerId):
        comp = serverApi.GetEngineCompFactory().CreateAttr(playerId)
        maxH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        nowH=comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)

        return 1/float(maxH)*nowH


    #攻击
    def SetHurt(self,pid,eid,hurt):
        comp = serverApi.GetEngineCompFactory().CreateHurt(eid)
        comp.Hurt(hurt,"override", pid, None, True)


    #在生物位置爆炸
    def SetExplodeByEntityId(self,playerId,entityId,Range):
        compp = serverApi.CreateComponent(entityId, "Minecraft", "pos")
        pos=compp.GetPos()
        if pos:
            comp = serverApi.GetEngineCompFactory().CreateExplosion(self.LevelId)
            comp.CreateExplosion(pos,Range,False,False,entityId,playerId)




    #获取玩家是否在水里
    def isPlayerInWater(self,playerId):
        pos=serverApi.CreateComponent(playerId, "Minecraft", "pos").GetPos()
        blockName=serverApi.GetEngineCompFactory().CreateBlockInfo(playerId).GetBlockNew((pos[0],pos[1]-1.2,pos[2]))["name"]
        if blockName=="minecraft:water" or blockName=="minecraft:flowing_water":
            return True
        else:
            return False




    #增加最大生命
    def AddMaxHealth(self,pid,HEALTH):
        comp = serverApi.GetEngineCompFactory().CreateAttr(pid)
        maxH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)

        comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,maxH+HEALTH)

    #减少最大生命
    def ReduceMaxHealth(self,pid,HEALTH):
        comp = serverApi.GetEngineCompFactory().CreateAttr(pid)
        maxH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)

        if maxH-HEALTH<1:
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,1)
        else:
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH,maxH-HEALTH)

    #增加最大速度
    def AddMaxSpeed(self,pid,SPEED):
        SPEED*=10000000000000000000
        print 1111111111111111111111
        comp = serverApi.GetEngineCompFactory().CreateAttr(pid)
        maxH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.SPEED)
        print maxH

        comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.SPEED,maxH+SPEED)

    #减少最大速度
    def ReduceMaxSpeed(self,pid,SPEED):
        SPEED*=10000000000000000000
        comp = serverApi.GetEngineCompFactory().CreateAttr(pid)
        maxH=comp.GetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.SPEED)

        if maxH-SPEED<1:
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.SPEED,1)
        else:
            comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.SPEED,maxH-SPEED)



    #获取全部盔甲字典
    def getAllArmor(self,playerId):
        armor={}
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        for i in range(0,4):
            ar=comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.ARMOR, i)
            s=str(i)
            if ar!=None:
                armor[s]=ar["itemName"]
            else:
                armor[s]=None
        return armor
        

    #获取全部盔甲计数字典
    def getAllArmorCount(self,armor):
        armorEff={}
        for i in range(0,4):
            itemName=armor[str(i)]
            if itemName!=None:
                cutName=itemName[10:self.cut[i]]
                if cutName in armorEff:
                    armorEff[cutName]+=1
                else:
                    armorEff[cutName]=1
        return armorEff









    
    crops={
    "minecraft:wheat":7,
    "minecraft:melon_stem":7,
    "minecraft:carrots":7,
    "minecraft:potatoes":7,
    "minecraft:beetroot":7,
    "minecraft:pumpkin_stem":7,
    "minecraft:aaaaaaaaa":7,
    "mwh_aoa3:seed_chilli_seeds":7,#辣椒种子
    "mwh_aoa3:seed_floracle_seeds":7,#粉花种子
    "mwh_aoa3:seed_goldicap_seeds":7,#金果种子
    "mwh_aoa3:seed_heart_fruit_seeds":7,#心果种子
    "mwh_aoa3:seed_holly_top_seeds":7,#冬青种子
    "mwh_aoa3:seed_lunacrike_seeds":7,#紫薯种子
    "mwh_aoa3:seed_tea_seeds":7,#茶籽
    "mwh_aoa3:seed_trilliad_seeds":7,#蓝花种子
    "mwh_aoa3:seed_bubble_berry_seeds":7,#泡沫浆果种子
    "mwh_aoa3:seed_luna_globe_seeds":7,#卢娜种子
    "mwh_aoa3:seed_lunalon_seeds":7,#月花种子
    "mwh_aoa3:seed_magic_marang_seeds":7,#魔法面包果种子
    "mwh_aoa3:seed_rosidon_seeds":7,#葡萄种子
    "mwh_aoa3:seed_tea_seeds":7,#茶籽

    "minecraft:nether_wart":3}

    #是否是农作物
    def IsCrops(self,blockName):
        if blockName in self.crops:
            return True
        
        return False

    #催熟农作物
    def RipeningCrops(self,playerId,pos):
        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(playerId)
        blockName = comp.GetBlockNew(pos)['name']
        if self.IsCrops(blockName):
            comp.SetBlockNew(pos, {"name": blockName,"aux":self.crops[blockName]})
            return True



