import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.parse import urlparse

url_data = pd.read_csv('dataset.csv')
def extract_features(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc, parsed_url.path

url_data['netloc'], url_data['path'] = zip(*url_data['url'].map(extract_features))

X = url_data[['netloc', 'path']]
y = url_data['label']

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
X = vectorizer.fit_transform(X['netloc'] + X['path']).tocsc()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_classifier = RandomForestClassifier(n_estimators=10, random_state=42)
rf_classifier.fit(X_train, y_train)

def is_safe(url):
    netloc, path = extract_features(url)
    vectorized_url = vectorizer.transform([netloc + path]).tocsc()
    prediction = rf_classifier.predict(vectorized_url)
    return "Safe" if prediction[0] == 1 else "Malicious"