import json
import itertools
import uuid
from pathlib import Path
import random
# consider editing to base less on selections and instead on layers that could be extracted to other layers
MESSAGE_CATEGORY="breakout from image"
def get_len_features(layer):
  return len(list(layer.getFeatures()))
def stopped(task):
    QgsMessageLog.logMessage(
        'Task "{name}" was canceled'.format(
            name=task.description()),
        MESSAGE_CATEGORY, Qgis.Info)
def logit(msg):
    QgsMessageLog.logMessage(msg, MESSAGE_CATEGORY, Qgis.Info)
def process(task,images_list,group_id):
    kmeans_clusters = []
    instance = QgsProject.instance()
    QgsMessageLog.logMessage('Started task {}'.format(task.description()), MESSAGE_CATEGORY, Qgis.Info)
    instance = QgsProject.instance()
    #group = QgsProject.instance().layerTreeRoot().findGroup("group2")
    QgsMessageLog.logMessage('beginning {}'.format(task.description()), MESSAGE_CATEGORY, Qgis.Info)

    map = {}
    fails = []
    max_images = 500
    # 24 meter bins for images
    bin_size=24
    lim = 5
    #children_len = len(group.children())
    # selected regions
    # Note this needs to exist means that you need to rename a layer probably if it doesn't work
    regions = QgsVectorLayer("correct_regions_5_30.geojson","regions","ogr")
    print(regions)
