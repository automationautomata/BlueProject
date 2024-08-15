import kivy
kivy.require('1.9.0')

from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

from kivy.properties import StringProperty, ListProperty, NumericProperty

global app


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

class TableHeader(ScrollView):
    _grid = None
    _width = NumericProperty(1740)
    _height = NumericProperty(50)
    _columns_width = ListProperty()
    _data_titles = ListProperty()

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
            label = MyLabelHeader(text=self._data_titles[col])
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
            for col in self._header._data_keys:
                if data[record][col] is not None and str(data[record][col]):
                    row.append(str(data[record][col]))
                else:
                    row.append('-')
            self.table_data.append(row)

        for empty in range(25 - len(self.table_data)):
            self.table_data.append(' ' * len(self._header._data_keys))

        self._update()

    def _update(self):
        self._grid.clear_widgets()
        for row in range(self._rows):
            for col in range(self._columns):
                label = MyLabelTable(text=self.table_data[row][col])
                self._grid.add_widget(label)

    def scroll_content(self, instance, value):
        self._header.scrolling(value)
