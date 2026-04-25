# Create test_nmr.py

import numpy as np
import matplotlib.pyplot as plt
import cv2
import ultralytics
from ultralytics import YOLO

print('All packages imported successfully!')

# Test numpy
arr = np.array([1, 2, 3])
print(f'Numpy test: Array sum = {arr.sum()}')

# Test matplotlib (just create a simple plot)
plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig('test_plot.png')
print('Matplotlib: Plot saved as test_plot.png')

# Test OpenCV
img = np.zeros((100, 100, 3), dtype=np.uint8)
print(f'OpenCV: Created image of shape {img.shape}')

# Test Ultralytics
print('Ultralytics: Package loaded successfully')
print('Note: First YOLO model download will happen when you run detection')

print('\\n✅ All tests passed! Environment is ready for NMR project.')
