#pragma once

#include "timer.h"
#include "image.h"

#include "raylib.h"

class Player
{
public:
	inline Vector2 GetPos() { return pos; };
	inline Vector2 GetInput() { return input; };
	inline float GetRotation() { return rotation; };
	inline float GetRadius() { return radius; };
	inline int GetHealth() { return health; };
	inline int GetDamage() { return health; };

	inline bool CheckAlive() { return health > 0; };
	inline void Damage(int damage) { health -= damage; };

	void GetInputs();
	void Cooldowns();
	void Update(float delta);
	void Draw();
protected:
	// Inputs
	Vector2 input = { 0,0 };

	// Movement
	Vector2 pos = { 0,0 };

	float acceleration = 2.3f;
	float drag = 0.14f;

	Vector2 velocity = { 0,0 };
	Vector2 accelerationVector = { 0,0 };

	float rotation = 0.0f;

	// Shooting
	bool canShoot = true;
	Timer shootTimer = Timer(0.15);

	// Stats
	int health = 100;

	// Graphics
	SpaceShooter::Image image = SpaceShooter::Image("resources/player.png", 7.0f);

	float radius = image.GetSize().x / 2.0f;
};