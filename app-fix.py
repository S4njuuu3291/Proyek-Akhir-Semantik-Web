import streamlit as st
import pandas as pd
from typing import Dict

# Konfigurasi halaman
st.set_page_config(
    page_title="Lontar Yusup Banyuwangi - Eksplorasi Naskah",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling kreatif untuk dark mode
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .baris-container {
        background: #1f1f1f;
        border: 1px solid #444;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .bait-label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .baris-grid {
        display: flex;
        gap: 1.2rem;
        flex-wrap: wrap;
    }
    .aksara-image img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        border: 1px solid #333;
    }
    .trans-terjemah {
        flex: 1;
        min-width: 260px;
    }
    .aksara-image {
        flex: 1;
        min-width: 300px;
        text-align: center;
    }
    .transliterasi-text, .terjemahan-text {
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .transliterasi-text {
        background: #0d47a1;
        color: white;
        border-left: 5px solid #1976d2;
    }
    .terjemahan-text {
        background: #4a148c;
        color: white;
        border-left: 5px solid #7b1fa2;
    }
</style>
""", unsafe_allow_html=True)

# Slot endpoint SPARQL
SPARQL_ENDPOINT = "http://localhost:3030/lontar/sparql"

# Dummy data


@st.cache_data
def load_dummy_data():
    data = []
    for i in range(96):
        bait = (i // 8) + 1
        data.append({
            'id': f'baris{i+1:03d}',
            'nomor': i + 1,
            'bait': bait,
            'transliterasi': f"Contoh transliterasi baris {i+1}",
            'terjemahan': f"Contoh terjemahan baris {i+1}",
            'gambar_url': f"https://via.placeholder.com/600x100?text=Baris+{i+1}"
        })
    return pd.DataFrame(data)


def display_baris(baris: Dict):
    st.markdown(f"""
    <div class='baris-container'>
        <div class='bait-label'>Bait {baris['bait']} • Baris {baris['nomor']}</div>
        <div class='baris-grid'>
            <div class='aksara-image'>
                <img src="{baris['gambar_url']}" alt="Gambar Aksara Baris {baris['nomor']}">
            </div>
            <div class='trans-terjemah'>
                <div class='transliterasi-text'>
                    <strong>Transliterasi:</strong><br>{baris['transliterasi']}
                </div>
                <div class='terjemahan-text'>
                    <strong>Terjemahan:</strong><br>{baris['terjemahan']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    st.markdown("""
    <div class="main-header">
        <h1>Eksplorasi Naskah Lontar Yusup Banyuwangi</h1>
        <p>Berbasis Semantic Web - RDF, SPARQL, dan Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_dummy_data()

    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input(
            "🔍 Cari kata dalam transliterasi atau terjemahan...", placeholder="Masukkan kata kunci")
    with col2:
        bait_options = ["Semua"] + sorted(df['bait'].unique())
        selected_bait = st.selectbox(
            "📖 Filter berdasarkan bait", options=bait_options)

    if query:
        df = df[df['transliterasi'].str.contains(
            query, case=False) | df['terjemahan'].str.contains(query, case=False)]

    if selected_bait != "Semua":
        df = df[df['bait'] == selected_bait]

    for _, row in df.iterrows():
        display_baris(row)


if __name__ == "__main__":
    main()
