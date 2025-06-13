import os
from tkinter import Image, Label
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from  kivy.uix.image import Image
import requests

load_dotenv()

Window.size = (300,500) #WIDTH, HEIGHT
 
class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        
        # OPEN WEATHER API        
        API_KEY = os.getenv('API_KEY')
        CITY = "Adelaide"
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            
            print(f"Weather in {CITY}:")
            print(f"Temperature: {temperature}°C")
            print(f"Description: {description}")
            print(f"Humidity: {humidity}%")
        else:
            print("Failed to retrieve weather data:", response.status_code)

        # BOX LAYOUT WITH IMAGE & LABEL FOR WEATHER
        weather_layout = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.05)
        weather_label = Label(
            text=f"{CITY} {round(data['main']['temp'],0)}°C {data['weather'][0]['description']}",
            size_hint=(0.7,1)
        )
        weather_icon = Image(
            source='mobile-kivy\\imgs\\CMV TRUCK.png', 
            size_hint=(0.3,1)
        )
        weather_layout.add_widget(weather_icon) 
        weather_layout.add_widget(weather_label)

        # CREATE TEXT INPUT
        self.result = TextInput(
            font_size=45,
            size_hint_y=0.2,
            readonly=True,
            halign="right",
            multiline=False,
            background_color=[0.2,0.2,0.2,1],
            foreground_color=[1,1,1,1]
        )

        # ADD WIDGET TO BOXLAYOUT INHERITED IN CLASS
        self.add_widget(weather_layout)
        self.add_widget(self.result)

        # CREATE BUTTONS
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '00', '.', '='],
        ]

        grid = GridLayout(cols=4, spacing=5, padding=10)
        for row in buttons:
            for button in row:
                grid.add_widget(
                    Button(
                        text=button, 
                        font_size=25,
                        on_press=self.button_click,
                        background_color=self.button_color(button)
                        )
                )
        
        self.add_widget(grid)

    def button_color(self, label):
        if label in {'C', '+/-', '%'}:
            return [0.6,0.6,0.6,1]
        elif label in {'/', '*', '-', '+', '='}:
            return [1, 0.5, 0, 1]
        return [0.3,0.3,0.3,1]

    def button_click(self, instance):
        text = instance.text
        if text == "C":
            self.result.text = ""
        elif text == "=":
            self.calculate()
        elif text == "+/-":
            self.toggle_neg()
        elif text == "%":
            self.convert_percent()
        else:
            self.result.text += text

    def calculate(self):
        try:
            self.result.text = str(eval(self.result.text))
        except Exception:
            self.result.text = "ERROR!"

    def toggle_neg(self):
        if self.result.text:
            self.result.text = self.result.text[1:] if self.result.text[0] == "-" else "-" + self.result.text

    def convert_percent(self):
        try:
            self.result.text = str(float(self.result.text)/100)
        except ValueError:
            self.result.text = "ERROR!"

class CalculatorApp(App):
    def build(self):
        return Calculator()
    

if __name__ == "__main__":
    CalculatorApp().run()
