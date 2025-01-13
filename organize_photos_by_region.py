import json
from pathlib import Path
q = Queue()
map={}
MESSAGE_CATEGORY="testing"

def stopped(task):
    QgsMessageLog.logMessage(
        'Task "{name}" was canceled'.format(
            name=task.description()),
        MESSAGE_CATEGORY, Qgis.Info)
def logit(msg):
    QgsMessageLog.logMessage(msg, MESSAGE_CATEGORY, Qgis.Info)
def process(task,regions):
  try:
    instance = QgsProject.instance()
    photos = instance.mapLayersByName("photos")[0]

    # perform the clipping
    for i,r in enumerate(regions):
      if task.isCanceled():
        stopped(task)
        return None
      task.setProgress(i/len(regions)*100)
      region = r["region"]
      # extract the region
      logit("extract by attr")
      all_region_layer = instance.mapLayersByName("regions")[0]
      region_layer = processing.run("native:extractbyattribute", {'INPUT':all_region_layer,'FIELD':'region','OPERATOR':0,'VALUE':region,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      # then use it on the photos layer 
      logit("clipping")
      photos_by_region = processing.run("native:clip", {'INPUT':photos,'OVERLAY':region_layer,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      # now we need to store the list of the features somehow
      logit("exporting")
      region_images =[p["photo"] for p in photos_by_region.getFeatures()]
      #()
      logit(f"Number of region_images {len(region_images)}")
      out = Path(f"handoff_images/{region}")
      out.mkdir(exist_ok=True)
      # for each image symlink into folder 
      for i,im in enumerate(region_images):
          sym_im = Path(f"{out}/{i:04d}.JPG")
          if not sym_im.exists():
              sym_im.symlink_to(im)
      #open(f"/tmp/{res['region']}","w").write(json.dump({"name":region,"images":region_images}))
  except Exception as e:
    logit(e)


def completed(exception,result=None):
    print(result)
        


instance = QgsProject.instance()
regions = instance.mapLayersByName("regions")[0]
manager =QgsApplication.taskManager()

task_number = 16
features = list(regions.getFeatures())
total_regions = len(features)
print("total",total_regions)
regions_per_task =total_regions//task_number +1
print("regions per",regions_per_task)
groups =[]
for i in range(0,total_regions,regions_per_task):
   group_features = features[i:i+regions_per_task]
   print(len(group_features))
   groups.append(group_features) 


for i,g in enumerate(groups):
  task = QgsTask.fromFunction(f"heavy work {i}",process,on_finished=completed,regions=g)
  manager.addTask(task)
  
