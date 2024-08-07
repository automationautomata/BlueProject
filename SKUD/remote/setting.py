
from threading import Thread
from typing import Callable
import tornado

from SKUD.remote.tools import Actions, Answer
from SKUD.remote.ui import AuthenticationHandler, QueryHandler, Websoket


def create_tornado_server(port: int, 
                          skud: Actions,
                          visits: Actions, 
                          auth: Callable[[str], Answer], 
                          isdaemon: bool = True) -> tuple[Thread, tornado.web.Application]:
    '''Создает поток, обрабатывающий запросы от десктоп приложений.
    `port` - номер сокета, skud - обрабатывает сообщения от клиента к БД СКУДа,
    `visits` - обрабатывает сообщения от клиента к БД посещений,
    `auth` - функция, производящяя аутентификацию, 
    `isdaemon` - подчиненный ли поток по отношению к главному.'''
    app = tornado.web.Application([
        (r"/", AuthenticationHandler, dict(verificator=auth)),
        (r"/ui", QueryHandler, dict(action=skud)),
        (r"/wss", Websoket, dict(actions=visits))
    ])
    
    app.listen(port)
    return Thread(target=tornado.ioloop.IOLoop.current().start, daemon=isdaemon), app
