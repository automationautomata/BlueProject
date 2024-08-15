import kivy
kivy.require('1.9.0')

from kivy.uix.button import Button

global app


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

class AddRecordButton(Button):
    def __init__(self, **kwargs):
        super(AddRecordButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.disabled_background_color = app.themes[app.current_theme]['Additionally'][2]

class EditRecordButton(Button):
    def __init__(self, **kwargs):
        super(EditRecordButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]

class DeleteRecordButton(Button):
    def __init__(self, **kwargs):
        super(DeleteRecordButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]

class CardsListButton(Button):
    def __init__(self, **kwargs):
        super(CardsListButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.disabled_background_color = app.themes[app.current_theme]['Additionally'][2]

class RoomsListButton(Button):
    def __init__(self, **kwargs):
        super(RoomsListButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.disabled_background_color = app.themes[app.current_theme]['Additionally'][2]

class RightsListButton(Button):
    def __init__(self, **kwargs):
        super(RightsListButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Additionally'][2]
        self.disabled_background_color = app.themes[app.current_theme]['Additionally'][2]

class ExplorerButton(Button):
    def __init__(self, **kwargs):
        super(ExplorerButton, self).__init__(**kwargs)
        self._update()

    def _update(self, *args):
        self.color = app.themes[app.current_theme]['Text']
        self.background_color = app.themes[app.current_theme]['Base'][2]
