import kivy
kivy.require('1.9.0')

from kivy.core.window import Window

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from kivy.graphics import BorderImage, Color, Line, Rectangle

global app

entities_db = [['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'] for _ in range(30)]
rules_db = [['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'] for _ in range(5)]

test = {'data': [{'card': '15',
                'isSabotagedCard': '0',
                'cardAddDate': '2024-08-08 20:29:38',
                'cardDelDate': None,
                'right': 1,
                'rightName': 'admin',
                'rightAddDate': '2024-08-08 20:29:38',
                'rightDelDate': None,
                'sid': 5,
                'type': '0',
                'entityAddDate': '2024-08-08 20:29:38',
                'entityDelDate': None}],
        'error': ''}

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
        self.ids.add_order_button._update()
        self.ids.edit_order_button._update()
        self.ids.delete_order_button._update()
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



class Footer(Widget):
    def on_size(self, *args):
        with self.canvas.before:
            Color(*app.themes[app.current_theme]['Additionally'][0])
            Rectangle(pos=(0, 0), size=(Window.width, 30))

    def _update(self):
        self.canvas.before.clear()
        self.canvas.before.add(Color(*app.themes[app.current_theme]['Additionally'][0]))
        self.canvas.before.add(Rectangle(pos=(0, 0), size=(Window.width, 30)))
