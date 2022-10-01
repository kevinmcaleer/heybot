# Countdown timer

from machine import RTC

def get_time():
    t = RTC()
    year = t.datetime()[0]
    month = t.datetime()[1]
    day = t.datetime()[2]
    hour = t.datetime()[4]
    minute = t.datetime()[5] 
    second = t.datetime()[6]
    h = hour +1 #BST
    m = minute
    s = second
    
    return h, m, s

class CountDownTimer():
    hours = 0
    minutes = 0
    seconds = 0
    duration = 25 # minutes default
    alarm = False
    
    def __init__(self):
        self.start_h, self.start_m, self.start_s = get_time()
        
    def go(self):
        self.start_h, self.start_m, self.start_s = get_time()
        self.start_m + self.duration
        return f'{self.hours:02}:{self.minutes:02}:{self.seconds:02}'
        
    def isalarm(self):
        current_h, current_m, current_s = get_time()
        if self.start_h - current_h <= 0 and \
           self.start_m - current_m+self.duration <= 0 and \
           self.start_s - current_s <= 0:
            self.alarm = True
            return True
        else:
            return False
    
    def tick(self):
        current_h, current_m, current_s = get_time()
        self.hours =  current_h - self.start_h
        self.minutes = current_m - self.start_m
        self.seconds =  current_s - self.start_s
        return f'{self.hours:02}:{self.minutes:02}:{self.seconds:02}'
    
    def status(self):
        current_h, current_m, current_s = get_time()
        remaining_h = self.start_h - current_h
        remaining_m = (self.start_m + self.duration) - current_m
        remaining_s = self.start_s - current_s
        if not self.isalarm():
            print(f'Start time    : {self.start_h:02}:{self.start_m:02}:{self.start_s:02}', end='')
            print(f' | Current time  : {current_h:02}:{current_m:02}:{current_s:02}', end='')
            print(f' | Target time   : {self.start_h:02}:{self.start_m+self.duration:02}:{self.start_s:02}', end='')
            print(f' | Remaining time: {remaining_h:02}:{remaining_m:02}:{remaining_s:02}')
        return remaining_h, remaining_m, remaining_s
        
        
# t = CountDownTimer()
# t.duration = 1
# print(t.go())
# while True and not t.isalarm():
#     t.tick()
#     h, m, s = t.status()
#     
# print("ALARM!")