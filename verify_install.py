
print('=== Verifying Package Installations ===')

try:
    import numpy as np
    print(f'✅ NumPy version: {np.__version__}')
except ImportError:
    print('❌ NumPy NOT installed')

try:
    import matplotlib
    print(f'✅ Matplotlib version: {matplotlib.__version__}')
except ImportError:
    print('❌ Matplotlib NOT installed')

try:
    import cv2
    print(f'✅ OpenCV version: {cv2.__version__}')
except ImportError:
    print('❌ OpenCV NOT installed')

try:
    import ultralytics
    print(f'✅ Ultralytics version: {ultralytics.__version__}')
except ImportError:
    print('❌ Ultralytics NOT installed')

print('=' * 40)

