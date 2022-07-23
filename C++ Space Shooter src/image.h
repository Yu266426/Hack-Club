#pragma once

#include "raylib.h"

#include <string>

namespace SpaceShooter
{
	class Image
	{
	public:
		Image(std::string path, float scale);

		inline Vector2 GetSize() { return size; };

		void Draw(Vector2 pos, float rotation);
	private:
		Texture2D texture;
		Vector2 size;
		Rectangle source;
		Vector2 center;
	};
}