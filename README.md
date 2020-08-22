# HookEventExtensionSample
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
* 参考 
    * https://www.notion.so/Anatomy-of-Hook-Scripts-47c2d5b796774afca51ff53a4c1e9f1c  
    * https://github.com/eirannejad/pyRevit/tree/master/extensions/pyRevitDevHooks.extension/hooks
    
### 2.1 Extensionフォルダ作成
* 今回は"HookEventSample"という名称で作成してみましょう。    
   Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension`  

### 2.2 hooksフォルダを追加
* HookEventSampleに、hooksフォルダを追加  
   Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\hooks`  
### 2.3 command.pyスクリプトを追加  
* hooksフォルダに、[command].pyを追加  
   Ex. `C:\Users\[UserName]\HookEventSample\HookEventSample.extension\hooks\[command].py`  

* commandには、準備されているコマンドの名称を記述することで、対象のコマンドをHookできます。
   * [Hook Script Types](https://www.notion.so/Extension-Hooks-b771ecf65f6a45fe87ae12beab2a73a6)

* 試しに、doc-changed.pyを作成して、変更コマンドをHookしてみましょう。
   * [DocumentChangedEventArgs](https://www.revitapidocs.com/2015/470504f7-c7cb-b259-6fd4-feb376e58d17.htm)
   * doc-changed.pyを作成します。  
   Ex. `C:\Users\[UserName]\HookEventExtentionSample\HookEventExtentionSample.extension\hooks\doc-changed.py`  
   * 追加されたエレメントの名称をダイアログで表示する処理を記述します。  
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
   * 2.1で作成したフォルダに、startup.pyファイルを作成しましょう。  
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

```

* トランザクション名称を取得する関数を追加します。
```
    #変更時トランザクション通知
    def docchanged_eventhandler(self, sender, args):
        #トランザクション名称取得
        self.transactionName = args.GetTransactionNames()[0]  
```


