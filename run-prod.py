from app import create_app

app = create_app()

if __name__ == '__main__':
    from gunicorn.app.base import BaseApplication

    class GunicornApp(BaseApplication):
        def __init__(self, wsgi_app, options=None):
            self.wsgi_app = wsgi_app
            self.options = options or {}
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)

        def load(self):
            return self.wsgi_app

    options = {
        'bind': '0.0.0.0:9292',
        'workers': 4,
    }
    GunicornApp(app, options).run()
