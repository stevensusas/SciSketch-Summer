# example metadata:
# [
#     {
#         "Filename": "Cells.png",
#         "Format": "PNG",
#         "Mode": "RGBA",
#         "Size": [1000, 1000],
#         "Category": "Biology",
#         "Description": "An icon representing biological cells.",
#         "Tags": ["biology", "cell", "microscopy"],
#         "Relationships": ["related to: Cell_spreader_(Glay).png"],
#         "UsageContext": "Used in biological and scientific illustrations.",
#         "CreationDate": "2022-01-15",
#         "Creator": "John Doe"
#     },
#     {
#         "Filename": "Cell_spreader_(Glay).png",
#         "Format": "PNG",
#         "Mode": "RGBA",
#         "Size": [400, 400],
#         "Category": "Laboratory Equipment",
#         "Description": "An icon representing a gray cell spreader.",
#         "Tags": ["laboratory", "equipment", "cell spreader"],
#         "Relationships": ["related to: Cells.png"],
#         "UsageContext": "Used in laboratory equipment illustrations.",
#         "CreationDate": "2022-01-20",
#         "Creator": "Jane Smith"
#     },
#     {
#         "Filename": "Cell_spreader_(black).png",
#         "Format": "PNG",
#         "Mode": "RGBA",
#         "Size": [400, 400],
#         "Category": "Laboratory Equipment",
#         "Description": "An icon representing a black cell spreader.",
#         "Tags": ["laboratory", "equipment", "cell spreader"],
#         "Relationships": ["related to: Cells.png"],
#         "UsageContext": "Used in laboratory equipment illustrations.",
#         "CreationDate": "2022-01-20",
#         "Creator": "Jane Smith"
#     }
# ]


import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exif

def get_image_metadata(image_path):
    # Open image file
    image = Image.open(image_path)
    
    # Basic metadata
    metadata = {
        "Filename": os.path.basename(image_path),
        "Format": image.format,
        "Mode": image.mode,
        "Size": image.size,
    }
    
    # Extract EXIF data
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value
    except AttributeError:
        pass
    
    # Extract additional metadata using exif library
    try:
        img_exif = exif.Image(image_path)
        if img_exif.has_exif:
            for attribute in dir(img_exif):
                if not attribute.startswith("_"):
                    metadata[attribute] = getattr(img_exif, attribute)
    except Exception as e:
        print(f"Error extracting exif data for {image_path}: {e}")
    
    return metadata

def extract_metadata_from_directory(directory):
    metadata_list = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            metadata = get_image_metadata(image_path)
            metadata_list.append(metadata)
    return metadata_list

# Directory containing icons
icon_directory = "demo_icon"

# Extract metadata
icon_metadata = extract_metadata_from_directory(icon_directory)

# Print metadata
for data in icon_metadata:
    print(data)
# {'Filename': 'Cells.png', 'Format': 'PNG', 'Mode': 'RGBA', 'Size': (1000, 1000)}
# {'Filename': 'Cell_spreader_(Glay).png', 'Format': 'PNG', 'Mode': 'RGBA', 'Size': (400, 400)}
# {'Filename': 'Cell_spreader_(black).png', 'Format': 'PNG', 'Mode': 'RGBA', 'Size': (400, 400)}
