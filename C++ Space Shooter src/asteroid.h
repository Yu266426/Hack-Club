#pragma once

#include "raylib.h"

enum class AsteroidTypes
{
	Large,
	Small
};

class Asteroid
{
public:
	Asteroid(AsteroidTypes type, Vector2 pos, float direction);

	inline AsteroidTypes GetType() { return type; };
	inline Vector2 GetPos() { return pos; };
	inline float GetRadius() { return radius; };
	inline float GetSpeed() { return speed; };
	inline float GetDamage() { return damage; };

	inline void Damage(int damage) { health -= damage; };
	inline bool CheckAlive() { return health > 0; };
	inline Vector2 GetMovement() { return movement; };

	void Update(float delta);
	void Draw();
private:
	AsteroidTypes type;

	Vector2 pos;

	Vector2 movement;

	float speed;

	float rotation;
	float rotationSpeed;

	int health;
	int damage;

	float radius;
};

void LoadAsteroidTextures();
void CleanUpAsteroidTextures();
