#include "game.h"
#include "player.h"
#include "asteroid.h"
#include "utils.h"
#include "image.h"
#include "particle.h"
#include "main.h"

#include "raymath.h"

#include <string>
#include <vector>
#include <map>

int points = 0;
Player* player = nullptr;
Timer* playerTrailTimer = nullptr;

Timer* playerDeathTimer = nullptr;

// Lasers
std::vector <Laser> lasers;

SpaceShooter::Image* laserImage = nullptr;

// Asteroids
std::vector <Asteroid> asteroids;

Timer* asteroidTimer = nullptr;

// Stars
int nStars = 100;
int borderBuffer = 50;
std::vector <Star> stars;

// Particles
std::vector <Particle> particles;

enum class ParticleTypes
{
	LargeAsteroid,
	SmallAsteroid,
	Laser,
	PlayerTrail,
	PlayerExplosion
};

std::map <ParticleTypes, std::vector<Color>> particleColours;

void InitializeGame()
{
	laserImage = new SpaceShooter::Image("resources/laser.png", 2.5f);

	LoadAsteroidTextures();

	player = new Player;

	playerTrailTimer = new Timer(0.03);
	playerDeathTimer = new Timer(5);

	asteroidTimer = new Timer(3);
	asteroidTimer->StartTimer();

	GenerateStars();

	// Load particle colours
	std::vector <Color> colours;
	colours.push_back({ 235, 143, 30, 255 });
	colours.push_back({ 235, 62, 14, 255 });
	colours.push_back({ 255, 208, 54, 255 });

	particleColours.emplace(ParticleTypes::LargeAsteroid, colours);

	colours.clear();
	colours.push_back({ 240, 109, 23, 255 });
	colours.push_back({ 246, 143, 35, 255 });
	colours.push_back({ 245, 162, 25, 255 });

	particleColours.emplace(ParticleTypes::SmallAsteroid, colours);

	colours.clear();
	colours.push_back({ 252, 207, 3, 255 });
	colours.push_back({ 255, 248, 43, 255 });
	colours.push_back({ 255, 166, 0, 255 });

	particleColours.emplace(ParticleTypes::Laser, colours);

	colours.clear();
	colours.push_back({ 3, 232, 252, 255 });
	colours.push_back({ 32, 179, 247, 255 });
	colours.push_back({ 0, 226, 230, 255 });

	particleColours.emplace(ParticleTypes::PlayerTrail, colours);

	colours.clear();
	colours.push_back({ 235, 143, 30, 255 });
	colours.push_back({ 235, 62, 14, 255 });
	colours.push_back({ 255, 208, 54, 255 });
	colours.push_back({ 240, 109, 23, 255 });
	colours.push_back({ 246, 143, 35, 255 });
	colours.push_back({ 245, 162, 25, 255 });
	colours.push_back({ 252, 207, 3, 255 });
	colours.push_back({ 255, 248, 43, 255 });
	colours.push_back({ 255, 166, 0, 255 });

	particleColours.emplace(ParticleTypes::PlayerExplosion, colours);
}

int GetPoints()
{
	return points;
}

void GenerateStars()
{
	for (int l = 0; l < nStars; l++)
	{
		stars.push_back(
			{
				{
					(float)GetRandomValue(-borderBuffer, GetScreenWidth() + borderBuffer),
					(float)GetRandomValue(-borderBuffer, GetScreenHeight() + borderBuffer),
					(float)GetRandomValue(9,21) / 3.0f
				},
				WHITE
			});
	}
}

void DrawStars(const Vector2& cameraPos)
{
	for (Star& star : stars)
	{
		DrawRectanglePro(
			{ star.pos.x - cameraPos.x * star.pos.z * 0.06f, star.pos.y - cameraPos.y * star.pos.z * 0.06f, star.pos.z, star.pos.z },
			{ star.pos.z / 2.0f, star.pos.z / 2.0f },
			45,
			star.colour
		);
	}
}

void CreateLaser(Vector2 pos, float speed, float angle, int damage)
{
	lasers.push_back({ pos, GetAngledOffset(speed, angle), angle, damage });
}

