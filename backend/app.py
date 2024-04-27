import json
import re 
import ast
import os
from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import nltk
from helpers.__init__ import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Set up NLTK
nltk.download('punkt')

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'init.json')

# Assuming your JSON data is stored in a file named 'init.json'
with open(json_file_path, 'r') as file:
    df = preprocess(json_file_path)
    inv_idx = token_inverted_index(df)
    idf = compute_idf(inv_idx, len(df))
    norms = compute_doc_norms(inv_idx, idf, len(df))

# Define SVD parameters
n_components = 100  # Adjust as needed
random_state = 42  # For reproducibility

# Preprocess text for SVD
text_corpus = df['Review'].apply(lambda x: ' '.join(x))

# Compute TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(text_corpus)

# Apply SVD
svd = TruncatedSVD(n_components=n_components, random_state=random_state)
svd_matrix = svd.fit_transform(tfidf_matrix)

app = Flask(__name__)
CORS(app)

def calculate_svd_similarity(query, doc_id):
    query_representation = svd.transform(tfidf_vectorizer.transform([query]))[0]
    doc_representation = svd_matrix[doc_id]
    return np.dot(query_representation, doc_representation) / (np.linalg.norm(query_representation) * np.linalg.norm(doc_representation))

def json_search(query):
    query = str(query)
    sorted_matches = index_search(query, inv_idx, idf, norms)
    final_list = []
    for sim, docID in sorted_matches[:10]:
        game_data = df.loc[df["ID"] == int(docID)]
        game_data.drop("Review", axis=1, inplace=True)
        game_data["Similarity"] = sim

        # Calculate SVD similarity and include it in the sorting
        svd_similarity = calculate_svd_similarity(query, int(docID))
        final_list.append((svd_similarity, game_data.iloc[0].to_dict()))

    # Sort final list based on SVD similarity
    final_list.sort(reverse=True, key=lambda x: x[0])

    if len(final_list) == 0:
        final_list.append({"Game": "No results. Please try a different query.", "Score": 0})

    return json.dumps([game_dict for _, game_dict in final_list])

@app.route("/")
def home():
    return render_template('base.html', title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return json_search(text)

if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
