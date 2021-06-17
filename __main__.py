import ui
from objc_util import create_objc_class, load_framework, ObjCClass, ObjCInstance, CGRect, on_main_thread
import pdbg

load_framework('SceneKit')
load_framework('ARKit')

SCNScene = ObjCClass('SCNScene')
ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')
ARSCNFaceGeometry = ObjCClass('ARSCNFaceGeometry')


def renderer_nodeForAnchor_(_self, _cmd, renderer, nodeFor_anchor):
  device = view.sceneView.device()
  faceGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(device)
  node = SCNNode.nodeWithGeometry_(faceGeometry)
  node.geometry().firstMaterial().fillMode = 1
  return node


def renderer_didUpdateNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  print('hoge')
  _node = ObjCInstance(node)
  faceAnchor = ObjCInstance(anchor)
  faceGeometry = _node.geometry()
  #faceGeometry.updateFromFaceGeometry_(faceAnchor.geometry())


myARSCNViewDelegate = create_objc_class(
  'myARSCNViewDelegate',
  methods=[  #renderer_nodeForAnchor_,
    renderer_didUpdateNode_forAnchor_
  ],
  protocols=['ARSCNViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.instance = ObjCInstance(self)
    self.load_view()
    self.view_will_appear()
    self.instance.addSubview_(self.sceneView)

  #@on_main_thread
  def load_view(self):
    ARFaceTrackingConfiguration.isSupported()
    frame = CGRect((0, 0), (100, 100))
    flex_w, flex_h = (1 << 1), (1 << 4)
    self.sceneView = ARSCNView.alloc()
    self.sceneView.initWithFrame_options_(frame, None)
    self.sceneView.autoresizingMask = (flex_w | flex_h)
    self.sceneView.showsStatistics = True
    self.sceneView.debugOptions = (1 << 1) | (1 << 31)
    deledate = myARSCNViewDelegate.alloc().init()
    #self.sceneView.setDelegate_(deledate)

  def view_will_appear(self):
    configuration = ARFaceTrackingConfiguration.new()
    configuration.maximumNumberOfTrackedFaces = ARFaceTrackingConfiguration.supportedNumberOfTrackedFaces(
    )
    configuration.isLightEstimationEnabled = True
    self.sceneView.session().runWithConfiguration_options_(
      configuration, (1 << 0) | (1 << 1))

  def will_close(self):
    self.sceneView.session().pause()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

