import kivy
kivy.require('1.9.0')

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle

from kivy.properties import StringProperty, ListProperty, NumericProperty

global app


class Tooltip(Label):
    def __init__(self, **kwargs):
        super(Tooltip, self).__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        self.pos = (1137.5, 600 - self.texture_size[1])
        self.size_hint = (None, None)
        self.size = self.texture_size
        self.valign = 'top'
        self.halign = 'left'
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=self.size, pos=self.pos)

class TipButton(Button):
    tooltip = None

    def __init__(self, tip_text, **kwargs):
        self.tooltip = Tooltip(text=tip_text)
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(TipButton, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        Clock.unschedule(self.display_tooltip)
        self.close_tooltip()
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip, 1)

    def close_tooltip(self, *args):
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args):
        Window.add_widget(self.tooltip)


class DomainWindow(Popup):
    def __init__(self, **kwargs):
        super(DomainWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()

class SortingWindow(Popup):
    def __init__(self, **kwargs):
        super(SortingWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()

class AddRecordWindow(Popup):
    _result = {}

    def __init__(self, **kwargs):
        super(AddRecordWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]

        self.open()

    def on_open(self):
        self.add_menu(self)

    def add_menu(self, instance):
        self._result = {}
        self.ids.main_area.clear_widgets()

        if app.root.ids.screen_manager.current == 'entities':
            self._result['add_card_button'] = Button(text='Add card',
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                pos=(self.width / 2 - 85, 225),
                size_hint=(None, None),
                size=(150, 50),
                on_release=self.add_card)
            self._result['linking_card_button'] = Button(text='Linking card',
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                pos=(self.width / 2 - 85, 125),
                size_hint=(None, None),
                size=(150, 50),
                on_release=self.linking_card)

        elif app.root.ids.screen_manager.current == 'rules':
            self._result['add_room_button'] = Button(text='Add room',
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                pos=(self.width / 2 - 85, 275),
                size_hint=(None, None),
                size=(150, 50),
                on_release=self.add_room)
            self._result['add_right_button'] = Button(text='Add right',
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                pos=(self.width / 2 - 85, 175),
                size_hint=(None, None),
                size=(150, 50),
                on_release=self.add_right)
            self._result['add_rule_button'] = Button(text='Add rule',
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                pos=(self.width / 2 - 85, 75),
                size_hint=(None, None),
                size=(150, 50),
                on_release=self.add_rule)

        self._result['cancel_button'] = Button(text='Cancel',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 130, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['cancel_button'].bind(on_release=self.cancel_dismiss)

        for el in self._result.values():
            self.ids.main_area.add_widget(el)

    def add_card(self, instance):
        self._result = {}
        self.ids.main_area.clear_widgets()

        self._result['card_label'] = Label(text='Card number',
            pos=(25, self.height - 125),
            size_hint=(None, None),
            size=(445, 15))
        self._result['card_result'] = TextInput(text='',
            cursor_color=app.themes[app.current_theme]['Additionally'][2],
            multiline=False,
            pos=(25, self.height - 175),
            size_hint=(None, None),
            size=(445, 35))

        self._result['confirm_button'] = Button(text='Confirm',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 130, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['confirm_button'].bind(on_release=lambda *args: self.confirm_dismiss(type='card', *args))
        self._result['cancel_button'] = Button(text='Cancel',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 240, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['cancel_button'].bind(on_release=self.cancel_dismiss)
        self._result['back_button'] = Button(text='<-',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(0, 0),
            size_hint=(None, None),
            size=(35, 35))
        self._result['back_button'].bind(on_release=self.add_menu)

        for el in self._result.values():
            self.ids.main_area.add_widget(el)

    def linking_card(self, instance):
        self._result = {}
        self.ids.main_area.clear_widgets()

        self._result['card_label'] = Label(text='Card number',
            pos=(25, self.height - 125),
            size_hint=(None, None),
            size=(200, 15))
        self._result['card_result'] = TextInput(text='',
            cursor_color=app.themes[app.current_theme]['Additionally'][2],
            multiline=False,
            pos=(25, self.height - 175),
            size_hint=(None, None),
            size=(200, 35))
        self._result['sid_label'] = Label(text='sid',
            pos=(25, self.height - 225),
            size_hint=(None, None),
            size=(200, 15))
        self._result['sid_result'] = TextInput(text='',
            cursor_color=app.themes[app.current_theme]['Additionally'][2],
            multiline=False,
            pos=(25, self.height - 275),
            size_hint=(None, None),
            size=(200, 35))
        self._result['type_label'] = Label(text='Type',
            pos=(250, self.height - 125),
            size_hint=(None, None),
            size=(100, 15))
        type_dropdown = DropDown()
        choice_btn_1 = Button(text='User',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            size_hint_y=None,
            height=35)
        choice_btn_1.bind(on_release=lambda choice_btn_1: type_dropdown.select(choice_btn_1.text))
        type_dropdown.add_widget(choice_btn_1)
        choice_btn_2 = Button(text='Group',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            size_hint_y=None,
            height=35)
        choice_btn_2.bind(on_release=lambda choice_btn_2: type_dropdown.select(choice_btn_2.text))
        type_dropdown.add_widget(choice_btn_2)
        self._result['type_result'] = Button(text='Choose...',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            border=[10, 10, 10, 10],
            pos=(250, self.height - 175),
            size_hint=(None, None),
            size=(100, 35))
        self._result['type_result'].bind(on_release=type_dropdown.open)
        type_dropdown.bind(on_select=lambda instance, x: setattr(self._result['type_result'], 'text', x))
        self._result['right_label'] = Label(text='Right',
            pos=(375, self.height - 125),
            size_hint=(None, None),
            size=(100, 15))
        right_dropdown = DropDown()
        # Запрос: список всех прав из бд
        list_of_right = ['right_1aaaaaaaaaaaaaaaaaaaa', 'right_2', 'right_3', 'right_4', 'right_5']

        for right in list_of_right:
            btn = TipButton(text=right,
                tip_text=right,
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                size_hint_y=None,
                height=35,
                text_size=(100, 35),
                valign='center',
                halign='center',
                shorten=True,
                shorten_from='right',
                split_str='')
            btn.bind(on_release=lambda btn: right_dropdown.select(btn.text))
            right_dropdown.add_widget(btn)
        self._result['right_result'] = Button(text='Choose...',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(375, self.height - 175),
            size_hint=(None, None),
            size=(100, 35))
        self._result['right_result'].bind(on_release=right_dropdown.open)
        right_dropdown.bind(on_select=lambda instance, x: setattr(self._result['right_result'], 'text', x))

        self._result['confirm_button'] = Button(text='Confirm',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 130, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['confirm_button'].bind(on_release=lambda *args: self.confirm_dismiss(type='link', *args))
        self._result['cancel_button'] = Button(text='Cancel',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 240, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['cancel_button'].bind(on_release=self.cancel_dismiss)
        self._result['back_button'] = Button(text='<-',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(0, 0),
            size_hint=(None, None),
            size=(35, 35))
        self._result['back_button'].bind(on_release=self.add_menu)

        for el in self._result.values():
            self.ids.main_area.add_widget(el)

    def add_room(self, instance):
        self._result = {}
        self.ids.main_area.clear_widgets()

        self._result['room_name_label'] = Label(text='Room name',
            pos=(25, self.height - 125),
            size_hint=(None, None),
            size=(445, 15))
        self._result['room_name_result'] = TextInput(text='',
            cursor_color=app.themes[app.current_theme]['Additionally'][2],
            multiline=False,
            pos=(25, self.height - 175),
            size_hint=(None, None),
            size=(445, 35))

        self._result['confirm_button'] = Button(text='Confirm',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 130, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['confirm_button'].bind(on_release=lambda *args: self.confirm_dismiss(type='room', *args))
        self._result['cancel_button'] = Button(text='Cancel',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 240, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['cancel_button'].bind(on_release=self.cancel_dismiss)
        self._result['back_button'] = Button(text='<-',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(0, 0),
            size_hint=(None, None),
            size=(35, 35))
        self._result['back_button'].bind(on_release=self.add_menu)

        for el in self._result.values():
            self.ids.main_area.add_widget(el)

    def add_right(self, instance):
        self._result = {}
        self.ids.main_area.clear_widgets()

        self._result['right_name_label'] = Label(text='Right name',
            pos=(25, self.height - 125),
            size_hint=(None, None),
            size=(445, 15))
        self._result['right_name_result'] = TextInput(text='',
            cursor_color=app.themes[app.current_theme]['Additionally'][2],
            multiline=False,
            pos=(25, self.height - 175),
            size_hint=(None, None),
            size=(445, 35))

        self._result['confirm_button'] = Button(text='Confirm',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 130, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['confirm_button'].bind(on_release=lambda *args: self.confirm_dismiss(type='right', *args))
        self._result['cancel_button'] = Button(text='Cancel',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 240, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['cancel_button'].bind(on_release=self.cancel_dismiss)
        self._result['back_button'] = Button(text='<-',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(0, 0),
            size_hint=(None, None),
            size=(35, 35))
        self._result['back_button'].bind(on_release=self.add_menu)

        for el in self._result.values():
            self.ids.main_area.add_widget(el)

    def add_rule(self, instance):
        self._result = {}
        self.ids.main_area.clear_widgets()


        self._result['room_label'] = Label(text='Room',
            pos=(25, self.height - 125),
            size_hint=(None, None),
            size=(200, 15))
        room_dropdown = DropDown()


        # Запрос: список всех комнат из бд
        list_of_room = ['room_1', 'room_2', 'room_3', 'room_4', 'room_5']

        for room in list_of_room:
            btn = TipButton(text=room,
                tip_text=room,
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                size_hint_y=None,
                height=35,
                text_size=(100, 35),
                valign='center',
                halign='center',
                shorten=True,
                shorten_from='right',
                split_str='')
            btn.bind(on_release=lambda btn: room_dropdown.select(btn.text))
            room_dropdown.add_widget(btn)
        self._result['room_result'] = Button(text='Choose...',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(25, self.height - 175),
            size_hint=(None, None),
            size=(200, 35))
        self._result['room_result'].bind(on_release=room_dropdown.open)
        room_dropdown.bind(on_select=lambda instance, x: setattr(self._result['room_result'], 'text', x))


        self._result['right_label'] = Label(text='Right',
            pos=(270, self.height - 125),
            size_hint=(None, None),
            size=(200, 15))
        right_dropdown = DropDown()
        # Запрос: список всех прав из бд
        list_of_right = ['right_1', 'right_2', 'right_3', 'right_4', 'right_5']

        for right in list_of_right:
            btn = TipButton(text=right,
                tip_text=right,
                background_normal='',
                background_color=app.themes[app.current_theme]['Additionally'][0],
                size_hint_y=None,
                height=35,
                text_size=(100, 35),
                valign='center',
                halign='center',
                shorten=True,
                shorten_from='right',
                split_str='')
            btn.bind(on_release=lambda btn: right_dropdown.select(btn.text))
            right_dropdown.add_widget(btn)
        self._result['right_result'] = Button(text='Choose...',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(270, self.height - 175),
            size_hint=(None, None),
            size=(200, 35))
        self._result['right_result'].bind(on_release=right_dropdown.open)
        right_dropdown.bind(on_select=lambda instance, x: setattr(self._result['right_result'], 'text', x))

        self._result['confirm_button'] = Button(text='Confirm',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 130, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['confirm_button'].bind(on_release=lambda *args: self.confirm_dismiss(type='right', *args))
        self._result['cancel_button'] = Button(text='Cancel',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(self.width - 240, 0),
            size_hint=(None, None),
            size=(100, 35))
        self._result['cancel_button'].bind(on_release=self.cancel_dismiss)
        self._result['back_button'] = Button(text='<-',
            background_normal='',
            background_color=app.themes[app.current_theme]['Additionally'][0],
            pos=(0, 0),
            size_hint=(None, None),
            size=(35, 35))
        self._result['back_button'].bind(on_release=self.add_menu)

        for el in self._result.values():
            self.ids.main_area.add_widget(el)

    def confirm_dismiss(self, instance, type):
        res = {}
        if type == 'card':
            # Запрос: проверка существования карты в бд
            res['number'] = self._result['card_result'].text
        print(res)
        print('Confirm')
        self.dismiss()

    def cancel_dismiss(self, instance):
        print('Cancel')
        self.dismiss()

class EditRecordWindow(Popup):
    def __init__(self, **kwargs):
        super(EditRecordWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()
        
class DeleteRecordWindow(Popup):
    def __init__(self, **kwargs):
        super(DeleteRecordWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()

class CardsListWindow(Popup):
    def __init__(self, **kwargs):
        super(CardsListWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()
       
class RoomsListWindow(Popup):
    def __init__(self, **kwargs):
        super(RoomsListWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open()

class RightsListWindow(Popup):
    def __init__(self, **kwargs):
        super(RightsListWindow, self).__init__(**kwargs)

    def open_win(self):
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.separator_color = app.themes[app.current_theme]['Base'][0]
        self.open() 