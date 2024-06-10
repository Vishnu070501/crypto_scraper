from celery import shared_task
from .models import Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(task_id):
    task = Task.objects.get(id=task_id)
    cmc = CoinMarketCap(task.coin)
    data = cmc.scrape_data()
    if data is None:
        task.status = 'FAILED'
        data = {
            "error": "data not found"
        }
    else:
        task.status = 'COMPLETED'
    task.output = data  
    task.save()