#pragma once

#include "raylib.h"

#include <vector>

struct Laser
{
	Vector2 pos;
	Vector2 movement;
	float rotation;
	int damage;
};

struct Star
{
	Vector3 pos;
	Color colour;
};

// Functions
void InitializeGame();

int GetPoints();

void GenerateStars();
void DrawStars(const Vector2& cameraPos);

void CreateLaser(Vector2 pos, float speed, float angle, int damage);

void UpdateGame(float delta, Camera2D camera);
void DrawGame(Camera2D camera);

void CleanUpGame();
