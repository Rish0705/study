
#功能方块系统

from mod.server.system.serverSystem import ServerSystem
import teachScripts.Config.config as modConfig
import mod.server.extraServerApi as serverApi
import math
import random
from teachScripts.MoroEngine.System.Math import Math


class magicSerSystem(object):
    SerSystem = None
    magicSerUtil=None

    particleDict={}
    levelId = serverApi.GetLevelId()
    funItem=modConfig.funItem
    ParticleMoveItem=[]
    weeknessEntity={}
    DoubleHurtEntity={}

    def __init__(self, SerSystem):
        self.SerSystem = SerSystem
        self.magicSerUtil = self


#原生事件_______________________________________________________________________________________________



    # 设置魔法
    def SetMagic(self,playerId,itemName):
        constant=self.GetMagicConStant(playerId)
        suc=False
        if constant:
            x,y,z=constant[0]
            velX,velY,velZ=constant[1]
            rot=constant[2]
            entityType=constant[3]

            damage=self.funItem[itemName]


            if itemName=="minecraft:stick":
                suc=True
                if self.isPlayerInWater(playerId):
                    damage+=5

                entityList=self.GetPointedEntity(playerId,50,1)

                for entityId in entityList:
                    self.SetHurt(playerId,entityId,damage)


            elif itemName=="minecraft:blaze_rod":
                suc=True

                entityList=self.GetPointedEntity(playerId,50,1)

                for entityId in entityList:
                    self.DoubleHurtEntity[entityId]=10
                    self.SetHurt(playerId,entityId,damage)

            elif itemName=="minecraft:bowl":
                Range=8
                compBlock = serverApi.GetEngineCompFactory().CreateBlockInfo(playerId)
                for eid in serverApi.GetEngineActor().keys()+serverApi.GetPlayerList():
                    if self.SerSystem.IsGoodEntity(eid):
                        if self.SerSystem.getEnDistance(playerId,eid)<=Range:

                            comp = serverApi.GetEngineCompFactory().CreateAttr(eid)
                            comp.SetEntityOnFire(0)

                for X in range(-1*Range,Range+1):
                    for Y in range(-1*Range,Range+1):
                        for Z in range(-1*Range,Range+1):
                            blockPos=(x+X, y+Y, z+Z)
                            blockDict = compBlock.GetBlockNew(blockPos)
                            if blockDict["name"] in ["minecraft:fire","minecraft:soul_fire"]:
                                compBlock.SetBlockNew(blockPos, {'name': 'minecraft:air','aux': 0})

            elif itemName=="minecraft:end_rod":
                Range=60

                compBlock = serverApi.GetEngineCompFactory().CreateBlockInfo(playerId)
                setPos=None
                dis=0

                for i in range(1,Range):
                    nowPos=(x+velX*i,y+velY*i,z+velZ*i)
                    blockName = compBlock.GetBlockNew(nowPos)['name']
                    if self.SerSystem.GetBlockNotVirtual(blockName):
                        dis=i-1
                        setPos=(x+velX*dis,y+velY*dis,z+velZ*dis)
                        break

                if setPos:
                    self.particleDict[setPos]={"time":300,"itemName":itemName,"playerId":playerId,"setPos":setPos,"pos":(x,y,z),"vel":(velX,velY,velZ),"dis":dis,"nowDis":0.6}
                    self.SerSystem.BroadcastToAllClient("GenerNotifyToClient",{"event":"SetMagic","pid":playerId,"itemName":itemName,"constant":constant,"setPos":setPos,"dis":dis})

            elif itemName=="minecraft:fireball":
                setPos=random.randint(0,99999999)
                Range=60

                self.particleDict[setPos]={"time":300,"itemName":itemName,"playerId":playerId,"pos":(x,y,z),"vel":(velX,velY,velZ),"dis":Range,"nowDis":0.6,"hurtRange":0}
                self.SerSystem.BroadcastToAllClient("GenerNotifyToClient",{"event":"SetMagic","pid":playerId,"itemName":itemName,"constant":constant,"dis":Range,})






            if suc:
                self.SerSystem.BroadcastToAllClient("GenerNotifyToClient",{"event":"SetMagic","pid":playerId,"itemName":itemName,"constant":constant})


    def particleSys(self):
        if self.particleDict:
            popKey=[]
            for particleId in self.particleDict:
                if self.particleDict[particleId]["time"]>0:
                    self.particleDict[particleId]["time"]-=1
                    self.ParticleMove(particleId)
                else:
                    popKey.append(particleId)

            for key in popKey:
                self.ParticleStop(key)
                self.particleDict.pop(key)

    #粒子运动时触发
    def ParticleMove(self,particleId):
        if "itemName" in self.particleDict[particleId]:
            itemName=self.particleDict[particleId]["itemName"]

            x,y,z=self.particleDict[particleId]["pos"]
            velX, velY, velZ=self.particleDict[particleId]["vel"]

            if itemName=="minecraft:end_rod":
                nowDis=self.particleDict[particleId]["nowDis"]
                dis=self.particleDict[particleId]["dis"]
                setPos=(x+velX*nowDis,y+velY*nowDis,z+velZ*nowDis)
                self.particleDict[particleId]["nowDis"]+=0.6

                for eid in serverApi.GetEngineActor().keys()+serverApi.GetPlayerList():
                    if self.SerSystem.getEntitiesCanAttack(eid):
                        comp = serverApi.GetEngineCompFactory().CreatePos(eid)
                        entityPos=comp.GetPos()

                        if Math.distance3D(entityPos,setPos)<=2:
                            self.SetHurt(self.particleDict[particleId]["playerId"],eid,10)


                        if nowDis>=dis:
                            self.particleDict[particleId]["time"]=0

            elif itemName=="minecraft:fireball":
                nowDis=self.particleDict[particleId]["nowDis"]
                dis=self.particleDict[particleId]["dis"]
                setPos=(x+velX*nowDis,y+velY*nowDis,z+velZ*nowDis)
                self.particleDict[particleId]["nowDis"]+=0.6

                
                if self.particleDict[particleId]["hurtRange"]<4:
                    self.particleDict[particleId]["hurtRange"]+=0.6
                else:
                    self.particleDict[particleId]["hurtRange"]=0
                    for eid in serverApi.GetEngineActor().keys()+serverApi.GetPlayerList():
                        if self.SerSystem.getEntitiesCanAttack(eid):
                            comp = serverApi.GetEngineCompFactory().CreatePos(eid)
                            entityPos=comp.GetPos()

                            if Math.distance3D(entityPos,setPos)<=3:
                                self.SetHurt(self.particleDict[particleId]["playerId"],eid,10)
                                comp = serverApi.CreateComponent(eid, "Minecraft", "action")
                                comp.SetMobKnockback(velX,velZ,5,velY,3)#击退
                                comp = serverApi.GetEngineCompFactory().CreateAttr(eid)
                                comp.SetEntityOnFire(5)


                            if nowDis>=dis:
                                self.particleDict[particleId]["time"]=0



    #粒子结束时触发
    def ParticleStop(self,particleId):
        if "itemName" in self.particleDict[particleId]:
            itemName=self.particleDict[particleId]["itemName"]


            if itemName=="minecraft:end_rod":
                playerId=self.particleDict[particleId]["playerId"]
                setPos=self.particleDict[particleId]["setPos"]
                comp = serverApi.CreateComponent(playerId, "Minecraft", "pos")
                comp.SetPos(setPos)

            # elif itemName=="minecraft:fireball":
            #     playerId=self.particleDict[particleId]["playerId"]
            #     setPos=self.particleDict[particleId]["setPos"]
            #     entityList=self.GetInRangeMobByPos(setPos,10)
            #     for entityId in entityList:
            #         self.SetHurt(playerId,entityId,5)
            #         comp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
            #         comp.SetEntityOnFire(10)





