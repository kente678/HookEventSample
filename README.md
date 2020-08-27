# HookEventSample
pyRevitでイベントをHookして、
任意の処理に繋げて楽しむExtensionを作りましょう。
## 0.参考
* 簡易pyrevitHookExtension：pyrevitに組み込まれていて、とても簡単にHookができます。  
    * https://www.notion.so/Anatomy-of-Hook-Scripts-47c2d5b796774afca51ff53a4c1e9f1c  
    * https://github.com/eirannejad/pyRevit/tree/master/extensions/pyRevitDevHooks.extension/hooks
    
* IUpdater：IUpdaterクラスを用いて、イベントのHookからトランザクション処理へ繋ぐことができます。
    * https://stackoverflow.com/questions/62665168/nameerror-raised-by-iupdater-registered-through-pyrevit
   



## 1.環境構築
石津さんのブログに倣って、pyRevit環境を作りましょう。
* https://qiita.com/yishizu/items/6e812db233b7fa970555  
### pyRevit  
* [pyRevit Installer](https://github.com/eirannejad/pyRevit/releases)

### Visual Studio Code  
* [Visual Studio Code Installer](https://code.visualstudio.com/download)

### Revit Python Shell
* [Revit Python Shell Installer](https://github.com/architecture-building-systems/revitpythonshell)

### RevitLookup
* [RevitLookup Installer](https://github.com/jeremytammik/RevitLookup)

### Revit Python Wrapper
* [Revit Python Wrapper Installer](https://revitpythonwrapper.readthedocs.io/en/latest/)


## 2.　pyrevitHookExtensionを用いた簡易フック
* pyrevitに組み込まれていて、とても簡単にHookができます。
* Revitの、「Basic Sample Project」を開きましょう。
* 参考 
    * https://www.notion.so/Anatomy-of-Hook-Scripts-47c2d5b796774afca51ff53a4c1e9f1c  
    * https://github.com/eirannejad/pyRevit/tree/master/extensions/pyRevitDevHooks.extension/hooks
    
### 2.1 Extensionフォルダ作成
* 今回は"HookEventSample.extension"という名称で作成してみましょう。    
   Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension`  

### 2.2 hooksフォルダを追加
* HookEventSample.extensionに、hooksフォルダを追加します。  
   Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\hooks`  
### 2.3 command.pyスクリプトを追加  
* hooksフォルダに、[command].pyを追加します。  
   Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\hooks\[command].py`  

* commandには、準備されているコマンドの名称を記述することで、対象のコマンドをHookできます。
   * [Hook Script Types](https://www.notion.so/Extension-Hooks-b771ecf65f6a45fe87ae12beab2a73a6)

* 試しに、doc-changed.pyを作成して、変更コマンドをHookしてみましょう。
   * [DocumentChangedEventArgs](https://www.revitapidocs.com/2015/470504f7-c7cb-b259-6fd4-feb376e58d17.htm)
   * doc-changed.pyを作成します。  
   Ex. `C:\Users\[UserName]\HookEventExtentionSample\HookEventExtentionSample.extension\hooks\doc-changed.py`  
   * とりあえず、ご挨拶をしましょう。(#-*- coding: utf-8 -*-を忘れずに）
```
#-*- coding: utf-8 -*-

print('hello')
```

* 各トランザクション名称を表示してみましょう。
```
#-*- coding: utf-8 -*-
from pyrevit import forms
from pyrevit import EXEC_PARAMS
from pyrevit import DB

command = EXEC_PARAMS.event_args
doc = command.GetDocument()


#Transaction名称
transactions = EXEC_PARAMS.event_args.GetTransactionNames()

for n in transactions:
   forms.alert(n)
```

* 追加されたエレメントの名称を表示してみましょう。
```
#-*- coding: utf-8 -*-
from pyrevit import forms
from pyrevit import EXEC_PARAMS
from pyrevit import DB

command = EXEC_PARAMS.event_args
doc = command.GetDocument()


#追加されたエレメントのId
addedIds = EXEC_PARAMS.event_args.GetAddedElementIds()
changedIds = EXEC_PARAMS.event_args.GetModifiedElementIds()


#変更対象名称表示
if addedIds:
    #配列が返るので、０番目のIdからエレメントを取得
    targetElement = doc.GetElement(addedIds[0])
    forms.alert(targetElement.Name)
elif changedIds:
    for i in changedIds:
        targetElement = doc.GetElement(i)
        #色々なIdsが返るので、カテゴリーを持つもののみ取得
        if not targetElement.Category == None:
            forms.alert(targetElement.Name)

```
### 2.4 doc-changed.pyスクリプトにトランザクション処理を追加
* せっかくフックできたので、追加、変更したものにコメントを追加してみましょう。

```
#変更対象にコメント記入

#トランザクション開始
t = DB.Transaction(doc, "Add Comment")
t.Start()
if addedIds:
    #配列が返るので、０番目のIdからエレメントを取得
    targetElement = doc.GetElement(addedIds[0])
    forms.alert(targetElement.Name)
elif changedIds:
    for i in changedIds:
        targetElement = doc.GetElement(i)
        #色々なIdsが返るので、カテゴリーを持つもののみ取得
        if not targetElement.Category == None:
            forms.alert(targetElement.Name)

t.Commit()
```
* 残念ながら、pyrevitHookExtensionでは、トランザクション処理は実行できません。
    * [EventHandlerは読み取り専用](https://thebuildingcoder.typepad.com/blog/2010/04/element-level-events.html)
* pyrevitHookExtensionはとても作り方が簡単なのですが、使い道がとても限られるようです。（良い使い道があったら、教えてください！）

## 3. IUpdaterクラスを用いたフック
* C#と同様に、IUpdaterクラスを用いれば、Pyrevitでもイベントをフックしつつ、トランザクション処理へ繋げることができます。

* 今回は、IUpdaterを用いて、追加、変更されたエレメントをハイライトするツールを作成します。
   * 追加、変更されたエレメントへ、コメントを追加します。
   * 追加、変更されたエレメントの色を変更します。
* 参考 
    * [Building Coderの記事](https://thebuildingcoder.typepad.com/blog/2012/06/documentchanged-versus-dynamic-model-updater.html)
    * [Pyrevitでの実装記事](https://stackoverflow.com/questions/62665168/nameerror-raised-by-iupdater-registered-through-pyrevit)
    * [Revit API Docs](https://www.revitapidocs.com/2020/ab8bc959-11c3-14c4-75ff-e1468973200e.htm)
    * [pyRevitのNotion](https://www.notion.so/Extension-Startup-Script-605ce7b1831d41d88741bc9a9eee42a7)
   

### 3.1 startup.pyスクリプトを追加
* IUpdaterクラスを作成しましょう。
   * 2.1で作成したHookEventSample.extensionフォルダに、startup.pyファイルを作成しましょう。  
      Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\startup.py`  
   * IUpdaterクラスを作成します。
   
```
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

    def GetUpdaterId(self):
        return self.id

    def GetUpdaterName(self):
        return "Sample Updater"

    def GetAdditionalInformation(self):
        return "Just an sample"
 
    def GetChangePriority(self):
        return DB.ChangePriority.Views

    #フック処理
    def Execute(self, data):
        
```          

### 3.2 追加、変更コメント記入処理を追加
* IUpdaterクラスに、変数と関数を追加します。
* 今回の作業用に、3Dビューを複製しましょう。
* コンストラクタに変数を追加
```
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

```

* トランザクション名称を取得する関数を追加します。
```
    #変更時トランザクション通知
    def docchanged_eventhandler(self, sender, args):
        #トランザクション名称取得
        self.transactionName = args.GetTransactionNames()[0]  
```

* startup.py内で、IUpdaterクラスを生成します。
```
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
```

* DocumentChangedハンドラーをセットします。（確認用）
```
#DocumentChangedハンドラー取得
HOST_APP.app.DocumentChanged += \
        framework.EventHandler[DB.Events.DocumentChangedEventArgs](
        updater.docchanged_eventhandler
        )
```

* お試しで、トランザクション名称を、printで確認してみましょう。  
  Execute関数に、フック処理の内容を記述します。
```
    #フック処理
    def Execute(self, data):
        print(self.transactionName)
```

* 追加、変更されたエレメントに、コメントを記入する処理を追加します。  
  引き続き、Execute関数内に記述します。（先ほどのprintは削除しましょう）
```
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
            except Exception as err:
                if commentParamChanged:
                    commentParamChanged.Set("{}: {}".format(err.__class__.__name__, err))
```

### 3.3 追加、変更エレメントの色変更
* カラーのオーバーライドセッティングをセットする関数を追加します。  
  （sampleUpdater内ではなく、とりあえずstartup.py上に追加しちゃいます。）
   * [OverrideGraphicSettings参考ページ](https://forums.autodesk.com/t5/revit-api-forum/using-api-to-change-color-and-or-material-of-directshape/td-p/7064149?profile.language=ja)
   * [Revit API Docs](https://www.revitapidocs.com/2020/bd467fbb-a9da-7cf1-1ef5-f0f3568db0ac.htm)
```
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
```

* SampleUpdaterのコンストラクタに、カラー設定用変数を追加します。
```
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
```

* Execute関数に、追加、変更があったエレメントのカラー変更をする処理を追加します。
```
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
```

## 4. 非変更エレメントの表示非表示コマンド
* 追加、変更に関与しなかったエレメントを表示非表示する機能を追加します。  
  (差分確認用）
### 4.1 HookSample.tabフォルダ作成
* HookEventSample.extensionに、HookSample.tabフォルダを追加します。  
  Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\HookSample.tab`  
  
### 4.2 Hook.panelフォルダ作成
* HookSample.tabnに、Hook.panelフォルダを追加します。  
  Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\HookSample.tab\Hook.panel` 
  
### 4.4 HideUnchanged.pushbuttonフォルダ作成
* Hook.panelフォルダに、HideUnchanged.pushbuttonフォルダを追加します。  
  Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\HookSample.tab\Hook.panel\HideUnchanged.pushbutton`
  
### 4.5 script.pyファイル作成
* HideUnchanged.pushbuttonフォルダに、script.pyファイルを追加します。  
  Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\HookSample.tab\Hook.panel\HideUnchanged.pushbutton\script.py`

### 4.6 icon.pngファイル追加
* HideUnchanged.pushbuttonフォルダに、icon.pngファイルを追加します。  
  Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\HookSample.tab\Hook.panel\HideUnchanged.pushbutton\icon.png`

### 4.7 非変更エレメントをFiltering
* 追加、変更コメントのついていない全てのエレメントをフィルタリングします。  
   * 下記サイトに「フィルタの反転を指定するブール値引数を持ったオーバーロード コンストラクタを使用して反転させることができます」 
     とあったので、それを利用します。  
  [フィルタリングの日本語解説](https://knowledge.autodesk.com/ja/support/revit-products/learn-explore/caas/CloudHelp/cloudhelp/2014/JPN/Revit/files/GUID-A2686090-69D5-48D3-8DF9-0AC4CC4067A5-htm.html)  
  [Revit API Docs](https://www.revitapidocs.com/2015/909615cd-8abd-044a-cff2-f21fd95b8ee7.htm)  
  
* 4.5で作成したscript.pyに、フィルタリング処理を記述します。
```
#-*- coding: utf-8 -*-
from pyrevit import DB, HOST_APP
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import ParameterFilterRuleFactory, ElementParameterFilter

from rpw import db


doc = HOST_APP.doc

#Fileter生成(コメントに変更と追加のあるエレメント)
#あまり使わなそうな「OST_PointClouds以外」、というルールでフィルタリングします。
#(「ほぼすべて」を対象とするいい用法があったら、教えてください！）
categoryFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_PointClouds, True)
BiParameter = db.builtins._BiParameter()
#コメントに「変更」と記入されているもの以外をフィルタリングします。
ruleChange = ParameterFilterRuleFactory.CreateEqualsRule(BiParameter.get_id('ALL_MODEL_INSTANCE_COMMENTS'), '変更', True)
parameterFilterChange = DB.ElementParameterFilter(ruleChange, True)
#コメントに「追加」と記入されているもの以外をフィルタリングします。
ruleAdd = ParameterFilterRuleFactory.CreateEqualsRule(BiParameter.get_id('ALL_MODEL_INSTANCE_COMMENTS'), '追加', True)
parameterFilterAdd = DB.ElementParameterFilter(ruleAdd, True)

#上記のルールで、対象を収集します。
collectorIds = DB.FilteredElementCollector(doc)\
.WherePasses(categoryFilter)\
.WherePasses(parameterFilterChange)\
.WherePasses(parameterFilterAdd)\
.ToElementIds()
```

### 4.7 対象エレメントの表示非表示
* トランザクションを開始して、対象のエレメントを表示非表示する処理を追加します。
   * [HideElementTemporary Method](https://www.revitapidocs.com/2015/df9e6656-eca7-b95c-0e50-05974d5a70fb.htm)
   * [DisableTemporaryViewMode Method](https://www.revitapidocs.com/2015/e87fc993-5dc8-bb39-b7a7-fe91d075489a.htm)
```
#変更がなかったエレメント表示変更
t = DB.Transaction(doc, "Hide Unchanged")
t.Start()

#非表示状態だったら、解除
if not doc.ActiveView.IsElementVisibleInTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate,collectorIds[0]):
        doc.ActiveView.DisableTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate)
#非変更エレメントを一時非表示（Hideはグループ等に適応できなかったため。。）
else:
    for id in collectorIds:
        doc.ActiveView.HideElementTemporary(id)

t.Commit()
```
  
### 4.8 対象エレメントの輪郭線表示
* 非変更対象を非表示ではなく、輪郭線表示にします。
* script.pyに、SetElementTransparency関数を追加します。輪郭線以外を透明度０に設定します。
```
#輪郭線以外を透明度０に設定
def SetElementTransparency(A):
    ogs = DB.OverrideGraphicSettings()
    ogs.SetSurfaceTransparency(A)
    ogs.SetCutBackgroundPatternVisible(A == 0)
    ogs.SetCutForegroundPatternVisible(A == 0)
    ogs.SetSurfaceBackgroundPatternVisible(A == 0)
    ogs.SetSurfaceForegroundPatternVisible(A == 0)
    
    return ogs
```

* カラーセットを作る処理を追加します。
```
doc = HOST_APP.doc

#Fileter生成(コメントに変更と追加のあるエレメント)
categoryFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_PointClouds, True)
BiParameter = db.builtins._BiParameter()
ruleChange = ParameterFilterRuleFactory.CreateEqualsRule(BiParameter.get_id('ALL_MODEL_INSTANCE_COMMENTS'), '変更', True)
parameterFilterChange = DB.ElementParameterFilter(ruleChange, True)
ruleAdd = ParameterFilterRuleFactory.CreateEqualsRule(BiParameter.get_id('ALL_MODEL_INSTANCE_COMMENTS'), '追加', True)
parameterFilterAdd = DB.ElementParameterFilter(ruleAdd, True)

collectorIds = DB.FilteredElementCollector(doc)\
.WherePasses(categoryFilter)\
.WherePasses(parameterFilterChange)\
.WherePasses(parameterFilterAdd)\
.ToElementIds()


#非表示用カラー
if doc.ActiveView.GetElementOverrides(collectorIds[0]).Transparency == 0:
    hideColor = SetElementTransparency(100)
else:
    hideColor = SetElementTransparency(0)

```
* トランザクション内の処理を、輪郭線表示用に修正します。
```
#変更がなかったエレメントの表示変更
t = DB.Transaction(doc, "Hide Unchanged")
t.Start()

#ElementOverrides適用

for id in collectorIds:
    doc.ActiveView.SetElementOverrides(id, hideColor)

"""
#非表示状態だったら、解除
if not doc.ActiveView.IsElementVisibleInTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate,collectorIds[0]):
        doc.ActiveView.DisableTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate)
#非変更エレメントを一時非表示（Hideはグループ等に適応できなかったため。。）
else:
    for id in collectorIds:
        doc.ActiveView.HideElementTemporary(id)
"""

t.Commit()
```
