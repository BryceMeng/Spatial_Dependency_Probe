from PIL import Image, ImageDraw
import random
import os

# Create output directory
output_dir = "trapezoid_circle_images"
os.makedirs(output_dir, exist_ok=True)

BASE_IMAGE_SIZE = (600, 600)  # Base image size

def generate_trapezoid_circle_image(
    image_size,
    trapezoid_size,
    circle_size,
    circle_offset,
    include_circle,
    circle_position,
    output_path
):
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)

    # Define trapezoid shape
    trapezoid_top_length = trapezoid_size[0]
    trapezoid_base_length = trapezoid_size[1]
    trapezoid_height = trapezoid_size[2]
    trapezoid_x_center = image_size[0] // 2
    trapezoid_y_base = image_size[1] * 2 // 3

    # Trapezoid vertices
    x1 = trapezoid_x_center - trapezoid_top_length // 2
    x2 = trapezoid_x_center + trapezoid_top_length // 2
    x3 = trapezoid_x_center + trapezoid_base_length // 2
    x4 = trapezoid_x_center - trapezoid_base_length // 2
    y1 = trapezoid_y_base - trapezoid_height
    y2 = trapezoid_y_base

    # Draw trapezoid
    draw.polygon([(x1, y1), (x2, y1), (x3, y2), (x4, y2)], fill="black")

    # Optionally draw a circle
    if include_circle:
        # Bounding box of the trapezoid
        bbox_left = min(x1, x4)
        bbox_right = max(x2, x3)
        bbox_top = y1
        bbox_bottom = y2

        # Determine circle position (outside the bounding box)
        if circle_position == "left":
            circle_x = bbox_left - circle_offset - circle_size
        elif circle_position == "right":
            circle_x = bbox_right + circle_offset
        else:
            raise ValueError("circle_position must be 'left' or 'right'.")

        # Align circle vertically with trapezoid center
        circle_y = (bbox_top + bbox_bottom) // 2 - circle_size // 2

        # Ensure the circle stays within image boundaries
        circle_x = max(20, min(circle_x, image_size[0] - circle_size - 20))
        circle_y = max(20, min(circle_y, image_size[1] - circle_size - 20))

        # Draw the circle
        draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], fill="black")

    # Save the image
    img.save(output_path)

# Generate 70 images for validation (or training)
circle_probability = 0.8   # Probability that a circle is included
left_probability = 0.6     # Probability that the circle is on the left side

for i in range(70):
    image_size = BASE_IMAGE_SIZE
    trapezoid_size = (
        random.randint(100, 200),  # Top edge length
        random.randint(200, 300),  # Base edge length
        random.randint(150, 250),  # Height
    )
    circle_size = random.randint(40, 80)       # Circle diameter
    circle_offset = random.randint(50, 100)    # Distance between circle and trapezoid

    # Determine whether to include the circle and its side
    include_circle = random.random() < circle_probability
    circle_position = "left" if random.random() < left_probability else "right"

    output_path = os.path.join(output_dir, f"image_{i + 1}.png")
    generate_trapezoid_circle_image(
        image_size,
        trapezoid_size,
        circle_size,
        circle_offset,
        include_circle,
        circle_position,
        output_path
    )

print(f"Generated images have been saved to folder: {output_dir}")
