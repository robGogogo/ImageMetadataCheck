import os

def analyze_image_authenticity(img_cls):
    """
    Analyze a single image for AI generation or manipulation indicators.
    Returns a detailed analysis dict.
    """
    metadata = img_cls.collect_all_metadata()
    
    analysis = {
        'filename': os.path.basename(img_cls.filename),
        'details': {}
    }
    
    camera_setting_tags = ['ISOSpeedRatings', 'FNumber', 'ExposureTime', 'FocalLength']
    

    has_make = 'Make' in metadata
    has_model = 'Model' in metadata
    has_datetime = 'DateTime' in metadata
    has_datetime_original = 'DateTimeOriginal' in metadata
    has_software = 'Software' in metadata
    has_gps = 'GPSInfo' in metadata and len(metadata.get('GPSInfo', {})) > 1
    has_ms_padding = '59932' in metadata or 59932 in metadata
    
    camera_settings_count = sum(1 for tag in camera_setting_tags if tag in metadata)
    
    total_exif_tags = len(metadata) - 1  # Exclude ImageInfo
    
    # Store details
    analysis['details'] = {
        'has_camera_make': has_make,
        'has_camera_model': has_model,
        'has_datetime': has_datetime,
        'has_datetime_original': has_datetime_original,
        'has_camera_settings': camera_settings_count > 0,
        'camera_settings_count': f"{camera_settings_count}/{len(camera_setting_tags)}",
        'has_gps': has_gps,
        'has_microsoft_padding': has_ms_padding,
        'total_exif_tags': total_exif_tags,
        'software': metadata.get('Software', 'None'),
    }
    
    return analysis


def print_analysis(analysis):
    """Pretty print the analysis results"""
    print("\n" + "=" * 70)
    print(f"IMAGE ANALYSIS: {analysis['filename']}")
    print("=" * 70)
    
    # Details only
    print(f"\n METADATA DETAILS:")
    for key, value in analysis['details'].items():
        print(f"   • {key.replace('_', ' ').title()}: {value}")
    
    print("=" * 70 + "\n")