import json
from multiprocessing import Process
import os
import subprocess
import time
import click

from controllers.auth_controller import AuthenticationController
from controllers.access_controller import AccessController
from controllers.ui_controller import SkudQueryHandler, UiController

from remote.server import create_tornado_server
from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger

from general.config import (ARDUINO_PORTS, ROOM_PORT_MAP, URL, 
                            DB_DIR, BACKUP_DIR,
                            SKUD_SCRIPT_PATH, SKUD_DB_NAME, 
                            VISITS_SCRIPT_PATH, VISITS_DB_NAME)

@click.group(chain=True)
def cli(): pass


@cli.command(name="clear")
@click.argument("name", type=str)
def clear_user(name): 
    '''Удаляет БД и бекапы пользователя с name'''
    try:
        click.echo()
        click.echo("Are you sure ? (Yes/No)", end=" ")
        if input().replace(" ", "") != "Yes":
            os.remove(f"{DB_DIR}\\{name}")
            os.remove(f"{BACKUP_DIR}\\{name}")
        click.echo()
    except BaseException as error:
        click.echo(f"\nERROR: {error}\n")



@cli.command(name="show-users")
def show_users():
    '''Выводит всех пользователей'''
    try:
        backups = os.listdir(BACKUP_DIR)
        click.echo(' '.join(user if user in backups else "\033[4m" + user + "\033[0m" for user in os.listdir(DB_DIR)))
        click.echo()
        click.echo("Users without backup was underlined")
    except BaseException as error:
        click.echo(f"\nERROR: {error}\n")

def skud(settings, name):
    # Запуск и настройка работы ардуино

    skud_db = DatabaseConnection(name=f"{name}-{SKUD_DB_NAME}", dirpath=f"{DB_DIR}\\{name}\\", 
                                scriptpath=SKUD_SCRIPT_PATH, backup_path=f"{BACKUP_DIR}\\{name}\\")

    visits_db = VisitLogger(name=f"{name}-{VISITS_DB_NAME}", dirpath=f"{DB_DIR}\\{name}", 

                            scriptpath=VISITS_SCRIPT_PATH, backup_path=f"{BACKUP_DIR}\\{name}\\")

    ac = AccessController(skud=skud_db, ports=ARDUINO_PORTS,
                        visits_db=visits_db, isdaemon=False)

    ac.start(settings["ROOM_PORT_MAP"])
    time.sleep(2)


    if True:
        click.echo('\n'.join(visits_db.execute_query("SELECT * FROM sqlite_temp_master;")))
        click.echo('\n'.join(visits_db.execute_query("SELECT * FROM visits_history;")))

    # Запуск и нстройка работы сервера

    ui_controller = UiController(skud_db=skud_db)
    auth_constroller = AuthenticationController(0, visits_db, skud_db)

    router = [(r"\\ui", SkudQueryHandler, ui_controller)]
    t, _ = create_tornado_server(settings["PORT"], router, auth=auth_constroller.authenticatior, isdaemon=False)

    t.start()
    print("sss")


@cli.command(name="create")
@click.argument("name", nargs=1, type=str)
@click.argument("settings_path", nargs=1,
    type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.option("--debug", "-d", type=bool,
    help="Вывод дополнительной инфоррмации на экран.",
    is_flag=True, flag_value=True
)
def create(name, settings_path, debug):
    '''Запустить СКУД с названием name или создать с его, если он не существует \n
        settings_path - путь к файлу с настройками СКУДа, \n
        debug - Вывод дополнительной инфоррмации на экран.'''
    if not settings_path: return

    keys = {"ROOM_PORT_MAP", "PORT"} 
    try:
        with open(settings_path, mode="r+", encoding="utf8") as file:
            settings: dict = json.loads(file.read())
        if settings.keys() == keys:
            click.echo("Settings error")
            click.echo("Settings contains incorrect keys")
            click.echo("The system has not been created")
            return
        with open(os.path.join(os.getcwd(), "global-settings.json"), "w+") as file:
            globals_settings = json.loads(file.read())
            globals_settings[name] = settings
            file.write(json.dumps(globals_settings))

    except BaseException as error:
        click.echo("Settings error")
        click.echo(error)
        click.echo("The system has not been created")

    

@cli.command(name="start")
@click.argument("names", required=False, multiple=True, type=str)
@click.option("--all", type=bool, help="Для всех пользователей.",
    is_flag=True, flag_value=True
)
def start(names="", all=False):
    try:
        if names == "": 
            click.echo("Empty list of users.")
            return
        else:
            enabled = names.split('\n')

        if all:
            with open(os.path.join(os.getcwd(), "global-settings.json"), "w+") as file:
                globals_settings: dict = json.loads(file.read())
                enabled = globals_settings.keys()

        click.echo(enabled)
        with open(os.path.join(os.getcwd(), "enabled"), "w+") as file:
            file.write('\n'.join(names))

        from systemd_service import Service
        daemon = Service("skud-service")
        try: daemon.enable()
        except: pass
        daemon.restart()
    except BaseException as error:
        click.echo("Start error")
        click.echo(error)
        click.echo("The system has not been started")

##### Wiegand ######

if __name__ == '__main__':
    cli()