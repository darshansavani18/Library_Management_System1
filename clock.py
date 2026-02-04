import time


def start_clock(label):
    def update():
        label.config(text=time.strftime("%I:%M:%S %p"))
        label.after(1000, update)
    update()
