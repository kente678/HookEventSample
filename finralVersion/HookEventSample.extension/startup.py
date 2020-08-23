#-*- coding: utf-8 -*-
#pylint: disable=C0103,E0401,W0703
from pyrevit import HOST_APP, DB, framework
from System import Guid
from Autodesk.Revit.UI import TaskDialog
import sys
import os

#アップデータークラス
class sampleUpdater(DB.IUpdater):
    #コンストラクタ
    def __init__(self, addin_id): 
        #updaterのID
        self.id = DB.UpdaterId(addin_id, Guid("A7931BDA-F0DC-41B5-83C9-C6FE03CC5025"))
        #追加エレメント
        self.addedId = []
        #トランザクション名称取得
        self.transactionName = None
        #追加対象用カラーセット
        self.addedColor = SetElementColor(255, 0, 0, 20)
        #変更対象用カラーセット
        self.changedColor = SetElementColor(0, 0, 255, 20)


    def GetUpdaterId(self):
        return self.id

    def GetUpdaterName(self):
        return "Sample Updater"

    def GetAdditionalInformation(self):
        return "Just an sample"
 
    def GetChangePriority(self):
        return DB.ChangePriority.Views

    #変更時トランザクション通知
    def docchanged_eventhandler(self, sender, args):
        #トランザクション名称取得
        self.transactionName = args.GetTransactionNames()[0]


    #フック処理
    def Execute(self, data):
        
        doc = data.GetDocument()
        #追加されたエレメントのId
        addedIds = data.GetAddedElementIds()
        #変更されたエレメントのId
        changedIds = data.GetModifiedElementIds()

        #追加エレメント用処理
        for id in addedIds:
            #エレメント取得
            elemAdded = doc.GetElement(id)
            #コメントパラメータ
            commentParamAdded = elemAdded.Parameter[DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS]
            try:
                if commentParamAdded:
                    #コメント記入
                    commentParamAdded.Set('追加')
                    #addedIdにId追加
                    self.addedId.append(id)
                    #対象エレメントの色変更
                    doc.ActiveView.SetElementOverrides(id, self.addedColor)
            except Exception as err:
                if commentParamAdded:
                    commentParamAdded.Set("{}: {}".format(err.__class__.__name__, err))

        #変更エレメント用処理
        for id in changedIds:
            #追加エレメントの時は、break
            if id in self.addedId:
                break
            elemChanged = doc.GetElement(id)
            commentParamChanged = elemChanged.Parameter[DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS]
            try:
                if commentParamChanged:
                    #コメント記入
                    commentParamChanged.Set('変更')
                    #対象エレメントの色変更
                    doc.ActiveView.SetElementOverrides(id, self.changedColor)
            except Exception as err:
                if commentParamChanged:
                    commentParamChanged.Set("{}: {}".format(err.__class__.__name__, err))
            
        
#カラーのオーバーライドセッティング
def SetElementColor(R, G, B, A):

    color = DB.Color(R,G,B)
    ogs = DB.OverrideGraphicSettings()
    ogs.SetProjectionLineColor(color)
    ogs.SetSurfaceBackgroundPatternColor(color)
    ogs.SetCutForegroundPatternColor(color)
    ogs.SetCutBackgroundPatternColor(color)
    ogs.SetCutLineColor(color)
    ogs.SetSurfaceForegroundPatternColor(color)
    ogs.SetSurfaceTransparency(A)
    return ogs





           


#新規にレビット立ち上げ時に、updater生成
updater = sampleUpdater(HOST_APP.addin_id)

#既に登録されているUpdaterがあったら、UpdaterRegistryをアンレジスター
if DB.UpdaterRegistry.IsUpdaterRegistered(updater.GetUpdaterId()):
    DB.UpdaterRegistry.UnregisterUpdater(updater.GetUpdaterId())
    
#UpdaterRegistryを登録
DB.UpdaterRegistry.RegisterUpdater(updater)

#フック対象エレメントにパーツを指定
elements_filter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_PointClouds, True)
#全ての変更タイプを取得
change_type = DB.Element.GetChangeTypeAny()
#追加変更タイプを取得
additional_type = DB.Element.GetChangeTypeElementAddition()
#変更トリガー登録
DB.UpdaterRegistry.AddTrigger(updater.GetUpdaterId(), elements_filter, change_type)
#追加トリガー登録
DB.UpdaterRegistry.AddTrigger(updater.GetUpdaterId(), elements_filter, additional_type)

#DocumentChangedハンドラー取得
HOST_APP.app.DocumentChanged += \
        framework.EventHandler[DB.Events.DocumentChangedEventArgs](
        updater.docchanged_eventhandler
        )