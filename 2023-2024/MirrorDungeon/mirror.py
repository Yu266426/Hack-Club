import enum


class MirrorTypes(enum.Enum):
	HORIZONTAL = enum.auto()
	VERTICAL = enum.auto()


class Mirror:
	def __init__(self) -> None:
		pass

	@classmethod
	def get_mirror_bit(cls, value):
		return 2 ** value
