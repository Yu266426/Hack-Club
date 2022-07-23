#pragma once

#include "raylib.h"

#include <map>
#include <vector>

Vector2 GetAngledOffset(float offset, float direction);

float GetAngleTo(const Vector2& from, const Vector2& to);