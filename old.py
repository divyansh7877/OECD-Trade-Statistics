df['geometry'] = df['the_geom'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, crs='epsg:4326')

