from client import Client
import time
from threading import Thread

c1 = Client('Adebowale')
time.sleep(1)
c2 = Client('Adewumi')


def update_messages():
    messages = []
    running = True
    while running:
        time.sleep(0.1)  # update every 0.1 sec
        new_messages = c1.get_messages()
        messages.extend(new_messages)

        for msg in new_messages:
            print(msg)

            if msg == "{quit}":
                running = False
                break


Thread(target=update_messages).start()

c1.send('Hello :)')
time.sleep(2)
c2.send('Hi!')
time.sleep(2)
c1.send('How have you been?!')
time.sleep(2)
c2.send('Bro, great!')
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()
