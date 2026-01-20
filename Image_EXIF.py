from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json
import os


class Image_EXIF:
    def __init__(self, img, EXIF_data, filename):
        self.img = img
        self.EXIF_data = EXIF_data
        self.filename = filename
        self.all_EXIF = {}

    def get_all_EXIF(self):
        for tag_id, value in self.EXIF_data.items(): # dict -> key, value
            tag_name = TAGS.get(tag_id, tag_id)
            self.all_EXIF[tag_name] = value

    def get_GPS_data(self):
        gps_info = self.EXIF_data.get_ifd(0x8825)  # GPS IFD tag
        if gps_info:
            gps_data = {}
            for tag_id, value in gps_info.items():
                tag_name = GPSTAGS.get(tag_id, tag_id)
                gps_data[tag_name] = value
            self.all_EXIF['GPSInfo'] = gps_data

    def get_non_EXIF_data(self):
        info = self.img.info  # Dictionary of all metadata
        self.all_EXIF['ImageInfo'] = info

    def collect_all_metadata(self):
        self.all_EXIF = {}
        self.get_all_EXIF()
        self.get_GPS_data()
        self.get_non_EXIF_data()
        return self.all_EXIF
    
    def display(self):
        metadata = self.collect_all_metadata()
        print(json.dumps(metadata, indent=2, default=str))

    def write(self, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        metadata = self.collect_all_metadata()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, default=str)
    