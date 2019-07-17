# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../deku')))
from deku.client import Client
from deku.services import Services
from deku.server import update as UpdateEndpoint
