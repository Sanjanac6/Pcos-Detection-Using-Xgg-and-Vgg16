import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import joblib
import tensorflow.keras as keras
from tensorflow.keras.applications.vgg16 import VGG16
import numpy as np
import xgboost
import torch

hide_streamlit_style = """
            <style>
            #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
    <style>
        @keyframes fadeInOut {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
        .animated-header {
            text-align: center;
            color: red;
            font-family: Arial, sans-serif; /* Change font family */
            animation: fadeInOut 3s linear infinite;
        }
    </style>
    <h1 class="animated-header">PCOS DETECTION</h1>
""", unsafe_allow_html=True)




def main():
    candidate_labels = ["PCOS", "NON-PCOS", "High Risk of PCOS", "PCOS along with high possibility of diabetes"]
    file_uploaded = st.file_uploader('Upload an Ultrasound Image...', type='jpg')
    # user_input = st.text_area("Enter your symptoms here...", height = 300)
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels = 4)
    # model.load_state_dict(torch.load('pytorch_model.bin'))
    # input_ids = tokenizer.encode(user_input, add_special_tokens = True)
    # with torch.no_grad() :
    #     logits  = model(torch.tensor([input_ids]))[0]
    # if user_input != '' :
    #     predicted_class  = torch.argmax(logits, dim = -1).item()
    #     predicted_label = candidate_labels[predicted_class]
    #     # st.write('Prediction : {}'.format(predicted_label))
    if file_uploaded is not None:
        image = Image.open(file_uploaded)
        st.write("Uploaded Ultrasound.")
        figure = plt.figure()
        plt.imshow(image)
        plt.axis('off')
        st.pyplot(figure)
        result = predict_class(image)
        st.write('Prediction : {}'.format(result))
        if result == 'PCOS':
            st.write('Kindly consult a doctor as soon as possible.')
        else:
            st.write('There is no need to worry but if symptoms appear, consult a doctor as soon as possible.')


def predict_class(rgb_image):
    with st.spinner('Loading, please be patient...'):
        model = joblib.load('xray.pkl')
        vggmodel = VGG16(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
        for layer in vggmodel.layers:
            layer.trainable = False

    label = {0: 'PCOS', 1: 'NORMAL'}

    # Resize the RGB image to (256, 256)
    test_image = keras.preprocessing.image.array_to_img(rgb_image, data_format='channels_last')
    test_image = test_image.resize((256, 256))

    # Convert the image to an array
    test_image = keras.preprocessing.image.img_to_array(test_image)

    # Normalize the image
    test_image /= 255.0

    # Expand the dimensions to match the model input shape
    test_image = np.expand_dims(test_image, axis=0)

    # Use VGG16 for feature extraction
    feature_extractor = vggmodel.predict(test_image)

    # Reshape the features
    features = feature_extractor.reshape(feature_extractor.shape[0], -1)

    # Make predictions
    prediction = model.predict(features)[0]
    final = label[prediction]

    return final


footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa; /* Light gray background */
        color: #333; /* Dark text color */
        text-align: center;
        padding: 10px 0; /* Add padding */
        box-shadow: 0px -2px 6px rgba(0, 0, 0, 0.1); /* Add shadow */
    }

    .footer a {
        color: #007bff; /* Blue link color */
        text-decoration: none;
    }

    .footer a:hover {
        color: #0056b3; /* Darker blue on hover */
        text-decoration: underline;
    }
</style>

<div class="footer">
    <p>PCOS Detection Web App</p>
    
</div>
"""


st.markdown(footer, unsafe_allow_html=True)
if __name__ == '__main__':
    main()