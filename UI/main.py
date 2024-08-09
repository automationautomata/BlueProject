import kivy
kivy.require('1.9.0')

from kivy.app import App

from kivy.config import Config
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.factory import Factory

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import BorderImage, Color, Line, Rectangle

from kivy.properties import StringProperty, ListProperty, NumericProperty

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', 'false')
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '600')
Config.write()
Builder.load_file('MyMain.kv')

entities_db = [['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'] for _ in range(30)]
rules_db = [['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'] for _ in range(5)]

test = {'data': [{'card': '15',
                'isSabotagedCard': '0',
                'cardAddDate': '2024-08-08 20:29:38',
                'cardDelDate': None,
                'right': 1,
                'rightName':'admin',
                'rightAddDate': '2024-08-08 20:29:38',
                'rightDelDate': None,
                'sid': 5,
                'type': '0',
                'entityAddDate': '2024-08-08 20:29:38',
                'entityDelDate': None}],
        'error': ''}

class ThemeButton(Button):
    def __init__(self, **kwargs):
        super(ThemeButton, self).__init__(**kwargs)
        self._update()

    def switch_theme(self, _root):
        app.current_theme = (app.current_theme + 1) % len(app.themes)

        _root._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]

class DomainButton(Button):
    def __init__(self, **kwargs):
        super(DomainButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]

    def DomainWindow(self):
        pass

class SortingButton(Button):
    def __init__(self, **kwargs):
        super(SortingButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]

"======================================================================================================================="

