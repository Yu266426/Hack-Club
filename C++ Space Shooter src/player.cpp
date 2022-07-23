#include "player.h"
#include "main.h"
#include "game.h"
#include "utils.h"

#include "raylib.h"
#include "raymath.h"

#include <string>

void Player::GetInputs()
{
	input.x = (float)IsKeyDown(KEY_D) - IsKeyDown(KEY_A);
	input.y = (float)IsKeyDown(KEY_S) - IsKeyDown(KEY_W);
	input = Vector2Normalize(input);

	rotation = GetAngleTo(pos, ScreenToWorld(GetMousePosition()));

	if (canShoot && IsMouseButtonDown(MOUSE_BUTTON_LEFT))
	{
		canShoot = false;
		shootTimer.StartTimer();

		CreateLaser(pos, 25.0f, rotation, 3);
	}
}

void Player::Cooldowns()
{
	double currentTime = GetTime();

	if (!canShoot && shootTimer.TimerDone())
	{
		canShoot = true;
	}
}

void Player::Update(float delta)
{
	GetInputs();

	// Movement Calculations
	accelerationVector = Vector2Multiply(input, { acceleration, acceleration });
	accelerationVector = Vector2Subtract(accelerationVector, Vector2Multiply(velocity, { drag, drag }));

	velocity = Vector2Add(velocity, Vector2Multiply(accelerationVector, { delta, delta }));

	pos = Vector2Add(pos, Vector2Multiply(velocity, { delta, delta }));

	Cooldowns();
}

void Player::Draw()
{
	image.Draw(pos, rotation);
}
