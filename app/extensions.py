from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

cors = CORS()
ma = Marshmallow()
migrate = Migrate()
