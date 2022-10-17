from pynput import mouse


class Counter:
    counter = {"left": ['левую кнопку', 0],
               "right": ['правую кнопку', 0],
               "middle": ['среднюю кнопку (колёсико)', 0],
               "x1": ['первую боковую кнопку', 0],
               "x2": ['вторую боковую кнопку', 0]}
    log = ''

    @staticmethod
    def on_click(x, y, button, pressed):
        if not pressed:  # the count of clicks after releasing the button
            Counter.counter[button.name][1] += 1
            Counter.log = f'Количество нажатий на {Counter.counter[button.name][0]}: {Counter.counter[button.name][1]}'

    @staticmethod
    def counting_clicks():
        listener = mouse.Listener(
            on_click=Counter.on_click)
        listener.start()
