#pragma once

#include "raylib.h"

class Particle
{
public:
	Particle(Vector2 pos, float speed, float direction, float size, float decay, Color colour);
	
	inline bool CheckAlive() { return size > 3; };

	void Update(float delta);
	void Draw();
private:
	Vector2 pos;

	Vector2 movement;

	float size;
	float decay;

	Color colour;
};