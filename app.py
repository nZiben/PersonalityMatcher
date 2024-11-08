import streamlit as st
import random
import time

# Симулированная база данных пользователей
users_db = {
    'user': {'password': 'userpass', 'type': 'user'},
    'admin': {'password': 'adminpass', 'type': 'admin'}
}

# Состояние сессии для отслеживания авторизованных пользователей
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['user_type'] = ''
    st.session_state['auth_mode'] = ''

# Функция для преобразования OCEAN в MBTI
def ocean_to_mbti(ocean_scores):
    # Упрощенная логика для демонстрации
    mbti_types = ['INTJ', 'ENTP', 'ISFJ', 'ESFP']
    return random.choice(mbti_types)

# Функция для предоставления подробных текстовых объяснений результатов OCEAN
def explain_ocean(ocean_scores):
    explanations = {
        'O': 'Открытость опыту: {}',
        'C': 'Добросовестность: {}',
        'E': 'Экстраверсия: {}',
        'A': 'Доброжелательность: {}',
        'N': 'Невротизм: {}'
    }
    details = []
    for trait, score in ocean_scores.items():
        details.append(explanations[trait].format(score))
    return '\n'.join(details)

# Функция для симуляции предсказания OCEAN из видео
def predict_ocean_from_video(video_file):
    # Заглушка для фактического предсказания модели
    # Замените это на код вывода модели
    st.write("Обработка видео и предсказание черт OCEAN...")
    ocean_scores = {
        'O': random.randint(1, 100),
        'C': random.randint(1, 100),
        'E': random.randint(1, 100),
        'A': random.randint(1, 100),
        'N': random.randint(1, 100)
    }
    return ocean_scores

# Страница входа и регистрации
def login_page():
    st.title("Добро пожаловать!")
    if st.session_state['auth_mode'] == '':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Войти"):
                st.session_state['auth_mode'] = 'login'
                st.rerun()
                    
        with col2:
            if st.button("Зарегистрироваться"):
                st.session_state['auth_mode'] = 'register'
                st.rerun()
    elif st.session_state['auth_mode'] == 'login':
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type='password')
        if st.button("Войти"):
            if username in users_db and users_db[username]['password'] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_type'] = users_db[username]['type']
                st.success("Успешный вход!")
                time.sleep(0.5)
                if st.button("Перейти в личный кабинет"):
                    # st.query_params.from_dict = {'page': users_db[username]['type']}
                    st.rerun()
            else:
                st.error("Неверное имя пользователя или пароль")
                if st.button("Попробовать снова"):
                    st.rerun()
    elif st.session_state['auth_mode'] == 'register':
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type='password')
        if st.button("Зарегистрироваться"):
            if username in users_db:
                st.error("Имя пользователя уже существует")
                st.rerun()
            else:
                users_db[username] = {'password': password, 'type': 'user'}
                st.success("Регистрация прошла успешно!")
                time.sleep(0.5)
                if st.button("Перейти в личный кабинет"):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['user_type'] = 'user'
                    # st.query_params.from_dict = {'page': users_db[username]['type']}
                    st.rerun()

# Личный кабинет пользователя
def user_dashboard():
    st.title(f"Добро пожаловать, {st.session_state['username']}")
    st.header("Загрузите свое видео для оценки личности")
    video_file = st.file_uploader("Загрузить видео", type=['mp4', 'mov', 'avi'])
    if video_file is not None:
        ocean_scores = predict_ocean_from_video(video_file)
        st.subheader("Ваши баллы OCEAN:")
        st.write(ocean_scores)
        mbti_type = ocean_to_mbti(ocean_scores)
        st.subheader(f"Ваш тип MBTI: {mbti_type}")
        explanation = explain_ocean(ocean_scores)
        st.subheader("Подробное объяснение:")
        st.write(explanation)
        st.header("Рекомендуемые профессии:")
        # Симулируем рекомендации по профессиям
        professions = ['Инженер-программист', 'Дата-сайентист', 'Графический дизайнер', 'Менеджер проекта']
        recommended = random.sample(professions, len(professions))
        for idx, profession in enumerate(recommended, 1):
            st.write(f"{idx}. {profession}")

# Панель администратора
def admin_dashboard():
    st.title("Панель администратора")
    st.header("Загрузка видео кандидатов")
    uploaded_videos = st.file_uploader("Загрузить видео", type=['mp4', 'mov', 'avi'], accept_multiple_files=True)
    desired_profession = st.text_input("Желаемая профессия")
    if st.button("Получить рейтинг кандидатов"):
        if uploaded_videos and desired_profession:
            st.write(f"Обработка видео для профессии: {desired_profession}")
            # Заглушка для обработки и ранжирования кандидатов
            candidates = [f"Кандидат_{i+1}" for i in range(len(uploaded_videos))]
            ranked_candidates = random.sample(candidates, len(candidates))
            st.subheader("Ранжированные кандидаты:")
            for idx, candidate in enumerate(ranked_candidates, 1):
                st.write(f"{idx}. {candidate}")
        else:
            st.error("Пожалуйста, загрузите видео и укажите желаемую профессию.")

# Основная логика приложения
def main():

    if not st.session_state['logged_in']:
        login_page()
    else:
        if st.button("Выйти"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.session_state['user_type'] = ''
            st.session_state['auth_mode'] = ''
            st.success("Вы вышли из системы.")
            time.sleep(1)
            if st.button("Перейти на главную страницу"):
                st.rerun()
                # st.stop()
        else:
            if st.session_state['user_type'] == 'user':
                user_dashboard()
            elif st.session_state['user_type'] == 'admin':
                admin_dashboard()
            else:
                st.error(f"У вас нет доступа к этой странице. {st.query_params.to_dict(), st.session_state['user_type']}")
                if st.button("Вернуться на главную страницу"):
                    # st.experimental_set_query_params()
                    st.rerun()
                else:
                    st.stop()

if __name__ == "__main__":
    main()
