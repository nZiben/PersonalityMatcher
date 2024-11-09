def mbti_to_ocean(mbti):
    # Словарь со средними значениями черт OCEAN для каждого типа MBTI
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

    mbti = mbti
    return mbti_ocean_mapping.get(mbti, None)
