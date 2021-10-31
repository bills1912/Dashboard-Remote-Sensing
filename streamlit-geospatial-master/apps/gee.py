import ee
import streamlit as st
import geemap.foliumap as geemap


def remoteSensing():

    st.header("Remote Sensing Classification")

    row1_col1, row1_col2 = st.columns([3, 1])
    width = 950
    height = 600

    ee.Authenticate()
    ee.Initialize()
    
    Map = geemap.Map()

    # Select the seven NLCD epoches after 2000.
    region = ["Kab. Nganjuk", "Kab. Abab Pematang Ilir", "Kab. Rokan Hulu"]

    # Get an NLCD image by year.
    def getRS(region):

        if region == "Kab. Nganjuk":
            Map.set_center(lat=-7.6, lon=112, zoom=10)
            ee_path = 'users/bills/nganjuk_polygon'
            nganjuk_landsat = ee.FeatureCollection(ee_path)
            nganjuk_landsat = nganjuk_landsat.geometry()

            # Clip the map
            landsat = ee.ImageCollection(ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
                         .filterDate('2020-03-10', '2020-03-15')
                         .filterBounds(nganjuk_landsat)).mean().clip(nganjuk_landsat)

            # Add the raster map
            cnn_model_landsat = ee.Image('users/bills/cnn_nganjuk_landsat')
            nganjuk_new = cnn_model_landsat.clip(nganjuk_landsat)
            
            

            # Add true color layer
            # Map.addLayer(landsat, {'min':0, 'max':3000, 'bands':['B4', 'B3', 'B2'], 'gamma':1.25}, 'Sentinel')

            # Add the result of remote sensing classification map
            Map.addLayer(nganjuk_new, {'min':0, 'max':7, 'palette':['#000000','#b800f5', '#3449eb', '#00ff54', '#ffea00', 
                                                                    '#327800', '#ffffff', '#ff0000']}, 'Kab. Nganjuk')
        
        elif region == "Kab. Abab Pematang Ilir":
            Map.set_center(lat=-3.207876813081164, lon=103.920726803023, zoom=10)
            ee_path = 'users/221709965/PALI'
            pali_sentinel = ee.FeatureCollection(ee_path)
            pali_sentinel = pali_sentinel.geometry()

            # Clip the map
            sentinel = ee.ImageCollection(ee.ImageCollection('COPERNICUS/S2')
                         .filterDate('2019-01-01', '2019-12-31')
                         .filterBounds(pali_sentinel)
                         .sort('CLOUD_COVERAGE_ASSESSMENT', False)).mean().clip(pali_sentinel)

            # Add the raster map
            raster_model = ee.Image('users/bills/sentinel_pali')
            pali_new = raster_model.clip(pali_sentinel)

            # Add true color layer
            Map.addLayer(sentinel, {'bands': ['B4','B3','B2'], 'min':0, 'max': 3000, 'gamma': 1.25}, "Sentinel")

            # Add the result of remote sensing classification map
            Map.addLayer(pali_new, {'palette':['#FFFFFF', '#9e0dd3', '#06ae07', '#eae80c', '#6b4e04', '#c30000'], 
                                   'min':0, 'max':5}, 'Kab. Abab Pematang Ilir')
        
        elif region == "Kab. Rokan Hulu":
            Map.set_center(lat=0.8984350205485738, lon=100.5401861369357, zoom=9)
            ee_path = 'users/221710079/Rokan_Hulu'
            rokan_hulu = ee.FeatureCollection(ee_path)
            rokan_hulu = rokan_hulu.geometry()

            ee_path = 'users/221710079/Rokan_Hulu'
            rokan_hulu = ee.FeatureCollection(ee_path)
            rokan_hulu = rokan_hulu.geometry()

            # Clip the map
            sentinel = ee.ImageCollection(ee.ImageCollection("COPERNICUS/S2")
                             .filterDate("2019-01-01", "2019-12-31")
                             .filterBounds(rokan_hulu)).mean().clip(rokan_hulu)

            # Add the raster map
            rf_model_rh = ee.Image('users/bills/rf_rh_sentinel_2019')
            new_rh = rf_model_rh.clip(rokan_hulu)

            # Add true color layer
            # Map.addLayer(sentinel, {'min':0, 'max':3000, 'bands':['B4', 'B3', 'B2'], 'gamma':1.25}, 'Sentinel')

            # Add the result of remote sensing classification map
            Map.addLayer(new_rh, {'min':0, 'max':5, 'palette':['#00FF00', 'A0522D', '006400	', 'blue', 'yellow', '808080']},
                     'Kab. Rokan Hulu')
    
    def getLegend(region):
        if region == "Kab. Nganjuk":
            legend_title = "Klasifikasi Lahan Kabupaten Nganjuk"
            legend_dict = {
                'Lahan Terbangun': 'b800f5',
                'Air': '3449eb',
                'Sawah': '00ff54',
                'Bera': 'ffea00',
                'Hutan': '327800',
                'Tol': 'ffffff',
                'Awan': 'ff0000'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict, layer_name='Kab. Nganjuk')
        
        elif region == "Kab. Abab Pematang Ilir":
            legend_title = "Klasifikasi Lahan Kabupaten Abab Pematang Ilir"
            legend_dict = {'Karet': 'c30000',
               'Sawit (Perkebunaan Non Karet)': '9e0dd3',
               'Hutan': '06ae07',
               'Bangunan': 'eae80c',
               'Tanah': '6b4e04',
               'Air': 'FFFFFF'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict)
        
        elif region == "Kab. Rokan Hulu":
            legend_title = "Klasifikasi Lahan Kabupaten Abab Pematang Ilir"
            legend_dict = {'Karet': '00FF00',
               'Sawit (Perkebunaan Non Karet)': 'A0522D',
               'Hutan': '006400',
               'Bangunan': '0E33ED',
               'Tanah': 'E8FA46',
               'Air': '808080'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict)

    with row1_col2:
        selected_region = st.multiselect("Select a year", region)
        add_legend = st.checkbox("Show legend")

    if selected_region:
        for region in selected_region:
            getRS(region)

        if add_legend:
            getLegend(region)

        with row1_col1:
            Map.to_streamlit(width=width, height=height)

    else:
        with row1_col1:
            Map.to_streamlit(width=width, height=height)

def app():
    st.title("Google Earth Engine Applications")

    apps = ["Remote Sensing Classification", "Another Future Applications"]

    selected_app = st.selectbox("Select an app", apps)

    if selected_app == "Remote Sensing Classification":
        remoteSensing()
