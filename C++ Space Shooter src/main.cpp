#include "main.h"
#include "game.h"

#include "raymath.h"

#include <string>

GameStates gameState = GameStates::Start;

float screenShake = 0;
int shakeAmount = 8;
Vector2 cameraPos;
Camera2D camera;

std::string startText = "Press Space To Start!";

int main()
{
	SetupWindow();
	InitializeGame();

	while (!WindowShouldClose())
	{
		float delta = GetFrameTime() * 60;

		// Updates
		switch (gameState)
		{
		case GameStates::Start:
			if (IsKeyPressed(KEY_SPACE))
			{
				ChangeGameState(GameStates::Game);
			}
			break;
		case GameStates::Game:
			UpdateGame(delta, camera);
			break;
		case GameStates::End:
			break;
		}

		// Drawing
		BeginDrawing();
		ClearBackground(BLACK);

		DrawStars(camera.target);

		switch (gameState)
		{
		case GameStates::Start: {
			int startTextWidth = MeasureText(startText.c_str(), 60);
			DrawText(startText.c_str(), GetScreenWidth() / 2 - startTextWidth / 2, GetScreenHeight() * 0.2f, 60, WHITE);
			break;
		}
		case GameStates::Game: {
			DrawGame(camera);
			break;
		}
		case GameStates::End: {
			std::string pointStr = std::to_string(GetPoints());
			int textWidth = MeasureText(pointStr.c_str(), 120);
			DrawText(pointStr.c_str(), GetScreenWidth() / 2 - textWidth / 2, GetScreenHeight() * 0.2f, 120, WHITE);
			break;
		}
		}

		//DrawFPS(10, 780);
		EndDrawing();
	}

	CleanUpGame();
	CloseWindow();
}

void SetupWindow()
{
	InitWindow(800, 800, "Space Shooter");
	SetWindowState(FLAG_VSYNC_HINT);

	//SetExitKey(0);

	// Todo: Load icon

	cameraPos = { 0,0 };
	camera = {
		{ GetScreenWidth() / 2.0f, GetScreenHeight() / 2.0f},
		cameraPos,
		0.0f,
		1.0f
	};
}

void ShakeScreen(float shakeTime)
{
	screenShake = shakeTime;
}

void MoveCamera(Vector2 target, float delta)
{
	cameraPos = Vector2Lerp(camera.target, target, 0.15 * delta);

	if (screenShake > 0)
	{
		camera.target = Vector2Add(cameraPos, { (float)GetRandomValue(-shakeAmount,shakeAmount),(float)GetRandomValue(-shakeAmount,shakeAmount) });
		screenShake -= GetFrameTime();
	}
	else
	{
		camera.target = cameraPos;
		screenShake = 0;
	}
}

Vector2 ScreenToWorld(Vector2 pos)
{
	return GetScreenToWorld2D(pos, camera);
}

void ChangeGameState(GameStates newState)
{
	gameState = newState;
}