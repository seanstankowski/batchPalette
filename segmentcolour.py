import os
import cv2
import numpy as np
import argparse
import csv

# Define color ranges in HSV
color_ranges = {
    'Red1': ((0, 50, 50), (15, 255, 255)),  # Lower range for red
    'Red2': ((170, 50, 50), (195, 255, 255)),  # Upper range for red, near the wrap-around
    'Yellow': ((25, 15, 100), (40, 255, 255)),  # Yellow range
    'Magenta': ((140, 100, 100), (170, 255, 255)),  # Magenta range
    'Pink': ((120, 15, 100), (160, 80, 255)),  # Pink range
    'White': ((0, 0, 200), (180, 17, 255)),  # White range
    'Orange': ((15, 15, 100), (26, 255, 255))  # Orange range
}

# Function to create mask and count valid pixels
def color_mask_and_valid_pixel_count(hsv_img, lower_bound, upper_bound):
    mask = cv2.inRange(hsv_img, lower_bound, upper_bound)
    valid_pixel_count = np.sum(mask > 0)
    return mask, valid_pixel_count

# Process each image
def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Store results
    color_masks = {}
    color_valid_pixel_counts = {}
    total_valid_pixels = 0  # To keep track of the total valid pixels across all color classes

    # Process each color and calculate total valid pixels
    for color, (lower, upper) in color_ranges.items():
        mask, valid_pixel_count = color_mask_and_valid_pixel_count(hsv_image, np.array(lower), np.array(upper))
        if 'Red' in color:  # Combine red masks
            if 'Red' in color_masks:
                color_masks['Red'] |= mask  # Use bitwise OR to combine masks
                color_valid_pixel_counts['Red'] = np.sum(color_masks['Red'] > 0)  # Update valid pixel count
            else:
                color_masks['Red'] = mask
                color_valid_pixel_counts['Red'] = valid_pixel_count
        else:
            color_masks[color] = mask
            color_valid_pixel_counts[color] = valid_pixel_count

    # Calculate total number of valid pixels across all color classes
    total_valid_pixels = sum(color_valid_pixel_counts.values())

    # Calculate the ratio of each color relative to the total valid pixels
    color_ratios = {color: (count / total_valid_pixels) * 100 if total_valid_pixels > 0 else 0
                    for color, count in color_valid_pixel_counts.items()}
    
    return color_ratios

# Write to CSV file
def write_to_csv(output_file, image_name, color_ratios):
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        color_values = [f"{color_ratios[color]:.2f}" for color in color_ratios]
        writer.writerow([image_name] + color_values)

# Main function to process the directory
def main(input_dir, output_file):
    # Create output CSV file and add headers
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        headers = ['Image', 'Red', 'Yellow', 'Magenta', 'Pink', 'White', 'Orange']
        writer.writerow(headers)
    
    # Get all jpg files from the input directory
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.jpg')]

    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        color_ratios = process_image(image_path)
        write_to_csv(output_file, image_file, color_ratios)
        print(f"Processed: {image_file}")

# Entry point for the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images and calculate color percentages.")
    parser.add_argument('input_dir', type=str, help="Directory containing the .jpg images.")
    parser.add_argument('output_file', type=str, help="Output CSV file to store color percentages.")
    
    args = parser.parse_args()
    
    main(args.input_dir, args.output_file)