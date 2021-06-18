from objc_util import create_objc_class, load_framework, ObjCClass, ObjCInstance, CGRect
import ui

import pdbg

load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')
ARSCNFaceGeometry = ObjCClass('ARSCNFaceGeometry')


SCNNode = ObjCClass('SCNNode')
SCNBox = ObjCClass('SCNBox')
SCNMaterial = ObjCClass('SCNMaterial')
SCNSphere = ObjCClass('SCNSphere')

UIColor = ObjCClass('UIColor')


def renderer_didAddNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  _renderer = ObjCInstance(renderer)
  faceGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(_renderer.device())
  _node = ObjCInstance(node)
  _node.addChildNode_(view.face_ar.virtualFaceNode)
  '''
  _node.geometry = faceGeometry
  material = _node.geometry().firstMaterial()
  material.metalness().intensity = 0.2
  material.roughness().intensity = 0.5
  material.diffuse().contents = UIColor.lightGrayColor()
  material.lightingModelName = 'SCNLightingModelPhysicallyBased'
  #_node.geometry().firstMaterial().fillMode = 1
  '''
  


def renderer_didUpdateNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  _node = ObjCInstance(node)
  faceGeometry = _node.geometry()
  faceAnchor = ObjCInstance(anchor)
  geometry = view.face_ar.virtualFaceNode.geometry()
  geometry.updateFromFaceGeometry_(faceAnchor.geometry())
  #faceGeometry.updateFromFaceGeometry_(faceAnchor.geometry())


myARSCNViewDelegate = create_objc_class(
  'myARSCNViewDelegate',
  methods=[renderer_didAddNode_forAnchor_, renderer_didUpdateNode_forAnchor_],
  protocols=['ARSCNViewDelegate'])


class FaceAR:
  def __init__(self):
    self.load_view()
    self.view_did_load()
    self.view_will_appear()

  def load_view(self):
    frame = CGRect((0, 0), (100, 100))
    flex_w, flex_h = (1 << 1), (1 << 4)
    self.sceneView = ARSCNView.alloc()
    self.sceneView.initWithFrame_options_(frame, None)
    self.sceneView.autoresizingMask = (flex_w | flex_h)
    self.sceneView.showsStatistics = True
    self.sceneView.debugOptions = (1 << 1) | (1 << 5)
    self.sceneView.setDelegate_(myARSCNViewDelegate.new())

    self.sceneView.scene().background().contents = UIColor.blackColor()
    
  def view_did_load(self):
    self.virtualFaceNode = SCNNode.new()
    device = self.sceneView.device()
    glassesGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(device)
    glassesGeometry.firstMaterial().setColorBufferWriteMask_(0)
    self.virtualFaceNode.setGeometry_(glassesGeometry)
    
    ball = SCNSphere.new()
    ball.geodesic = True
    ball.segmentCount = 8
    ball.radius = 0.03
    
    material = SCNMaterial.new()
    material.diffuse().contents = UIColor.redColor()
    material.lightingModelName = 'SCNLightingModelPhysicallyBased'
    
    ball_node = SCNNode.new()
    ball_node.setGeometry_(ball)
    
    ball_node.position = (0.0, 0.0, 0.06)
    ball_node.geometry().materials = [material]
    #pdbg.state(ball_node.geometry().materials())
    
    
    
    
    
    
    self.virtualFaceNode.addChildNode_(ball_node)
    

  def view_will_appear(self):
    configuration = ARFaceTrackingConfiguration.new()
    configuration.isLightEstimationEnabled = True
    self.sceneView.session().runWithConfiguration_options_(
      configuration, (1 << 0) | (1 << 1))

  def view_will_disappear(self):
    self.sceneView.session().pause()


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.face_ar = FaceAR()
    self.instance = ObjCInstance(self)
    self.instance.addSubview_(self.face_ar.sceneView)

  def will_close(self):
    self.face_ar.view_will_disappear()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
