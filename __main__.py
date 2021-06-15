import ui
from objc_util import load_framework, ObjCClass, ObjCInstance, on_main_thread, CGRect, NSObject, create_objc_class
import pdbg

load_framework('ARKit')
load_framework('SceneKit')

ARSCNView = ObjCClass('ARSCNView')

ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')

SCNScene = ObjCClass('SCNScene')




def renderer_nodeForAnchor_anchor_(_self, _cmd, renderer, node, anchor):
  print(renderer)



class View(ui.View):
  def __init__(self):#, *args, **kwargs):
    methods = [
      renderer_nodeForAnchor_anchor_
    ]
    protocols = ['ARSCNViewDelegate']
    pyARSCNViewDelegate = create_objc_class(
      'pyARSCNViewDelegate', NSObject, methods=methods, protocols=protocols)
    
    #ui.View.__init__(self, *args, **kwargs)
    self.instance = ObjCInstance(self)
    self.view_did_load()
    self.view_will_appear(pyARSCNViewDelegate)
    self.instance.addSubview_(self.scn)

  @on_main_thread
  def view_did_load(self):
    self.scn = ARSCNView.alloc()
    # 初期画面サイズ指定
    self.scn.initWithFrame_options_(CGRect((0, 0), (100, 100)), None)
    self.scn.autorelease()
    # 全画面
    self.scn.autoresizingMask = (18)
    # 統計データ出す
    self.scn.showsStatistics = True
    self.scn.autoenablesDefaultLighting = True
    # オブジェクトの線やら何やらのデバッグ
    self.scn.debugOptions = (1 << 1) | (1 << 30) | (1 << 32)
    self.scene = SCNScene.scene()
    self.scn.scene = self.scene
    #pdbg.all(self.scn.device())
    

  def view_will_appear(self, delegate):
    #print(delegate)
    configuration = ARFaceTrackingConfiguration.new()
    #pdbg.state(ARFaceTrackingConfiguration.supportsWorldTracking())
    self.scn.session().runWithConfiguration_(configuration)
    self.scn.delegate = delegate.alloc().init()

  def view_will_disappear(self):
    self.scn.session().pause()

  def will_close(self):
    self.view_will_disappear()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

