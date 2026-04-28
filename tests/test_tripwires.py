import os
import pytest
import geopandas as gpd
from shapely.geometry import Polygon
import sys

# Add analysis/scripts to path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis', 'scripts')))
from november_tripwires import run_tripwires

def test_crs_validation_failure(tmp_path):
    # Create a dummy ED shapefile in the wrong projected CRS (e.g., EPSG:3857)
    # The script should raise ValueError for non-3401 projected CRS.
    p1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    eds = gpd.GeoDataFrame({'name_2026': ['ED1'], 'geometry': [p1]}, crs="EPSG:3857")
    eds_path = tmp_path / "eds_wrong_crs.gpkg"
    eds.to_file(eds_path, driver="GPKG")
    
    with pytest.raises(ValueError, match="Expected shapefile to be in Alberta 10-TM"):
        run_tripwires(str(eds_path))

def test_crs_geographic_reprojection(tmp_path, capsys):
    # Geographic CRS (e.g., EPSG:4326) should be gracefully reprojected
    p1 = Polygon([(-114, 51), (-113, 51), (-113, 52), (-114, 52)])
    eds = gpd.GeoDataFrame({'name_2026': ['ED1'], 'geometry': [p1]}, crs="EPSG:4326")
    eds_path = tmp_path / "eds_geo_crs.gpkg"
    eds.to_file(eds_path, driver="GPKG")
    
    # Should not raise ValueError
    run_tripwires(str(eds_path))
    captured = capsys.readouterr()
    assert "Reprojecting to Alberta 10-TM" in captured.out

def test_drain_pattern_detection(tmp_path, capsys):
    # Create a dummy city (e.g., Medicine Hat)
    city_poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    cities = gpd.GeoDataFrame({'name': ['Medicine Hat (CY)'], 'geometry': [city_poly]}, crs="EPSG:3401")
    cities_path = tmp_path / "cities.gpkg"
    cities.to_file(cities_path, driver="GPKG")
    
    # Medicine Hat pop ~63k -> 63k / 51648 = ceil(1.22) = 2 expected seats.
    # We will split the city into 3 EDs.
    ed1 = Polygon([(0, 0), (10, 0), (10, 4), (0, 4)]) # 40%
    ed2 = Polygon([(0, 4), (10, 4), (10, 8), (0, 8)]) # 40%
    ed3 = Polygon([(0, 8), (10, 8), (10, 10), (0, 10)]) # 20%
    
    eds = gpd.GeoDataFrame({'name_2026': ['ED1', 'ED2', 'ED3'], 'geometry': [ed1, ed2, ed3]}, crs="EPSG:3401")
    eds_path = tmp_path / "eds_split.gpkg"
    eds.to_file(eds_path, driver="GPKG")
    
    run_tripwires(str(eds_path), str(cities_path))
    captured = capsys.readouterr()
    
    # Expect a RED ALERT because 3 > 2 expected seats
    assert "[RED ALERT]" in captured.out
    assert "Medicine Hat" in captured.out
    assert "split into 3 districts" in captured.out
    
    # Test valid split (2 EDs)
    ed4 = Polygon([(0, 0), (10, 0), (10, 5), (0, 5)]) # 50%
    ed5 = Polygon([(0, 5), (10, 5), (10, 10), (0, 10)]) # 50%
    eds_valid = gpd.GeoDataFrame({'name_2026': ['ED4', 'ED5'], 'geometry': [ed4, ed5]}, crs="EPSG:3401")
    eds_valid_path = tmp_path / "eds_valid.gpkg"
    eds_valid.to_file(eds_valid_path, driver="GPKG")
    
    run_tripwires(str(eds_valid_path), str(cities_path))
    captured_valid = capsys.readouterr()
    assert "[PASS]" in captured_valid.out
    assert "kept intact (2 districts)" in captured_valid.out
