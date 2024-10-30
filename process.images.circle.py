# process_images.py
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Ensure the display does not block processing when running from a shell script
plt.switch_backend('Agg')

# Get all JPEG files in the current directory
image_files = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg'))]

for filename in image_files:
    img = cv2.imread(filename)

    # Define the center and radius of the circle (adjust these values as needed)
    center_x, center_y = 2000, 1350  # Center of the circle
    radius = 600  # Radius of the circle

    # Create a mask with the same dimensions as the image
    mask = np.zeros(img.shape[:2], dtype="uint8")

    # Draw a white filled circle on the mask
    cv2.circle(mask, (center_x, center_y), radius, 255, -1)

    # Apply the mask to the image using bitwise_and
    masked_image = cv2.bitwise_and(img, img, mask=mask)

    # Convert the cropped region to RGB (if you want to display with matplotlib)
    masked_image_rgb = cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB)

    # If you want to save the result as PNG with a transparent background:
    # Create an alpha channel where the circle is opaque and the rest is transparent
    if filename.lower().endswith('.png'):
        bgr_image = img.copy()
        alpha_channel = np.zeros(mask.shape, dtype="uint8")
        alpha_channel[mask == 255] = 255  # Make the circular region opaque
        bgr_image = cv2.merge((img[:, :, 0], img[:, :, 1], img[:, :, 2], alpha_channel))
        new_file_name = f"{os.path.splitext(filename)[0]}_cropped.png"
        cv2.imwrite(new_file_name, bgr_image)  # Save the image with alpha channel
    else:
        # Save as JPEG with black background (default behavior)
        new_file_name = f"{os.path.splitext(filename)[0]}_cropped.JPG"
        cv2.imwrite(new_file_name, masked_image)  # Save the masked image

    print(f"Processed and saved: {new_file_name}")
