from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.parse import urlparse
import joblib
import pandas as pd

app = Flask(__name__)

rf_classifier = joblib.load('random_forest_model.pkl')

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)

url_data = pd.read_csv('dataset.csv')
url_data = url_data.sample(n=100000, random_state=42)

def extract_features(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc, parsed_url.path

url_data['netloc'], url_data['path'] = zip(*url_data['url'].map(extract_features))

X_train = vectorizer.fit_transform(url_data['netloc'] + url_data['path']).tocsc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    if request.method == 'POST':
        input_text = request.form['inputText']

        def is_safe(url):
            try:
                netloc, path = extract_features(url)
                vectorized_url = vectorizer.transform([netloc + path]).tocsc()
                prediction = rf_classifier.predict(vectorized_url)
                return "Safe" if prediction[0] == 1 else "Malicious"
            except Exception as e:
                return f"Error: {e}"

        output = is_safe(input_text)
        return render_template('index.html', input_text=input_text, output_text=output)

if __name__ == '__main__':
    app.run(debug=True)
