from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from fractions import Fraction

class FractionCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super(FractionCalculator, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.fraction1_input = TextInput(hint_text='Fraction 1 (e.g., 3/4)', multiline=False, font_size=48)
        self.add_widget(self.fraction1_input)

        self.fraction2_input = TextInput(hint_text='Fraction 2 (e.g., 5/6)', multiline=False, font_size=48)
        self.add_widget(self.fraction2_input)

        self.result = Label(text='Result: ', font_size= 48)
        self.add_widget(self.result)

        self.add_button = Button(text='Add')
        self.add_button.bind(on_press=self.add_fractions)
        self.add_widget(self.add_button)

        self.subtract_button = Button(text='Subtract')
        self.subtract_button.bind(on_press=self.subtract_fractions)
        self.add_widget(self.subtract_button)

        self.multiply_button = Button(text='Multiply')
        self.multiply_button.bind(on_press=self.multiply_fractions)
        self.add_widget(self.multiply_button)

        self.divide_button = Button(text='Divide')
        self.divide_button.bind(on_press=self.divide_fractions)
        self.add_widget(self.divide_button)

    def parse_fraction(self, fraction_str):
        numerator, denominator = map(int, fraction_str.split('/'))
        return Fraction(numerator, denominator)

    def add_fractions(self, instance):
        fraction1 = self.parse_fraction(self.fraction1_input.text)
        fraction2 = self.parse_fraction(self.fraction2_input.text)
        result = fraction1 + fraction2
        self.result.text = f'Result: {result}'

    def subtract_fractions(self, instance):
        fraction1 = self.parse_fraction(self.fraction1_input.text)
        fraction2 = self.parse_fraction(self.fraction2_input.text)
        result = fraction1 - fraction2
        self.result.text = f'Result: {result}'

    def multiply_fractions(self, instance):
        fraction1 = self.parse_fraction(self.fraction1_input.text)
        fraction2 = self.parse_fraction(self.fraction2_input.text)
        result = fraction1 * fraction2
        self.result.text = f'Result: {result}'

    def divide_fractions(self, instance):
        fraction1 = self.parse_fraction(self.fraction1_input.text)
        fraction2 = self.parse_fraction(self.fraction2_input.text)
        result = fraction1 / fraction2
        self.result.text = f'Result: {result}'

class FractionCalculatorApp(App):
    def build(self):
        return FractionCalculator()

if __name__ == '__main__':
    FractionCalculatorApp().run()
