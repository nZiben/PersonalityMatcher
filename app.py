import streamlit as st
import random
import time
import datetime
import os
import tempfile

import whisper
from moviepy.editor import VideoFileClip

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from translate_OCEAN_to_other.explain_mbti_type import explain_mbti_type 
from translate_OCEAN_to_other.ocean_to_mbti import ocean_to_mbti
from translate_OCEAN_to_other.mbti_to_ocean import mbti_to_ocean

# Создаем базу данных SQLite
engine = create_engine('sqlite:///mydatabase.db')
Base = declarative_base()

# Определяем модели

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    user_type = Column(String)

    videos = relationship("Video", order_by="Video.id", back_populates="user")

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    filename = Column(String)
    upload_time = Column(DateTime)
    ocean_scores = Column(String)  # Можно хранить в виде JSON строки
    mbti_type = Column(String)
    description = Column(Text)  # Транскрибированный текст

    user = relationship("User", back_populates="videos")

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    personality_type = Column(String)
    description = Column(Text)

# Создаем таблицы
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Добавление начальных пользователей
def add_initial_users():
    existing_user = session.query(User).filter_by(username='user').first()
    if not existing_user:
        new_user = User(username='user', password='userpass', user_type='user')
        session.add(new_user)
    existing_admin = session.query(User).filter_by(username='admin').first()
    if not existing_admin:
        new_admin = User(username='admin', password='adminpass', user_type='admin')
        session.add(new_admin)
    session.commit()

add_initial_users()

# Состояние сессии для отслеживания авторизованных пользователей
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['user_type'] = ''
    st.session_state['auth_mode'] = ''

# Функция для симуляции предсказания OCEAN из видео
def predict_ocean_from_video(video_file):
    # Заглушка для фактического предсказания модели
    # Замените это на код вывода модели
    st.write("Обработка видео и предсказание черт OCEAN...")
    time.sleep(2)
    ocean_scores = {
        'O': random.randint(1, 100),
        'C': random.randint(1, 100),
        'E': random.randint(1, 100),
        'A': random.randint(1, 100),
        'N': random.randint(1, 100)
    }
    return ocean_scores

