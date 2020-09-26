import os
import numpy as np

os.system('cls' if os.name == 'nt' else 'clear')


print("\n")
print("* * * * * * * * * * * * * * *")
print("Pyrax: A Terminal-Based Paraxial Raytracing Application Written in Python")
print("Author: Gregory M. Nero")
print("Contact: gnero@email.arizona.edu")
print("Version 0.1")
print("* * * * * * * * * * * * * * *")
print("\n")

print("Enter System Specifications")
number_of_surfaces = int(input("Number of Surfaces: "))
number_of_spaces = number_of_surfaces + 1
number_of_rays = int(input("Number of Rays: "))
number_of_surface_attributes = 2 + number_of_rays
number_of_space_attributes = 2 + number_of_rays
surfaces = {surf: np.zeros(number_of_surface_attributes) for surf in range(number_of_surfaces)}
spaces = {spac: np.zeros(number_of_space_attributes) for spac in range(number_of_spaces)}

print("\n")

print("Enter Ray Properties")
for ray in range(0, number_of_rays):
    
    print("* Ray Number:", ray)

    ray_height_in_image_plane = float(input("Ray Height in Image Plane [mm]: "))

    surfaces[0][2 + ray] = ray_height_in_image_plane

print("\n")

print("Enter Surface Properties")
for surface in range(0, number_of_surfaces):

    print("* Surface Number:", surface)
    curvature = float(input("Radius of Curvature [mm]: "))
    power = float(input("Power [mm^-1]: "))

    surfaces[surface][0] = curvature
    surfaces[surface][1] = power

print("\n")

print("Enter Space Properties")
for space in range(0, number_of_spaces):

    print("* Space Number:", space)
    thickness = float(input("Thickness [mm]: "))
    index_of_refraction = float(input("Index of Refraction: "))

    spaces[space][0] = thickness
    spaces[space][1] = index_of_refraction
