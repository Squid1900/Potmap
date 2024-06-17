import os

def initialize_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w') as file:
            file.write("Suburb,Latitude,Longitude\n")

initialize_csv("pothole_locations.csv")
