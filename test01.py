from heybot import Heybot

hey = Heybot()

hey.name = "Mertle"


while True:
    hey.set_timer(25) # set the timer for 25 minutes

    while not hey.timeup():
        hey.tick()

    hey.alert("time is up!, press head to reset for another 25")