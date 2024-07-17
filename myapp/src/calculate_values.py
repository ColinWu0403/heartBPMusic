import random


def calculate_acousticness(data):
    mood = data['mood']
    complexity = data['complexity']

    if complexity == 'intricate':
        if mood == 'happy':
            value = random.uniform(0.2, 0.7)
        elif mood == 'sad':
            value = random.uniform(0.4, 0.8)
        elif mood == 'energetic':
            value = random.uniform(0, 0.4)
        elif mood == 'calm':
            value = random.uniform(0.1, 0.6)
        elif mood == 'excited':
            value = random.uniform(0, 0.3)
        elif mood == 'reflective':
            value = random.uniform(0.3, 0.7)
        elif mood == 'creative':
            value = random.uniform(0, 0.7)
    else:  # otherwise simple
        if mood == 'happy':
            value = random.uniform(0.4, 0.8)
        elif mood == 'sad':
            value = random.uniform(0.3, 0.8)
        elif mood == 'energetic':
            value = random.uniform(0, 0.2)
        elif mood == 'calm':
            value = random.uniform(0.3, 0.5)
        elif mood == 'excited':
            value = random.uniform(0, 0.3)
        elif mood == 'reflective':
            value = random.uniform(0.3, 0.6)
        elif mood == 'creative':
            value = random.uniform(0, 0.6)

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_danceability(data):
    mood = data['mood']
    energy_level = data['energyLevel']

    if mood == 'happy':
        value = random.uniform(0.5, 0.8)
    elif mood == 'sad':
        value = random.uniform(0, 0.35)
    elif mood == 'energetic':
        value = random.uniform(0.55, 0.95)
    elif mood == 'calm':
        value = random.uniform(0.15, 0.4)
    elif mood == 'excited':
        value = random.uniform(0.6, 0.95)
    elif mood == 'reflective':
        value = random.uniform(0.2, 0.55)
    elif mood == 'creative':
        value = random.uniform(0.4, 0.7)

    if energy_level == 'lowest':
        value -= random.uniform(0.075, 0.125)
    elif energy_level == 'low':
        value -= random.uniform(0.025, 0.075)
    elif energy_level == 'high':
        value += random.uniform(0.025, 0.075)
    elif energy_level == 'highest':
        value += random.uniform(0.075, 0.125)
    else:
        value += 0

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_energy(data):
    energy_level = data['energyLevel']
    mood = data['mood']

    if energy_level == 'lowest':
        value = random.uniform(0, 0.25)
    elif energy_level == 'low':
        value = random.uniform(0.25, 0.4)
    elif energy_level == 'moderate':
        value = random.uniform(0.4, 0.65)
    elif energy_level == 'high':
        value = random.uniform(0.65, 0.8)
    elif energy_level == 'highest':
        value = random.uniform(0.8, 1)

    if mood == 'happy':
        value += random.uniform(0, 0.05)
    elif mood == 'sad':
        value -= random.uniform(0, 0.05)
    elif mood == 'energetic':
        value += random.uniform(0, 0.1)
    elif mood == 'calm':
        value -= random.uniform(0, 0.1)
    elif mood == 'excited':
        value += random.uniform(0, 0.15)
    elif mood == 'reflective':
        value -= random.uniform(0, 0.025)

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_instrumentalness(data):
    instrument_dominance = data['instrumentDominance']
    ambiance = data['ambiance']

    if instrument_dominance == 'vocals':
        value = random.uniform(0, 0.15)
    elif instrument_dominance == 'balanced':
        value = random.uniform(0.15, 0.3)
    elif instrument_dominance == 'instrumental':
        value = random.uniform(0.3, 1.0)

    if ambiance == 'ambient':
        value += random.uniform(0, 0.05)
    else:
        value += random.uniform(-0.025, 0.025)

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_liveness(data):
    ambiance = data['ambiance']
    instrument_dominance = data['instrumentDominance']

    if ambiance == 'ambient':
        value = random.uniform(0, 0.1)
    elif ambiance == 'clear':
        value = random.uniform(0.1, 0.2)
    elif ambiance == 'dynamic':
        value = random.uniform(0.075, 0.225)

    if instrument_dominance == 'instrumental':
        value -= random.uniform(0, 0.025)
    elif instrument_dominance == 'vocals':
        value += random.uniform(0, 0.025)

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_loudness(data):
    energy_level = data['energyLevel']
    ambiance = data['ambiance']

    if energy_level == 'lowest':
        value = random.uniform(-15, -12)
    elif energy_level == 'low':
        value = random.uniform(-12, -9)
    elif energy_level == 'moderate':
        value = random.uniform(-9, -7.5)
    elif energy_level == 'high':
        value = random.uniform(-7.5, -6.5)
    elif energy_level == 'highest':
        value = random.uniform(-6.5, -4.5)

    if ambiance =='ambient':
        value -= random.uniform(0, 1)
    elif ambiance =='clear':
        value += random.uniform(0, 0.025)
    elif ambiance == 'dynamic':
        value += random.uniform(0, 1)

    if value > 0:
        value = 0

    return round(value, 4)


