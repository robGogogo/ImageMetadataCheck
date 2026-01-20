from PIL import Image
from Image_EXIF import Image_EXIF
from utils.header import print_header
from analyze_image_authencity import analyze_image_authenticity, print_analysis
import os


def write_image_exif(img_cls):
    """Display image metadata and write to JSON"""

    file_name = os.path.basename(img_cls.filename)
    file_name_no_ext = os.path.splitext(file_name)[0]
    json_filename = f"{file_name_no_ext}.json"

    file_path = os.path.join("json_files", json_filename)

    img_cls.collect_all_metadata()
    img_cls.write(file_path)


def print_image_exif(img_cls):
    img_cls.collect_all_metadata()
    img_cls.display()


def main():
    image_files = [
        "GT3RS.jpg",
        "Ian.JPG",
        "560SL.png",
        "me.jpg",
    ]

    image_classes = []

    # Load images and write EXIF JSON string
    for image_name in image_files:
        img = Image.open(os.path.join("Images", image_name))
        img_class = Image_EXIF(img, img.getexif(), img.filename)

        write_image_exif(img_class)
        image_classes.append(img_class)

    # Analyzation
    for img_class in image_classes:
        analysis = analyze_image_authenticity(img_class)
        print_analysis(analysis)


if __name__ == "__main__":
    main()
