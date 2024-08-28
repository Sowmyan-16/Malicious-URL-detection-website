import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from urllib.parse import urlparse
import joblib
from sklearn.utils import shuffle

# Load and preprocess the dataset
url_data = pd.read_csv('dataset.csv')

# Shuffling the dataset to improve randomness
url_data = shuffle(url_data, random_state=42)

def extract_features(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc, parsed_url.path

url_data['netloc'], url_data['path'] = zip(*url_data['url'].map(extract_features))

# Split data into features (X) and labels (y)
X = url_data[['netloc', 'path']]
y = url_data['label']

# Vectorize features
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
X = vectorizer.fit_transform(X['netloc'] + X['path']).tocsc()

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest classifier with fewer estimators
rf_classifier = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1) # Utilize all CPU cores
rf_classifier.fit(X_train, y_train)

# Calculate model accuracy on the test set
y_pred = rf_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Save trained model to a file
joblib.dump(rf_classifier, 'random_forest_model2.pkl')
