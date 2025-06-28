import streamlit as st
import pandas as pd
from typing import Dict
from SPARQLWrapper import SPARQLWrapper, JSON
import re
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -------------- [TIDAK ADA PERUBAHAN DI SINI] ------------------


def show_wordcloud_for_bait(df, bait_num):
    df_bait = df[df['bait'] == bait_num]
    all_text = " ".join(df_bait['transliterasi'])
    all_text = re.sub(r'[^\w\s]', '', all_text).lower()
    if not all_text.strip():
        st.info("Belum ada data untuk bait ini.")
        return
    wordcloud = WordCloud(width=800, height=300,
                          background_color='white').generate(all_text)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)


def show_stats_for_bait(df, bait_num):
    df_bait = df[df['bait'] == bait_num]
    if df_bait.empty:
        st.info("Tidak ada data untuk bait ini.")
        return
    df_bait['panjang_baris'] = df_bait['transliterasi'].str.len()
    df_bait['jumlah_kata'] = df_bait['transliterasi'].str.split().apply(len)
    rata_panjang = df_bait['panjang_baris'].mean()
    max_panjang = df_bait['panjang_baris'].max()
    min_panjang = df_bait['panjang_baris'].min()
    rata_kata = df_bait['jumlah_kata'].mean()
    max_kata = df_bait['jumlah_kata'].max()
    min_kata = df_bait['jumlah_kata'].min()
    st.markdown(f"""
    <div style="background:#222;padding:1rem;border-radius:10px;margin-bottom:1rem;color:white">
    <b>Statistik Panjang Baris & Jumlah Kata (Bait {bait_num})</b><br>
    <ul>
      <li><b>Panjang baris (karakter)</b>:
          rata-rata: {rata_panjang:.1f}, terpendek: {min_panjang}, terpanjang: {max_panjang}
      </li>
      <li><b>Jumlah kata per baris</b>:
          rata-rata: {rata_kata:.1f}, terkecil: {min_kata}, terbesar: {max_kata}
      </li>
      <li><b>Total baris pada bait ini:</b> {len(df_bait)}
      </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


def sidebar_metadata():
    st.sidebar.markdown(
        """
        <div style="background:#232c43;padding:1.1rem 1rem;border-radius:10px;color:#f3f6fa;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,0.13);font-size:0.98rem;">
            <b>Lontar Yusup Banyuwangi</b><br>
            <ul style="padding-left:.5em; margin:0;">
                <li><b>Penyusun:</b> Wiwin Indiarti</li>
                <li><b>Penyunting:</b> Nur Hasibin, Adi Purwadi, SM Anasrullah</li>
                <li><b>Penerbit:</b> Elmatera Publishing, Yogyakarta (2018)</li>
                <li><b>ISBN:</b> 978-602-5714-34-4</li>
                <li><b>Desain:</b> Mamuloto</li>
            </ul>
            <div style="color:#c5cae9;font-size:0.92em; margin-top:0.5em;">
                <i>Sumber katalog: Perpustakaan Nasional RI</i>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Kode CSS tetap ---


st.set_page_config(
    page_title="Lontar Yusup Banyuwangi - Eksplorasi Naskah",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .transliterasi-text, .terjemahan-text, .pegon-text {
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-size: 1.22rem;
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
    .pegon-text {
        background: #f5f2e7;
        color: #141111;
        border-left: 5px solid #bc8b4b;
        font-family: 'Amiri', 'Scheherazade', 'Lateef', serif;
        direction: rtl;
        unicode-bidi: embed;
        font-size: 2em;
        word-break: break-word;
        text-align: center;
        /* biar mirip arab */
    }
    .highlight {
        background: #fff176;
        color: #111 !important;
        padding: 2px 5px;
        border-radius: 4px;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Scheherazade:wght@400;700&family=Lateef&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

SPARQL_ENDPOINT = "http://localhost:3030/lontar/sparql"

# ------------ BAGIAN INI DIEDIT UNTUK TEKS PEGON ------------


@st.cache_data
def load_data_from_fuseki():
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX : <http://yusupbanyuwangi.org/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?baris ?baitClean ?gambarClean ?translitClean ?terjemahClean ?teksPegonClean
    WHERE {
      ?baris a :BarisNaskah ;
             :mengandungAksara ?aksara ;
             :hasTransliteration ?t ;
             :hasTranslation ?terj .
      ?aksara rdf:value ?gambar ;
              :teksPegon ?teksPegon .
      ?t rdf:value ?translit .
      ?terj rdf:value ?terjemah .
      BIND(REPLACE(STR(?baris), "^.*baris", "") AS ?barisStr)
      BIND(xsd:integer(?barisStr) AS ?barisNum)
      BIND(xsd:integer(FLOOR((?barisNum - 1) / 8.0) + 1) AS ?bait)
      BIND(STR(?bait) AS ?baitClean)
      BIND(STR(?gambar) AS ?gambarClean)
      BIND(STR(?translit) AS ?translitClean)
      BIND(STR(?terjemah) AS ?terjemahClean)
      BIND(STR(?teksPegon) AS ?teksPegonClean)
    }
    ORDER BY ?barisNum
    """)
    results = sparql.query().convert()
    data = []
    for row in results["results"]["bindings"]:
        nomor = int(re.sub(r"\D", "", row['baris']['value']))
        data.append({
            'id': row['baris']['value'].split('#')[-1],
            'nomor': nomor,
            'bait': int(row['baitClean']['value']),
            'transliterasi': row['translitClean']['value'],
            'terjemahan': row['terjemahClean']['value'],
            'teks_pegon': row['teksPegonClean']['value'],
            'gambar_url': row['gambarClean']['value']
        })
    return pd.DataFrame(data)


def highlight(text, keyword):
    if not keyword:
        return text
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"<span class='highlight'>{m.group(0)}</span>", text)

# ------------ TAMPILKAN TEKS PEGON DI UI ------------


def display_baris(baris: Dict, keyword="", parent=None):
    translit = highlight(baris['transliterasi'], keyword)
    terjemah = highlight(baris['terjemahan'], keyword)
    pegon = baris['teks_pegon']

    container = parent if parent else st

    container.markdown(f"""
    <div class='baris-container' style="width: 100%; box-sizing: border-box;">
        <div class='bait-label'>Bait {baris['bait']} - Baris {baris['nomor']}</div>
        <div class='baris-grid'>
            <div class='aksara-image'>
                <img src="{baris['gambar_url']}" alt="Gambar Aksara Baris {baris['nomor']}">
            </div>
            <div class='trans-terjemah'>
                <div class='pegon-text'>
                    <strong></strong>{pegon}
                </div>
                <div class='transliterasi-text'>
                    <strong>Transliterasi:</strong><br>{translit}
                </div>
                <div class='terjemahan-text'>
                    <strong>Terjemahan:</strong><br>{terjemah}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------ [FUNGSI LAIN TIDAK ADA PERUBAHAN] ------------


def filter_dataframe(df, query, bait):
    df_filtered = df.copy()
    if query:
        mask = (
            df_filtered['transliterasi'].str.contains(query, case=False)
            | df_filtered['terjemahan'].str.contains(query, case=False)
            | df_filtered['teks_pegon'].str.contains(query, case=False)
        )
        df_filtered = df_filtered[mask]
    if bait != "Semua":
        df_filtered = df_filtered[df_filtered['bait'] == bait]
    return df_filtered


def download_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def main():
    st.markdown("""
    <div class="main-header">
        <h1>Eksplorasi Naskah Lontar Yusup Banyuwangi</h1>
        <p>Berbasis Semantic Web - RDF, SPARQL, dan Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data_from_fuseki()
    bait_list = sorted(df['bait'].unique())
    bait_min = min(bait_list)
    bait_max = max(bait_list)

    if 'bait_idx' not in st.session_state:
        st.session_state.bait_idx = bait_min

    st.sidebar.title("Navigasi Bait")
    st.sidebar.markdown(f"**Bait Saat Ini: {st.session_state.bait_idx}**")

    col_prev, col_next = st.sidebar.columns([1, 1])
    with col_prev:
        if st.button("⬅️ Prev", key="prev_bait") and st.session_state.bait_idx > bait_min:
            st.session_state.bait_idx -= 1
            st.rerun()
    with col_next:
        if st.button("Next ➡️", key="next_bait") and st.session_state.bait_idx < bait_max:
            st.session_state.bait_idx += 1
            st.rerun()

    selected_bait = st.sidebar.number_input(
        "Atau pilih bait langsung:", min_value=bait_min, max_value=bait_max,
        value=st.session_state.bait_idx, step=1, key="bait_picker"
    )
    if selected_bait != st.session_state.bait_idx:
        st.session_state.bait_idx = selected_bait
        st.rerun()

    query = st.text_input(
        "🔍 Cari kata dalam Pegon, transliterasi, atau terjemahan...", placeholder="Masukkan kata kunci"
    )

    if not query:
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("📊 Word Cloud kata terpopuler pada bait ini", expanded=True):
                show_wordcloud_for_bait(df, st.session_state.bait_idx)
        with col2:
            with st.expander("📈 Statistik panjang baris & jumlah kata pada bait ini", expanded=True):
                show_stats_for_bait(df, st.session_state.bait_idx)

    st.markdown("""
    <div style="background:#fff3cd; color:#664d03; border:1px solid #ffecb5; border-radius:8px; padding:12px; margin-top:1rem; margin-bottom:1rem;">
    <b>Catatan:</b> Teks Pegon yang ditampilkan adalah hasil konversi otomatis dari gambar aksara ke font menggunakan 
    <a href="https://pegonku.vercel.app/indo-pegon" target="_blank">PegonKu</a>. Hasil konversi ini belum 100% akurat dan mungkin ada kesalahan atau variasi dalam penulisan.
    <br>
    </div>
    """, unsafe_allow_html=True)

    if query:
        filtered_df = filter_dataframe(df, query, "Semua")
    else:
        filtered_df = df[df['bait'] == st.session_state.bait_idx].head(8)

    st.sidebar.markdown("### Ekspor Hasil")
    st.sidebar.download_button(
        label="⬇️ Download CSV",
        data=download_csv(filtered_df),
        file_name=f"lontar_bait{st.session_state.bait_idx}.csv",
        mime="text/csv"
    )
    sidebar_metadata()

    rows = filtered_df.to_dict('records')

    for i in range(0, len(rows), 2):
        cols = st.columns(2)
        with cols[0]:
            display_baris(rows[i], keyword=query, parent=st)
        if i + 1 < len(rows):
            with cols[1]:
                display_baris(rows[i+1], keyword=query, parent=st)


if __name__ == "__main__":
    main()