# stoppin ghere
    sel = list(regions.getFeatures())
    QgsMessageLog.logMessage("start loop", MESSAGE_CATEGORY, Qgis.Info)
    #print("running part of total")
    # ensure that we step up by the number of entries in a group, until we reach the total
    total = len(images_list)
    for i,image_layer in enumerate(images_list) :
        if image_layer ==None:
            continue
        QgsMessageLog.logMessage(f'running {i}', MESSAGE_CATEGORY, Qgis.Info)
        
        layer_name = image_layer.name().replace("hour","")
        logit(f"working on {layer_name}")
        task.setProgress(i/total*100)
        if task.isCanceled():
            stopped(task)
            return None
    #    
    #    #pull out the particular region we want to work with 
        
        extracted_region = processing.run("native:extractbyattribute", {'INPUT':regions.source(),'FIELD':'region','OPERATOR':0,'VALUE':layer_name,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
        buffered_region = processing.run("native:buffer", {'INPUT':extracted_region,'DISTANCE':50,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':True,'SEPARATE_DISJOINT':False,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
        #print("it worked on ",region["region"],buffered_region)
        ### make use of the option to specify feature as source via  processing feature source def
        ##
        ## random place points within buffered region
        random_points = processing.run("qgis:randompointsinsidepolygons", {'INPUT':buffered_region,'STRATEGY':0,'VALUE':1500,'MIN_DISTANCE':20,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
        ## join by attribute using repro as input 2
        joined_random = processing.run("native:joinbynearest", {'INPUT':random_points,'INPUT_2':image_layer,'FIELDS_TO_COPY':[],'DISCARD_NONMATCHING':True,'PREFIX':'','NEIGHBORS':1,'MAX_DISTANCE':20,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]

        ## delete based on similar geometry, and attribute specifying the photo path
        no_dup_geo = processing.run("native:deleteduplicategeometries", {'INPUT':joined_random,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
        no_dup_attr = processing.run("native:removeduplicatesbyattribute", {'INPUT':no_dup_geo,'FIELDS':['photo'],'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
        #print("done_sampling",len(list(no_dup_attr.getFeatures())))
        kmeans_dict = processing.run("native:kmeansclustering", {'INPUT':no_dup_attr,'CLUSTERS':10,'FIELD_NAME':'CLUSTER_ID','SIZE_FIELD_NAME':'CLUSTER_SIZE','OUTPUT':'TEMPORARY_OUTPUT'})
        kmeans = kmeans_dict["OUTPUT"]
        # reproject otherwise select by distance will fail
        kmeans = processing.run("native:reprojectlayer", {'INPUT':kmeans,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32612'),'CONVERT_CURVED_GEOMETRIES':False,'OPERATION':'+proj=noop','OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]

        # region is the name
        region_name = layer_name
        kmeans_ind = kmeans.fields().indexOf("CLUSTER_ID")
        ###print(len(kmeans.uniqueValues(kmeans_ind)))
        ##instance.addMapLayer(kmeans)
        should_end = False
        if len(kmeans.uniqueValues(kmeans_ind)) ==0 :
          #print("empty tile")
          continue
        for i in kmeans.uniqueValues(kmeans_ind):
            sub_region_name = f"{region_name}_{i}"
            
# get the kmeans vector that corresponds to this cluster val
            kmeans.selectByExpression(f"\"CLUSTER_ID\"={i}")
            kmeans_cluster =  processing.run("native:extractbyattribute", {'INPUT':kmeans,'FIELD':'CLUSTER_ID','OPERATOR':0,'VALUE':i,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
            # don't continue if no points in cluster
            cluster_images_len = len(list(kmeans_cluster.getFeatures()))
            if cluster_images_len < 10:
              #print("less than 10 in cluster")
              continue
            #print("got kmeans",kmeans_cluster)
            #print(cluster_images_len)
            #print(kmeans_cluster.sourceCrs())
            processing.run("native:createspatialindex", {'INPUT':kmeans_cluster})
            processing.run("native:createspatialindex", {'INPUT':kmeans})
            kmeans_cluster_buffer = processing.run("native:extractwithindistance", {'INPUT':kmeans,'REFERENCE':kmeans_cluster,'DISTANCE':100,'OUTPUT':f"qgis_tmp_layers/cluster_{sub_region_name}.gpkg"})["OUTPUT"]
            #print(kmeans_cluster_buffer,get_len_features(kmeans_cluster_buffer))
        #    #paths = []
        #    ###print("up to paths len sub"+str(len(sub_features)))
        #    #for f in kmeans_cluster_buffer.getFeatures():
        #    #    ###print(f)
        #    #    impath = f.attribute("photo")
        #    #    fpath = Path(impath)            
        #    #    paths.append(str(fpath))
        #    ##    
        #    ##print(paths)
        #    #uniques = list(set(paths))
        #    #print(len(uniques))
        #    #logit(f"completed region {sub_region_name}")
        #    #map[sub_region_name] =uniques
        #    # consider this tying in with the kickoff qgis script so we don't have to worry about the jsons getting left around anywhere
    
    #return kmeans_clusters
    ###print(map)
    ###logit("skipping output")
    #out = Path(f"./qgis_cluster{uuid.uuid4()}")
    #out.mkdir()
    #Path(f"{out}/map_images_by_labeled_region_clusters.json").write_text(json.dumps(map))
def completed(exception,result=None):
    if exception is None:
        if result is None:
            QgsMessageLog.logMessage(
                'Completed with no exception and no result '\
                '(probably manually canceled by the user)',
                MESSAGE_CATEGORY, Qgis.Warning)
        else:
            QgsMessageLog.logMessage("completed",
                MESSAGE_CATEGORY, Qgis.Info)
    else:
        QgsMessageLog.logMessage("Exception: {}".format(exception),
                                 MESSAGE_CATEGORY, Qgis.Critical)
        raise exception

instance = QgsProject.instance()
treeroot = instance.layerTreeRoot()
manager = QgsApplication.taskManager()
# get all the children of a group holding the images layers
group = treeroot.findGroup("images_group")
children_layers = [gc.layer() for gc in group.children()]
in_each = 1

images_by_group = list(itertools.zip_longest(*(iter(children_layers),)*in_each))
  #print(regions_by_group)
print("images to procees are",images_by_group)
for i in range(len(images_by_group)):

    images = images_by_group[i]
    task = QgsTask.fromFunction(f"heavy function_{i}",process,on_finished=completed,images_list=images,group_id=i)
    manager.addTask(task)
