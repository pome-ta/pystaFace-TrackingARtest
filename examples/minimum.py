from objc_util import create_objc_class, load_framework, ObjCClass, ObjCInstance, CGRect
import ui


load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')
ARSCNFaceGeometry = ObjCClass('ARSCNFaceGeometry')


def renderer_didAddNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  _renderer = ObjCInstance(renderer)
  faceGeometry = ARSCNFaceGeometry.faceGeometryWithDevice_(_renderer.device())
  _node = ObjCInstance(node)
  _node.geometry = faceGeometry
  _node.geometry().firstMaterial().fillMode = 1


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
    self.sceneView.debugOptions = (1 << 1) | (1 << 31)
    self.sceneView.setDelegate_(myARSCNViewDelegate.new())

  def view_will_appear(self):
    configuration = ARFaceTrackingConfiguration.new()
    self.sceneView.session().runWithConfiguration_(configuration)

  def will_close(self):
    self.sceneView.session().pause()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

