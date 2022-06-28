# -*- coding: utf-8 -*-

# 从客户端API中拿到我们需要的ViewBinder / ViewRequest / ScreenNode

import client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

import time
import math
import random
import copy


class teachUIScreen(ScreenNode):
    CSystem=None
    teachUINode=None
    mwh_bagSystemUINode=None
    startSwitch=True
    MainSwitch=True
    MainMode="按钮"


    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()
        


    def Create(self):
        pass


    #初始化
    def Init(self):
        self.AddTouchEventHandler("/menu1", self.menu1, {"isSwallow": True})
        self.AddTouchEventHandler("/menu1/start", self.menu1Start, {"isSwallow": True})
        self.AddTouchEventHandler("/menu2", self.menu2, {"isSwallow": True})
        self.AddTouchEventHandler("/menu3", self.menu3, {"isSwallow": True})
        self.AddTouchEventHandler("/menu2/m2b0", self.menu2m2b0, {"isSwallow": True})





        #二级菜单按钮
        menu2ButtomText=["功能一","功能二","功能三","功能四","功能五","功能六","功能七"]
        for i in range(0,len(menu2ButtomText)):
            self.AddTouchEventHandler("/menu2/m2b"+str(i), self.menu2Buttom, {"isSwallow": False})
            labelUIControl = self.GetBaseUIControl("/menu2/m2b"+str(i)+'/button_label').asLabel()
            labelUIControl.SetText(menu2ButtomText[i])


        #三级菜单按钮
        menu3ButtomText=["功能一","功能二","功能三","功能四","功能五","功能六","功能七"]
        for i in range(0,len(menu3ButtomText)):
            self.AddTouchEventHandler("/menu3/m3b"+str(i), self.menu3Buttom, {"isSwallow": False})
            # labelUIControl = self.GetBaseUIControl("/menu3/m3b"+str(i)+'/button_label').asLabel()
            # labelUIControl.SetText(menu3ButtomText[i])











        self.closeAllSecUi()


    #统一关闭界面
    def closeAllSecUi(self):
        self.setVisible("/sight",False)
        self.setVisible("/menu1",True)
        self.setVisible("/menu2",False)
        self.setVisible("/menu3",False)





#原生事件_______________________________________________________________________________________________

    #帧事件
    def tick(self):
        
        self.RelativePosMoveUItick()





#次生事件_______________________________________________________________________________________________

    #读取位置
    def readLocation(self,data):
        self.readLocationTick=5


    #设置建造模式
    def SetBuildMode(self,mode):
        labelUIControl = self.GetBaseUIControl("/menu1"+'/button_label').asLabel()
        labelUIControl.SetText(mode)
        self.MainMode=mode





#按钮事件_______________________________________________________________________________________________





    #一级菜单
    def menu1(self,args):
        if self.RelativePosMoveUI(args,False):
            self.setVisible("/menu1",False)
            self.setVisible("/menu2",True)



    #一级菜单开始
    def menu1Start(self,args):
        if self.RelativePosMoveUI(args,"/menu1"):
            if self.MainSwitch:
                textures="stop"
                texturesBack="None"
                self.MainSwitch=False

                baseUIControl = self.teachUINode.GetBaseUIControl("/menu1")
                baseUIControl.SetSize((0,0))

                labelUIControl = self.GetBaseUIControl("/menu1"+'/button_label').asLabel()
                labelUIControl.SetText("")
            else:
                textures="star"
                texturesBack="mainMemu"
                self.MainSwitch=True

                baseUIControl = self.teachUINode.GetBaseUIControl("/menu1")
                baseUIControl.SetSize((130,33))

                labelUIControl = self.GetBaseUIControl("/menu1"+'/button_label').asLabel()
                labelUIControl.SetText(self.MainMode)
                print self.MainMode


            self.SetSpritePro("/menu1/start","textures/ui/"+textures)
            self.SetSpritePro("/menu1","textures/ui/"+texturesBack)




    #二级菜单
    def menu2(self,args):
        if self.RelativePosMoveUI(args,False):
            self.setVisible("/menu1",True)
            self.setVisible("/menu2",False)
            self.setVisible("/menu3",False)





    #二级菜单功能
    def menu2Buttom(self,args):
        if self.RelativePosMoveUI(args,"/menu2"):
            ButtonPath=args['ButtonPath']
            eid=args['ButtonPath'][-1:]
            labelUIControl = self.GetBaseUIControl(ButtonPath+'/button_label').asLabel()
            Btext=labelUIControl.GetText()

            self.SetBuildMode(Btext)


            self.setVisible("/menu1",True)
            self.setVisible("/menu2",False)
            self.setVisible("/menu3",False)

    def menu2m2b0(self,args):

            self.setVisible("/menu1",True)
            self.setVisible("/menu2",True)
            self.setVisible("/menu3",True)





    #三级菜单
    def menu3(self,args):
        if self.RelativePosMoveUI(args,False):
            self.setVisible("/menu1",True)
            self.setVisible("/menu2",True)
            self.setVisible("/menu3",False)



    #三级菜单功能
    def menu3Buttom(self,args):
        if self.RelativePosMoveUI(args,"/menu3"):
            ButtonPath=args['ButtonPath']
            eid=args['ButtonPath'][-1:]
            # labelUIControl = self.GetBaseUIControl(ButtonPath+'/button_label').asLabel()
            # Btext=labelUIControl.GetText()

            # self.SetBuildMode(Btext)

            # self.setVisible("/menu1",True)
            # self.setVisible("/menu2",False)








    #模板
    def Template(self,args):
        if self.RelativePosMoveUI(args,False):
            ButtonPath=args['ButtonPath']
            eid=args['ButtonPath'][-1:]
            labelUIControl = self.GetBaseUIControl(ButtonPath+'/button_label').asLabel()
            Btext=labelUIControl.GetText()