#次生事件_______________________________________________________________________________________________


    # 实体受到伤害时触发
    def DamageEvent(self, args):
        entityId=args["entityId"]

        if entityId in self.DoubleHurtEntity:
            args["damage"]=int(args["damage"]*2)






    def tick1s(self):
        if self.DoubleHurtEntity:
            popKey=[]
            for entityId in self.DoubleHurtEntity:
                if self.DoubleHurtEntity[entityId]>0:
                    self.DoubleHurtEntity[entityId]-=1
                else:
                    popKey.append(entityId)
            
            if popKey:
                for key in popKey:
                    self.DoubleHurtEntity.pop(key)







    def tick(self):
        self.particleSys()


#通用组件_______________________________________________________________________________________________

    # 获取生物范围内生物
    def GetInRangeMob(self, playerId,dis):
        comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
        playerPos=comp.GetPos()
        entityList=[]

        for eid in serverApi.GetEngineActor().keys():
            if self.SerSystem.getEntitiesCanAttack(eid):
                comp = serverApi.GetEngineCompFactory().CreatePos(eid)
                entityPos=comp.GetPos()

                if Math.distance3D(entityPos,playerPos)<=dis:
                    entityList.append(eid)
        
        return entityList



    # 获取生物范围内生物
    def GetInRangeMobByPos(self, playerPos,dis):
        entityList=[]

        for eid in serverApi.GetEngineActor().keys():
            if self.SerSystem.getEntitiesCanAttack(eid):
                comp = serverApi.GetEngineCompFactory().CreatePos(eid)
                entityPos=comp.GetPos()

                if Math.distance3D(entityPos,playerPos)<=dis:
                    entityList.append(eid)
        
        return entityList



    # 获取坐标范围内生物
    def GetInRangeMobByPos2D(self, playerPos,dis,hight):
        entityList=[]

        for eid in serverApi.GetEngineActor().keys():
            if self.SerSystem.getEntitiesCanAttack(eid):
                comp = serverApi.GetEngineCompFactory().CreatePos(eid)
                entityPos=comp.GetPos()


                yDisparity=abs(entityPos[1]-playerPos[1])

                if yDisparity<hight:
                    if Math.distance3D(entityPos,playerPos)<=dis:
                        entityList.append(eid)
        
        return entityList



    # 获取魔法引擎常用参数
    def GetMagicConStant(self,playerId):
        comppo = serverApi.CreateComponent(playerId, "Minecraft", "pos")
        pos=comppo.GetPos()
        if pos:
            compr = serverApi.CreateComponent(playerId, "Minecraft", "engineType")
            entityType=compr.GetEngineTypeStr()

            if entityType!="minecraft:player":
                compmx = serverApi.CreateComponent(playerId, "Minecraft", "collisionBox")
                Keey=compmx.GetSize()[1]
                Keex=compmx.GetSize()[0]
                pos=(pos[0],pos[1]+Keey*0.725,pos[2])

            rotComp = serverApi.CreateComponent(playerId, "Minecraft", "rot")
            rot=rotComp.GetRot()
            vel=serverApi.GetDirFromRot(rot)

            return [pos,vel,rot,entityType]
        else:
            return False


    #获取面向方块坐标
    def GetPointedBlock(self,playerId,pos,vel):
        x,y,z=pos
        velX,velY,velZ=vel
        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
        dim = serverApi.CreateComponent(playerId, "Minecraft", "dimension").GetEntityDimensionId()
        for i in range(0,60):
            blockDict = comp.GetBlockNew((x+velX*i, y+velY*i, z+velZ*i),dim)
            data=[(x+velX*i, y+velY*i, z+velZ*i),i]
            if blockDict["name"]!="minecraft:air" and blockDict["name"]!="minecraft:water":
                data[1]-=1
                return data
        
        return data



    #添加药水
    def AddEffectToEntity(self,pid,eff,time,level,par):
        if self.SerSystem.getEntitiesCanAttack(pid):
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
        if self.SerSystem.getEntitiesCanAttack(eid):
            comp = serverApi.GetEngineCompFactory().CreateHurt(eid)
            comp.Hurt(hurt,"override", pid, None, True)

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
            return item["auxValue"]
        else:
            return None


    #设置手持物品特殊值
    def setCarriedAuxValue(self,pid,auxValue):
        comp = serverApi.CreateComponent(pid, 'Minecraft', 'item')
        item = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED,0)
        if item:
            item["auxValue"]=auxValue
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
            comp = serverApi.GetEngineCompFactory().CreateExplosion(self.levelId)
            comp.CreateExplosion(pos,Range,False,False,entityId,playerId)


    #获取玩家是否在水里
    def isPlayerInWater(self,playerId):
        pos=serverApi.CreateComponent(playerId, "Minecraft", "pos").GetPos()
        blockName=serverApi.GetEngineCompFactory().CreateBlockInfo(playerId).GetBlockNew((pos[0],pos[1]-1.2,pos[2]))["name"]
        if blockName=="minecraft:water" or blockName=="minecraft:flowing_water":
            return True
        else:
            return False





    # een射线发射者实体
    # JULI射线距离
    # BIG射线口径（粗细）
    # xpy 横偏移
    # ypy 纵偏移（这两个偏移我是用来做精准度的，moba里没什么大用）
    #会返回een实体面向射线内的实体list
    def GetPointedEntity(self,een,JULI,BIG,xpy=0,ypy=0):
        returnid = []
        SWKmobs=serverApi.GetEngineActor().keys()+serverApi.GetPlayerList()
        #这个self.pmobs需要换成你的玩家实体库

        comp=serverApi.CreateComponent(een, "Minecraft", "pos")
        enpos=comp.GetPos()
        ox = enpos[0]
        oy = enpos[1]
        oz = enpos[2]
        compr = serverApi.CreateComponent(een, "Minecraft", "engineType")
        entityType=compr.GetEngineTypeStr()
        if entityType!="minecraft:player":
            compmx = serverApi.CreateComponent(een, "Minecraft", "collisionBox")
            Keey=compmx.GetSize()[1]
            Keex=compmx.GetSize()[0]
            oy+=Keey*0.725
        comp = serverApi.CreateComponent(een, "Minecraft", "rot")
        yaw=comp.GetRot()[1]+xpy
        pitch=comp.GetRot()[0]+ypy
        if entityType=="minecraft:phantom":
            pitch-=-36
            oy-=0.5
        xk = math.tan((360 - yaw)/360.0*2.0*math.pi)
        yk = math.tan((360 - pitch)/360.0*2.0*math.pi)
        key = BIG
        inlist = []
        for i in SWKmobs:
            compr = serverApi.CreateComponent(i, "Minecraft", "engineType")
            entityType=str(compr.GetEngineTypeStr())
            if entityType!="None":
                if entityType!="minecraft:Undefined" and entityType!="minecraft:ItemEntity" and entityType!="minecraft:PrimedTnt" and entityType!="minecraft:FallingBlock" and entityType!="minecraft:MovingBlock" and entityType!="minecraft:Experience" and entityType!="minecraft:EnderCrystal" and entityType!="minecraft:FireworksRocket" and entityType!="minecraft:FishingHook" and entityType!="minecraft:Chalkboard" and entityType!="minecraft:Painting" and entityType!="minecraft:LeashKnot" and entityType!="minecraft:BoatRideable" and entityType!="minecraft:LightningBolt" and entityType!="minecraft:AreaEffectCloud" and entityType!="minecraft:Balloon" and entityType!="minecraft:Shield" and entityType!="minecraft:Lectern" and entityType!="minecraft:ArmorStand" and entityType!="minecraft:Agent" and entityType!="minecraft:TripodCamera" and entityType!="minecraft:Minecart" and entityType!="minecraft:MinecartRideable" and entityType!="minecraft:MinecartHopper" and entityType!="minecraft:MinecartTNT" and entityType!="minecraft:MinecartChest" and entityType!="minecraft:MinecartFurnace" and entityType!="minecraft:MinecartCommandBlock" and entityType!="minecraft:Projectile" and entityType!="minecraft:DragonFireball" and entityType!="minecraft:ThrownEgg" and entityType!="minecraft:Snowball" and entityType!="minecraft:ThrownPotion" and entityType!="minecraft:SmallFireball" and entityType!="minecraft:LingeringPotion" and entityType!="minecraft:AbstractArrow" and entityType!="minecraft:Trident":
                    comp = serverApi.CreateComponent(i, "Minecraft", "pos")
                    
                    enpos1=comp.GetPos()
                    dx = enpos1[0] - ox
                    dy = enpos1[1] - oy + 0.5
                    dz = enpos1[2] - oz
                    comp = serverApi.CreateComponent(i, "Minecraft", "collisionBox")
                    Keey=key+comp.GetSize()[1]
                    Keex=key+comp.GetSize()[0]
                    if (dz*xk-Keex)<dx and (dz*xk+Keex)>dx and (math.sqrt((dx*dx)+(dz*dz))*yk-Keey)<dy and (math.sqrt((dx*dx)+(dz*dz))*yk+Keey)>dy:
                        if i!=een:
                            inlist.append(i)
        for o in inlist:
            comp = serverApi.CreateComponent(o, "Minecraft", "pos")
            enpos2=comp.GetPos()
            dx = enpos2[0] - ox
            dy = enpos2[1] - oy + 0.5
            dz = enpos2[2] - oz
            tanse = math.sqrt((dx*dx)+(dy*dy)+(dz*dz))
            if tanse<JULI:
                returnid.append(o)
        return inlist
        #返回射线内的实体list



    def GetDistanceByXYZ(self,enx,eny,enz,Enx,Eny,Enz):#距离计算函数,填写两个实体返回距离
        return math.sqrt(math.pow(eny-Eny,2)+math.pow(math.sqrt(math.pow(Enx-enx,2)+math.pow(Enz-enz,2)),2))

    def GetDistanceByEnXYZ(self,en,enx,eny,enz):#距离计算函数,填写两个实体返回距离
        compp = serverApi.CreateComponent(en, "Minecraft", "pos")
        Enpos=compp.GetPos()
        comp = serverApi.CreateComponent(en, "Minecraft", "collisionBox")
        bwhsize=comp.GetSize()
        if Enpos!=None:
            if bwhsize==None:
                Keey=1
                Keex=1
            else:
                Keey=bwhsize[1]/2
                Keex=bwhsize[0]/2

        
            Enx=Enpos[0]
            Eny=Enpos[1]
            Enz=Enpos[2]
            # Keey=Keey*Keey
            # Keex=Keex*Keex
            yy=Eny-eny
            xx=Enx-enx
            zz=Enz-enz
            return math.sqrt((yy*yy)+(xx*xx)+(zz*zz))
        else:
            return 9999



    #距离计算函数,填写两个实体返回距离
    def GetDistanceByEn(self,en,enn):
        comp1 = serverApi.CreateComponent(en, "Minecraft", "pos")
        comp2 = serverApi.CreateComponent(enn, "Minecraft", "pos")
        if comp1.GetPos()!=None and comp2.GetPos()!=None:
            Enpos1=comp1.GetPos()
            Enpos2=comp2.GetPos()
            Enx=Enpos1[0]
            Eny=Enpos1[1]
            Enz=Enpos1[2]

            enx=Enpos2[0]
            eny=Enpos2[1]
            enz=Enpos2[2]

            yy=Eny-eny
            xx=Enx-enx
            zz=Enz-enz
            return math.sqrt((yy*yy)+(xx*xx)+(zz*zz))
        else:
            return 99999

    #获取enlist数组内的离entity最近生物
    def GetNearestEn(self,entity,enlist,distance):
        minD=distance
        NerEn=False
        for i in enlist:
            NowDis=self.GetDistanceByEn(entity,i)
            if NowDis<minD and NowDis>=3:
                minD=NowDis
                NerEn=i
        return NerEn