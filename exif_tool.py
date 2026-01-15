from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    """
    Extracts metadata like Camera Model, Date, and GPS from an image.
    """
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return {"Status": "No EXIF data found."}
            
        data = {}
        for tag, value in exif.items():
            name = TAGS.get(tag, tag)
            if name == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_name = GPSTAGS.get(t, t)
                    gps_data[sub_name] = value[t]
                data[name] = gps_data
            else:
                data[name] = str(value)
        return data
    except Exception as e:
        return {"Error": str(e)}
