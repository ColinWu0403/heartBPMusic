import uuid
from django.shortcuts import render
from django.http import JsonResponse
from .src.ecg import calculate_bpm
from .models import SongRequestFeatures

def index(request):
    return render(request, 'index.html')

def get_bpm(request):
    if request.method == 'GET':
        ecg_file_path = "signals/04048"  # Replace with actual path to your ECG file
        # bpm, rounded_bpm = calculate_bpm(ecg_file_path)
        rounded_bpm = 120

        # Store the BPM value in session for future use
        unique_id = str(uuid.uuid4())
        request.session['id'] = unique_id
        request.session['bpm'] = rounded_bpm

        SongRequestFeatures.objects.create(
            id=unique_id,
            bpm=rounded_bpm,
            acousticness=0.0,
            danceability=0.0,
            energy=0.0,
            instrumentalness=0.0,
            liveness=0.0,
            loudness=0.0,
            speechiness=0.0,
            mode=0,
            valence=0.0
        )

        return JsonResponse({'bpm': rounded_bpm, 'id': unique_id}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_bpm_from_session(request):
    if request.method == 'GET':
        bpm = request.session.get('bpm')
        if bpm:
            return JsonResponse({'bpm': bpm}, status=200)
        else:
            return JsonResponse({'error': 'BPM not found in session'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def submit_questions(request):
    if request.method == 'POST':
        data = request.POST
        bpm = request.session.get('bpm')  # Retrieve BPM from session

        if bpm:
            request.session['acousticness'] = data.get('acousticness', 0.0)
            request.session['danceability'] = data.get('danceability', 0.0)
            request.session['energy'] = data.get('energy', 0.0)
            request.session['instrumentalness'] = data.get('instrumentalness', 0.0)
            request.session['liveness'] = data.get('liveness', 0.0)
            request.session['loudness'] = data.get('loudness', 0.0)
            request.session['speechiness'] = data.get('speechiness', 0.0)
            request.session['mode'] = data.get('mode', 0)
            request.session['valence'] = data.get('valence', 0.0)

            # Update SongRequestFeatures entry with additional data
            unique_id = request.session.get('id')
            if unique_id:
                song_request = SongRequestFeatures.objects.get(id=unique_id)
                song_request.acousticness = request.session['acousticness']
                song_request.danceability = request.session['danceability']
                song_request.energy = request.session['energy']
                song_request.instrumentalness = request.session['instrumentalness']
                song_request.liveness = request.session['liveness']
                song_request.loudness = request.session['loudness']
                song_request.speechiness = request.session['speechiness']
                song_request.mode = request.session['mode']
                song_request.valence = request.session['valence']
                song_request.save()

                # Return the updated session data
                return JsonResponse({
                    'bpm': bpm,
                    'acousticness': request.session['acousticness'],
                    'danceability': request.session['danceability'],
                    'energy': request.session['energy'],
                    'instrumentalness': request.session['instrumentalness'],
                    'liveness': request.session['liveness'],
                    'loudness': request.session['loudness'],
                    'speechiness': request.session['speechiness'],
                    'mode': request.session['mode'],
                    'valence': request.session['valence'],
                    # Add other fields
                }, status=200)
            else:
                return JsonResponse({'error': 'Session ID not found'}, status=400)

        else:
            return JsonResponse({'error': 'Session expired'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
