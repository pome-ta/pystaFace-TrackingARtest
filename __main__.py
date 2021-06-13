import ui
from objc_util import load_framework, ObjCClass, ObjCInstance
import pdbg

load_framework('ARKit')
load_framework('SceneKit')

ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')

pdbg.state(ARSCNView)



class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)


if __name__ == '__main__':
  view = View()
  #view.present(style='fullscreen', orientations=['portrait'])
