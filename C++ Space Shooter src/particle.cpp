#include "particle.h"
#include "utils.h"

#include "raymath.h"

Particle::Particle(Vector2 pos, float speed, float direction, float size, float decay, Color colour)
{
	this->pos = pos;

	movement = GetAngledOffset(speed, direction);

	this->size = size;
	this->decay = decay;

	this->colour = colour;
}

void Particle::Update(float delta)
{
	pos = Vector2Add(pos, Vector2Multiply(movement, { delta, delta }));

	size -= decay * delta;
}

void Particle::Draw()
{
	DrawRectanglePro({ pos.x, pos.y, size, size }, { size / 2.0f, size / 2.0f }, 45, colour);
}
