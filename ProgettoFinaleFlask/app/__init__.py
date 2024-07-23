from flask import Flask

app = Flask(__name__)
app.secret_key = "99,345èè}0-abc.662pl"


from . import routes
from . import models


