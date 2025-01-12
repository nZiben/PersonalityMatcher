# Prediction of Personality Type via Video Résumé and Job Recommendations Considering OCEAN, MBTI, and the Dark Triad Indicators

## Project Overview

This project aims to predict an individual's personality type based on the OCEAN model using multiple domains. The solution is transparent and ensures high-speed operation — approximately 1 second per video (note that the model is quantized). Additionally, a list of professions has been compiled, mapped to personality types based on OCEAN, MBTI, and the Dark Triad.

## Functional Features and Technical Solution

1. ### Multimodal Personality Analysis Model
   The model processes three types of data (text, audio, video), allowing for precise analysis of personality characteristics based on the **OCEAN** system and converting them into **MBTI**. This approach ensures:
   - Deep contextual understanding,
   - High noise resilience,
   - Enhanced emotional interpretation,
   - Decision transparency.

2. ### Transformation of OCEAN into MBTI and the "Dark Triad"
   Using empirical data and the distribution of **OCEAN** across each **MBTI** type, accurate conversion is implemented:
   - A list of professions was compiled and processed.
   - Professions were mapped to OCEAN and MBTI personality types.
   - For MBTI — threshold values correlated with OCEAN were used,
   - For the "Dark Triad" — coefficients for each OCEAN trait to build a profile for each characteristic.

3. ### Model Processing Speed
   High processing speed (~1 second per video) due to an optimized quantized model. Suitable for handling large datasets, critical for quick selection and ranking.

4. ### Two-Stage Job Vacancy Ranking
   We use **BM25** search for textual vacancy analysis and personalize the ranking using OCEAN assessment. This allows finding the most relevant vacancies for each candidate.

---

## Project Killer Features
- **OCEAN-to-MBTI and Dark Triad Transformation**: Scientifically grounded and accurate transformation enables expanded analysis options.
- **Multimodal Approach**: Analysis of video, audio, and text ensures maximum assessment accuracy.
- **Two-Stage Job Ranking**: Technology that enhances recommendation relevance.

---

## Technology Stack
- Python, PyTorch, OpenCV, Librosa, Whisper, Streamlit
- SQLite, SQLAlchemy
- Transformers, FaceNet, MTCNN, Catboost, Sber LightAutoML

---

## Solution Uniqueness
The project stands out for its precise integration of three modalities, the ability to translate the OCEAN system into MBTI and the Dark Triad, and a high level of interpretability for all participants (employers and candidates).
---

### Graphical Interface

#### For Employees
- A personal dashboard for video uploads.
- Receiving textual feedback.
- Viewing job recommendations with a ranked vacancy list.
- Additional feature: earning on the platform.

#### For Employers
- Admin panel for uploading multiple videos.
- Specifying desired profession and personality type.
- Receiving a ranked list of candidates.

### Conversion of OCEAN to MBTI and Other Systems
- Translation of results into MBTI types.
- Conversion to other personality assessment systems.
- Textual explanation of user strengths and weaknesses.

## Project Structure

model/ — personality type prediction model. 
professions/ — mapping of professions. 
translation/ — tools for translating between OCEAN, MBTI, and other systems. 
app_with_model.py - application with model prediction (long initialization, memory requirements). 
app.py — main application.

## Installation and Launch

Instructions for installing and launching the project will be provided in subsequent sections.

# FFmpeg and ffmpeg-python

## What is FFmpeg?

FFmpeg is a powerful tool for processing multimedia files. It enables numerous audio and video operations.

## What is ffmpeg-python?

ffmpeg-python is a Python library providing a convenient interface to use FFmpeg's capabilities within Python code. It allows easy integration of media processing functions into applications.

# Installing FFmpeg

## macOS

1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)```
   
2. Install FFmpeg:
   ```bash
   brew install ffmpeg```
   
3. Check the installation:
   ```bash
   ffmpeg -version```
   
## Windows

1. Download FFmpeg:
   Go to the FFmpeg official website and select the Windows version. It is recommended to use the build from gyan.dev or another reliable source.

2. Unpack the archive:
   After downloading the archive (usually in the format .zip), unpack it.

3. Add FFmpeg to the PATH:

   - Press ``Win + R``, type sysdm.cpl and press Enter.
   - Go to the Advanced tab and click on Environment Variables.
   - In the "System Variables" section, find the Path variable, select it and click "Edit".
   - Click "Create" and add the path to the bin folder inside the FFmpeg directory, for example: C:ffmpegbin.
   - Click "OK" to save the changes.

4. Check the installation:
Open the command prompt (CMD) and type:
      ```bash
      ffmpeg -version```
If the installation is successful, you will see information about the FFmpeg version.

## Linux

To install FFmpeg on Linux, use your distribution's package manager.:
      ```bash
      sudo apt-get install ffmpeg```

# Installing ffmpeg-python library

After installing FFmpeg, you can install the ffmpeg-python library via pip:
      ```bash
      pip install ffmpeg-python ```

Done. Now you can use the app.

> **Note:** FFmpeg is needed to run Streamlit, don't forget about it!


# Launching a Docker container

## Requirements
- **Docker** — Make sure that Docker is installed on your device. If Docker is not installed, download it from the official website: [Docker](https://www.docker.com/products/docker-desktop ).

## Installation and Launch

1. **Clone the repository**:
    ```bash
    git clone https://github.com/nZiben/video_cv_matching.git
    cd video_cv_matching```

2. **Build a Docker image**:
    ```bash
    docker build -t video_cv_matching_image .```

3. **Launch the Docker container**:
    ```bash
    docker run -p 8501:8501 video_cv_matching_image```

4. **Open the app**:
    - Go to the browser and open [http://localhost:8501 ](http://localhost:8501 ) to see the application interface.

## Stopping and Restarting the container

### Container stop

1. Open a new terminal.
2. Enter the command to find out the ID of the running container.:
    ```bash
    docker ps```
3. Use the `docker stop` command to stop the container:
    ```bash
    docker stop <CONTAINER_ID>```
   Replace the `<CONTAINER_ID>` with the ID of your container.

### Restarting an existing container

To restart a previously stopped container:

1. Find his `CONTAINER ID` or name using:
    ```bash
    docker ps -a```
    
2. Then use the command:
    ```bash
    docker start <CONTAINER_ID or name>```

### Restarting the container with reassembly

If you need to make changes to the image and reassemble the container:

1. Rebuild the image:
    ```bash
    docker build -t video_cv_matching_image .```

2. Restart the container:
    ```bash
    docker run -p 8501:8501 video_cv_matching_image```

## Additional information

-**Dependency Update**: If you change dependencies, don't forget to update `requirements.txt `before reassembling the image.
- **Using Docker Compose**: If the project requires multiple services, you can add the `docker-compose' file.yml` for easier startup.
