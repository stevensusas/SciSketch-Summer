import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = '/Users/stevensu/SciSketch-Summer/Contour/1-s2.0-S009286742400967X-fx1.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Set your threshold value (Adjust this value)
threshold_value = 200

# Apply thresholding
_, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

# Detect contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours and get object coordinates
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # Draw rectangle around detected objects
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(f"Object found at coordinates: x={x}, y={y}, width={w}, height={h}")

# Display the image with detected objects
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()
