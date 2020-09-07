import datetime
import ee
import ee.mapclient


ee.Authenticate()
ee.Initialize()

# Filter the L7 collection to a single month.
# collection = (ee.ImageCollection('LANDSAT/LC08/C01/T1_RT_TOA')
#               .filterDate(datetime.datetime(2019, 11, 1),
#                           datetime.datetime(2019, 12, 1)))

# Filter the L7 collection to a single month.
collection = ee.ImageCollection('LANDSAT/LE07/C01/T1_TOA')


def NDVI(image):
  """A function to compute NDVI."""
  return image.expression('float(b("B4") - b("B3")) / (b("B4") + b("B3"))')


def SAVI(image):
  """A function to compute Soil Adjusted Vegetation Index."""
  return ee.Image(0).expression(
      '(1 + L) * float(nir - red)/ (nir + red + L)',
      {
          'nir': image.select('B4'),
          'red': image.select('B3'),
          'L': 0.2
      })

vis = {
    'min': 0,
    'max': 1,
    'palette': [
        'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
        '99B718', '74A901', '66A000', '529400', '3E8601',
        '207401', '056201', '004C00', '023B01', '012E01',
        '011D01', '011301'
    ]}

# earth engine lat-long map
ee.mapclient.centerMap(81.24609000000004,20.75260000000003, 12)
ee.mapclient.addToMap(collection.map(NDVI).mean(), vis)
# ee.mapclient.addToMap(collection.map(SAVI).mean(), vis)