# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import mod.client.extraClientApi as clientApi
# 获取客户端system的基类ClientSystem
ClientSystem = clientApi.GetClientSystemCls()
import teachScripts.Config.config as modConfig
from mod.client.clientEvent import ClientEvent


from teachScripts.magic.magicCliSystem import magicCliSystem
# from TeachItemScripts.item.bigItemSystem import bigItemSystem





class teachClientSystem(ClientSystem):
    teachUINode=None

    magicCliSystem=None
    bigItemSystem=None


    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        super(teachClientSystem, self).__init__(namespace, systemName)
        self.ListenEvent()
        comp = clientApi.GetEngineCompFactory().CreateQueryVariable(clientApi.GetLevelId())


        self.playerId = clientApi.GetLocalPlayerId()
        self.leveId = clientApi.GetLevelId()


        self.magicCliSystem=magicCliSystem(self)
        # self.bigItemSystem=bigItemSystem(self)


    def ListenEvent(self): 


        # 注册自定义通讯
        self.ListenForEvent(modConfig.modName, modConfig.serverName, "GenerNotifyToClient", self,self.GenerNotifyToClient)
        # self.ListenForEvent(modConfig.modName, modConfig.serverName, "BigItemGenerNotifyToClient", self,self.BigItemPivot)

        #注册ui
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), ClientEvent.UiInitFinished,self, self.OnUIInitFinished)
        # # #注册网易接口的事件
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self,self.tick)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "TapOrHoldReleaseClientEvent", self,self.TapOrHoldReleaseClientEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "HoldBeforeClientEvent", self,self.HoldBeforeClientEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "RightClickReleaseClientEvent", self,self.RightClickReleaseClientEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "RightClickBeforeClientEvent", self,self.RightClickBeforeClientEvent)
        
        # self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnCarriedNewItemChangedClientEvent", self, self.OnItemChanged)
        # self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnLocalPlayerStopLoading", self, self.OnLocalPlayerStopLoading)

    def UnListenEvent(self):


        self.UnListenForEvent(modConfig.modName, modConfig.serverName, "GenerNotifyToClient", self,self.GenerNotifyToClient)
        # self.UnListenForEvent(modConfig.modName, modConfig.serverName, "BigItemGenerNotifyToClient", self,self.BigItemPivot)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self,self.tick)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "TapOrHoldReleaseClientEvent", self,self.TapOrHoldReleaseClientEvent)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "HoldBeforeClientEvent", self,self.HoldBeforeClientEvent)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "RightClickReleaseClientEvent", self,self.RightClickReleaseClientEvent)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "RightClickBeforeClientEvent", self,self.RightClickBeforeClientEvent)
        # self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnCarriedNewItemChangedClientEvent", self, self.OnItemChanged)
        # self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnLocalPlayerStopLoading", self, self.OnLocalPlayerStopLoading)




    def Destroy(self):
        self.UnListenEvent()



    # UI创建完成
    pcorpe=0
    buttonMove = {}
    def OnUIInitFinished(self, args):

        # #背包系统
        # clientApi.RegisterUI(modConfig.modName, "MWH_bagSystem", "TeachItemScripts.UI.MWH_bagSystem.MWH_bagSystemUIScreen","MWH_bagSystem.main")
        # self.mwh_bagSystemUINode = clientApi.CreateUI(modConfig.modName, "MWH_bagSystem", {"isHud": 1})

        clientApi.RegisterUI(modConfig.modName, "teachUI", "teachScripts.UI.teachUI.teachUIScreen","teachUI.main")
        self.teachUINode = clientApi.CreateUI(modConfig.modName, "teachUI", {"isHud": 1})


        if self.teachUINode:
            self.teachUINode.CSystem = self
            self.teachUINode.teachUINode = self.teachUINode
            # self.teachUINode.mwh_bagSystemUINode = self.mwh_bagSystemUINode
            self.teachUINode.Init()

        #     self.mwh_bagSystemUINode.CSystem = self
        #     self.mwh_bagSystemUINode.otherUINode = self.teachUINode
        #     self.mwh_bagSystemUINode.mwh_bagSystemUINode = self.mwh_bagSystemUINode
        #     self.mwh_bagSystemUINode.Init()

        # # 发送UInode
        # if self.iceAndFireUINode:
        #     # 获取平台
        #     if self.GetPlatform() == 0:
        #         self.pcorpe = 1
        #     else:
        #         self.pcorpe = 0





    # 通用发送数据
    def GenerNotifyToServer(self, args):
        self.NotifyToServer("GenerNotifyToServer", args)

    # 通用接收数据
    def GenerNotifyToClient(self, args):
        if args["event"] == "SetMagic":
            self.magicCliSystem.SetMagic(args)
        # elif args["event"] == "getPlayerAllItem":
        #     self.mwh_bagSystemUINode.getPlayerAllItem(args)


    #原生事件_____________________________________________________________________________________________________________________________



    def tick(self):
        if self.teachUINode:
            self.magicCliSystem.tick()
            self.teachUINode.tick()
            
        #     self.mwh_bagSystemUINode.tick()

    # 长按
    def RightClickBeforeClientEvent(self, args):
        self.HoldBeforeClientEvent(args)
        # self.bigItemSystem.HoldBeforeClientEvent(args)

    # 长按后松手
    def RightClickReleaseClientEvent(self, args):
        self.TapOrHoldReleaseClientEvent(args)

    # 长按
    def HoldBeforeClientEvent(self, args):
        self.magicCliSystem.HoldBeforeClientEvent(args)

    # 长按后松手
    def TapOrHoldReleaseClientEvent(self, args):

        # self.GenerNotifyToServer({"event":"print","pid":self.playerId,"data":123})
        self.magicCliSystem.TapOrHoldReleaseClientEvent(args)
        # self.bigItemSystem.TapOrHoldReleaseClientEvent(args)




    # #客户端加载完成
    # def OnLocalPlayerStopLoading(self,args):
    #     self.BigItemPivot(args)

    # #物品切换
    # def OnItemChanged(self,args):
    #     self.BigItemPivot(args)

    # #巨型物品调用枢纽
    # def BigItemPivot(self,args):
    #     if "event" in args:
    #         if args["event"]=="weapon_init":
    #             self.bigItemSystem.weapon_init(args)
    #         elif args["event"]=="weapon_discard":
    #             self.bigItemSystem.weapon_discard(args)
    #         elif args["event"]=="client_loaded":
    #             self.bigItemSystem.client_loaded(args)

    #     elif "playerId" in args:
    #         self.bigItemSystem.client_loaded(args)
    #     elif "itemDict" in args:
    #         self.bigItemSystem.carried_change(args)


    #次生事件_____________________________________________________________________________________________________________________________


    #通用组件_____________________________________________________________________________________________________________________________

