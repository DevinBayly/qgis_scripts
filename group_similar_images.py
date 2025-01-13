def process_and_group_images_in_region(region,criteria,images_to_process=None,add_to_map=False):
  try:
    buffered_region = processing.run("native:buffer", {'INPUT':region,'DISTANCE':50,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'SEPARATE_DISJOINT':False,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
    # clip the images from the phtoos
    # a variable holding the "images to process", as layers
    if images_to_process ==None:
      images_to_process = processing.run("native:clip", {'INPUT':'photos','OVERLAY':buffered_region,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
    ##reproject 
    repro = processing.run("native:reprojectlayer", {'INPUT':images_to_process,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32612'),'CONVERT_CURVED_GEOMETRIES':False,'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=12 +ellps=WGS84','OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
    # assign back to images to process
    images_to_process = repro

    #ensure that we reproject into the meter space
    print(len(list(images_to_process.getFeatures())))

    # loop control variables
    # percentage coverage
    area = 0
    # separate list holding the extracted layers
    # while area below threshold, this is about the amount a region is
    threshold = 1280000
    kill_limit = 7
    results = []
    while area <threshold:
      kill_limit -=1
      if kill_limit <0:
        break
      # go over the unique months, and get selections of each,
      crit_id = images_to_process.fields().indexOf(criteria)
      unique_crits = list(images_to_process.uniqueValues(crit_id))
      print(unique_crits)
      crit_feature_lists = []
      for unique_crit in unique_crits:
        # construct expression for filtering that 
        expr = f"{criteria}={unique_crit}"
        features_len = len(list(images_to_process.getFeatures(expr)))
        crit_feature_lists.append(features_len)
      print(crit_feature_lists)
      # figure out which crit had the most features
      biggest_crit_count = max(crit_feature_lists)
      biggest_crit_index = crit_feature_lists.index(biggest_crit_count)
      crit= unique_crits[biggest_crit_index]
      ## extract that by attribute
      biggest_crit_images = processing.run("native:extractbyattribute", {'INPUT':images_to_process,'FIELD':criteria,'OPERATOR':0,'VALUE':crit,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      if add_to_map:
        QgsProject.instance().addMapLayer(biggest_crit_images)
      else:
        results.append(biggest_crit_images)
      ## ovalize
      ovalized = processing.run("native:rectanglesovalsdiamonds", {'INPUT':biggest_crit_images,'SHAPE':2,'WIDTH':50,'HEIGHT':50,'ROTATION':0,'SEGMENTS':50,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      ## dissolve 
      dissolved = processing.run("native:dissolve", {'INPUT':ovalized,'FIELD':[],'SEPARATE_DISJOINT':False,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      ## calculate a difference against the layer that represents the remaining images
      remaining_images = processing.run("native:extractbyattribute", {'INPUT':images_to_process,'FIELD':criteria,'OPERATOR':1,'VALUE':crit,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      ## this becomes the next round of images to process
      images_to_process = processing.run("native:difference", {'INPUT':remaining_images,'OVERLAY':dissolved,'OUTPUT':'TEMPORARY_OUTPUT','GRID_SIZE':None})["OUTPUT"]
      ## calculate the percentage that the dissolved overlaps with the region that we are working on
      geom_attr = processing.run("qgis:exportaddgeometrycolumns", {'INPUT':dissolved,'CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
      area += next(geom_attr.getFeatures())["area"] 
    ## this should proceed until we have something like 90% coverage of the region
  except Exception as e:
    print(e)
    if add_to_map:
      QgsProject.instance().addMapLayer(images_to_process)
    else:
      results.append(images_to_process)
  if not add_to_map:
    return results



  ## function that takes in a set of images that are the majority, then a set that aren't
  ## the function will then reproject and ovalize, dissolve to make a outline
  ## then that outline is applied in a difference to the set that aren't the majority

region_labels = """
h_11
""".strip().split("\n")
for region_label in region_labels:
  #region_label = region["region"]
  #region_label = region_feat["region"]
  # extract the region matching the label
  region = processing.run("native:extractbyattribute", {'INPUT':'regions','FIELD':'region','OPERATOR':0,'VALUE':region_label,'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
  print(region)

  ## which ever has the largest amount becomes the first, and by attribute we extract those images, and extract the ones that don't match that criteria
  ## then we pass that layer
  # do the month,
  month_results = process_and_group_images_in_region(region,"month",add_to_map=False)
  print("now_proceeding with hour grouping")
  print(month_results)
  # now merge the month results together 
  month_single_layer= processing.run("native:mergevectorlayers", {'LAYERS':month_results,'CRS':QgsCoordinateReferenceSystem('EPSG:32612'),'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
  month_single_layer.setName("month"+region_label)
  print("merged")
  #then the hours
  #TODO need to be able to add the photos that were selected from the total in the last pass to this pass
  hour_results = process_and_group_images_in_region(region,"hour",images_to_process = month_single_layer,add_to_map=False)
  hour_save_path = processing.run("native:mergevectorlayers", {'LAYERS':hour_results,'CRS':QgsCoordinateReferenceSystem('EPSG:32612'),'OUTPUT':f"qgis_tmp_layers/hour{region_label}.gpkg"})["OUTPUT"]
  # open the layer now
  hour_single_layer = QgsVectorLayer(hour_save_path, f"hour{region_label}", "ogr")
  QgsProject.instance().addMapLayers([hour_single_layer])


  # split 
