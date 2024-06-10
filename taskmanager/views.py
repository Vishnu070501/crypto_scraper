# taskmanager/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import StartScrapingSerializer
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request):
        serializer = StartScrapingSerializer(data=request.data)
        if serializer.is_valid():
            job = Job.objects.create()
            coins = serializer.validated_data['coins']
            
            for coin in coins:
                task = Task.objects.create(job=job, coin=coin)
                scrape_coin_data.delay(task.id)
            
            return Response({"job_id": str(job.id)}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            tasks = job.tasks.all()
            task_data = []
            for task in tasks:
                task_data.append({
                    "coin": task.coin,
                    "output": task.output,
                    "status": task.status
                })
            return Response({"job_id": str(job.id), "tasks": task_data}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
