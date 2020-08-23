#-*- coding: utf-8 -*-
from pyrevit import DB, HOST_APP
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import ParameterFilterRuleFactory, ElementParameterFilter

from rpw import db

#輪郭線以外を透明度０に設定
def SetElementTransparency(A):
    ogs = DB.OverrideGraphicSettings()
    ogs.SetSurfaceTransparency(A)
    ogs.SetCutBackgroundPatternVisible(A == 0)
    ogs.SetCutForegroundPatternVisible(A == 0)
    ogs.SetSurfaceBackgroundPatternVisible(A == 0)
    ogs.SetSurfaceForegroundPatternVisible(A == 0)
    """
    #輪郭を白くする
    if A != 0:
        color = DB.Color(255,255,255)
        ogs.SetCutLineColor(color)
        ogs.SetProjectionLineColor(color)
    """

    return ogs

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

"""
#非表示用カラー（Hideはグループ等に適応できなかったため。。）
if doc.ActiveView.GetElementOverrides(collectorIds[0]).Transparency == 0:
    hideColor = SetElementTransparency(100)
else:
    hideColor = SetElementTransparency(0)
"""

#変更がなかったエレメントの表示変更
t = DB.Transaction(doc, "Hide Unchanged")
t.Start()

#ElementOverrides適用
"""
for id in collectorIds:
    doc.ActiveView.SetElementOverrides(id, hideColor)
"""

#Hideする(透明化とどちらが良いか)

#非表示状態だったら、解除
if not doc.ActiveView.IsElementVisibleInTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate,collectorIds[0]):
        doc.ActiveView.DisableTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate)
#非変更エレメントを一時非表示
else:
    for id in collectorIds:
        doc.ActiveView.HideElementTemporary(id)

t.Commit()

