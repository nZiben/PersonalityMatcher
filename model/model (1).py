from sentence_transformers import SentenceTransformer
import random
import librosa
import numpy as np
import pandas as pd
import ffmpeg as ff
import cv2
import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchmetrics.regression import MeanAbsolutePercentageError
from torch.utils.data import Dataset, DataLoader
import os
import matplotlib.pyplot as plt
from facenet_pytorch import MTCNN, InceptionResnetV1
from torchvision import transforms
from PIL import Image
import json    
from tqdm import tqdm
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import mean_absolute_error
from time import time

import warnings 
warnings.filterwarnings('ignore')

os.environ["TOKENIZERS_PARALLELISM"] = "true"

device = 'cpu'

class MultimodalTransformer:
    # Класс для осуществления препроцессинга данных
    def __init__(self, device, verbose=False, return_path=False):
        self.text_model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True).to(device)
        self.mtcnn = MTCNN(margin=20, keep_all=True, device=device)
        self.cv_model = InceptionResnetV1(pretrained='vggface2').eval().to(device)
        self.device = device
        self.verbose = verbose
        self.return_path = return_path


    def __call__(self, sample):
        path = sample['video_path']
        text = sample['transcription']
        
        # получение кадров из видео
        frames = self.get_frames(path)

        # получение мел-кепстральных коэффициентов из аудио
        mfcc = self.transform_audio(path)
        mfcc = torch.FloatTensor(mfcc)

        if 'labels' in sample.keys():
            if self.return_path:
                return (path, text, frames, mfcc, sample['labels'])
            return (text, frames, mfcc, sample['labels'])
        else:
            if self.return_path:
                return (path, text, frames, mfcc, )
            return (text, frames, mfcc, )

    def transform_texts(self, texts):
        # получение эмбеддингов транскрипций видео
        if self.verbose:
            print('Calculating text embeddings...')
        embeddings = self.text_model.encode(texts, task='classification', prompt_name='classification')
        return embeddings

    def get_frames(self, path):
        # получение кадров из видео
        cap = cv2.VideoCapture(path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
        random_indexes = sorted(random.sample(range(total_frames), 6))
        
        video_frames = []
        current_index = 0
        
        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            
            if i == random_indexes[current_index]:
                video_frames.append(cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (640, 360)))
                current_index += 1
                if current_index >= 6:
                    break

        cap.release()
        cv2.destroyAllWindows()

        return video_frames

    def detect_and_embed(self, batch_images):
        # детекция и эмбеддинг лиц на кадрах из видео
        if self.verbose:
            print('Detecting faces...')
        faces_list = self.mtcnn(batch_images)
        del batch_images
        
        all_faces = []
    
        for faces in faces_list:
            if faces is not None and len(faces) > 0:
                faces_resized = [torch.nn.functional.interpolate(faces[0].unsqueeze(0), size=(160, 160), mode='bilinear', align_corners=False).squeeze(0)]
                all_faces.extend(faces_resized)
            else:
                all_faces.extend([torch.zeros(3, 160, 160, dtype=torch.float32)])
        
        if all_faces:
            all_faces_tensor = torch.stack(all_faces).to(self.device)
            del all_faces

            if self.verbose:
                print('Embedding faces...')
            embeddings = self.cv_model(all_faces_tensor).cpu()
            del all_faces_tensor
            return embeddings
        else:
            return None

    def aggregate_embeddings(self, embeddings):
        # агрегирование эмбеддингов кадров
        if embeddings is not None and len(embeddings) > 0:
            return torch.mean(embeddings, axis=1)
        else:
            return None
    
    def transform_video(self, video_frames):
        # получение агрегированных эмбеддингов из кадров видео
        if len(video_frames[0].shape) == 4:
            tensor_data = torch.stack(video_frames, axis=1)
            tensor_data_ = tensor_data.reshape(tensor_data.shape[0]*tensor_data.shape[1], *tensor_data.shape[2:])
            embeddings = self.detect_and_embed(tensor_data_)
            del tensor_data_
            aggregated = self.aggregate_embeddings(embeddings.reshape(tensor_data.shape[0], tensor_data.shape[1], 512))
        else:
            tensor_data = torch.stack(video_frames, axis=0)
            embeddings = self.detect_and_embed(tensor_data)
            aggregated = self.aggregate_embeddings(embeddings.unsqueeze(0))
            
        del embeddings

        return aggregated

    def transform_audio(self, path):
        # получение мел-кепстральных коэффициентов из аудио
        inputfile = ff.input(path) # загружаем видео
        out = inputfile.output('-', format='f32le', acodec='pcm_f32le', ac=1, ar='44100', loglevel='quiet') # отделяем звук
        raw = out.run(capture_stdout=True)
        del inputfile, out
        raw_data = np.frombuffer(raw[0],np.float32)

        mfcc_data = librosa.feature.mfcc(y=raw_data, n_mfcc=16) # получаем MFCC из звуковой дорожки
        mfcc_data_standardized = (mfcc_data - np.mean(mfcc_data)) / np.std(mfcc_data) # стандартизация

        # truncating и padding
        if mfcc_data_standardized.shape[1] > 1319:
            processed = mfcc_data_standardized[:, :1319]
        else:
            n_pad_cols = 1319 - mfcc_data_standardized.shape[1]
            padding = np.zeros((16, n_pad_cols))

            processed = np.hstack((padding, mfcc_data_standardized))

        del mfcc_data, mfcc_data_standardized, raw_data

        return processed

