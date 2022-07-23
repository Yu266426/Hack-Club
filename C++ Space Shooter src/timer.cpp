#include "timer.h"

#include "raylib.h"

Timer::Timer(double duration)
{
	this->duration = duration;
}

void Timer::StartTimer()
{
	startTime = GetTime();
}

bool Timer::TimerDone()
{
	return (GetTime() - startTime) > duration;
}
