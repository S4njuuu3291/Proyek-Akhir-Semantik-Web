import streamlit as st
import pandas as pd
from typing import List, Dict
import base64

# Konfigurasi halaman
st.set_page_config(
    page_title="Lontar Yusup Banyuwangi - Eksplorasi Naskah",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .baris-container {
        border: 2px solid #e1e5e9;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .aksara-image {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #dee2e6;
    }
    
    .transliterasi-text {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
    }
    
    .terjemahan-text {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
        margin: 0.5rem 0;
        font-family: 'Arial', sans-serif;
        font-size: 1rem;
    }
    
    .copy-button {
        background: #28a745;
        color: white;
        border: none;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .filter-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Data dummy untuk demo
@st.cache_data
def load_dummy_data():
    """Memuat data dummy untuk demonstrasi"""
    data = []
    sample_texts = [
        ("يوسف نبي أولى", "Yusuf nabi ula", "Yusuf adalah nabi utama"),
        ("والله أعلم بالصواب", "wallahu a'lam bil sawab", "Dan Allah lebih mengetahui yang benar"),
        ("بسم الله الرحمن الرحيم", "bismillahi rahmani rahim", "Dengan nama Allah Yang Maha Pengasih lagi Maha Penyayang"),
        ("الحمد لله رب العالمين", "alhamdulillahi rabbil alamin", "Segala puji bagi Allah Tuhan semesta alam"),
        ("إياك نعبد وإياك نستعين", "iyyaka na'budu wa iyyaka nasta'in", "Hanya kepada-Mu kami menyembah dan hanya kepada-Mu kami memohon pertolongan"),
        ("اهدنا الصراط المستقيم", "ihdinash shiratal mustaqim", "Tunjukilah kami jalan yang lurus"),
        ("صراط الذين أنعمت عليهم", "shiratal lazina an'amta alaihim", "Jalan orang-orang yang telah Engkau beri nikmat"),
        ("غير المغضوب عليهم", "ghairi maghdubi alaihim", "Bukan jalan mereka yang dimurkai"),
        ("ولا الضالين", "wa lad dallin", "Dan bukan pula jalan mereka yang sesat"),
        ("آمين يا رب العالمين", "amin ya rabbal alamin", "Amin ya Tuhan semesta alam")
    ]
    
    for i in range(96):
        # Cycle through sample texts
        sample = sample_texts[i % len(sample_texts)]
        data.append({
            'id': f'baris{i+1:03d}',
            'nomor': i + 1,
            'aksara_pegon': sample[0],
            'transliterasi': sample[1],
            'terjemahan': sample[2],
            'gambar_url': f"https://via.placeholder.com/400x80/2196F3/FFFFFF?text=Baris+{i+1}"
        })
    
    return pd.DataFrame(data)

def create_copy_button(text: str, button_id: str) -> str:
    """Membuat tombol copy dengan JavaScript"""
    return f"""
    <button class="copy-button" onclick="navigator.clipboard.writeText('{text}').then(function() {{
        alert('Teks berhasil disalin!');
    }})">
        📋 Copy
    </button>
    """

def display_baris_naskah(baris_data: Dict, show_images: bool = True, show_transliterasi: bool = True, show_terjemahan: bool = True):
    """Menampilkan satu baris naskah dalam container yang stylish"""
    
    with st.container():
        st.markdown(f"""
        <div class="baris-container">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">
                📜 Baris {baris_data['nomor']} - ID: {baris_data['id']}
            </h4>
        """, unsafe_allow_html=True)
        
        # Gambar aksara (jika diaktifkan)
        if show_images:
            st.markdown(f"""
            <div class="aksara-image">
                <h5 style="color: #495057; margin-bottom: 1rem;">🖼️ Aksara Arab Pegon</h5>
                <img src="{baris_data['gambar_url']}" style="max-width: 100%; height: auto; border-radius: 5px;">
                <p style="margin-top: 0.5rem; font-style: italic; color: #6c757d;">
                    Teks Asli: {baris_data['aksara_pegon']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Transliterasi (jika diaktifkan)
        if show_transliterasi:
            st.markdown(f"""
            <div class="transliterasi-text">
                <strong>🔤 Transliterasi Latin:</strong><br>
                {baris_data['transliterasi']}
                {create_copy_button(baris_data['transliterasi'], f"trans_{baris_data['id']}")}
            </div>
            """, unsafe_allow_html=True)
        
        # Terjemahan (jika diaktifkan)
        if show_terjemahan:
            st.markdown(f"""
            <div class="terjemahan-text">
                <strong>🇮🇩 Terjemahan Bahasa Indonesia:</strong><br>
                {baris_data['terjemahan']}
                {create_copy_button(baris_data['terjemahan'], f"terj_{baris_data['id']}")}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Header utama
    st.markdown("""
    <div class="main-header">
        <h1>📜 Lontar Yusup Banyuwangi</h1>
        <h3>Sistem Eksplorasi Naskah Berbasis Semantic Web</h3>
        <p>Transliterasi dan Terjemahan Naskah Tradisional Banyuwangi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_dummy_data()
    
    # Sidebar untuk kontrol dan statistik
    with st.sidebar:
        st.markdown("## 🎛️ Kontrol Tampilan")
        
        # Toggle untuk tampilan
        show_images = st.checkbox("🖼️ Tampilkan Gambar Aksara", value=True)
        show_transliterasi = st.checkbox("🔤 Tampilkan Transliterasi", value=True)
        show_terjemahan = st.checkbox("🇮🇩 Tampilkan Terjemahan", value=True)
        
        st.markdown("---")
        
        # Statistik
        st.markdown("## 📊 Statistik Naskah")
        
        total_baris = len(df)
        st.markdown(f"""
        <div class="stats-card">
            <h4>{total_baris}</h4>
            <p>Total Baris Naskah</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter berdasarkan bahasa
        st.markdown("## 🌐 Info Bahasa")
        st.info("**Bahasa Asli:** Jawa (Dialek Osing)")
        st.info("**Aksara:** Arab Pegon")
        st.info("**Transliterasi:** Latin")
        st.info("**Terjemahan:** Bahasa Indonesia")
        
        st.markdown("---")
        st.markdown("## ℹ️ Tentang Naskah")
        st.markdown("""
        Lontar Yusup Banyuwangi adalah naskah tradisional yang memuat nilai-nilai religius 
        dan kearifan lokal masyarakat Banyuwangi. Naskah ini ditulis dalam bahasa Jawa 
        dialek Osing dengan aksara Arab Pegon.
        """)
    
    # Area pencarian dan filter
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Cari dalam transliterasi atau terjemahan:",
            placeholder="Masukkan kata kunci untuk pencarian...",
            help="Pencarian akan dilakukan pada teks transliterasi dan terjemahan"
        )
    
    with col2:
        # Dropdown untuk sorting
        sort_option = st.selectbox(
            "📋 Urutkan berdasarkan:",
            ["Nomor Baris (Asc)", "Nomor Baris (Desc)"],
            help="Pilih cara pengurutan data"
        )
    
    with col3:
        # Items per page
        items_per_page = st.selectbox(
            "📄 Baris per halaman:",
            [5, 10, 20, 50, "Semua"],
            index=1,
            help="Jumlah baris yang ditampilkan per halaman"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter data berdasarkan pencarian
    filtered_df = df.copy()
    
    if search_query:
        mask = (
            filtered_df['transliterasi'].str.contains(search_query, case=False, na=False) |
            filtered_df['terjemahan'].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
        
        if len(filtered_df) == 0:
            st.warning(f"🔍 Tidak ditemukan hasil untuk pencarian: **{search_query}**")
            st.info("💡 Tips: Coba gunakan kata kunci yang lebih umum atau periksa ejaan.")
            return
        else:
            st.success(f"🎯 Ditemukan **{len(filtered_df)}** hasil untuk pencarian: **{search_query}**")
    
    # Sorting
    if sort_option == "Nomor Baris (Desc)":
        filtered_df = filtered_df.sort_values('nomor', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('nomor', ascending=True)
    
    # Pagination
    if items_per_page != "Semua":
        total_items = len(filtered_df)
        total_pages = (total_items - 1) // items_per_page + 1
        
        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                current_page = st.number_input(
                    f"Halaman (1-{total_pages}):",
                    min_value=1,
                    max_value=total_pages,
                    value=1,
                    help=f"Navigasi halaman - Total: {total_pages} halaman"
                )
            
            start_idx = (current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            filtered_df = filtered_df.iloc[start_idx:end_idx]
            
            # Info pagination
            st.info(f"📄 Menampilkan halaman {current_page} dari {total_pages} ({len(filtered_df)} baris)")
    
    # Tampilkan hasil
    if len(filtered_df) > 0:
        st.markdown("---")
        st.markdown("## 📜 Isi Naskah")
        
        # Progress bar untuk loading visual
        progress_bar = st.progress(0)
        
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            # Update progress
            progress = (idx + 1) / len(filtered_df)
            progress_bar.progress(progress)
            
            # Tampilkan baris
            display_baris_naskah(
                row.to_dict(),
                show_images=show_images,
                show_transliterasi=show_transliterasi,
                show_terjemahan=show_terjemahan
            )
        
        # Clear progress bar
        progress_bar.empty()
        
        # Summary di akhir
        st.markdown("---")
        st.markdown("### 📊 Ringkasan Tampilan")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Ditampilkan", len(filtered_df))
        
        with col2:
            st.metric("Dari Total", len(df))
        
        with col3:
            if search_query:
                st.metric("Hasil Pencarian", len(filtered_df))
            else:
                st.metric("Mode", "Tampil Semua")
        
        with col4:
            st.metric("Status", "✅ Berhasil")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
        <h4>🎓 Proyek Akhir Semantic Web</h4>
        <p><strong>Kelompok:</strong> Raihan Muhammad Fuad Amin, Sanjukin Pinem, Dzakwan Fadhlullah</p>
        <p><strong>Universitas Padjadjaran | <strong>Semantic Web</p>
        <p style="margin-top: 1rem; font-style: italic; color: #6c757d;">
            "Melestarikan budaya tradisional melalui teknologi semantic web"
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()