from app import create_app
from config import ProductionConfig

app = create_app()
app.config.from_object(ProductionConfig)

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 9292)
    )
