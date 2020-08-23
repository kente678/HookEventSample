#-*- coding: utf-8 -*-
from pyrevit import forms
from pyrevit import EXEC_PARAMS
from pyrevit import DB

command = EXEC_PARAMS.event_args
doc = command.GetDocument()


#追加されたエレメントのId
addedIds = EXEC_PARAMS.event_args.GetAddedElementIds()
changedIds = EXEC_PARAMS.event_args.GetModifiedElementIds()

"""
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
"""

"""
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
"""

