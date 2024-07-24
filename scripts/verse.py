from PIL import Image, ImageOps

def invert_image_colors(input_image_path, output_image_path):
    # Load the image
    image = Image.open(input_image_path)
    
    # Invert the colors
    inverted_image = ImageOps.invert(image.convert('RGB'))
    
    # Save the inverted image
    inverted_image.save(output_image_path)

# 示例用法
input_image_path = '/home/agou/vv/MedSegDiff/UAVDCD/label/frame_0499.jpg'
output_image_path = '/home/agou/vv/MedSegDiff/UAVDCD/label/frame_0499.jpg'
invert_image_colors(input_image_path, output_image_path)

