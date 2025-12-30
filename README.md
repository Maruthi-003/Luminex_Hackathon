# Luminex_Hackathon
Luminex Hackathon Movie Recommender

Overview
Luminex is a content based movie recommendation system developed for the Luminex Hackathon. The application recommends movies based on genre relevance and rating signals and presents results through a clean OTT style user interface.

Recommendation Approach
The deployed system uses content based filtering. Movies are matched using genre overlap and ranked using a weighted relevance score combined with movie ratings. This approach was selected for its interpretability and scalability in the absence of user interaction data.

Machine Learning Exploration
In addition to the deployed logic, the project includes experimental exploration of machine learning techniques inside the Jupyter notebook. This includes K Nearest Neighbors for movie similarity and Matrix Factorization using Singular Value Decomposition on genre feature vectors. These models were explored and evaluated but not deployed due to computational cost and limited performance improvement for this dataset.

Tech Stack
Python
Streamlit
Pandas
Scikit learn
Cosine similarity
KNN and SVD for experimentation
TMDB API for movie posters

Data Handling
The movie dataset is large and is loaded from Hugging Face to support cloud deployment. Streamlit caching is used to optimize performance.

Project Structure
app.py contains the Streamlit application
Lumi_hack.ipynb contains ML experimentation
requirements.txt contains dependencies
README.md contains project documentation

Deployment Notes
The application is deployed using Streamlit Cloud. Large datasets are accessed remotely and memory safe query based similarity is used.
