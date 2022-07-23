#pragma once

#include "raylib.h"

enum class GameStates
{
	Start,
	Game,
	End
};

void SetupWindow();

void ShakeScreen(float shakeTime);

void MoveCamera(Vector2 target, float delta);

Vector2 ScreenToWorld(Vector2 pos);

void ChangeGameState(GameStates newState);
