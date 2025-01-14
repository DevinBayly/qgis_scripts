**Note some or all of these scripts are path specific to the project they were developed during**
## Processing Steps Scripts
### kickoff_photogrammetry_on_selection.py
* Instead of using a grid of regions that we automatically segment our images using, we can manually select a few and send them off for processing
* After loading geotagged images we can use a visual selection on the images, and then send them off for photogrammetry
* This step involves submitting images for running on the hpc so in the terminal that started qgis you will need to submit your netid passwd because it's ssh'ing to one of the HPC clusters and submitting jobs
* once this step completes we will need to move on to merging the separate reconstructed materials

### organize_photos_by_region.py
* this is a handoff specific script
* it is also a background process script
* takes all the regions and creates 16 tasks that run in parallel
* each task gets a list of regions and then it clips out the images that fall within each region and symlinks them to a handoff region output folder

### tarring_selection.py
* path specific script, be advised you may need to update
* This script will automatically tar up the raster and a few other folders
### symlink_selected_images_to_regions_folder.py
* background task scriptS
* from selected regions in a created group, this will iterate over the images and put them in a specific folder to be used in reconstruction
### show_missing_regions.py
* this iterates over the grid of regions and when it finds a region who's missing one of the 5 sub orthos, 
* also tries to add new attributes to the region that have to do with the time elapsed since the file's creation
### qgis_tif_loader.py

### manual_select.py
* using a qgis expression
* old script that shows how to manually select images that fall within a range of lat lon,
### make_poly.py
* does what it says

### loading_photo_points_by_region_name
* path specific script, be advised you may need to update
* this script loads a particular region's images when provided a region name or several region names

## load_missing.py
* this script iterates over the regions that don't have existing odm orthophotos
* it will import the photos found for any region that failed reconstruction

### layers_iterator.py
* prints the extent of the layers of the map
### kickoff_on_selected_layer.py
* this script takes an active layer of photos groups by region
* it ensures that they exist in the region_labeled_image_cluster_groups folder
* it then submits them for reconstruction through elgato
### group_similar_images.py
### fill_remove.py
### draw_group_boxes.py
### double_checking_breakout_manually.py
### core_dump_check.py
### checking_ortho_light_levels
### checking_merged_regions.py
### check_completed_clusters.py
### change_gradient_value.py
### breakout_from_image_collection.py
### breakout_by_region_with_clusters.py
### align_dems.py
### add_image_time_props.py
### splitter.py
* This script is breaking images up according to their latitude and longitude values
* this is less efficient than other approaches used later in the project
### handmade_image_dots.py
* the beginning of a script that creates images points by hand