# Функция для транскрипции аудио из видео
def transcribe_video_audio(video_file: str, model_name: str = "tiny"):
    # временный файл в оперативке
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_audio_file:
        # аудио из видео
        with VideoFileClip(video_file) as video:
            video.audio.write_audiofile(temp_audio_file.name)
        # распознаем
        model = whisper.load_model(model_name)
        result = model.transcribe(temp_audio_file.name)
    return result["text"]

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
            user = session.query(User).filter_by(username=username, password=password).first()
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_type'] = user.user_type
                st.success("Успешный вход!")
                st.rerun()
            else:
                st.error("Неверное имя пользователя или пароль")
    elif st.session_state['auth_mode'] == 'register':
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type='password')
        if st.button("Зарегистрироваться"):
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                st.error("Имя пользователя уже существует")
            else:
                new_user = User(username=username, password=password, user_type='user')
                session.add(new_user)
                session.commit()
                st.success("Регистрация прошла успешно!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_type'] = 'user'
                st.rerun()

# Личный кабинет пользователя
def user_dashboard():
    st.title(f"Добро пожаловать, {st.session_state['username']}")
    user = session.query(User).filter_by(username=st.session_state['username']).first()
    last_video = session.query(Video).filter_by(user_id=user.id).order_by(Video.upload_time.desc()).first()
    if last_video:
        st.header("Ваш последний загруженный видео")
        st.subheader(f"Название видео: {last_video.filename}")
        st.subheader("Ваши баллы OCEAN:")
        st.write(eval(last_video.ocean_scores))
        st.subheader(f"Ваш тип MBTI: {last_video.mbti_type}")
        st.subheader("Подробное объяснение:")
        st.write(last_video.description)
    else:
        st.write("У вас еще нет загруженных видео.")
    if st.button("Загрузить новое видео"):
        st.session_state['upload_new_video'] = True
        st.rerun()
    if 'upload_new_video' in st.session_state and st.session_state['upload_new_video']:
        st.header("Загрузите свое видео для оценки личности")
        video_file = st.file_uploader("Загрузить видео", type=['mp4', 'mov', 'avi'])
        if video_file is not None:
            # Save the uploaded video to a file
            user_videos_folder = f"uploaded_videos/{user.username}"
            if not os.path.exists(user_videos_folder):
                os.makedirs(user_videos_folder)
            video_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{video_file.name}"
            video_path = os.path.join(user_videos_folder, video_filename)
            with open(video_path, 'wb') as out_file:
                out_file.write(video_file.read())
            # Process the video
            ocean_scores = predict_ocean_from_video(video_path)
            mbti_type = ocean_to_mbti(ocean_scores)
            explanation = explain_mbti_type(mbti_type)
            # Transcribe video audio
            transcribed_text = transcribe_video_audio(video_path)
            # Save to database
            new_video = Video(
                user_id=user.id,
                filename=video_filename,
                upload_time=datetime.datetime.now(),
                ocean_scores=str(ocean_scores),
                mbti_type=mbti_type,
                description=explanation
            )
            session.add(new_video)
            session.commit()
            st.success("Видео успешно загружено и обработано!")
            # Display the results
            st.subheader(f"Название видео: {video_filename}")
            st.subheader(f"Название видео: {video_filename}")
            st.subheader("Ваши баллы OCEAN:")
            st.write(ocean_scores)
            st.subheader(f"Ваш тип MBTI: {mbti_type}")
            st.subheader("Подробное объяснение:")
            st.write(explanation)
            # Clear the upload_new_video flag
            st.session_state['upload_new_video'] = False
            st.rerun()

# Панель администратора
def admin_dashboard():
    st.title("Панель администратора")
    if 'admin_page' not in st.session_state:
        st.session_state['admin_page'] = 'main'
    if st.session_state['admin_page'] == 'main':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Создать новую вакансию"):
                st.session_state['admin_page'] = 'create_vacancy'
                st.rerun()
        with col2:
            st.write("Список вакансий:")
            vacancies = session.query(Vacancy).all()
            for vacancy in vacancies:
                if st.button(vacancy.title):
                    st.session_state['selected_vacancy'] = vacancy.id
                    st.session_state['admin_page'] = 'view_vacancy'
                    st.rerun()
    elif st.session_state['admin_page'] == 'create_vacancy':
        st.header("Создать новую вакансию")
        title = st.text_input("Название вакансии")
        personality_type = st.text_input("Тип личности")
        description = st.text_area("Описание вакансии")
        if st.button("Сохранить вакансию"):
            new_vacancy = Vacancy(title=title, personality_type=personality_type, description=description)
            session.add(new_vacancy)
            session.commit()
            st.success("Вакансия успешно создана!")
            st.session_state['admin_page'] = 'main'
            st.rerun()
        if st.button("Отменить"):
            st.session_state['admin_page'] = 'main'
            st.rerun()
    elif st.session_state['admin_page'] == 'view_vacancy':
        vacancy_id = st.session_state['selected_vacancy']
        vacancy = session.query(Vacancy).filter_by(id=vacancy_id).first()
        if vacancy:
            st.header(f"Вакансия: {vacancy.title}")
            st.write(f"Тип личности: {vacancy.personality_type}")
            st.write(f"Описание: {vacancy.description}")
            st.header("Загрузка видео кандидатов")
            uploaded_videos = st.file_uploader("Загрузить видео", type=['mp4', 'mov', 'avi'], accept_multiple_files=True)
            if st.button("Загрузить видео"):
                if uploaded_videos:
                    for video_file in uploaded_videos:
                        # Save the uploaded video
                        video_folder = f"vacancy_videos/{vacancy.id}"
                        if not os.path.exists(video_folder):
                            os.makedirs(video_folder)
                        video_filename = video_file.name
                        video_path = os.path.join(video_folder, video_filename)
                        with open(video_path, 'wb') as out_file:
                            out_file.write(video_file.read())
                        # Process the video
                        ocean_scores = predict_ocean_from_video(video_path)
                        mbti_type = ocean_to_mbti(ocean_scores)
                        explanation = explain_mbti_type(mbti_type)
                        # Transcribe video audio
                        transcribed_text = transcribe_video_audio(video_path)
                        # Save to database
                        new_video = Video(
                            user_id=None,  # Since these are candidate videos, not associated with a user
                            filename=video_filename,
                            upload_time=datetime.datetime.now(),
                            ocean_scores=str(ocean_scores),
                            mbti_type=mbti_type,
                            description=explanation
                        )
                        session.add(new_video)
                        session.commit()
                    st.success("Видео успешно загружены и обработаны!")
                    st.rerun()
                else:
                    st.error("Пожалуйста, загрузите видео.")
            if st.button("Получить рейтинг кандидатов"):
                # Retrieve candidate videos for this vacancy
                video_folder = f"vacancy_videos/{vacancy.id}"
                if os.path.exists(video_folder):
                    # Get all video filenames
                    candidate_videos = os.listdir(video_folder)
                    # For simplicity, simulate ranking
                    ranked_candidates = candidate_videos  # В реальном сценарии вы бы ранжировали на основе критериев
                    st.subheader("Ранжированные кандидаты:")
                    for idx, candidate in enumerate(ranked_candidates, 1):
                        st.write(f"{idx}. {candidate}")
                else:
                    st.error("Нет загруженных видео для этой вакансии.")
            if st.button("Вернуться к списку вакансий"):
                st.session_state['admin_page'] = 'main'
                st.rerun()
        else:
            st.error("Вакансия не найдена.")

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
            st.rerun()
        else:
            if st.session_state['user_type'] == 'user':
                user_dashboard()
            elif st.session_state['user_type'] == 'admin':
                admin_dashboard()
            else:
                st.error(f"У вас нет доступа к этой странице.")
                if st.button("Вернуться на главную страницу"):
                    st.rerun()
                else:
                    st.stop()

if __name__ == "__main__":
    main()