void SpawnAsteroids()
{
	if (asteroidTimer->TimerDone())
	{
		// Spawn asteroids
		Vector2 playerDirection = player->GetInput();

		// If player is not moving, spawn randomly
		if (Vector2Length(playerDirection) == 0)
		{
			int amount = GetRandomValue(2, 3);
			for (int l = 0; l < amount; l++)
			{
				Vector2 asteroidSpawnPoint = Vector2Add(player->GetPos(), GetAngledOffset(900, (float)GetRandomValue(-720, 720) / 3.0f));
				asteroids.push_back(Asteroid(AsteroidTypes::Large, asteroidSpawnPoint, GetAngleTo(asteroidSpawnPoint, player->GetPos())));
			}
		}
		else
		{
			int amount = GetRandomValue(1, 2);
			for (int l = 0; l < amount; l++)
			{
				Vector2 asteroidSpawnPoint = Vector2Add(player->GetPos(), GetAngledOffset(900, GetAngleTo({ 0, 0 }, playerDirection) + GetRandomValue(-12, 12)));

				asteroids.push_back(Asteroid(AsteroidTypes::Large, asteroidSpawnPoint, GetAngleTo(asteroidSpawnPoint, player->GetPos())));
			}
		}

		double newDuration = asteroidTimer->GetDuration() * 0.98;
		if (newDuration < 0.5)
		{
			newDuration = 0.5;
		}
		asteroidTimer->ChangeDuration(newDuration);
		asteroidTimer->StartTimer();
	}
}

// Particle Creators
void CreateAsteroidParticles(Asteroid& asteroid, AsteroidTypes asteroidType)
{
	if (asteroidType == AsteroidTypes::Large)
	{
		ShakeScreen(0.2);

		std::vector <Color>& colours = particleColours[ParticleTypes::LargeAsteroid];
		int particleAmount = GetRandomValue(120, 160);

		for (int l = 0; l < particleAmount; ++l)
		{
			particles.push_back(Particle(
				Vector2Add(asteroid.GetPos(), GetAngledOffset(GetRandomValue(0, asteroid.GetRadius()), GetRandomValue(0, 360))),
				(float)GetRandomValue(asteroid.GetSpeed() + 3, asteroid.GetSpeed() + 15) / 3.0f,
				Vector2Angle({ 0,0 }, asteroid.GetMovement()) * RAD2DEG + GetRandomValue(-30, 30),
				GetRandomValue(12, 17),
				(float)GetRandomValue(20, 30) / 100.f,
				colours[GetRandomValue(0, colours.size() - 1)]
			));
		}


		int asteroidAmount = GetRandomValue(1, 3);
		for (int l = 0; l < asteroidAmount; ++l)
		{
			asteroids.push_back(Asteroid(
				AsteroidTypes::Small,
				{ Vector2Add(asteroid.GetPos(), GetAngledOffset(GetRandomValue(0, asteroid.GetRadius() * 0.8f), GetRandomValue(0, 360))) },
				GetAngleTo({ 0, 0 }, asteroid.GetMovement()) + GetRandomValue(-15, 15)
			));
		}
	}
	else if (asteroidType == AsteroidTypes::Small)
	{
		ShakeScreen(0.1);

		std::vector <Color>& colours = particleColours[ParticleTypes::SmallAsteroid];
		int particleAmount = GetRandomValue(60, 90);

		for (int l3 = 0; l3 < particleAmount; ++l3)
		{
			particles.push_back(Particle(
				Vector2Add(asteroid.GetPos(), GetAngledOffset(GetRandomValue(0, asteroid.GetRadius()), GetRandomValue(0, 360))),
				(float)GetRandomValue(asteroid.GetSpeed() + 3, asteroid.GetSpeed() + 15) / 3.0f,
				Vector2Angle({ 0,0 }, asteroid.GetMovement()) * RAD2DEG + GetRandomValue(-30, 30),
				GetRandomValue(8, 14),
				(float)GetRandomValue(30, 60) / 100.f,
				colours[GetRandomValue(0, colours.size() - 1)]
			));
		}
	}
}

