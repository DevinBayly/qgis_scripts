from osgeo import gdal
import math
from scipy.spatial import KDTree
#https://gis.stackexchange.com/questions/221292/retrieve-pixel-value-with-geographic-coordinate-as-input-with-gdal
def get_raster_value(geo_x: float, geo_y: float, ds: gdal.Dataset, band_index: int = 1):
    """Return raster value that corresponds to given coordinates."""
    forward_transform = ds.GetGeoTransform()
    reverse_transform = gdal.InvGeoTransform(forward_transform)
    pixel_coord = gdal.ApplyGeoTransform(reverse_transform, geo_x, geo_y)
    pixel_x = math.floor(pixel_coord[0])
    pixel_y = math.floor(pixel_coord[1])
    print(pixel_x,pixel_y)
    band: gdal.Band = ds.GetRasterBand(band_index)
    print(band)
    val_arr = band.ReadAsArray(pixel_x, pixel_y, 1, 1) # Avoid reading the whole raster into memory - read 1x1 array
    return val_arr[0][0]
    
def alt_method(ds):
    

    # GetGeoTransform gives the (x, y) origin of the top left pixel,
    # the x and y resolution of the pixels, and the rotation of the
    # raster. If the raster is rotated (i.e. the rotation values are
    # anything other than 0) this method will not work.

    # The information is returned as tuple:
    # (TL x, X resolution, X rotation, TL y, Y rotation, y resolution)
    TL_x, x_res, _, TL_y, _, y_res = ds.GetGeoTransform()
    x,y= -12266751.79,3712892.96
    # The point where you wish to sample the raster
    coordinate = (x,y)

    # Divide the difference between the x value of the point and origin,
    # and divide this by the resolution to get the raster index
    x_index = (x - TL_x) / x_res

    # and the same as the y
    y_index = (y - TL_y) / y_res

    # Read the raster as an array
    array = ds.ReadAsArray()
    print(y_index,x_index)
    # Sample with the indexs, not that y_index should be first as the index is
    # [rows, columns] in a 2d grid in python
    pixel_val = array[y_index, x_index]
    return pixel_val
    
# https://opensourceoptions.com/blog/pyqgis-get-raster-data-with-gdal/
def make_ds(layer):
    return gdal.Open(layer.dataProvider().dataSourceUri())
    
#https://gis.stackexchange.com/questions/85192/getting-extent-of-layer-in-qgis
# suuggestion boundingBoxOfSelected
layer = iface.activeLayer()
extent = layer.extent()

print(alt_method(make_ds(layer)))