import csv
from tkinter import filedialog, messagebox
from tkinter import *

from polycircles import polycircles
import simplekml

# Todo: Verify selected file is a csv file with proper columns.

# 30 miles in meters
my_radius = 48280.3 * 2

# Pop up a message box stating the radius of the circle
root = Tk()
root.withdraw()
messagebox.showinfo("Notice", "Please make sure the file you select has the following columns: \n"
                                "Latitude, Longitude, Name, Business Phone, After-Hours Phone, Address")


# Open a dialog box to select the csv file
csv_file = filedialog.askopenfilename()

# Read the csv file and store the data in a list
with open(csv_file, 'r') as f:
    next(f)
    reader = csv.reader(f)
    data = list(reader)

# Create a kml object
kml = simplekml.Kml()

# Loop through the list and generate a kml file
for row in data:
    # Create a poly circle object
    poly_circle_1 = polycircles.Polycircle(latitude=float(row[0]),
                                           longitude=float(row[1]),
                                           radius=my_radius,
                                           number_of_vertices=18)

    poly_circle_2 = polycircles.Polycircle(latitude=float(row[0]),
                                         longitude=float(row[1]),
                                         radius=my_radius*2,
                                         number_of_vertices=18)

    # Create a polygon
    polygon1 = kml.newpolygon(name=row[2], outerboundaryis=poly_circle_1.to_kml())
    polygon2 = kml.newpolygon(name=row[2], outerboundaryis=poly_circle_2.to_kml())

    # Set the color of the polygon
    polygon1.style.polystyle.color = simplekml.Color.changealphaint(7, simplekml.Color.yellow)
    polygon2.style.polystyle.color = simplekml.Color.changealphaint(5, simplekml.Color.green)

    # Create a point
    point = kml.newpoint(name=row[2],
                         description=" Address: " + row[5] + " Business #: " + row[3] + " After-Hours #: " + row[4],
                         coords=[(float(row[1]), float(row[0]))])


kml.save("export.kml")
