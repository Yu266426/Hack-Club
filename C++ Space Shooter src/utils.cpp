#include "utils.h"

#include "raymath.h"

Vector2 GetAngledOffset(float offset, float direction)
{
	return Vector2Rotate({ offset,0 }, direction * DEG2RAD);
}

float GetAngleTo(const Vector2& from, const Vector2& to)
{
	Vector2 aimVector = Vector2Subtract(to, from);
	return (float)atan2(aimVector.y, aimVector.x) * RAD2DEG;
}