class SortingWindow(Popup):
    def __init__(self, **kwargs):
        super(SortingWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()

"======================================================================================================================="

class ExplorerButton(Button):
    def __init__(self, **kwargs):
        super(ExplorerButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Base'][2]

"======================================================================================================================="

class MyLabelTable(Label):
    def __init__(self, **kwargs):
        super(MyLabelTable, self).__init__(**kwargs)

    def on_size(self, *args):
        self.parent_win = self.parent.parent
        self.canvas.before.clear()
        self.background_normal = ''
        self.color = app.themes[app.current_theme]['Text']
        with self.canvas.before:
            Color(*app.themes[app.current_theme]['Base'][0])
            Rectangle(pos=self.pos, size=self.size)
            Color(*app.themes[app.current_theme]['Additionally'][2])
            Rectangle(pos=(self.x + 1, self.y + 1), size=(self.width - 2, self.height - 2))

class MyLabelHeader(Label):
    def __init__(self, **kwargs):
        super(MyLabelHeader, self).__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        self.background_normal = ''
        self.color = app.themes[app.current_theme]['Text']
        with self.canvas.before:
            Color(*app.themes[app.current_theme]['Base'][0])
            Rectangle(pos=self.pos, size=self.size)
            Color(*app.themes[app.current_theme]['Additionally'][0])
            Rectangle(pos=(self.x + 1, self.y + 1), size=(self.width - 2, self.height - 2))

class TableHeader(ScrollView):
    _grid = None
    _width = NumericProperty(1740)
    _height = NumericProperty(50)
    _columns_width = ListProperty()
    _titles = ListProperty()

    def __init__(self, **kwargs):
        super(TableHeader, self).__init__(**kwargs)
        self.pos = (5, Window.height - 105)
        self.size_hint = (None, None)
        self.size = (self._width, self._height)
        self.bar_width = 0
        self.do_scroll_x = False
        self.do_scroll_y = False

    def load_data(self, *args):
        self._update()

    def _update(self, *args):
        self._grid.clear_widgets()
        for col in range(self._columns):
            label = MyLabelHeader(text=self._titles[col])
            self._grid.add_widget(label)

    def scrolling(self, dist):
        if dist == 0:
            self.scroll_x = 0
        else:
            self.scroll_x = dist[0] / (1 - dist[1])

class TableContent(ScrollView):
    _grid = None
    _header = None
    _width = NumericProperty(1740)
    _height = NumericProperty(610)
    _rows = NumericProperty()
    _columns_width = ListProperty()
    table_data = ListProperty()

    def __init__(self, **kwargs):
        super(TableContent, self).__init__(**kwargs)
        self.pos = (5, 35)
        self.size_hint = (None, None)
        self.size = (self._width, self._height)
        self.bar_width = 10
        self.scroll_type = ['bars'] # Перемещение с помощью ползунков
        self.always_overscroll = False
        self.smooth_scroll_end = 10
        self.do_scroll_x = True
        self.do_scroll_y = True

        self.bind(hbar=self.scroll_content)

    def load_data(self, data1, test):
        if test['error']:
            raise NameError(test['error'])

        data = test['data']
        for record in range(len(data)):
            row = []
            for col in self._header._titles:
                if data[record][col] is not None and str(data[record][col]):
                    row.append(str(data[record][col]))
                else:
                    row.append('-')
            self.table_data.append(row)

        for empty in range(25 - len(self.table_data)):
            self.table_data.append(' ' * len(self._header._titles))

        self._update()

    def _update(self):
        self._grid.clear_widgets()
        for row in range(self._rows):
            for col in range(self._columns):
                label = MyLabelTable(text=self.table_data[row][col])
                self._grid.add_widget(label)

    def scroll_content(self, instance, value):
        print(value)
        self._header.scrolling(value)

"======================================================================================================================="

class Footer(Widget):
    def on_size(self, *args):
        with self.canvas.before:
            Color(*app.themes[app.current_theme]['Additionally'][0])
            Rectangle(pos=(0, 0), size=(Window.width, 30))

    def _update(self):
        self.canvas.before.clear()
        self.canvas.before.add(Color(*app.themes[app.current_theme]['Additionally'][0]))
        self.canvas.before.add(Rectangle(pos=(0, 0), size=(Window.width, 30)))

"======================================================================================================================="

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.ids.entities_table.load_data(entities_db, test)
        self.ids.entities_header.load_data()
        self.ids.access_rules_table.load_data(rules_db, {'data': [], 'error': ''})
        self.ids.access_rules_header.load_data()

    def _update(self):
        Window.clearcolor = app.themes[app.current_theme]['Base'][0]
        self.ids.theme_button._update()
        self.ids.domain_button._update()
        self.ids.sorting_button._update()
        self.ids.go_entites_screen._update()
        self.ids.go_access_rules_screen._update()
        self.ids.go_logs_screen._update()
        self.ids.footer._update()
        self.ids.entities_header._update()
        self.ids.entities_table._update()
        self.ids.access_rules_header._update()
        self.ids.access_rules_table._update()

class EntitiesScreen(Screen):
    def __init__(self, **kwargs):
        super(EntitiesScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        Window.clearcolor = app.themes[app.current_theme]['Base'][0]

class RulesScreen(Screen):
    pass

class LogsScreen(Screen):
    pass

"======================================================================================================================="

class TestApp(App):
    def __init__(self, **kwargs):
        App.__init__(self)
        self.current_theme = 0
        self.themes = [
                {
                    'Base': [[0, .01, .2], [.1, .1, .5], [.2, .2, .5]],
                    'Additionally': [[.01, .3, .3], [.05, .4, .3], [.2, .35, .3], [.007, .25, .25]],
                    'Accent': [[.9, .05, .3], [.9, .3, .5], [.65, .05, .2]],
                    'Text': [1, 1, 1]
                },
                {
                    'Base': [[.85, .9, 1], [.75, .8, .9], [.75, .75, .9]],
                    'Additionally': [[.85, .6, .8], [.75, .5, .7], [.85, .7, .85], [.8, .55, .75]],
                    'Accent': [[.9, .8, .05], [.8, .7, .01], [.9, .8, .3]],
                    'Text': [0, 0, 0]
                },
                {
                    'Base': [[.15, .1, 0], [.15, .15, .05], [.3, .15, 0]],
                    'Additionally': [[.35, .25, .05], [.4, .3, .15], [.5, .4, .3], [.3, .2, .01]],
                    'Accent': [[.05, .04, .03], [.25, .25, .25], [.97, .96, .95]],
                    'Text': [1, 1, 1]
                },
                {
                    'Base': [[.8, .8, .8], [.95, .95, .95], [.65, .65, .65]],
                    'Additionally': [[.1, .45, .1], [.15, .4, .15], [.35, .55, .35], [.05, .4, .05]],
                    'Accent': [[0, 0, .6], [.1, .1, .7], [.25, .25, .8]],
                    'Text': [0, 0, 0]
                }]
        global app
        app = self

    def build(self):
        # Принять файлы с бд
        ms = MainScreen()

        return ms

if __name__ == '__main__':
    TestApp().run()