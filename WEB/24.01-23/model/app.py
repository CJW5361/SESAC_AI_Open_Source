from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# 모델 로드
model = tf.keras.models.load_model('keras_model.h5')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 업로드된 파일 처리
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # 이미지를 모델 입력 형식으로 변환
            img = image.load_img(uploaded_file, target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.0

            # 모델 예측
            prediction = model.predict(img)
            class_names = ['가위', '바위', '보']
            predicted_class = class_names[np.argmax(prediction)]
            confidence = np.max(prediction) * 100

            return render_template('result.html', predicted_class=predicted_class, confidence=confidence)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
