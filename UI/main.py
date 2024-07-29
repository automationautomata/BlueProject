import kivy
kivy.require('1.9.0')

from kivy.app import App

from kivy.config import Config
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.widget import Widget
from kivy.uix.label import Label

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
    table_color = ListProperty([0, 0, 0, .5])
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
    header_color = ListProperty([0, 0, 0, .5])
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self.header_color[0], self.header_color[1], self.header_color[2], self.header_color[3])
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x + 1, self.y + 1),
                size=(self.width - 2, self.height - 2),
                border=(10, 10, 10, 10),
                Color=[1, 1, 1, 1])

"======================================================================================================================="

class Table(Widget):
    table_color = ListProperty([.2, .2, .2, .7])
    header_color = ListProperty([.2, .2, .7, .5])
    table_height = NumericProperty(3)
    table_width = NumericProperty(3)
    table_columns = NumericProperty(3)
    table_rows = NumericProperty(5)
    table_data = []
    cols_titles = []

    def addHeader(self, list):
        self.cols_titles = list
        self.Build()

    def addRow(self, list):
        self.table_data.insert(0, list)
        self.Build()

    def Build(self):
        self.grid.clear_widgets()
        header = 0
        while self.table_columns > header:
            text = ""
            if len(self.cols_titles) > header:
                text = self.cols_titles[header]
            h = MyLabelHeader(text=text,
                size_hint=[db_entities_columns_width[header], .25],
                header_color=self.header_color)
            print(h)
            self.grid.add_widget(h)
            header += 1

        rowCheck = 0
        while rowCheck < self.table_rows - 1:
            columnCheck = 0
            while columnCheck < self.table_columns:
                text = ""
                if len(self.table_data) > rowCheck:
                    if len(self.table_data[rowCheck]) > columnCheck:
                        text = self.table_data[rowCheck][columnCheck]

                label = MyLabelTable(text=text,
                    size_hint=[db_entities_columns_width[columnCheck], .25],
                    table_color=self.table_color)
                self.grid.add_widget(label)
                columnCheck += 1
            rowCheck += 1

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)

        with self.canvas:
            self.grid = GridLayout(cols=self.table_columns,
                rows=self.table_rows,
                size=[self.table_width, self.table_height])

        for _ in range(self.table_rows):
            for _ in range(self.table_columns):
                label = MyLabelTable(text="primary")
                self.grid.add_widget(label)

"======================================================================================================================="

class EntitiesScreen(Screen):
    pass

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

if __name__ == '__main__':
    TestApp().run()