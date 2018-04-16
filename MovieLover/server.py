import tornado.ioloop
import tornado.web
import Settings
import pymysql
from Handlers import *
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/signup", SignUpHandler),
            (r"/show/(\d+)",DetailHandler),
            (r"/show/(\d+)/seats",SeatsHandler),
            (r"/show/(\d+)/payment",PaymentHandler)
        ]
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            "login_url": "/login"
        }
        # Open database connection
        self.db = pymysql.connect(Settings.MYSQL_HOST,Settings.MYSQL_USER,Settings.MYSQL_PW,Settings.MYSQL_DB)
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()