void CreateLaserParticles(const Laser& laser)
{
	std::vector <Color>& colours = particleColours[ParticleTypes::Laser];
	int amount = GetRandomValue(4, 6);

	for (int l3 = 0; l3 < amount; l3++)
	{
		particles.push_back(Particle(
			Vector2Add(laser.pos, GetAngledOffset(GetRandomValue(0, 10), GetRandomValue(0, 360))),
			GetRandomValue(7, 12),
			Vector2Angle({ 0,0 }, laser.movement) * RAD2DEG + GetRandomValue(-10, 10),
			GetRandomValue(11, 16),
			(float)GetRandomValue(60, 100) / 100.f,
			colours[GetRandomValue(0, colours.size() - 1)]
		));
	}
}

void CreatePlayerTrailParticles()
{
	if (playerTrailTimer->TimerDone())
	{
		std::vector <Color>& colours = particleColours[ParticleTypes::PlayerTrail];

		int amount = GetRandomValue(1, 3);

		for (int l = 0; l < amount; ++l)
		{
			particles.push_back(Particle(
				Vector2Add(player->GetPos(), GetAngledOffset(player->GetRadius() * 0.7f, player->GetRotation() + 180)),
				GetRandomValue(4, 6),
				player->GetRotation() + 180 + GetRandomValue(-10, 10),
				GetRandomValue(9, 13),
				(float)GetRandomValue(70, 120) / 100.f,
				colours[GetRandomValue(0, colours.size() - 1)]
			));
		}

		playerTrailTimer->StartTimer();
	}
}

void CreatePlayerExplosionParticles()
{
	ShakeScreen(3.0f);

	std::vector <Color>& colours = particleColours[ParticleTypes::PlayerExplosion];

	int amount = GetRandomValue(2, 4);

	for (int l = 0; l < amount; ++l)
	{
		int particleAmount = GetRandomValue(120, 160);

		float direction = GetRandomValue(-180, 180);

		for (int l2 = 0; l2 < particleAmount; ++l2)
		{
			particles.push_back(Particle(
				Vector2Add(player->GetPos(), GetAngledOffset(GetRandomValue(0, player->GetRadius()), GetRandomValue(0, 360))),
				(float)GetRandomValue(5, 30) / 3.0f,
				direction + GetRandomValue(-30, 30),
				GetRandomValue(12, 25),
				(float)GetRandomValue(15, 25) / 100.f,
				colours[GetRandomValue(0, colours.size() - 1)]
			));
		}
	}

	int particleAmount = GetRandomValue(120, 160);

	for (int l2 = 0; l2 < particleAmount; ++l2)
	{
		particles.push_back(Particle(
			Vector2Add(player->GetPos(), GetAngledOffset(GetRandomValue(0, player->GetRadius()), GetRandomValue(0, 360))),
			(float)GetRandomValue(5, 20) / 3.0f,
			GetRandomValue(-180, 180),
			GetRandomValue(12, 19),
			(float)GetRandomValue(20, 30) / 100.f,
			colours[GetRandomValue(0, colours.size() - 1)]
		));
	}
}

