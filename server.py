# import json
# import textwrap
#
# import tornado.web
#
# import tornado
# from tornado.options import define, options
# define("port", default=8001, help="Please send email to me", type=int)
#
# from src import dou
#
# class ReverseHandler(tornado.web.RequestHandler):
#     def get(self, input_word):
#         obj = {
#             "aa": '1'
#         }
#         j = json.dumps(obj)
#         print j
#         self.write(j)
#         # self.write(input_word[::-1])
#
# class WrapHandler(tornado.web.RequestHandler):
#     def post(self):
#         text = self.get_argument("text")
#         width = self.get_argument("width", 40)
#         self.write(textwrap.fill(text, width))
#
# if __name__ == "__main__":
#     tornado.options.parse_command_line()
#     app = tornado.web.Application(
#         handlers = [
#             (r"/reverse/(\w+)", ReverseHandler),
#             (r"/get_email", dou.getEmailHandler),
#             (r"/wrap", WrapHandler)
#         ]
#     )
#     http_server = tornado.httpserver.HTTPServer(app)
#     http_server.listen(options.port)
#     tornado.ioloop.IOLoop.instance().start()



import tornado.ioloop
import tornado.web


from src import dou

import tieba

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/get_email", dou.getEmailHandler),
        (r"/get_tieba_email", tieba.getTiebaEmail),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8001)
    tornado.ioloop.IOLoop.current().start()