import ui
from objc_util import load_framework, ObjCClass, ObjCInstance, on_main_thread, CGRect
import pdbg

load_framework('ARKit')
load_framework('SceneKit')

#ARSession = ObjCClass('ARSession')
ARSCNView = ObjCClass('ARSCNView')
#ARFaceAnchor = ObjCClass('ARFaceAnchor')
ARFaceTrackingConfiguration = ObjCClass('ARFaceTrackingConfiguration')

SCNScene = ObjCClass('SCNScene')


configuration = ARFaceTrackingConfiguration.new()
#pdbg.state(configuration.maximumNumberOfTrackedFaces)




class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.instance = ObjCInstance(self)
    self.view_did_load()
    self.view_will_appear()
    self.instance.addSubview_(self.scn)
  
  @on_main_thread
  def view_did_load(self):
    self.scn = ARSCNView.alloc()
    # 初期画面サイズ指定
    self.scn.initWithFrame_options_(CGRect((0, 0), (100, 100)), None)
    # 全画面
    self.scn.autoresizingMask = (18)
    # 統計データ出す
    self.scn.showsStatistics = True
    self.scn.autoenablesDefaultLighting = True
    # オブジェクトの線やら何やら
    self.scn.debugOptions = (1 << 1) | (1 << 30)
    scene = SCNScene.scene()
    self.scn.scene = scene
    
    
  def view_will_appear(self):
    self.scn.session().runWithConfiguration_(configuration)
    
  def view_will_disappear(self):
    self.scn.session().pause()
    
  def will_close(self):
    self.view_will_disappear()
    
    
    


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
