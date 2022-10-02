from countdowntimer import CountDownTimer

t = CountDownTimer()

t.duration_in_seconds = 10

while not t.isalarm():
    t.status()