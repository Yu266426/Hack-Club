import json


class App:
	def __init__(self):
		self.running = True

		self.commands = {
			"quit": self.quit,
			"q": self.quit,
			"list": self.list,
			"l": self.list,
			"update_emails": self.update_emails,
			"ue": self.update_emails,
			"add_override": self.add_email_override,
			"ao": self.add_email_override,
			"remove_override": self.remove_email_override,
			"ro": self.remove_email_override,
			"add_member": self.add_member,
			"am": self.add_member,
			"remove_member": self.remove_member,
			"rm": self.remove_member,
			"find_member": self.find_member,
			"fm": self.find_member
		}

	# * Functions
	def quit(self):
		self.running = False

	@staticmethod
	def list(list_type: str):
		with open("hack_club_members.json") as file:
			data = json.load(file)

			print("--------------------")
			if list_type in data:
				for val in data[list_type]:
					print(val)
			else:
				print("Not an option to list")
			print("--------------------")

	@staticmethod
	def update_emails():
		with open("hack_club_members.json") as file:
			data = json.load(file)

		emails = []
		for name in data["members"]:
			if name not in data["email_overrides"]:
				split_name: list[str] = name.split(" ")

				if len(split_name) > 2:
					print(f"Warning: {name} has more than 2 parts. An override may be needed.")

				email = ""
				for part in split_name[:-1]:
					email += part.lower()
				email += "."
				email += split_name[-1].lower()
				email += "@smus.ca"

				emails.append(email)
			else:
				emails.append(data["email_overrides"][name])

		data["emails"] = emails
		with open("hack_club_members.json", "w") as file:
			file.write(json.dumps(data))

	@staticmethod
	def add_email_override(name: str, email: str):
		with open("hack_club_members.json") as file:
			data = json.load(file)

		if name in data["members"]:
			data["email_overrides"][name] = email
			with open("hack_club_members.json", "w") as file:
				file.write(json.dumps(data))
		else:
			print(f"{name} not a member")

	@staticmethod
	def remove_email_override(name: str):
		with open("hack_club_members.json") as file:
			data = json.load(file)

		if name in data["email_overrides"]:
			del data["email_overrides"][name]
			with open("hack_club_members.json", "w") as file:
				file.write(json.dumps(data))
		else:
			print("Not an email override")

	@staticmethod
	def add_member(name: str):
		with open("hack_club_members.json") as file:
			data = json.load(file)

		data["members"].append(name)
		data["members"].sort()

		with open("hack_club_members.json", "w") as file:
			file.write(json.dumps(data))

	@staticmethod
	def remove_member(name: str):
		with open("hack_club_members.json") as file:
			data = json.load(file)

		if name in data["members"]:
			data["members"].remove(name)
			with open("hack_club_members.json", "w") as file:
				file.write(json.dumps(data))
		else:
			print("Member does not exist")

	@staticmethod
	def find_member(name: str):
		with open("hack_club_members.json") as file:
			data = json.load(file)

		if name in data["members"]:
			print(f"{name} is a member")
		else:
			print(f"{name} is not a member")

	# * Update
	def update(self):
		user_input = input("Input: ").split(" ")

		# Is valid command
		if user_input[0].lower().strip() in self.commands:
			command = self.commands[user_input[0].lower().strip()]

			# Command has arguments
			if len(command.__annotations__) > 0:
				args = []

				# Process inputs
				# If arg surrounded with ", then multiple spaces are allowed
				is_multi = False
				current_arg = ""
				for arg in user_input[1:]:
					if not is_multi and arg.startswith('"'):
						is_multi = True
						current_arg = arg[1:]
						current_arg += " "
						continue
					elif is_multi and arg.endswith('"'):
						is_multi = False
						current_arg += arg[:-1]
						args.append(current_arg)
						continue

					if is_multi:
						current_arg += arg
						current_arg += " "
					else:
						args.append(arg)

				# Convert args to appropriate type
				for index, arg_info in enumerate(command.__annotations__.items()):
					args[index] = arg_info[1](args[index])

				# Try running command
				try:
					command(*args)
				except TypeError:
					print(f"{command.__name__} has wrong arguments: {args}")
					print(f"Should instead accept {command.__annotations__}")

			# Run command with no arguments
			else:
				command()

		# Not a valid command
		else:
			print("Not a valid command")


if __name__ == '__main__':
	app = App()

	while app.running:
		app.update()
