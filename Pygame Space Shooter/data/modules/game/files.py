import os.path
import sys

CURRENT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

DATA_DIR = os.path.join(CURRENT_DIR, "data")
ASSET_DIR = os.path.join(DATA_DIR, "assets")
IMAGE_ASSET_DIR = os.path.join(ASSET_DIR, "image_assets")
IMAGE_DIR = os.path.join(IMAGE_ASSET_DIR, "images")
IMAGE_CONFIG_DIR = os.path.join(IMAGE_ASSET_DIR, "configs")
