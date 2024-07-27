import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Step 1: Read the NCL RGB file and extract RGB color values
rgb_file = "blue_red.rgb"  # Replace with the path to your NCL RGB file
with open(rgb_file, "r") as file:
    lines = file.readlines()

rgb_data = []
for line in lines:
    if line.strip() and not line.startswith("#"):
        rgb_values = line.split()
        rgb_data.append([float(rgb_values[0]), float(rgb_values[1]), float(rgb_values[2])])

# Step 2: Normalize the color values to the range [0, 1]
norm_rgb_data = np.array(rgb_data) / 255.0

# Step 3: Create a custom colormap using the normalized color values
cmap = LinearSegmentedColormap.from_list('custom_colormap', norm_rgb_data, N=len(norm_rgb_data))

# Example usage of the colormap
x = np.linspace(0, 1, 100)
y = np.sin(2 * np.pi * x)

plt.scatter(x, y, c=x, cmap=cmap)
plt.colorbar()
plt.show()

