#include "image.h"

namespace SpaceShooter
{
	Image::Image(std::string path, float scale)
	{
		texture = LoadTexture(path.c_str());
		size = { (float)texture.width * scale, (float)texture.height * scale };
		source = { 0,0, (float)texture.width,(float)texture.height };
		center = { size.x / 2.0f, size.y / 2.0f };
	}

	void Image::Draw(Vector2 pos, float rotation)
	{
		DrawTexturePro(texture, source, { pos.x, pos.y, size.x, size.y }, center, rotation, WHITE);
	}
}