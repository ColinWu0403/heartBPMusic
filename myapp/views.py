from django.shortcuts import render
from django.http import JsonResponse
from .src.ecg import calculate_bpm

def index(request):
    return render(request, 'index.html')

def get_bpm(request):
    if request.method == 'GET':
        ecg_file_path = "data/04048"  # Replace with actual path to your ECG file
        bpm, rounded_bpm = calculate_bpm(ecg_file_path)
        
        return JsonResponse({'bpm': rounded_bpm}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)