# Plots cotyledon outlines as polygons and tests the autocorrelation function of
# stomatal positions within the polygons versus that of random points within
# the polygons

import sys
import numpy as np;
import openpyxl;
import matplotlib.mlab as mlab;
import matplotlib.pyplot as pyplot;
#import matplotlib.patches as patches;
import random;

# Takes a workbook sheet and a point count and returns an Nx2 numpy array of point values
def recordSheetCoordinates(point_sheet, point_count):
    points = [[0 for i in range(2)] for j in range(point_count)];
    for i in range(0, point_count):
        points[i][0] = int(round(point_sheet.cell(row = i + 3, column = 1).value));
        points[i][1]= int(round(point_sheet.cell(row = i + 3, column = 2).value));
        points = np.array(points);
    return points;

# Reads in the Excel File (must be of version .xlsx) and gets the worksheet names
crelox_data_file_name = sys.argv[1];
crelox_wb = openpyxl.load_workbook(crelox_data_file_name);
crelox_wb_sheet_names = crelox_wb.get_sheet_names();

# Reads in the data from the worksheets
stomata_sheet = crelox_wb.get_sheet_by_name('Stomatal Positions');
cotyledon_sheet = crelox_wb.get_sheet_by_name('Cotyledon Outline');

stomata_count = stomata_sheet.max_row - 2;
cotyledon_point_count = cotyledon_sheet.max_row - 2;

stomata_points = recordSheetCoordinates(stomata_sheet, stomata_count);
cotyledon_points = recordSheetCoordinates(cotyledon_sheet, cotyledon_point_count);
#cotyledon_points[np.argsort(cotyledon_points[:, 1])];

# Gets the number of sector outline worksheets. Relies on the fact that the sector
# worksheets come sequentially immediately following the cotyledon outline worksheet
sector_names = ['Sector 1 Outline', 'Sector 2 Outline', 'Sector 3 Outline', 'Sector 4 Outline', 'Sector 5 Outline', 'Sector 6 Outline', 'Sector 7 Outline', 'Sector 8 Outline', 'Sector 9 Outline', 'Sector 10 Outline'];
cot_sheet_index = crelox_wb_sheet_names.index('Cotyledon Outline');
number_of_sectors = len(crelox_wb_sheet_names) - (cot_sheet_index + 1);

# Gets the correct worksheets for sector outlines based on number_of_sectors
# Plots points for each sector's outline
for i in range(0, number_of_sectors):
    sector_sheet = crelox_wb.get_sheet_by_name(sector_names[i]);
    sector_point_count = sector_sheet.max_row - 2;
    sector_points = recordSheetCoordinates(sector_sheet, sector_point_count);
    #sector_points[np.argsort(sector_points[:, 1])];
    pyplot.plot(sector_points[:,0], sector_points[:,1], 'g');

#Plots the cotyledon outline and stomatal points
pyplot.plot(stomata_points[:,0], stomata_points[:,1], 'b.');
pyplot.plot(cotyledon_points[:,0], cotyledon_points[:,1], 'm');
#pyplot.gca().add_patch(patches.Polygon(cotyledon_points,closed=True,fill=False)) #This turns a non-polygon into a polygon???
pyplot.axis('equal');
pyplot.show();


# Check if the given list of points are inside the polygon specified by the list of
# polygon_points. Returns the indices of the points_list whose points are inside the
# given polygon
def checkPointsInPolygon(polygon_list, points_list):
    inside = mlab.inside_poly(points_list, polygon_list);
    return inside;
    '''
    if (mlab.is_closed_polygon(polygon_list)):
        inside = mlab.inside_poly(points_list, polygon_list);
        print(inside); #return inside;
    else:
        #make closed polygon
    '''

# Takes the number of random points to be generated, the maximum x-coordinate value
# of the cotyledon outline, and the maximum y-coordinate value of the cotyledon
# outline and returns an Nx2 numpy array of random points.
def generateRandomPoints(number_of_points, x_max, y_max):
    random_points = [[0 for i in range(number_of_points)] for j in range(2)];
    for k in range(0, number_of_points):
        random_points[0][k] = random.randint(0, x_max);
        random_points[1][k] = random.randint(0, y_max);  
        random_points = np.array(random_points);
    return random_points;
    
#print(checkPointsInPolygon(cotyledon_points, stomata_points));


#vertcies Nx2 float array of vertices
#numpy.genfromtxt: (names=True) or skip_header