from aqt import mw

if mw is None:
    raise ReferenceError('couldn`t import mw')

config = mw.addonManager.getConfig(__name__)