void UpdateGame(float delta, Camera2D camera)
{
	MoveCamera(player->GetPos(), delta);

	// Updates
	if (player->CheckAlive())
	{
		player->Update(delta);
		CreatePlayerTrailParticles();
	}

	for (int l = 0; l < lasers.size(); ++l)
	{
		Laser& laser = lasers[l];

		laser.pos = Vector2Add(laser.pos, Vector2Multiply(laser.movement, { delta, delta }));

		if (Vector2Distance(laser.pos, player->GetPos()) > 700)
		{
			lasers.erase(lasers.begin() + l);
			--l;
		}
	}

	for (int l = 0; l < asteroids.size(); ++l)
	{
		Asteroid& asteroid = asteroids[l];

		asteroid.Update(delta);

		if (Vector2Distance(asteroid.GetPos(), player->GetPos()) > 1200)
		{
			asteroids.erase(asteroids.begin() + l);
			--l;
		}
	}

	for (int l = 0; l < particles.size(); ++l)
	{
		Particle& particle = particles[l];

		particle.Update(delta);

		if (!particle.CheckAlive())
		{
			particles.erase(particles.begin() + l);
			--l;
		}
	}

	for (Star& star : stars)
	{
		Vector2 displayPos = { star.pos.x - camera.target.x * star.pos.z * 0.06f, star.pos.y - camera.target.y * star.pos.z * 0.06f };

		if (displayPos.x < -borderBuffer)
		{
			star.pos.x += GetScreenWidth() + borderBuffer * 2;
		}
		else if (displayPos.x > GetScreenWidth() + borderBuffer)
		{
			star.pos.x -= GetScreenWidth() + borderBuffer * 2;
		}

		if (displayPos.y < -borderBuffer)
		{
			star.pos.y += GetScreenHeight() + borderBuffer * 2;
		}
		else if (displayPos.y > GetScreenHeight() + borderBuffer)
		{
			star.pos.y -= GetScreenHeight() + borderBuffer * 2;
		}
	}

	// Handle Collisions
	for (int l = 0; l < lasers.size(); ++l)
	{
		Laser& laser = lasers[l];

		for (int l2 = 0; l2 < asteroids.size(); ++l2)
		{
			Asteroid& asteroid = asteroids[l2];

			if (CheckCollisionCircles(laser.pos, 5, asteroid.GetPos(), asteroid.GetRadius()))
			{
				asteroid.Damage(laser.damage);

				if (!asteroid.CheckAlive())
				{
					AsteroidTypes asteroidType = asteroid.GetType();
					CreateAsteroidParticles(asteroid, asteroidType);

					switch (asteroidType)
					{
					case AsteroidTypes::Large:
						points += 20;
						break;
					case AsteroidTypes::Small:
						points += 5;
						break;
					}

					asteroids.erase(asteroids.begin() + l2);
					--l2;
				}

				CreateLaserParticles(laser);
				lasers.erase(lasers.begin() + l);
				--l;

				// To avoid laser hiting an asteroid after it's deleted
				break;
			}
		}
	}

	if (player->CheckAlive())
	{
		for (int l = 0; l < asteroids.size(); ++l)
		{
			Asteroid& asteroid = asteroids[l];

			if (CheckCollisionCircles(player->GetPos(), player->GetRadius(), asteroid.GetPos(), asteroid.GetRadius()))
			{
				asteroid.Damage(player->GetDamage());
				player->Damage(asteroid.GetDamage());

				if (!asteroid.CheckAlive())
				{
					AsteroidTypes asteroidType = asteroid.GetType();
					CreateAsteroidParticles(asteroid, asteroidType);


					asteroids.erase(asteroids.begin() + l);
					--l;
				}

				if (!player->CheckAlive())
				{
					playerDeathTimer->StartTimer();
					CreatePlayerExplosionParticles();
				}
			}
		}
	}
	else
	{
		if (playerDeathTimer->TimerDone())
		{
			ChangeGameState(GameStates::End);
		}
	}

	if (player->CheckAlive())
	{
		SpawnAsteroids();
	}
}

void DrawGame(Camera2D camera)
{
	BeginMode2D(camera);

	for (Asteroid& asteroid : asteroids)
	{
		asteroid.Draw();
	}

	for (Laser& laser : lasers)
	{
		laserImage->Draw(laser.pos, laser.rotation);
	}

	for (Particle& particle : particles)
	{
		particle.Draw();
	}

	if (player->CheckAlive())
	{
		player->Draw();
	}

	EndMode2D();

	// UI
	// Score
	std::string pointStr = std::to_string(points);
	int textWidth = MeasureText(pointStr.c_str(), 50);
	DrawText(pointStr.c_str(), GetScreenWidth() - textWidth - 10, 10, 50, WHITE);

	// Health bar
	DrawRectangle(10, 10, 200 + 4, 40 + 4, DARKGRAY);
	float healthRatio = (float)player->GetHealth() / 100.0f;
	DrawRectangle(12, 12, std::max(0.0f, 200.0f * healthRatio), 40, GREEN);
}

void CleanUpGame()
{
	delete player;
	delete playerTrailTimer;
	delete playerDeathTimer;

	delete laserImage;

	delete asteroidTimer;

	CleanUpAsteroidTextures();
}