class MultimodalInterviewModel(nn.Module):
    def __init__(self, use_torch_clf=True):
        super(MultimodalInterviewModel, self).__init__()
        
        self.use_torch_clf = use_torch_clf
        # audio
        self.relu = nn.ReLU()
        self.conv1 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3)
        self.batchnorm1 = nn.BatchNorm1d(num_features=32)
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=4, kernel_size=3)
        self.batchnorm2 = nn.BatchNorm1d(num_features=4)
        self.fc_audio = nn.Linear(in_features=1312, out_features=512)


        
        self.fusion_layer = nn.Linear(in_features=2048, out_features=2048)
        
        
        # Final output layer
        self.output_layer = nn.Linear(in_features=2048, out_features=6)
        self.sigmoid = nn.Sigmoid()

    
    def forward(self, audio_input, video_input, text_input):
        # Get features from each modality
        # AUDIO
        aud = self.conv1(audio_input)
        aud = self.batchnorm1(aud)
        aud = self.relu(aud)
        aud = self.pool(aud)
        aud = self.conv2(aud)
        aud = self.batchnorm2(aud)
        aud = self.relu(aud)
        aud = self.pool(aud)
        aud = aud.flatten(start_dim=1)
        aud = self.fc_audio(aud)
        aud = self.relu(aud)


        
        # Concatenate modality features
        x = torch.cat((aud, video_input, text_input), dim=1)

        if self.use_torch_clf:
            # Fusion and prediction
            x = self.fusion_layer(x)
            x = self.relu(x)
            x = self.output_layer(x)
            out = self.sigmoid(x)
            
            return out
        else:
            return x

class OneVideoProcessor:
    def __init__(self, cb_model=None, emb_model=None, torch_path=None, transformer=None, device='cpu'):

        self.transformer = MultimodalTransformer(device='cpu')

        # катбуст не работает без гпу
        self.cb_model = cb_model 
        self.emb_model = emb_model

        torch_model = MultimodalInterviewModel()
        torch_model.load_state_dict(torch.load(torch_path, map_location=torch.device('cpu')))
        torch_model.eval()

        self.torch_model = torch_model
        self.ocean = ('O', 'C', 'E', 'A', 'N', 'I')

    def transform(self, video_path, transcription):
        text_embed = self.transformer.transform_texts(transcription)
        text_embed = torch.FloatTensor(text_embed)
        frames = self.transformer.get_frames(video_path)
        frames = [torch.FloatTensor(frame) for frame in frames]
        video_embed = self.transformer.transform_video(frames)
        audio_embed = self.transformer.transform_audio(video_path)
        audio_embed = torch.FloatTensor(audio_embed).unsqueeze(0)

        return text_embed, video_embed, audio_embed

    def predict_cb(self, video_path, transcription):
        # без гпу не работает
        text_embed, video_embed, audio_embed = self.transform(video_path, transcription)

        audio_embed, video_embed, text_embed = audio_embed.to(device), video_embed.to(device), text_embed.to(device)
        
        embed = self.emb_model(audio_embed, video_embed, text_embed)

        pred = self.cb_model.predict(embed.cpu().detach().numpy())
        pred_dict = dict(zip(self.ocean, pred))

        return pred_dict

    def predict_pt(self, video_path, transcription):
        text_embed, video_embed, audio_embed = self.transform(video_path, transcription)

        audio_embed, video_embed, text_embed = audio_embed.to(device), video_embed.to(device), text_embed.to(device)

        pred = self.torch_model(audio_embed, video_embed, text_embed)

        pred_dict = dict(zip(self.ocean, pred))

        return pred_dict