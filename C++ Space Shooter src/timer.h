#pragma once

class Timer
{
public:
	Timer(double duration);

	inline double GetDuration() { return duration; };
	inline void ChangeDuration(double newDuration) { duration = newDuration; };

	void StartTimer();
	bool TimerDone();
private:
	double duration;
	double startTime = 0;
};