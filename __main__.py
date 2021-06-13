import ui
from objc_util import load_framework, ObjCClass, ObjCInstance
import pdbg

load_framework('ARKit')
load_framework('SceneKit')

ARSession = ObjCClass('ARSession')
ARSCNView = ObjCClass('ARSCNView')
ARFaceAnchor = ObjCClass('ARFaceAnchor')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')


configuration = ARFaceTrackingConfiguration.alloc()
pdbg.state(configuration.maximumNumberOfTrackedFaces)
#maximumNumberOfTrackedFaces
class ViewController:
  def __init__(self):
    pass

class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.instance = ObjCInstance(self)


if __name__ == '__main__':
  view = View()
  #view.present(style='fullscreen', orientations=['portrait'])
