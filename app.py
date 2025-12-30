import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Cine Match – Smart Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS (UI MAGIC)
# -------------------------------
st.markdown("""
<style>

/* =====================================================
   GLOBAL THEME
===================================================== */
html, body, [class*="css"] {
    background-color: #0b0b0b !important;
    color: #ffffff !important;
    font-family: 'Segoe UI', sans-serif;
}

/* =====================================================
   HERO SECTION
===================================================== */
.big-title {
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #e50914, #f5c518);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeInDown 1s ease;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #b3b3b3;
    margin-bottom: 30px;
    animation: fadeIn 1.2s ease;
}

/* =====================================================
   INPUTS
===================================================== */
input, textarea {
    background-color: #141414 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #333 !important;
    padding: 10px !important;
}

/* =====================================================
   BUTTON
===================================================== */
.stButton > button {
    background: linear-gradient(90deg, #e50914, #b20710);
    color: white;
    font-size: 18px;
    font-weight: 700;
    border-radius: 30px;
    padding: 0.6em 2.2em;
    border: none;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 25px rgba(229,9,20,0.7);
}

/* =====================================================
   HORIZONTAL SCROLL ROW (OTT STYLE)
===================================================== */
.movie-scroll {
    display: flex;
    gap: 32px;
    overflow-x: auto;
    padding: 25px 10px 35px 10px;
    scroll-behavior: smooth;
    animation: fadeInUp 0.8s ease;
}

/* Scrollbar (subtle, premium) */
.movie-scroll::-webkit-scrollbar {
    height: 8px;
}

.movie-scroll::-webkit-scrollbar-track {
    background: transparent;
}

.movie-scroll::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
}

.movie-scroll::-webkit-scrollbar-thumb:hover {
    background: rgba(255,255,255,0.35);
}

/* =====================================================
   MOVIE CARD (NETFLIX / PRIME STYLE)
===================================================== */
.movie-card {
    min-width: 280px;
    max-width: 280px;
    background: linear-gradient(180deg, #181818, #121212);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0,0,0,0.85);
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
}

/* Hover pop */
.movie-card:hover {
    transform: translateY(-12px) scale(1.06);
    box-shadow: 0 20px 45px rgba(229,9,20,0.45);
}

/* Glow sweep */
.movie-card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 22px;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(229,9,20,0.25),
        transparent
    );
    opacity: 0;
    transition: opacity 0.3s ease;
}

.movie-card:hover::before {
    opacity: 1;
}

/* =====================================================
   POSTER IMAGE EFFECT
===================================================== */
.movie-card img {
    width: 100% !important;
    max-width: 220px;
    border-radius: 14px;
    margin-bottom: 14px;
    transition: transform 0.4s ease;
}

.movie-card:hover img {
    transform: scale(1.08);
}

/* =====================================================
   TEXT STYLING
===================================================== */
.movie-card h3 {
    font-size: 16px;
    font-weight: 700;
    margin-top: 10px;
}

.movie-card p {
    font-size: 13px;
    color: #b3b3b3;
}

/* =====================================================
   METRICS STYLE
===================================================== */
[data-testid="metric-container"] {
    background: #141414;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.7);
    animation: fadeIn 1s ease;
}

/* =====================================================
   PROGRESS BAR
===================================================== */
.stProgress > div > div {
    background: linear-gradient(90deg, #e50914, #f5c518);
}

/* =====================================================
   ANIMATIONS
===================================================== */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* =====================================================
   FOOTER HIDE
===================================================== */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# LOAD PKL DATA
# -------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    url = "https://huggingface.co/datasets/Maruthi333/Movies.csv/resolve/main/Movies.csv"
    
    df = pd.read_csv(url)

    # preprocessing (unchanged)
    df["title"] = df["title"].str.lower().str.strip()
    df["genres"] = df["genres"].fillna("").str.lower().str.strip()
    df["vote_average"] = df["vote_average"].astype(float)

    return df


df = load_data()

# -------------------------------
# TMDB CONFIG
# -------------------------------
TMDB_API_KEY = "6a9a5e8b756af2981b8623d6b2a60ee1"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

def fetch_poster(title):
    try:
        r = requests.get(
            SEARCH_URL,
            params={"api_key": TMDB_API_KEY, "query": title},
            timeout=5
        )
        data = r.json()
        if data.get("results"):
            poster = data["results"][0].get("poster_path")
            if poster:
                return IMAGE_BASE_URL + poster
    except:
        pass
    return None

# -------------------------------
# RECOMMENDER LOGIC (UNCHANGED)
# -------------------------------
def filter_by_genres_strict(user_input):
    user_genres = {
        g.strip()
        for g in user_input.replace("and", ",").split(",")
        if g.strip()
    }

    filtered = df[
        df["genres"].apply(lambda g: all(ug in g for ug in user_genres))
    ]
    return filtered, user_genres

def compute_relevance(row, user_genres):
    movie_genres = {g.strip() for g in row["genres"].split(",")}
    matched = len(user_genres & movie_genres)

    intent_score = matched / len(user_genres)
    coverage_score = matched / len(movie_genres)

    return 0.7 * intent_score + 0.3 * coverage_score

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<div class='big-title'>🎬 CINE MATCH</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Intelligent Movie Recommendation Engine</div>", unsafe_allow_html=True)
st.write("")

# -------------------------------
# INPUT SECTION
# -------------------------------
col1, col2 = st.columns([3,1])

with col1:
    user_input = st.text_input(
        "Enter a Movie Name or Genre Combination",
        placeholder="example: action, thriller or inception"
    )

with col2:
    top_n = st.slider("Results", 1, 10, 5)

# -------------------------------
# RECOMMEND BUTTON
# -------------------------------
if st.button(" Recommend Movies"):
    if not user_input.strip():
        st.warning("Please enter a movie name or genres")
    else:
        with st.spinner("Analyzing preferences..."):
            user_input = user_input.lower().strip()

            if user_input in df["title"].values:
                base_genres = df[df["title"] == user_input]["genres"].values[0]
                filtered, user_genres = filter_by_genres_strict(base_genres)
                display_title = f"Based on: {user_input.title()}"
            else:
                filtered, user_genres = filter_by_genres_strict(user_input)
                display_title = f"Genres: {user_input.title()}"

            if filtered.empty:
                st.error("No movies found matching your input.")
            else:
                filtered = filtered.copy()
                filtered["relevance"] = filtered.apply(
                    lambda row: compute_relevance(row, user_genres),
                    axis=1
                )

                filtered["final_score"] = (
                    0.75 * filtered["relevance"] +
                    0.25 * (filtered["vote_average"] / 10)
                )

                results = filtered.sort_values(
                    by="final_score",
                    ascending=False
                ).head(top_n)

                # -------------------------------
                # METRICS
                # -------------------------------
                m1, m2, m3 = st.columns(3)
                m1.metric(" Avg Relevance", f"{results['relevance'].mean()*100:.1f}%")
                m2.metric("⭐ Avg Rating", f"{results['vote_average'].mean():.2f}/10")
                m3.metric(" Movies Found", len(results))

                st.markdown(f"## {display_title}")

                # -------------------------------
                # MOVIE CARDS
                # -------------------------------
                cols = st.columns(top_n)
                for col, (_, row) in zip(cols, results.iterrows()):
                    with col:
                        poster = fetch_poster(row["title"])
                        st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                        if poster:
                            st.image(poster,width=100)
                        st.markdown(f"### {row['title'].title()}")
                        st.caption(row["genres"])
                        st.progress(int(row["final_score"] * 100))
                        st.markdown(
                            f"⭐ **{row['vote_average']}** |  **{int(row['relevance']*100)}%**"
                        )
                        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.write("")
st.markdown(
    "<p style='text-align:center;color:#aaa;'>Built for ML Hackathon • Movie Recommender</p>",
    unsafe_allow_html=True
)