WINDOW_SIZE = (800, 800)
FOLLOW_ROOM = 10

# TODO: Most are not final values "finished" (Large asteroid, laser, player trail)
PARTICLE_ATTRIBUTES = {
	"large asteroid": {"size": [20, 34], "speed": [2, 4], "decay": [0.6, 1], "colour": [(235, 143, 30), (235, 62, 14), (255, 208, 54)]},
	"medium asteroid": {"size": [20, 34], "speed": [2, 3], "decay": [0.6, 1], "colour": [(240, 109, 23), (246, 143, 35), (245, 162, 25)]},
	"laser": {"size": [11, 16], "speed": [1, 4], "decay": [0.2, 0.6], "colour": [(252, 207, 3), (255, 248, 43), (255, 166, 0)]},
	"player": {"size": [20, 34], "speed": [2, 4], "decay": [0.6, 1.3], "colour": [(235, 143, 30), (235, 62, 14), (255, 208, 54), (240, 109, 23), (246, 143, 35), (245, 162, 25), (252, 207, 3), (255, 248, 43), (255, 166, 0)]},
	"player trail": {"size": [11, 16], "speed": [1, 2], "decay": [0.6, 1.2], "colour": [(3, 232, 252), (32, 179, 247), (0, 226, 230)]},
	"fireball": {"size": [20, 34], "speed": [2, 3], "decay": [0.6, 1], "colour": [(235, 143, 30), (235, 62, 14), (255, 208, 54), (240, 109, 23), (246, 143, 35), (245, 162, 25), (252, 207, 3), (255, 248, 43), (255, 166, 0)]}
}

ASTEROID_ATTRIBUTES = {
	"large asteroid": {"speed": [4, 6], "rotation": 1, "health": 20, "damage": 20, "radius": 100}

}
