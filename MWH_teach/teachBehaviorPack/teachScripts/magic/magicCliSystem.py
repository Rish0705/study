# 功能方块系统
# -*- coding: UTF-8 -*-
from mod.client.system.clientSystem import ClientSystem
from mod.client.clientEvent import ClientEvent
import mod.client.extraClientApi as clientApi
import teachScripts.Config.config as modConfig
import math
import random
from teachScripts.MoroEngine.System.Math import Math

class magicCliSystem(object):
    CliSystem = None
    magicCliUtil = None
    particleDict = {}
    funItemSwitch=False
    funItem=modConfig.funItem
    ParticleMoveItem=[]

    def __init__(self, CliSystem):
        self.CliSystem = CliSystem
        self.magicCliSystemUtil = self
        self.playerId = clientApi.GetLocalPlayerId()

    def SetMagic(self, args):
        playerId = args["pid"]
        itemName = args["itemName"]
        suc = False

        if "constant" in args:
            constant = args["constant"]
            x, y, z = constant[0]
            velX, velY, velZ = constant[1]
            rot = constant[2]
            entityType = constant[3]




    #原生事件_____________________________________________________________________________________________________________________________



    # 长按
    def HoldBeforeClientEvent(self, args):
        itemName=self.getPlayerCarried()

        if itemName in self.funItem:
            self.funItemSwitch=True
            self.CliSystem.teachUINode.setVisible("/sight",True)
            args["cancel"]=True




    # 长按后松手
    def TapOrHoldReleaseClientEvent(self, args):
        itemName=self.getPlayerCarried()
        if self.funItemSwitch:
            self.funItemSwitch=False
            self.CliSystem.teachUINode.setVisible("/sight",False)
            if itemName in self.funItem:
                self.CliSystem.GenerNotifyToServer({"event":"SetMagic","pid":self.playerId,"itemName":itemName})


    def tick(self):
        self.particleSys()



    #次生事件_____________________________________________________________________________________________________________________________




    # 设置魔法
    def SetMagic(self,args):
        constant=args["constant"]
        playerId=args["pid"]
        itemName=args["itemName"]
        suc=False

        x,y,z=constant[0]
        velX,velY,velZ=constant[1]
        rot=constant[2]
        entityType=constant[3]




        if itemName=="minecraft:stick":

            for dis in range(0,100):
                k=dis*0.5
                particleId = self.CliSystem.CreateEngineParticle("effects/end.json",(x + velX*k, y + velY*k, z + velZ*k))
                ctrlComp = self.CliSystem.CreateComponent(particleId, "Minecraft", "particleControl")
                ctrlComp.Play()
                self.particleDict[particleId]={"time":90}

        elif itemName=="minecraft:end_rod":
            k=0.6

            particleId = self.CliSystem.CreateEngineParticle("effects/moveEnd.json",(x + velX*k, y + velY*k, z + velZ*k))
            ctrlComp = self.CliSystem.CreateComponent(particleId, "Minecraft", "particleControl")
            ctrlComp.Play()



            self.particleDict[particleId]={"time":300,"itemName":itemName,"setPos":args["setPos"],"pos":(x,y,z),"vel":(velX,velY,velZ),"dis":args["dis"],"nowDis":k}

        elif itemName=="minecraft:fireball":
            k=0.6
            for i in range(0,20):
                rx=random.randint(-2,2)
                ry=random.randint(-2,2)
                rz=random.randint(-2,2)

                initPos=(x+rx + velX*k, y+ry + velY*k, z+rz + velZ*k)

                particleId = self.CliSystem.CreateEngineParticle("effects/firedragon_magic.json",initPos)
                ctrlComp = self.CliSystem.CreateComponent(particleId, "Minecraft", "particleControl")
                ctrlComp.Play()

                self.particleDict[particleId]={"time":300,"itemName":itemName,"playerId":playerId,"pos":initPos,"vel":(velX,velY,velZ),"dis":args["dis"],"nowDis":k}

        else:
            for dis in range(0,200):
                k=dis*0.5
                particleId = self.CliSystem.CreateEngineParticle("effects/end.json",(x + velX*k, y + velY*k, z + velZ*k))
                ctrlComp = self.CliSystem.CreateComponent(particleId, "Minecraft", "particleControl")
                ctrlComp.Play()
                self.particleDict[particleId]={"time":90}




    #粒子总入口
    def particleSys(self):
        if self.particleDict:
            popKey=[]
            for particleId in self.particleDict:
                if self.particleDict[particleId]["time"]>0:
                    self.particleDict[particleId]["time"]-=1
                    self.particleMove(particleId)

                else:
                    popKey.append(particleId)

            for key in popKey:

                comp = clientApi.CreateComponent(key, "Minecraft", "particleControl")
                comp.Stop()
                self.CliSystem.DestroyEntity(key)
                self.particleDict.pop(key)

    #粒子运动
    def particleMove(self,particleId):

        if "itemName" in self.particleDict[particleId]:
            itemName=self.particleDict[particleId]["itemName"]
            x,y,z=self.particleDict[particleId]["pos"]
            velX,velY,velZ=self.particleDict[particleId]["vel"]

            if itemName=="minecraft:end_rod":
                


                nowDis=self.particleDict[particleId]["nowDis"]
                dis=self.particleDict[particleId]["dis"]
                setPos=(x+velX*nowDis,y+velY*nowDis,z+velZ*nowDis)


                comp = clientApi.CreateComponent(particleId, "Minecraft", "particleTrans")
                comp.SetPos(setPos)
                self.particleDict[particleId]["nowDis"]+=0.6

                if nowDis>=dis:
                    self.particleDict[particleId]["time"]=0


            elif itemName=="minecraft:fireball":
                nowDis=self.particleDict[particleId]["nowDis"]
                dis=self.particleDict[particleId]["dis"]
                setPos=(x+velX*nowDis,y+velY*nowDis,z+velZ*nowDis)


                comp = clientApi.CreateComponent(particleId, "Minecraft", "particleTrans")
                comp.SetPos(setPos)
                self.particleDict[particleId]["nowDis"]+=0.6

                if nowDis>=dis:
                    self.particleDict[particleId]["time"]=0
                

    #通用组件_____________________________________________________________________________________________________________________________





    # 获取手持物品名称
    def getPlayerCarried(self):
        comp = clientApi.GetEngineCompFactory().CreateItem(self.playerId)
        item = comp.GetCarriedItem()
        if item:
            return item["itemName"]
        else:
            return None
