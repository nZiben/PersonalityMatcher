def ocean_to_dark_triad(ocean_scores):
    # Извлечение значений OCEAN из словаря
    O, C, E, A, N = ocean_scores['O'], ocean_scores['C'], ocean_scores['E'], ocean_scores['A'], ocean_scores['N']
    
    # Коэффициенты из таблицы для каждой черты темной триады
    narcissism_coeffs = {
        'E': 0.42,
        'A': -0.36,
        'C': -0.06,
        'N': 0.02,
        'O': 0.38
    }
    
    machiavellianism_coeffs = {
        'E': -0.05,
        'A': -0.47,
        'C': -0.34,
        'N': 0.12,
        'O': -0.03
    }
    
    psychopathy_coeffs = {
        'E': 0.34,
        'A': -0.25,
        'C': -0.24,
        'N': -0.34,
        'O': 0.24
    }
    
    # Расчет значений темной триады
    narcissism = (narcissism_coeffs['E'] * E +
                  narcissism_coeffs['A'] * A +
                  narcissism_coeffs['C'] * C +
                  narcissism_coeffs['N'] * N +
                  narcissism_coeffs['O'] * O)
    
    machiavellianism = (machiavellianism_coeffs['E'] * E +
                        machiavellianism_coeffs['A'] * A +
                        machiavellianism_coeffs['C'] * C +
                        machiavellianism_coeffs['N'] * N +
                        machiavellianism_coeffs['O'] * O)
    
    psychopathy = (psychopathy_coeffs['E'] * E +
                   psychopathy_coeffs['A'] * A +
                   psychopathy_coeffs['C'] * C +
                   psychopathy_coeffs['N'] * N +
                   psychopathy_coeffs['O'] * O)
    
    narcissism = max(0, narcissism)
    machiavellianism = max(0, machiavellianism)
    psychopathy = max(0, psychopathy)

    # Возвращение результатов в виде словаря
    return {
        'Narcissism': narcissism,
        'Machiavellianism': machiavellianism,
        'Psychopathy': psychopathy
    }
