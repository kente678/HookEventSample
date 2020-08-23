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
* 今回は"HookEventExtentionSample"という名称で作成してみましょう。    
   Ex. `C:\Users\[UserName]\HookEventExtentionSample\HookEventExtentionSample.extension`  

### 2.2 hooksフォルダを追加
* HookEventExtentionSampleに、hooksフォルダを追加  
   Ex. `C:\Users\[UserName]\HookEventExtentionSample\HookEventExtentionSample.extension\hooks`  
### 2.3 command.pyスクリプトを追加  
* hooksフォルダに、[command].pyを追加  
   Ex. `C:\Users\[UserName]\HookEventExtentionSample\HookEventExtentionSample.extension\hooks\[command].py`  

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
* C#と同様に、IUpdaterクラスを用いれば、イベントをフックしつつ、トランザクション処理へ繋げることができます。
* 参考 
    * https://stackoverflow.com/questions/62665168/nameerror-raised-by-iupdater-registered-through-pyrevit

### 3.1 startup.py作成

### 3.2 任意のViewを複製