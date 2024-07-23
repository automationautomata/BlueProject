import kivy
kivy.require('1.9.0')

from kivy.app import App

from kivy.config import Config
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import BorderImage
from kivy.graphics import Color, Line, Rectangle

from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', 'false')
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '600')
Config.write()
Builder.load_file('MyMain.kv')

class MyLabelTable(Label):
    table_color = ListProperty([0, 0, 0, 1])
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self.table_color[0], self.table_color[1], self.table_color[2], self.table_color[3])
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x + 1, self.y + 1),
                size=(self.width - 2, self.height - 2),
                border=(10, 10, 10, 10),
                Color=[1, 1, 1, 1])

"======================================================================================================================="

class MyLabelHeader(Label):
    header_color = ListProperty([0, 0, 0, 1])
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self.header_color[0], self.header_color[1], self.header_color[2], self.header_color[3])
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x + 1, self.y + 1),
                size=(self.width - 2, self.height - 2),
                border=(20, 20, 20, 20),
                Color=[1, 1, 1, 1])

"======================================================================================================================="

class TableHeader(Widget):
    _color = ListProperty([.25, .25, .25, .1])
    _height = NumericProperty(50)
    _width = NumericProperty(Window.width)
    _rows = NumericProperty(1)
    _columns = NumericProperty(6)
    _titles = ListProperty([])
    _columns_width = ListProperty([.32, .2, .12, .12, .12, .12])

    def on_size(self, *args):
        with self.canvas:
            self.grid = GridLayout(rows=self._rows,
                cols=self._columns,
                size=[self._width, self._height],
                pos=self.pos)

        for col in range(self._columns):
            label = MyLabelHeader(text=self._titles[col],
                size_hint=[self._columns_width[col], .25],
                header_color=self._color)
            self.grid.add_widget(label)

"======================================================================================================================="

class Table(ScrollView):
    _color = ListProperty([.4, .8, 1, .1])
    _height = NumericProperty(650)
    _width = NumericProperty(Window.width)
    _rows = NumericProperty(30)
    _columns = NumericProperty(6)
    _columns_width = ListProperty([.32, .2, .12, .12, .12, .12])
    table_data = ListProperty([])

    def load_data(self, grid_link):
        for _ in range(self._rows):
            for col in range(self._columns):
                label = MyLabelTable(text='Аа',
                    size_hint=[self._columns_width[col], .25],
                    table_color=self._color)
                grid_link.add_widget(label)

"======================================================================================================================="

class EntitiesScreen(Screen):
    def on_enter(self, *args):
        self.ids.entities_table.load_data(self.ids.content)

"======================================================================================================================="

class RulesScreen(Screen):
    pass

"======================================================================================================================="

class LogsScreen(Screen):
    pass

"======================================================================================================================="

class TestApp(App):
    def build(self):
        # Принять файлы с бд
        sm = ScreenManager()
        sm.add_widget(EntitiesScreen(name='entities'))
        sm.add_widget(RulesScreen(name='rules'))
        sm.add_widget(LogsScreen(name='logs'))

        return sm

    def on_pause(self):
        return True

if __name__ == '__main__':
    TestApp().run()