#通用组件_______________________________________________________________________________________________



    #设置UI显示隐藏并记录状态
    GuiState={}
    def setVisible(self,path,Bool):
        self.SetVisible(path, Bool)
        self.GuiState[path]=Bool



    #获取UI是否显示
    def getVisible(self,path):
        if path in self.GuiState:
            return self.GuiState[path]
        else:
            return None

    #简单更换图片(全换)
    def SetSpriteAll(self,imageButtonPath,imagePath):
        buttonDefaultPath = imageButtonPath + "/default"
        buttonHoverPath = imageButtonPath + "/hover"
        buttonPressedPath = imageButtonPath + "/pressed"
        self.teachUINode.SetSprite(buttonDefaultPath, imagePath)
        self.teachUINode.SetSprite(buttonHoverPath, imagePath)
        self.teachUINode.SetSprite(buttonPressedPath, imagePath)

    #简单更换图片(双图)
    def SetSpritePro(self,imageButtonPath,imagePath):
        buttonDefaultPath = imageButtonPath + "/default"
        buttonHoverPath = imageButtonPath + "/hover"
        buttonPressedPath = imageButtonPath + "/pressed"
        self.teachUINode.SetSprite(buttonDefaultPath, imagePath)
        self.teachUINode.SetSprite(buttonHoverPath, imagePath+"1")
        self.teachUINode.SetSprite(buttonPressedPath, imagePath+"1")

    # 三维坐标距离
    def distance3D(self, position1, position2):
        if not position1 or not position2:
            return 999
        dx = position1[0] - position2[0]
        dy = position1[1] - position2[1]
        dz = position1[2] - position2[2]
        return (dx * dx + dy * dy + dz * dz) ** 0.5

    #二维两点距离计算
    def Distance2D(self,pos1,pos2):
        return math.sqrt(math.pow(pos1[0]-pos2[0],2)+math.pow(pos1[1]-pos2[1],2))

    DontSaveUI=["/gemstone_panel/gemstone_button","/gemstone_panel/gemstone_button_label"]

    #UI相对移动引擎
    #开头定义:buttonMove=None
    #参数:args,特殊按钮路径(例如触摸按钮和要移动的按钮路径不一样)
    #返回值:弹起时如果在按下后移动,返回False,未移动返回True
    buttonMove=None
    def RelativePosMoveUI(self,args,BooL):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        tpos = (args["TouchPosX"], args["TouchPosY"])
        touchEvent = args["TouchEvent"]
        if BooL==False:
            tpath=args['ButtonPath']
        else:
            tpath=BooL
        if touchEvent == touchEventEnum.TouchUp:
            pos=self.GetPosition(tpath)
            if self.Distance2D(self.buttonMove[3],pos)<4:
                self.buttonMove=None
                return True
            else:
                if tpath not in self.DontSaveUI:
                    self.CSystem.GenerNotifyToServer({"pid":self.playerId,"event":"buttonMove","path":tpath,"pos":pos})

                self.buttonMove=None
                return False
        elif touchEvent == touchEventEnum.TouchDown:
            self.buttonMove=[None,None,tpath,self.GetPosition(tpath)]
        elif touchEvent == touchEventEnum.TouchCancel:
            self.buttonMove=None
        elif touchEvent == touchEventEnum.TouchMove:
            if self.buttonMove[1]==None and tpos!=(0.0,0.0):
                UIPosition = self.GetPosition(tpath)
                self.buttonMove[1]=(tpos[0]-UIPosition[0],tpos[1]-UIPosition[1])
            if self.buttonMove[1]!=None:
                self.buttonMove[0]=(tpos[0]-self.buttonMove[1][0],tpos[1]-self.buttonMove[1][1])


    #UI移动引擎tick组件
    def RelativePosMoveUItick(self):
        if self.buttonMove!=None:
            if self.buttonMove[0]!=None:

                if self.buttonMove[2]=="/gemstone_panel/gemstone_button" or self.buttonMove[2]=="/gemstone_panel/gemstone_button_label":
                    pmax=(-200,-350)
                    pmin=(-1100,-1100)
                    if self.buttonMove[0][0]>pmax[0]:
                        self.buttonMove[0]=(pmax[0],self.buttonMove[0][1])
                    if self.buttonMove[0][0]<pmin[0]:
                        self.buttonMove[0]=(pmin[0],self.buttonMove[0][1])
                    if self.buttonMove[0][1]>pmax[1]:
                        self.buttonMove[0]=(self.buttonMove[0][0],pmax[1])
                    if self.buttonMove[0][1]<pmin[1]:
                        self.buttonMove[0]=(self.buttonMove[0][0],pmin[1])

                self.SetPosition(self.buttonMove[2], self.buttonMove[0])