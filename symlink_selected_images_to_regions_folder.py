from pathlib import Path
import subprocess as sp

def stopped(task):
    QgsMessageLog.logMessage(
        'Task "{name}" was canceled'.format(
            name=task.description()),
        MESSAGE_CATEGORY, Qgis.Info)

group = QgsProject.instance().layerTreeRoot().findGroup("clusters")
def symlink_contents(task,photos,name,delete=False):
  out =Path(f"./region_labeled_image_cluster_groups/{name}/images")
  # remove the folder if this already exists
  print(f"will remove {out.parent}")
  if delete:
    sp.run(f"rm -rf {out.parent}",shell=True)
  else:
    # check if files exists
    if out.exists():
        return 
  out.mkdir(exist_ok=True,parents=True)

  total = len(list(photos.getFeatures()))
  for i,f in enumerate(photos.getFeatures()):
      # get the photo name rom the f
      if task.isCanceled():
          stopped(task)
          return None
      fpath = Path(f["photo"])
      sympath = Path(f"{out}/{fpath.name}")
      task.setProgress(i/total*100)
      if not sympath.is_symlink():
          sympath.symlink_to(fpath.absolute())

manager = QgsApplication.taskManager()
for i,child in enumerate(group.children()):
  photos = child.layer()
  name = photos.name().replace("cluster_","")
  task = QgsTask.fromFunction(f"function {i}",symlink_contents,photos=photos,name=name,delete=True) 
  manager.addTask(task)
