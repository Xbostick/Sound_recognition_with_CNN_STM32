import librosa
import cmsisdsp as dsp
import scipy.signal as sig
import cmsisdsp.mfcc as mfcc
from cmsisdsp.datatype import F32
from audiomentations import Compose, AddGaussianNoise, PitchShift,  Shift
import numpy as np
from math import pi
import pandas as pd
from tqdm import tqdm
import os

# Constants
FFTSize = 512
numOfDctOutputs = 40
freq_min = 80.0
freq_high = 7600.0
numOfMelFilters = 120
PI = pi
window_size = 10
sample_rate = 22600

# Precomputed values
window = sig.windows.hamming(FFTSize, sym = True)
filtLen,filtPos,packedFilters = mfcc.melFilterMatrix(F32,freq_min, freq_high, numOfMelFilters,sample_rate,FFTSize)
dctMatrixFilters = mfcc.dctMatrix(F32,numOfDctOutputs, numOfMelFilters)

def save_precomputed_values():
    """
    Save precomputed filter and transformation matrices to text files for later use.
    """
    with open("window.txt", "w+") as f:
        f.write(", ".join(map(str, window)))
    with open("melFilterMatrix.txt", "w+") as f:
        f.write("filtLen, " + ", ".join(map(str, filtLen)) + "\n")
        f.write("filtPos, " + ", ".join(map(str, filtPos)) + "\n")
        f.write("packedFilters, " + ", ".join(map(str, packedFilters)) + "\n")
    with open("dctMatrixFilters.txt", "w+") as f:
        f.write(", ".join(map(str, dctMatrixFilters)))
    print("Saved precomputed values.")


def compute_mfcc_CMSIS(audio):
    """
    Compute MFCC features using CMSIS-DSP library.
    
    :param audio: Input audio signal as a NumPy array.
    :return: MFCC feature matrix.
    """
    mfccf32 = dsp.arm_mfcc_instance_f32()
    status = dsp.arm_mfcc_init_f32(mfccf32,FFTSize,numOfMelFilters,numOfDctOutputs,dctMatrixFilters,
        filtPos,filtLen,packedFilters,window)

    res_ar = []
    for i in range(0,int(np.floor(len(audio)/FFTSize))):
        tmp =  np.zeros(FFTSize *2)
        res = dsp.arm_mfcc_f32(mfccf32,audio[FFTSize*i:FFTSize*(i+1)],tmp)
        res_ar.append(res)

    return np.array(res_ar)

def get_from_center(audio, sr = 22600, shift = 2):
    """
    Extracts a segment of the audio centered around the middle.
    
    :param audio: Input audio array.
    :param sr: Sample rate of the audio.
    :param shift: Number of seconds around the center to keep.
    :return: Extracted audio segment.
    """
    half_duration = int(len(audio)/2)
    return audio[half_duration - shift * sr : half_duration + shift * sr]

def get_features(file_name, class_label, augmented):
    """
    Load audio, preprocess it, and extract MFCC features.
    
    :param file_name: Path to the audio file.
    :param class_label: Corresponding label of the audio.
    :param augmented: Whether to apply audio augmentations.
    :return: Extracted features and class label.
    """  
    audio,_ = librosa.load(file_name, mono=True, sr= 22600)
    audio = get_from_center(audio)
    features = []
    if augmented:
        augment1 = Compose([
            AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.055, p=0.5),
            PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
        ])
        augment2 = Compose([
            AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.055, p=0.5),
            PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
            Shift(p=0.5),
        ])
        augment3 = Compose([
            AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.055, p=0.5),
            Shift(p=0.5),
        ])
        augment4 = Compose([
            PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
            Shift(p=0.7),
        ])
    features.append(compute_mfcc_CMSIS(audio))
    return features, class_label

def reread_sound(path =  "./Dataset/Data_labels.csv"):
    """
    Load dataset metadata from a CSV file.
    
    :param path: Path to the CSV file.
    :return: Pandas DataFrame with metadata.
    """
    return pd.read_csv(path)

