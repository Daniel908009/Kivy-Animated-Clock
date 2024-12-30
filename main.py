from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.effectwidget import Rectangle
from kivy.uix.label import CoreLabel
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
import time
import math

class ColorPopup(Popup):
    def __init__(self, caller, color):
        super(ColorPopup, self).__init__()
        self.caller = caller
        self.color = color
        self.ids.forW.text = "Picking color for " + color
        if color == "main":
            self.ids.colorPicker.color = self.caller.mainColor
        elif color == "background":
            self.ids.colorPicker.color = self.caller.mainBackgroundColor
        elif color == "number":
            self.ids.colorPicker.color = self.caller.numbersColor
        elif color == "second":
            self.ids.colorPicker.color = self.caller.handColors[0]
        elif color == "minute":
            self.ids.colorPicker.color = self.caller.handColors[1]
        elif color == "hour":
            self.ids.colorPicker.color = self.caller.handColors[2]
    def save_color(self):
        if self.color == "main":
            self.caller.mainColor = (self.ids.colorPicker.color[0], self.ids.colorPicker.color[1], self.ids.colorPicker.color[2], self.ids.colorPicker.color[3])
        elif self.color == "background":
            self.caller.mainBackgroundColor = (self.ids.colorPicker.color[0], self.ids.colorPicker.color[1], self.ids.colorPicker.color[2], self.ids.colorPicker.color[3])
        elif self.color == "number":
            self.caller.numbersColor = (self.ids.colorPicker.color[0], self.ids.colorPicker.color[1], self.ids.colorPicker.color[2], self.ids.colorPicker.color[3])
        elif self.color == "second":
            self.caller.handColors[0] = (self.ids.colorPicker.color[0], self.ids.colorPicker.color[1], self.ids.colorPicker.color[2], self.ids.colorPicker.color[3])
        elif self.color == "minute":
            self.caller.handColors[1] = (self.ids.colorPicker.color[0], self.ids.colorPicker.color[1], self.ids.colorPicker.color[2], self.ids.colorPicker.color[3])
        elif self.color == "hour":
            self.caller.handColors[2] = (self.ids.colorPicker.color[0], self.ids.colorPicker.color[1], self.ids.colorPicker.color[2], self.ids.colorPicker.color[3])
        self.dismiss()

class TimerPopup(Popup):
    def __init__(self, caller):
        super(TimerPopup, self).__init__()
        self.caller = caller
    def apply(self):
        if self.ids.hours.text == "":
            self.ids.hours.text = "0"
        if self.ids.minutes.text == "":
            self.ids.minutes.text = "0"
        if self.ids.seconds.text == "":
            self.ids.seconds.text = "0"
        self.caller.destinationTime = int(self.ids.hours.text) * 3600 + int(self.ids.minutes.text) * 60 + int(self.ids.seconds.text)
        self.dismiss()

class SettingsPopup(Popup):
    def __init__(self, caller):
        super(SettingsPopup, self).__init__()
        self.caller = caller
        self.ids.typeSpinner.text = self.caller.type
        self.ids.firstUICheckBox.active = self.caller.design[0]
        self.ids.secondUICheckBox.active = self.caller.design[1]
        self.ids.thirdUICheckBox.active = self.caller.design[2]
        self.mainColor = self.caller.mainColor
        self.mainBackgroundColor = self.caller.mainBackgroundColor
        self.numbersColor = self.caller.numbersColor
        self.handColors = self.caller.handColors
        self.timeSetting()
    def save_settings(self):
        self.caller.type = self.ids.typeSpinner.text
        self.caller.design[0] = self.ids.firstUICheckBox.active
        self.caller.design[1] = self.ids.secondUICheckBox.active
        self.caller.design[2] = self.ids.thirdUICheckBox.active
        self.caller.mainColor = self.mainColor
        self.caller.mainBackgroundColor = self.mainBackgroundColor
        self.caller.handColors = self.handColors
        if self.ids.typeSpinner.text == "Timer":
            a = self.destinationTime
            if a == 0 or a == None:
                a = 1
            self.caller.time = a
        self.caller.setup()
        self.dismiss()
    def timeSetting(self):
        self.ids.timeGrid.clear_widgets()
        if self.ids.typeSpinner.text == "Clock":
            self.ids.timeGrid.add_widget(Label(text="Automatic"))
        elif self.ids.typeSpinner.text == "Timer":
            self.ids.timeGrid.add_widget(Button(text="Set Time",on_press=self.setTimer, background_color=(1, 0, 0, 1)))
        elif self.ids.typeSpinner.text == "Stopwatch":
            self.ids.timeGrid.add_widget(Label(text="None"))
    def setTimer(self, instance):
        popup = TimerPopup(self)
        popup.open()
    def pick_color(self, color):
        popup = ColorPopup(self, color)
        popup.open()
    def close(self):
        self.dismiss()

