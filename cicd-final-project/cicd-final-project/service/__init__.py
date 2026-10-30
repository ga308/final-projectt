"""Counter service package."""
from flask import Flask

app = Flask(__name__)

from service import routes  # noqa: E402,F401
