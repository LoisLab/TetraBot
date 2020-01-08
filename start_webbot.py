from webserver import *
from bob import *

bot = Bob()
w = WebServer(80, bot)
w.start()

