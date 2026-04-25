import cv2
import numpy as np

# Load your video
cap = cv2.VideoCapture("data/videos/test_near_miss.mp4")

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error loading video")
    exit()

points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked: ({x}, {y})")
        points.append([x, y])
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        display_frame = frame.copy()
        scale = 0.3  # adjust if needed (0.3, 0.4, etc.)
        display_frame = cv2.resize(display_frame, None, fx=scale, fy=scale)
        cv2.imshow("Frame", display_frame)

display_frame = frame.copy()

scale = 0.3  # adjust if needed (0.3, 0.4, etc.)
display_frame = cv2.resize(display_frame, None, fx=scale, fy=scale)

cv2.imshow("Frame", display_frame)
cv2.setMouseCallback("Frame", click_event)

print("👉 Click 4 points on the ROAD (rectangle shape)")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Image points:", points)

def order_points(pts):
    pts = np.array(pts, dtype=np.float32)

    # sort by y (top first, bottom later)
    pts = pts[np.argsort(pts[:, 1])]

    top = pts[:2]
    bottom = pts[2:]

    # sort left/right within top
    if top[0][0] < top[1][0]:
        top_left, top_right = top
    else:
        top_right, top_left = top

    # sort left/right within bottom
    if bottom[0][0] < bottom[1][0]:
        bottom_left, bottom_right = bottom
    else:
        bottom_right, bottom_left = bottom

    return np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.float32)


if len(points) != 4:
    print("Need exactly 4 points")
    exit()

image_points = order_points(points)
print("Ordered points:", image_points)

# 🔴 YOU DEFINE THIS (REAL WORLD ESTIMATE)
world_points = np.array([
    [0, 20],   # top-left  (far)
    [6, 20],   # top-right (far)
    [0, 0],    # bottom-left (near)
    [6, 0]     # bottom-right (near)
], dtype=np.float32)

H, _ = cv2.findHomography(image_points, world_points)

print("\n✅ COPY THIS MATRIX:\n")
print(H)