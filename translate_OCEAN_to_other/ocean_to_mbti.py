def ocean_to_mbti(ocean_scores):
    O, C, E, A, N = ocean_scores['O'], ocean_scores['C'], ocean_scores['E'], ocean_scores['A'], ocean_scores['N']

    if O >= 0.6 and O <= 0.94 and C >= 0.54 and C <= 0.89 and E <= 0.41 and A > 0.5 and N > 0.28:
        return 'INFJ'
    elif O >= 0.56 and O <= 0.94 and C < 0.32 and E > 0.13 and E <= 0.52 and A > 0.18 and N > 0.54:
        return 'INFP'
    elif O >= 0.61 and O <= 0.91 and C >= 0.56 and C <= 0.98 and E > 0.04 and E <= 0.35 and A < 0.39 and N >= 0.3 and N <= 0.8:
        return 'INTJ'
    elif O >= 0.56 and O <= 0.85 and C > 0.06 and C <= 0.45 and E > 0.1 and E <= 0.39 and A < 0.22 and N > 0.3:
        return 'INTP'
    elif O < 0.5 and C > 0.32 and C <= 0.72 and E <= 0.4 and A >= 0.64 and N > 0.5:
        return 'ISFJ'
    elif O > 0.13 and O <= 0.55 and C < 0.22 and E <= 0.47 and A > 0.42 and N > 0.71:
        return 'ISFP'
    elif O < 0.33 and C >= 0.5 and E <= 0.29 and A < 0.43 and N > 0.62:
        return 'ISTJ'
    elif O > 0.07 and O <= 0.45 and C < 0.3 and E <= 0.47 and A < 0.18 and N > 0.54:
        return 'ISTP'
    elif O > 0.53 and C > 0.61 and E > 0.55 and A > 0.74 and N < 0.5:
        return 'ENFJ'
    elif O > 0.75 and C < 0.44 and E > 0.63 and A > 0.57 and N < 0.42:
        return 'ENFP'
    elif O > 0.5 and O <= 0.87 and C > 0.72 and E <= 0.68 and A < 0.5 and N < 0.4:
        return 'ENTJ'
    elif O > 0.63 and C > 0.35 and C <= 0.71 and E > 0.62 and A < 0.29 and N < 0.36:
        return 'ENTP'
    elif O > 0.14 and O <= 0.44 and C >= 0.53 and C <= 0.82 and E > 0.55 and E <= 0.91 and A > 0.75 and N > 0.2 and N <= 0.7:
        return 'ESFJ'
    elif O > 0.09 and O <= 0.36 and C > 0.1 and C <= 0.41 and E > 0.66 and E <= 0.95 and A > 0.6 and N > 0.25 and N <= 0.75:
        return 'ESFP'
    elif O > 0.08 and O <= 0.43 and C > 0.69 and E > 0.52 and E <= 0.83 and A < 0.62 and N < 0.47:
        return 'ESTJ'
    elif O > 0.07 and O <= 0.36 and C > 0.15 and C <= 0.42 and E > 0.6 and E <= 0.92 and A < 0.31 and N < 0.5:
        return 'INFJ'

    # Если не найдено точного соответствия, находим ближайший MBTI тип
    mbti_ocean_mapping = {
        'INFJ': {'O': 0.77, 'C': 0.715, 'E': 0.25, 'A': 0.75, 'N': 0.64},
        'INFP': {'O': 0.75, 'C': 0.16, 'E': 0.325, 'A': 0.59, 'N': 0.77},
        'INTJ': {'O': 0.76, 'C': 0.77, 'E': 0.195, 'A': 0.195, 'N': 0.55},
        'INTP': {'O': 0.705, 'C': 0.255, 'E': 0.245, 'A': 0.11, 'N': 0.65},
        'ISFJ': {'O': 0.25, 'C': 0.52, 'E': 0.2, 'A': 0.82, 'N': 0.75},
        'ISFP': {'O': 0.34, 'C': 0.11, 'E': 0.235, 'A': 0.71, 'N': 0.855},
        'ISTJ': {'O': 0.165, 'C': 0.75, 'E': 0.145, 'A': 0.215, 'N': 0.81},
        'ISTP': {'O': 0.26, 'C': 0.15, 'E': 0.235, 'A': 0.09, 'N': 0.77},
        'ENFJ': {'O': 0.765, 'C': 0.805, 'E': 0.775, 'A': 0.87, 'N': 0.25},
        'ENFP': {'O': 0.875, 'C': 0.22, 'E': 0.815, 'A': 0.785, 'N': 0.21},
        'ENTJ': {'O': 0.685, 'C': 0.86, 'E': 0.84, 'A': 0.25, 'N': 0.2},
        'ENTP': {'O': 0.815, 'C': 0.53, 'E': 0.81, 'A': 0.145, 'N': 0.18},
        'ESFJ': {'O': 0.29, 'C': 0.675, 'E': 0.73, 'A': 0.875, 'N': 0.45},
        'ESFP': {'O': 0.225, 'C': 0.255, 'E': 0.805, 'A': 0.8, 'N': 0.5},
        'ESTJ': {'O': 0.255, 'C': 0.845, 'E': 0.675, 'A': 0.31, 'N': 0.235},
        'ESTP': {'O': 0.215, 'C': 0.285, 'E': 0.76, 'A': 0.155, 'N': 0.25},
    }

    # Вычисляем евклидово расстояние до каждого MBTI типа
    min_distance = float('inf')
    closest_mbti = None

    for mbti_type, scores in mbti_ocean_mapping.items():
        distance = ((O - scores['O']) ** 2 +
                    (C - scores['C']) ** 2 +
                    (E - scores['E']) ** 2 +
                    (A - scores['A']) ** 2 +
                    (N - scores['N']) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_mbti = mbti_type

    return closest_mbti
