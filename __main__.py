import ui
from objc_util import create_objc_class, load_framework, ObjCClass, ObjCInstance, CGRect, NSObject, nsurl
import pdbg

load_framework('SceneKit')
load_framework('ARKit')

SCNScene = ObjCClass('SCNScene')
ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')

ARSCNFaceGeometry = ObjCClass('ARSCNFaceGeometry')
ARFaceAnchor = ObjCClass('ARFaceAnchor')
SCNNode = ObjCClass('SCNNode')
SCNReferenceNode = ObjCClass('SCNReferenceNode')

obj_uri = nsurl('./assets/ARFaceGeometry.obj')
#face = SCNReferenceNode.referenceNodeWithURL_(obj_uri)
#pdbg.state(face.referenceURL())

def renderer_nodeForAnchor_(_self, _cmd, renderer, nodeFor_anchor):
  '''
  _renderer = ObjCInstance(renderer)
  device = _renderer.device()
  faceGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(device)
  node = SCNNode.nodeWithGeometry_(faceGeometry)
  node.geometry().firstMaterial().fillMode = 1
  return node
  '''
  contentNode = SCNReferenceNode.referenceNodeWithURL_(obj_uri)
  return contentNode
  

def renderer_didUpdateNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  #print('----------')
  #pdbg.state(ObjCInstance(node))
  #pdbg.state(ObjCInstance(node))
  _node = ObjCInstance(node)
  faceAnchor = ObjCInstance(anchor)# if anchor else ARFaceAnchor.new()
  
  
  faceGeometry = _node.geometry()
  pdbg.state(faceAnchor)
  faceGeometry.updateFromFaceGeometry_(faceAnchor.geometry())
  
  

myARSCNViewDelegate = create_objc_class(
  'myARSCNViewDelegate',
  methods=[renderer_nodeForAnchor_, 
  renderer_didUpdateNode_forAnchor_],
  protocols=['ARSCNViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.instance = ObjCInstance(self)
    self.load_view()
    self.view_will_appear()
    self.instance.addSubview_(self.sceneView)

  def load_view(self):
    obj_uri = nsurl('./assets/ARFaceGeometry.obj')
    #scene = SCNScene.sceneWithURL_options_(face_uri, None)
    frame = CGRect((0, 0), (100, 100))
    flex_w, flex_h = (1 << 1), (1 << 4)
    self.sceneView = ARSCNView.alloc()
    self.sceneView.initWithFrame_options_(frame, None)
    self.sceneView.autoresizingMask = (flex_w | flex_h)
    self.sceneView.showsStatistics = True
    self.sceneView.debugOptions = (1 << 1) | (1 << 31)
    #self.sceneView.scene = scene
    #pdbg.state(scene)
    deledate = myARSCNViewDelegate.new()
    self.sceneView.setDelegate_(deledate)

  def view_will_appear(self):
    configuration = ARFaceTrackingConfiguration.new()
    configuration.maximumNumberOfTrackedFaces = ARFaceTrackingConfiguration.supportedNumberOfTrackedFaces()
    configuration.isLightEstimationEnabled = True
    self.sceneView.session().runWithConfiguration_options_(configuration, (1 << 0) | (1 << 1))

  def will_close(self):
    self.sceneView.session().pause()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
  #pdbg.state(view.sceneView.session().currentFrame())
  #pdbg.state(view.sceneView.scene())


