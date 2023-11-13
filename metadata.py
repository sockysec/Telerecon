from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import csv
import folium
from folium.plugins import MarkerCluster
import unicodedata


# Function to remove non-alphanumeric characters from a string
def remove_non_alphanumeric(text):
    return ''.join(char for char in text if char.isalnum())


# Function to extract metadata from an image
def extract_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img._getexif()
    except (AttributeError, OSError):
        metadata = None

    return metadata


# Function to extract GPS metadata from an image
def extract_gps_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            gps_info = exif_data.get(34853)  # GPSInfo tag ID
    except (AttributeError, OSError, KeyError):
        gps_info = None

    return gps_info


# Function to parse and format GPS/Geo data
def parse_gps_info(gps_info):
    if not gps_info:
        return None

    gps_data = {}
    for tag, value in gps_info.items():
        tag_name = GPSTAGS.get(tag, tag)
        gps_data[tag_name] = value

    return gps_data


# Main function
if __name__ == "__main__":
    # Ask the user for a target @Username
    target_username = input("Enter the target @Username: ").strip()

    # Remove "@" symbol if present
    if target_username.startswith("@"):
        target_username = target_username[1:]

    # Define the directories for media analysis and output
    media_directories = [
        os.path.join("Collection", target_username, f"{target_username}_media"),  # Media subdirectory
        os.path.join("Collection", target_username),  # Main user directory
    ]

    # Ensure the output directory exists
    output_directory = os.path.join("Collection", target_username)
    os.makedirs(output_directory, exist_ok=True)

    # Define output CSV and HTML map visualization filenames
    output_csv_file = os.path.join(output_directory, f"{target_username}_gps_metadata.csv")
    map_filename = os.path.join(output_directory, f"{target_username}_GPSmetadata_map.html")

    gps_found = False
    gps_locations = []

    for media_directory in media_directories:
        if not os.path.exists(media_directory):
            continue

        for filename in os.listdir(media_directory):
            if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
                image_path = os.path.join(media_directory, filename)
                metadata = extract_metadata(image_path)
                if gps_info := extract_gps_metadata(image_path):
                    gps_found = True
                    gps_data = parse_gps_info(gps_info)
                    author_bytes = metadata.get(315, "N/A")  # Author tag ID (bytes or string)
                    if isinstance(author_bytes, bytes):
                        try:
                            author = author_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            author = "N/A"  # Use "N/A" for non-UTF-8 encoded names
                    else:
                        author = author_bytes

                    # Remove non-alphanumeric characters from author name
                    author = remove_non_alphanumeric(author)

                    date_time = metadata.get(306, "N/A")  # DateTimeOriginal tag ID
                    camera = metadata.get(271, "N/A")  # Make tag ID
                    gps_data.update({
                        "Author": author,
                        "DateTime": date_time,
                        "Camera": camera
                    })
                    gps_locations.append((filename, gps_data))

    if gps_found:
        print("\033[32m" + "GPS metadata found." + "\033[0m")
    else:
        print("\033[31m" + "No GPS metadata found." + "\033[0m")

    with open(output_csv_file, mode="w", newline="", encoding='utf-8') as csv_file:
        fieldnames = ["ImageName", "Author", "DateTime", "Camera", "GPSInfo"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for filename, gps_data in gps_locations:
            # Remove non-alphanumeric characters from GPSInfo
            gps_data = {key: remove_non_alphanumeric(str(value)) for key, value in gps_data.items()}
            writer.writerow({
                "ImageName": filename,
                "Author": gps_data.get("Author", "N/A"),
                "DateTime": gps_data.get("DateTime", "N/A"),
                "Camera": gps_data.get("Camera", "N/A"),
                "GPSInfo": gps_data,
            })

    if gps_locations:
        # Create a map visualization with automatic zoom and position
        my_map = folium.Map(location=None, zoom_start=None)
        marker_cluster = MarkerCluster().add_to(my_map)

        for filename, gps_data in gps_locations:
            lat = gps_data.get("GPSLatitude", [0, 0, 0])
            lon = gps_data.get("GPSLongitude", [0, 0, 0])
            lat_deg = lat[0] + lat[1] / 60 + lat[2] / 3600
            lon_deg = lon[0] + lon[1] / 60 + lon[2] / 3600

            popup_html = f"<b>Image:</b> {filename}<br>" \
                         f"<b>Author:</b> {gps_data.get('Author', 'N/A')}<br>" \
                         f"<b>Date/Time:</b> {gps_data.get('DateTime', 'N/A')}<br>" \
                         f"<b>Camera:</b> {gps_data.get('Camera', 'N/A')}</font>"

            folium.Marker(location=[lat_deg, lon_deg], popup=popup_html).add_to(marker_cluster)

        # Fit the map to the bounds of the plotted data
        my_map.fit_bounds(marker_cluster.get_bounds())

        # Save the map to an HTML file
        my_map.save(map_filename)

    print(f"GPS metadata analysis completed. Results saved to {output_csv_file}")

    # Ask if the user wants to return to the launcher
    launcher = input('Do you want to return to the launcher? (y/n)')

    if launcher == 'y':
        print('Restarting...')
        exec(open("launcher.py").read())
