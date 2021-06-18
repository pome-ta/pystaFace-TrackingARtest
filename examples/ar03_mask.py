from objc_util import create_objc_class, load_framework, ObjCClass, ObjCInstance, CGRect
import ui


load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')
ARSCNFaceGeometry = ObjCClass('ARSCNFaceGeometry')

UIColor = ObjCClass('UIColor')


def renderer_didAddNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  _renderer = ObjCInstance(renderer)
  faceGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(_renderer.device())
  _node = ObjCInstance(node)
  _node.geometry = faceGeometry
  material = _node.geometry().firstMaterial()
  material.metalness().intensity = 0.2
  material.roughness().intensity = 0.5
  material.diffuse().contents = UIColor.lightGrayColor()
  material.lightingModelName = 'SCNLightingModelPhysicallyBased'
  _node.Opacity = 0.8


def renderer_didUpdateNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  _node = ObjCInstance(node)
  faceGeometry = _node.geometry()
  faceAnchor = ObjCInstance(anchor)
  faceGeometry.updateFromFaceGeometry_(faceAnchor.geometry())


myARSCNViewDelegate = create_objc_class(
  'myARSCNViewDelegate',
  methods=[renderer_didAddNode_forAnchor_, renderer_didUpdateNode_forAnchor_],
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
    frame = CGRect((0, 0), (100, 100))
    flex_w, flex_h = (1 << 1), (1 << 4)
    self.sceneView = ARSCNView.alloc()
    self.sceneView.initWithFrame_options_(frame, None)
    self.sceneView.autoresizingMask = (flex_w | flex_h)
    self.sceneView.showsStatistics = True
    #self.sceneView.debugOptions = (1 << 1) | (1 << 30)
    self.sceneView.setDelegate_(myARSCNViewDelegate.new())

  def view_will_appear(self):
    configuration = ARFaceTrackingConfiguration.new()
    configuration.isLightEstimationEnabled = True
    self.sceneView.session().runWithConfiguration_(configuration)

  def view_will_disappear(self):
    self.sceneView.session().pause()

  def will_close(self):
    self.view_will_disappear()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
