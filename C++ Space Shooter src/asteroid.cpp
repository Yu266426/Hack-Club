#include "asteroid.h"
#include "utils.h"
#include "image.h"

#include "raymath.h"

SpaceShooter::Image* largeAsteroidImage = nullptr;
SpaceShooter::Image* smallAsteroidImage = nullptr;

Asteroid::Asteroid(AsteroidTypes type, Vector2 pos, float direction)
{
	this->type = type;

	this->pos = pos;
	rotation = GetRandomValue(0, 360);

	switch (type)
	{
	case AsteroidTypes::Large:
		damage = 15;
		health = 15;

		rotationSpeed = (float)GetRandomValue(-120, 120) / 100.0f;

		speed = (float)GetRandomValue(25, 35) / 5.0f;

		movement = GetAngledOffset(speed, direction);

		radius = largeAsteroidImage->GetSize().x / 2.0f;
		break;
	case AsteroidTypes::Small:
		health = 8;
		damage = 8;

		rotationSpeed = (float)GetRandomValue(-180, 180) / 100.0f;

		speed = (float)GetRandomValue(30, 40) / 5.0f;

		movement = GetAngledOffset(speed, direction);

		radius = smallAsteroidImage->GetSize().x / 2.0f;
		break;
	}
}

void Asteroid::Update(float delta)
{
	pos = Vector2Add(pos, Vector2Multiply(movement, { delta, delta }));

	rotation += rotationSpeed * delta;
}

void Asteroid::Draw()
{
	switch (type)
	{
	case AsteroidTypes::Large:
		largeAsteroidImage->Draw(pos, rotation);
		break;
	case AsteroidTypes::Small:
		smallAsteroidImage->Draw(pos, rotation);
		break;
	}
}

void LoadAsteroidTextures()
{
	largeAsteroidImage = new SpaceShooter::Image("resources/large asteroid.png", 5.0f);
	smallAsteroidImage = new SpaceShooter::Image("resources/small asteroid.png", 5.0f);
}

void CleanUpAsteroidTextures()
{
	delete largeAsteroidImage;
	delete smallAsteroidImage;
}