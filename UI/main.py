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

class ThemeButton(Button):
    _color = ListProperty()

    def switch_theme(self, _root, color_themes):
        print(_root.ids.keys())
        if color_themes['Current theme'] == 0:
            color_themes['Current theme'] = 1
            Window.clearcolor = (color_themes['Screen'][1][0],
                color_themes['Screen'][1][1],
                color_themes['Screen'][1][2],
                color_themes['Screen'][1][3])

            _root.ids.theme_button._color = color_themes['Theme button'][1]

            _root.ids.go_entites_screen._color = color_themes['Explorer buttons'][1]
            _root.ids.go_access_rules_screen._color = color_themes['Explorer buttons'][1]
            _root.ids.go_logs_screen._color = color_themes['Explorer buttons'][1]

            _root.ids.entities_header._color = color_themes['Table header'][1]
            _root.ids.entities_table._color = color_themes['Table content'][1]
        else:
            color_themes['Current theme'] = 0
            Window.clearcolor = (color_themes['Screen'][0][0],
                color_themes['Screen'][0][1],
                color_themes['Screen'][0][2],
                color_themes['Screen'][0][3])

            _root.ids.theme_button._color = color_themes['Theme button'][0]

            _root.ids.go_entites_screen._color = color_themes['Explorer buttons'][0]
            _root.ids.go_access_rules_screen._color = color_themes['Explorer buttons'][0]
            _root.ids.go_logs_screen._color = color_themes['Explorer buttons'][0]

            _root.ids.entities_header._color = color_themes['Table header'][0]
            _root.ids.entities_table._color = color_themes['Table content'][0]

        _root.ids.theme_button._update()
        _root.ids.go_entites_screen._update()
        _root.ids.go_access_rules_screen._update()
        _root.ids.go_logs_screen._update()
        _root.ids.entities_header._update()
        _root.ids.entities_table._update()

    def _update(self, *args):
        self.background_color = self._color
"======================================================================================================================="

class ExplorerButton(Button):
    _color = ListProperty()

    def _update(self, *args):
        self.background_color = self._color

"======================================================================================================================="

class MyLabelTable(Label):
    _color = ListProperty()
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self._color[0], self._color[1], self._color[2], self._color[3])
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x + 1, self.y + 1),
                size=(self.width - 2, self.height - 2),
                border=(10, 10, 10, 10),
                Color=[1, 1, 1, 1])

"======================================================================================================================="

class MyLabelHeader(Label):
    _color = ListProperty()
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self._color[0], self._color[1], self._color[2], self._color[3])
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(pos=(self.x + 1, self.y + 1),
                size=(self.width - 2, self.height - 2),
                border=(20, 20, 20, 20),
                Color=[1, 1, 1, 1])

"======================================================================================================================="

class TableHeader(Widget):
    _color = ListProperty()
    _height = NumericProperty(50)
    _width = NumericProperty(Window.width)
    _rows = NumericProperty(1)
    _columns = NumericProperty(6)
    _titles = ListProperty([])
    _columns_width = ListProperty([.32, .2, .12, .12, .12, .12])

    def on_size(self, *args):
        self._update(*args)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            self.grid = GridLayout(rows=self._rows,
                cols=self._columns,
                size=[self._width, self._height],
                pos=self.pos)

        for col in range(self._columns):
            label = MyLabelHeader(text=self._titles[col],
                size_hint=[self._columns_width[col], .25],
                _color=self._color)
            self.grid.add_widget(label)

"======================================================================================================================="

class TableContent(ScrollView):
    _grid = None
    _color = ListProperty()
    _height = NumericProperty(650)
    _width = NumericProperty(Window.width)
    _columns_width = ListProperty()
    table_data = ListProperty([['A', 'A', 'A', 'A', 'A', 'A'],
        ['A', 'A', 'A', 'A', 'A', 'A'],
        ['A', 'A', 'A', 'A', 'A', 'A'],
        ['A', 'A', 'A', 'A', 'A', 'A'],
        ['A', 'A', 'A', 'A', 'A', 'A'],
        ])

    def load_data(self, grid_link):
        self._grid = grid_link
        for row in range(self._rows):
            for col in range(self._columns):
                label = MyLabelTable(text=self.table_data[row][col],
                    size_hint=[self._columns_width[col], .25],
                    _color=self._color)
                self._grid.add_widget(label)

    def _update(self):
        self._grid.clear_widgets()
        for row in range(self._rows):
            for col in range(self._columns):
                label = MyLabelTable(text=self.table_data[row][col],
                    size_hint=[self._columns_width[col], .25],
                    _color=self._color)
                self._grid.add_widget(label)

"======================================================================================================================="

class Footer(Widget):
    _color = ListProperty([.25, .25, .25, .1])
    def on_size(self, *args):
        with self.canvas:
            Color(self._color[0], self._color[1], self._color[2], self._color[3])
            Rectangle(pos=(0, 0), size=(Window.width, 30))

"======================================================================================================================="

class EntitiesScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.entities_content.clear_widgets()
        self.ids.entities_table.load_data(self.ids.entities_content)

"======================================================================================================================="

class RulesScreen(Screen):
    pass

"======================================================================================================================="

class LogsScreen(Screen):
    pass

"======================================================================================================================="

class TestApp(App):
    app_color_themes = {'Current theme': 0,
                        'Screen': [[1, 1, 1, 1],
                            [0, 0, 0, 1]],
                        'Theme button': [[1, 1, 1, 1],
                            [1, 1, .5, 1]],
                        'Table header': [[1, 1, 1, 1],
                            [.25, .25, .25, 1]],
                        'Table content': [[1, 1, 1, 1],
                            [.4, .8, 1, 1]],
                        'Footer': [[1, 1, 1, 1],
                            [.25, .25, .25, .1]],
                        'Explorer buttons': [[1, 1, 1, 1],
                            [.5, .5, .8, 1]]}
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