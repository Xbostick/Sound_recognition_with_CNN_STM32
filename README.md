# STM32 Lightweight CNN Deployment

## 📌 Project Overview
This project focuses on creating and deploying a **lightweight Convolutional Neural Network (CNN) for STM32 microcontrollers**. The pipeline includes data preprocessing, model training, conversion to TensorFlow Lite (TFLite), and deployment on STM32 hardware.

## 🛠 Features
- **Audio Preprocessing:** Extracts MFCC features from audio using `librosa` and `CMSIS-DSP`.
- **CNN Model:** Trains a small-scale CNN optimized for embedded deployment.
- **TFLite Conversion:** Converts and quantizes the model for STM32 compatibility.
- **Docker Environment:** Provides a reproducible environment for model development.

## 🚀 Getting Started
### Setup Environment
Clone the repository and build the Docker image:
```sh
 git clone https://github.com/your-repo/stm32-cnn.git
 cd stm32-cnn
 docker build -t stm32-cnn .
```

### Run Jupyter Notebook
```sh
docker run -p 8888:8888 -v $(pwd):/usr/src/app stm32-cnn
```
Then open the link shown in the terminal.


## 📂 Project Structure
```
📦 stm32-cnn
 ┣ 📂 STM32_code
 ┃ ┃ ... 
 ┃ ┃ ...
 ┃ ┃ 📜 README.md           # cpp project documentation
 ┣ 📂 ModelCreating_python
 ┃ ┣ 📜 dataPreprocess.py  # Preprocesses audio data
 ┃ ┣ 📜 model.py           # Defines and trains the CNN model
 ┃ ┣ 📜 modelConvert.py    # Converts the model to TFLite
 ┣ 📜 Dockerfile          # Containerized environment setup
 ┣ 📜 requirements.txt    # Required Python dependencies
 ┣ 📜 README.md           # Project documentation
```

## 📌 Notes
- The MFCC feature extraction uses **both `librosa.mfcc` and `CMSIS-DSP`** for comparison.
- The model is trained using TensorFlow and later optimized for embedded deployment.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🔹 **Contributions:** Feel free to open an issue or pull request!