def process_features(metadata):
    """
    Process and extract features from a dataset based on metadata.
    
    :param metadata: DataFrame containing dataset metadata.
    :return: Dictionary with processed features and labels.
    """
    mean_audio_duration = int(89/2) * 4# Estimated duration based on experience
    max_count = 10
    total_quantity = 0
    if "split" in metadata:
        feature_list_test = []
        classes_list_test = []
        feature_list_train = []
        classes_list_train = []
        for index_num,row in tqdm(metadata.iterrows(), total = metadata.shape[0]):
            file_name = os.path.join(row["file_path"])
            class_label = row["label"]
            datas, class_label = get_features(file_name, class_label, augmented = True)
            for data in datas:
                extra_shape = mean_audio_duration-data.shape[0]
                if (extra_shape > 0):
                    try:
                        new_data = np.append(data, np.zeros(shape=(extra_shape, numOfDctOutputs), dtype=float), axis=0)
                        data = new_data
                    except:
                        print("error processing ",file_name, data.shape)
                        continue
                if extra_shape < 0:
                    data = data[:mean_audio_duration]

                total_quantity += 1
                if row["split"] == "test":
                    feature_list_test.append(data.flatten())
                    classes_list_test.append(class_label)
                elif row["split"] == "train":
                    feature_list_train.append(data.flatten())
                    classes_list_train.append(class_label)

        print(f"Correctly parsed: {total_quantity} files")
        return {"train_features":feature_list_train,
                "test_features" : feature_list_test,
                "train_classes": classes_list_train,
                 "test_classes" : classes_list_test}
    else:
        feature_list = []
        classes_list = []
        for index_num,row in tqdm(metadata.iterrows(), total = metadata.shape[0]):
            file_name = os.path.join(row["file_path"])
            class_label = row["label"]
            datas, class_label = get_features(file_name, class_label, augmented = True)
            for data in datas:
                extra_shape = mean_audio_duration-data.shape[0]
                if (extra_shape > 0):
                    try:
                        new_data = np.append(data, np.zeros(shape=(extra_shape, numOfDctOutputs), dtype=float), axis=0)
                        data = new_data
                    except:
                        print("error processing ",file_name, data.shape)
                        continue
                if extra_shape < 0:
                    data = data[:mean_audio_duration]

                total_quantity += 1
                feature_list.append(data.flatten())
                classes_list.append(class_label)

        print(f"Correctly parsed: {total_quantity} files")
        return {"features" : feature_list,
                "classes" : classes_list}

def save_features(computed_dataset, save_folder = "./Dataset/precomputed" ):
    """
    Save extracted features to disk for future use.
    
    :param computed_dataset: Dictionary containing extracted features.
    :param save_folder: Directory to store precomputed features.
    """
    if (not os.path.isdir(save_folder)): os.mkdir(save_folder)
    if "features" in computed_dataset:
        np.save(os.path.join(save_folder, "features"), computed_dataset['features'])
        np.save(os.path.join(save_folder, "classes"), computed_dataset["classes"])
    elif "train_features" in computed_dataset:
        np.save(os.path.join(save_folder, "train_features"), computed_dataset['train_features'])
        np.save(os.path.join(save_folder, "train_classes"), computed_dataset["train_classes"])
        np.save(os.path.join(save_folder, "test_features"), computed_dataset['test_features'])
        np.save(os.path.join(save_folder, "test_classes"), computed_dataset["test_classes"])

def load_features(metadata, update = False, processed_path = "./Dataset/precomputed", splitted = False):
    """
    Load precomputed features or process them if needed.
    
    :param metadata: DataFrame containing dataset metadata.
    :param update: If True, recompute features.
    :param processed_path: Path to precomputed features.
    :param splitted: Set to True if dataset is splitted.
    :return: Dictionary with features and labels.
    """
    already_serialized = os.path.isdir(processed_path)
    if not update:
        if (already_serialized) and not splitted:
            print("Features are loading from already computed dataset...")
            feature_list = np.load(os.path.join(processed_path, "features.npy"))
            print(feature_list.shape)
            classes_list = np.load(os.path.join(processed_path, "classes.npy"))
            print("Features are loaded succesfully.")
            return {"features" : feature_list,
                     "classes" : classes_list}
        elif (already_serialized) and splitted:
            print("Features are loading from already computed and splitted dataset...")
            feature_list_train = np.load(os.path.join(processed_path, "train_features.npy"))
            feature_list_test = np.load(os.path.join(processed_path, "test_features.npy"))
            classes_list_train = np.load(os.path.join(processed_path, "train_classes.npy"))
            classes_list_test = np.load(os.path.join(processed_path, "test_classes.npy"))
            return {"train_features":feature_list_train,
                "test_features" : feature_list_test,
                "train_classes": classes_list_train,
                 "test_classes" : classes_list_test}
        else:
            raise Warning(f"Serialized data in {processed_path} folder is not found. Load dataset or fix naming.")
    else:
        print(f'Total: {metadata.shape[0]} audio files')
        print("Recreating Features...")
        _processed = process_features(metadata)
        save_features(_processed)
        print("Features are processed succesfully.")
        return _processed

