# Plant Disease Detection Architecture

## System Architecture

                +----------------------+
                |  PlantVillage Dataset |
                +----------+-----------+
                           |
                           |
                           ▼
                 Image Preprocessing
                           |
                           ▼
                Data Augmentation
                           |
                           ▼
           Train / Validation / Test Split
                           |
                           ▼
             MobileNetV2 Transfer Learning
                           |
                           ▼
                  Fine Tuning Layers
                           |
                           ▼
                  Softmax Classification
                           |
                           ▼
                 Disease Prediction
                           |
                           ▼
               Streamlit Web Application

------------------------------------------------------------

## Components

### Dataset

Contains healthy and diseased plant leaf images.

### Image Preprocessing

- Resize Images
- Normalize Pixel Values
- Label Encoding

### Data Augmentation

- Rotation
- Zoom
- Horizontal Flip
- Width Shift
- Height Shift

### Deep Learning Model

Transfer Learning

Base Model

MobileNetV2

Classifier

GlobalAveragePooling2D

↓

Dense Layer

↓

Dropout

↓

Output Layer (Softmax)

### Evaluation

- Accuracy
- Loss
- Precision
- Recall
- F1 Score
- Confusion Matrix

### Deployment

Streamlit

Image Upload

↓

Prediction

↓

Display Disease Name

↓

Display Confidence