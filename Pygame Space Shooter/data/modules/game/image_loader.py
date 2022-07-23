import json
import os

import pygame

from data.modules.game.files import IMAGE_DIR, IMAGE_CONFIG_DIR


class ImageLoader:
	images: dict[str, pygame.Surface] = {}

	@staticmethod
	def load_images():
		for _, __, files in os.walk(IMAGE_DIR):
			for file in files:
				image_name = file[:-4]
				image = pygame.image.load(os.path.join(IMAGE_DIR, file))

				image = ImageLoader.load_config(image_name, image)

				ImageLoader.images[image_name] = image

	@staticmethod
	def load_config(image_name: str, image: pygame.Surface):
		config_path = os.path.join(IMAGE_CONFIG_DIR, f"{image_name}.json")

		if not os.path.isfile(config_path):
			ImageLoader.create_config(image_name, image)

		with open(config_path, "r") as config_file:
			config_json = json.load(config_file)

			return pygame.transform.scale(image, (config_json["width"] * config_json["scale"], config_json["height"] * config_json["scale"]))

	@staticmethod
	def create_config(image_name: str, image: pygame.Surface):
		# Create a configs directory if it does not exist
		if not os.path.isdir(IMAGE_CONFIG_DIR):
			os.mkdir(IMAGE_CONFIG_DIR)

		# Makes the file_name into a json
		file_name = f"{image_name}.json"
		file_path = os.path.join(IMAGE_CONFIG_DIR, file_name)

		# Creates a default config if it does not exist
		image_config_path = os.path.join(IMAGE_CONFIG_DIR, file_path)
		if not os.path.isfile(image_config_path):
			# Creates config file
			config_file = open(file_path, "x")

			# Creates the contents
			config_json = {
				"width": image.get_width(),
				"height": image.get_height(),
				"scale": 1
			}

			# Writes the contents
			with open(file_path, "w") as config_file:
				config_file.write(json.dumps(config_json))

	@staticmethod
	def get_image(image_name):
		return ImageLoader.images[image_name]