class MainGrid(FloatLayout):
    def setup(self):
        self.ids.mainLabel.text = str(self.type)
        if self.clockEvent:
            self.clockEvent.cancel()
        if self.type == "Clock":
            self.ids.startStopButton.text = "///////////"
            self.ids.startStopButton.background_color = (0, 0, 1, 1)
            self.ids.startStopButton.disabled = True
            self.clockEvent = Clock.schedule_interval(self.update, 1)
        else:
            self.ids.startStopButton.text = "Start"
            self.ids.startStopButton.background_color = (0, 1, 0, 1)
            self.ids.startStopButton.disabled = False
            if self.type != "Timer":
                self.time = 0
            self.getAngles()
            self.drawClock()
            self.drawHands()
    def startStop(self):
        if self.ids.startStopButton.text == "Start":
            self.ids.startStopButton.text = "Stop"
            self.ids.startStopButton.background_color = (1, 0, 0, 1)
            self.clockEvent = Clock.schedule_interval(self.update, 1)
        elif self.ids.startStopButton.text == "Stop":
            self.ids.startStopButton.text = "Start"
            self.ids.startStopButton.background_color = (0, 1, 0, 1)
            self.clockEvent.cancel()
    def resize(self):
        self.radius = self.size[0] / 4
        self.centerX = self.size[0] / 2
        self.centerY = self.size[1] / 2
        self.drawClock()
        self.drawHands()
    def change_type(self):
        popup = SettingsPopup(self)
        popup.open()
    def update(self, t):
        self.getTime()
        self.getAngles()
        self.drawClock()
        self.drawHands()
        if self.type == "Timer":
            if self.time <= 0:
                self.startStop()
    def getAngles(self):
        if self.type == "Clock":
            # getting the second angle
            self.secondAngle = 6 * self.time.tm_sec * -1 + 90
            # getting the minute angle
            self.minuteAngle = (6 * self.time.tm_min + self.time.tm_sec / 10 - 90) * -1
            # getting the hour angle
            self.hourAngle = (30 * self.time.tm_hour + self.time.tm_min / 2 - 90) * -1
        else:
            hours, minutes = divmod(self.time, 3600)
            minutes, seconds = divmod(minutes, 60)
            # getting the second angle
            self.secondAngle = seconds * -6 + 90
            # getting the minute angle
            self.minuteAngle = minutes * -6 + 90
            # getting the hour angle
            self.hourAngle = hours * -30 + 90
    def getTime(self):
        if self.type == "Clock":
            self.time = time.localtime()
        elif self.type == "Stopwatch":
            self.time += 1
        elif self.type == "Timer":
            self.time -= 1
    def drawClock(self):
        self.ids.canvast.canvas.clear()
        # drawing the outer clock circle
        if self.design[0]:
            self.ids.canvast.canvas.add(Color(self.mainColor[0], self.mainColor[1], self.mainColor[2],self.mainColor[3]))
            self.ids.canvast.canvas.add(Ellipse(pos=(self.centerX - self.radius, self.centerY - self.radius), size=(self.radius * 2, self.radius * 2)))
        # drawing the hour lines??? or whatever its called
        if self.design[1]:
            self.ids.canvast.canvas.add(Color(self.mainColor[0], self.mainColor[1], self.mainColor[2],self.mainColor[3]))
            for i in range(12):
                angle = math.radians(i * 30)
                x1 = self.centerX + self.radius * math.cos(angle)
                y1 = self.centerY + self.radius * math.sin(angle)
                x2 = self.centerX + (self.radius + 5) * math.cos(angle)
                y2 = self.centerY + (self.radius + 5) * math.sin(angle)
                self.ids.canvast.canvas.add(Line(points=[x1, y1, x2, y2], width=2))
        # drawing the numbers
        if self.design[2] and self.type == "Clock": # in case it is a clock
            self.drawNumHours()
        elif self.design[2]: # in case it is a timer or a stopwatch it will change the numbers dynamicaly based on the time left
            hours, minutes = divmod(self.time, 3600)
            minutes, seconds = divmod(minutes, 60)
            if hours > 0: # this will display the same thing as if its a clock
                self.drawNumHours()
            else: # this will draw increments of 5 instead of the hours
                for i in range(12):
                    num = i*5
                    num = 60 - num
                    if num == 0:
                        num = 60
                    text = CoreLabel(text=str(num), font_size=25, color=(self.numbersColor[0], self.numbersColor[1], self.numbersColor[2], self.numbersColor[3]))
                    text.refresh()
                    texture = text.texture
                    texture_size = list(texture.size)
                    x = self.centerX + (self.radius+25) * math.cos(math.radians((i+3) * 30)) - texture_size[0] / 2
                    y = self.centerY + (self.radius+25) * math.sin(math.radians((i+3) * 30)) - texture_size[1] / 2
                    self.ids.canvast.canvas.add(Rectangle(texture=texture, pos=(x, y), size=texture_size))
        # drawing the inner clock circle
        self.ids.canvast.canvas.add(Color(self.mainBackgroundColor[0], self.mainBackgroundColor[1], self.mainBackgroundColor[2],self.mainBackgroundColor[3]))
        self.ids.canvast.canvas.add(Ellipse(pos=(self.centerX - self.radius + 10, self.centerY - self.radius + 10), size=(self.radius * 2 - 20, self.radius * 2 - 20)))
    def drawNumHours(self):
        for i in range(12):
            number = i + 9
            if number > 12:
                textNumber = number - 12
            elif number == 12:
                textNumber = 0
            else:
                textNumber = number
            answer = 12 - textNumber
            text = CoreLabel(text=str(answer), font_size=25, color=(self.numbersColor[0], self.numbersColor[1], self.numbersColor[2], self.numbersColor[3]))
            text.refresh()
            texture = text.texture
            texture_size = list(texture.size)
            x = self.centerX + (self.radius+25) * math.cos(math.radians(i * 30)) - texture_size[0] / 2
            y = self.centerY + (self.radius+25) * math.sin(math.radians(i * 30)) - texture_size[1] / 2
            self.ids.canvast.canvas.add(Rectangle(texture=texture, pos=(x, y), size=texture_size))
    def drawHands(self):
        # drawing the seconds hand
        self.ids.canvast.canvas.add(Color(self.handColors[0][0], self.handColors[0][1], self.handColors[0][2],self.handColors[0][3]))
        self.ids.canvast.canvas.add(Line(points=[self.centerX, self.centerY, self.centerX + self.radius * 0.9 * math.cos(math.radians(self.secondAngle)), self.centerY + self.radius * 0.9 * math.sin(math.radians(self.secondAngle))], width=1))
        # drawing the minute hand
        self.ids.canvast.canvas.add(Color(self.handColors[1][0], self.handColors[1][1], self.handColors[1][2],self.handColors[1][3]))
        self.ids.canvast.canvas.add(Line(points=[self.centerX, self.centerY, self.centerX + self.radius * 0.8 * math.cos(math.radians(self.minuteAngle)), self.centerY + self.radius * 0.8 * math.sin(math.radians(self.minuteAngle))], width=2))
        # drawing the hour hand
        self.ids.canvast.canvas.add(Color(self.handColors[2][0], self.handColors[2][1], self.handColors[2][2],self.handColors[2][3]))
        self.ids.canvast.canvas.add(Line(points=[self.centerX, self.centerY, self.centerX + self.radius * 0.6 * math.cos(math.radians(self.hourAngle)), self.centerY + self.radius * 0.6 * math.sin(math.radians(self.hourAngle))], width=3))

class ClockApp(App):
    def build(self):
        return MainGrid()
    

if __name__ == '__main__':
    ClockApp().run()