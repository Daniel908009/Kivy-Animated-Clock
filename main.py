from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
import time
import math

class MainGrid(FloatLayout):
    def startStop(self):
        print("Start")
        if self.ids.startStopButton.text == "Start":
            self.ids.startStopButton.text = "Stop"
            self.ids.startStopButton.background_color = (1, 0, 0, 1)
            self.clockEvent = Clock.schedule_interval(self.update, 1)
        elif self.ids.startStopButton.text == "Stop":
            self.ids.startStopButton.text = "Start"
            self.ids.startStopButton.background_color = (0, 1, 0, 1)
            self.clockEvent.cancel()
    def resize(self):
        print("Resize")
        self.radius = self.size[0] / 4
        self.centerX = self.size[0] / 2
        self.centerY = self.size[1] / 2
        self.drawClock()
    def change_type(self):
        print("Change type")
    def update(self, t):
        self.getTime()
        self.getAngles()
        self.drawClock()
        self.drawHands()
    def getAngles(self):
        if self.type == "currentTime":
            print(self.time.tm_sec, self.time.tm_min, self.time.tm_hour)
            # getting the second angle
            self.secondAngle = 6 * self.time.tm_sec * -1 + 90
            # getting the minute angle
            self.minuteAngle = 6 * self.time.tm_min + self.time.tm_sec / 10 * -1 - 90
            # getting the hour angle
            self.hourAngle = 30 * self.time.tm_hour + self.time.tm_min / 2 * -1
        else:
            # getting the second angle
            self.secondAngle = 6 * self.time
            # getting the minute angle
            self.minuteAngle = self.time / 10
            # getting the hour angle
            self.hourAngle = self.time / 2
    def getTime(self):
        if self.type == "currentTime":
            self.time = time.localtime()
        else:
            self.time += 1
    def drawClock(self):
        self.ids.canvast.canvas.clear()
        print("Drawing Clock")
        # drawing the outer clock circle
        self.ids.canvast.canvas.add(Color(self.mainColor[0], self.mainColor[1], self.mainColor[2],self.mainColor[3]))
        self.ids.canvast.canvas.add(Ellipse(pos=(self.centerX - self.radius, self.centerY - self.radius), size=(self.radius * 2, self.radius * 2)))
        # drawing the hour lines???
        self.ids.canvast.canvas.add(Color(self.mainColor[0], self.mainColor[1], self.mainColor[2],self.mainColor[3]))
        for i in range(12):
            angle = math.radians(i * 30)
            x1 = self.centerX + self.radius * math.cos(angle)
            y1 = self.centerY + self.radius * math.sin(angle)
            x2 = self.centerX + (self.radius + 5) * math.cos(angle)
            y2 = self.centerY + (self.radius + 5) * math.sin(angle)
            self.ids.canvast.canvas.add(Line(points=[x1, y1, x2, y2], width=2))
        # drawing the inner clock circle
        self.ids.canvast.canvas.add(Color(self.mainBackgroundColor[0], self.mainBackgroundColor[1], self.mainBackgroundColor[2],self.mainBackgroundColor[3]))
        self.ids.canvast.canvas.add(Ellipse(pos=(self.centerX - self.radius + 10, self.centerY - self.radius + 10), size=(self.radius * 2 - 20, self.radius * 2 - 20)))
    def drawHands(self):
        # drawing the second hand
        self.ids.canvast.canvas.add(Color(self.handColors[0][0], self.handColors[0][1], self.handColors[0][2],self.handColors[0][3]))
        self.ids.canvast.canvas.add(Line(points=[self.centerX, self.centerY, self.centerX + self.radius * math.cos(math.radians(self.secondAngle)), self.centerY + self.radius * math.sin(math.radians(self.secondAngle))], width=1))
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