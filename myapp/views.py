import uuid
import logging, json
from django.shortcuts import render
from django.http import JsonResponse
from .models import SongRequestFeatures
from .src.ecg import calculate_bpm
from .src.knn import find_closest_song


logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def get_bpm(request):
    if request.method == 'GET':
        ecg_file_path = "signals/04048"  # Replace with actual path to your ECG file
        # bpm, rounded_bpm = calculate_bpm(ecg_file_path)
        rounded_bpm = 128

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
        # Clear previous session data
        if 'closest_song' in request.session:
            del request.session['closest_song']

        # Log received data
        print(f"Received POST data: {request.POST}")

        data = json.loads(request.body)
        bpm = request.session.get('bpm')  # Retrieve BPM from session

        if bpm:
            request.session['acousticness'] = float(data.get('acousticness', 0.0))
            request.session['danceability'] = float(data.get('danceability', 0.0))
            request.session['energy'] = float(data.get('energy', 0.0))
            request.session['instrumentalness'] = float(data.get('instrumentalness', 0.0))
            request.session['liveness'] = float(data.get('liveness', 0.0))
            request.session['loudness'] = float(data.get('loudness', 0.0))
            request.session['speechiness'] = float(data.get('speechiness', 0.0))
            request.session['mode'] = int(data.get('mode', 0))
            request.session['valence'] = float(data.get('valence', 0.0))

            print(bpm)
            print(request.session['acousticness'])
            print(request.session['danceability'])
            print(request.session['energy'])
            print(request.session['instrumentalness'])
            print(request.session['liveness'])
            print(request.session['loudness'])
            print(request.session['speechiness'])
            print(request.session['mode'])
            print(request.session['valence'])

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

                user_features = [
                    request.session['bpm'],
                    request.session['acousticness'],
                    request.session['danceability'],
                    request.session['energy'],
                    request.session['instrumentalness'],
                    request.session['liveness'],
                    request.session['loudness'],
                    request.session['speechiness'],
                    request.session['mode'],
                    request.session['valence']
                ]

                closest_song_series, closest_song = find_closest_song(user_features)

                def get_value(d):
                    return next(iter(d.values()))

                response_data = {
                    'name': get_value(closest_song['name']),
                    'artists': get_value(closest_song['artists']),
                    'bpm': get_value(closest_song['bpm']),
                    'genre': get_value(closest_song['genre']),
                    'key': get_value(closest_song['key']),
                    'acousticness': get_value(closest_song['acousticness']),
                    'danceability': get_value(closest_song['danceability']),
                    'energy': get_value(closest_song['energy']),
                    'instrumentalness': get_value(closest_song['instrumentalness']),
                    'liveness': get_value(closest_song['liveness']),
                    'loudness': get_value(closest_song['loudness']),
                    'speechiness': get_value(closest_song['speechiness']),
                    'mode': get_value(closest_song['mode']),
                    'valence': get_value(closest_song['valence']),
                    'href': get_value(closest_song['href']),
                    'uri': get_value(closest_song['uri'])
                }

                request.session['closest_song'] = response_data

                # Return the closest song to the features in the request
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({'error': 'Session ID not found'}, status=400)

        else:
            return JsonResponse({'error': 'Session expired'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_closest_song(request):
    if request.method == 'GET':
        closest_song = request.session.get('closest_song')
        if closest_song:
            return JsonResponse(closest_song)
        else:
            return JsonResponse({'error': 'No song found in session'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
