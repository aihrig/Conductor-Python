import os
import sys

sys.path.append('/')
from MicroWebSrv2 import *
from conductor.train import Train


'''
Route functions
'''

@WebRoute(POST, '/headlights/on')
def HeadlightsOn(MicroWebSrv2, request):
    # TODO: move to train class, MCU
    hst01 = Train("hst01")
    hst01.headlights.on()
    request.Response.ReturnOkJSON({'status':'ok'})

@WebRoute(POST, '/headlights/off')
def HeadlightsOn(MicroWebSrv2, request):
    # TODO: move to train class, MCU
    hst01 = Train("hst01")
    hst01.headlights.off()
    request.Response.ReturnOkJSON({'status':'ok'})

@WebRoute(POST, '/headlights/alternate')
def HeadlightsOn(MicroWebSrv2, request):
    # TODO: move to train class, MCU
    hst01 = Train("hst01")
    hst01.headlights.alternate_start()
    request.Response.ReturnOkJSON({'status':'ok'})
