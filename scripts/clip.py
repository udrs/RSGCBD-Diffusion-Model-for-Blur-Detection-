from PIL import Image
import os

def crop_center(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Define the size of the cropped image
    crop_width = 1024
    crop_height = 1024

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)
            
            image = Image.open(input_image_path)
            img_width, img_height = image.size

            # Calculate the coordinates for the center crop
            left = (img_width - crop_width) // 2
            top = (img_height - crop_height) // 2
            right = left + crop_width
            bottom = top + crop_height

            # Crop the image
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save(output_image_path)

# 示例用法
input_folder = '/home/agou/vv/MedSegDiff/UAVDCD2/natural'
output_folder = '/home/agou/vv/MedSegDiff/UAVDCD2/natural'
crop_center(input_folder, output_folder)

