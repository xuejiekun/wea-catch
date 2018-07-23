# -*- coding: utf-8 -*-
from flask_script import Manager
from wea_foshan.web import create_app

app = create_app()
print(app)

manager = Manager(app)


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
