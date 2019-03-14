# -*- coding:utf-8 -*-

import os
import webapp
import config

os.chdir(os.path.dirname(os.path.abspath(__file__)))

cfg = config.base
app = webapp.create_app(cfg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=cfg.PORT)