def calculate_speechiness(data):
    instrument_dominance = data['instrumentDominance']
    ambiance = data['ambiance']
    complexity = data['complexity']

    if instrument_dominance == 'vocals':
        value = random.uniform(0.075, 0.2)
    elif instrument_dominance == 'balanced':
        value = random.uniform(0.06, 0.125)
    elif instrument_dominance == 'instrumental':
        value = random.uniform(0, 0.065)

    if ambiance == 'ambient':
        value -= random.uniform(0, 0.025)
    elif ambiance == 'dynamic':
        value += random.uniform(0, 0.025)

    if complexity == 'intricate':
        value += random.uniform(0, 0.01)
    elif complexity == 'simple':
        value -= random.uniform(0, 0.01)

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_mode(data):
    mood = data['mood']

    if mood == 'happy':
        mode = 1
    elif mood == 'sad':
        mode = 0
    elif mood == 'energetic':
        choices = [1, 0]
        weights = [0.67, 0.33]
        mode = random.choices(choices, weights=weights)[0]
    elif mood == 'calm':
        choices = [1, 0]
        weights = [0.60, 0.40]
        mode = random.choices(choices, weights=weights)[0]
    elif mood == 'excited':
        choices = [1, 0]
        weights = [0.75, 0.25]
        mode = random.choices(choices, weights=weights)[0]
    elif mood == 'reflective':
        choices = [1, 0]
        weights = [0.40, 0.60]
        mode = random.choices(choices, weights=weights)[0]
    elif mood == 'creative':
        choices = [1, 0]
        weights = [0.80, 0.20]
        mode = random.choices(choices, weights=weights)[0]
    return mode


def calculate_valence(data):
    mood = data['mood']
    energy_level = data['energyLevel']

    if mood == 'happy':
        value = random.uniform(0.6, 0.8)
    elif mood == 'sad':
        value = random.uniform(0.2, 0.45)
    elif mood == 'energetic':
        value = random.uniform(0.5, 0.8)
    elif mood == 'calm':
        value = random.uniform(0.3, 0.6)
    elif mood == 'excited':
        value = random.uniform(0.65, 0.9)
    elif mood == 'reflective':
        value = random.uniform(0.35, 0.55)
    elif mood == 'creative':
        value = random.uniform(0.45, 0.55)

    if energy_level == 'lowest':
        value -= random.uniform(0.05, 0.075)
    elif energy_level == 'low':
        value -= random.uniform(0.025, 0.05)
    elif energy_level == 'high':
        value += random.uniform(0.025, 0.05)
    elif energy_level == 'highest':
        value += random.uniform(0.07, 0.075)
    else:
        value += 0

    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return round(value, 4)


def calculate_values(data):
    return {
        'acousticness': calculate_acousticness(data),
        'danceability': calculate_danceability(data),
        'energy': calculate_energy(data),
        'instrumentalness': calculate_instrumentalness(data),
        'liveness': calculate_liveness(data),
        'loudness': calculate_loudness(data),
        'speechiness': calculate_speechiness(data),
        'mode': calculate_mode(data),
        'valence': calculate_valence(data),
    }
