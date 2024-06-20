from src.config.celery import app


@app.task(name="test_celery_task")
def test_celery_task() -> str:
    return "Gooooooooood"
