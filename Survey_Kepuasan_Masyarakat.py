import streamlit as st
import pandas as pd
from prosesskm import buat_dataframe_hasil, grafik, korelasi_spearman
from filterskm import filter_data2

st.set_page_config(page_title="SKM Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("📊 Dashboard Indeks Survei Kepuasan Masyarakat")

with open("data/template_file.xlsx", "rb") as file:
    file_data = file.read()

# Tombol download
st.download_button(
    label="📥 Download Template Excel SKM",
    data=file_data,
    file_name="template_file.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Upload file
filenames = []
uploaded_files = st.file_uploader("Upload Excel file")

if not uploaded_files:
    st.info(" Silakan unggah file Excel/CSV, nilai yang diterima hanya dalam range 1-4", icon="ℹ️")
    st.stop()
else:
    st.subheader("📋 DATA") 
    df = pd.read_excel(uploaded_files, header=[0,1])
    df.columns = [col[1] if "Unnamed" not in col[1] else col[0]for col in df.columns]
    st.dataframe(df, width='stretch', hide_index=True)

    st.divider()

    opsi = list(df.columns[6:7]) 
    opsi.append("GLOBAL")         

    pilih_elemen1 = st.selectbox(
        "Lihat Berdasarkan",
        opsi,
        index=1, 
    )
    
    if not pilih_elemen1:
        st.stop()

    elif pilih_elemen1 == "GLOBAL":
        # hitung hasil
        df_hasil, indeks_up, iup_konversi, mutu, kinerja, Nilai_Konversi_Per_Unsur = buat_dataframe_hasil(df)

        st.subheader("📈 Hasil Perhitungan")
        df_hasil.index = range(1, len(df_hasil) + 1)
        st.dataframe(df_hasil, width='stretch', hide_index=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Indeks Unit Pelayanan", value=round(indeks_up, 2))
        with col2:
            st.metric(label="Nilai Unit Pelayanan", value=round(iup_konversi, 2))
        with col3:
            st.metric(label="Mutu", value=(mutu))
        with col4:
            st.metric(label="Kinerja", value=(kinerja))

        st.subheader("📈 Karakteristik Responden")
        fig_jk, fig_usia, fig_pd, fig_pk, fig_jl = grafik(df)
        cols1, cols2, cols3 = st.columns(3)                  
        with cols1:
            st.plotly_chart(fig_pd, use_container_width=True)
        with cols2: 
            st.plotly_chart(fig_jk, use_container_width=True)
        with cols3:
            st.plotly_chart(fig_usia, use_container_width=True)


        cols4, cols5 = st.columns(2)
        with cols4:
            st.plotly_chart(fig_pk)
        with cols5:
            st.plotly_chart(fig_jl)

        plt1, plt2 = korelasi_spearman(df, Nilai_Konversi_Per_Unsur)
        cols6, cols7 = st.columns(2)
        with cols6:
            st.pyplot(plt1, use_container_width=True)
        with cols7:
            st.pyplot(plt2, use_container_width=True)
    else:
        pilih_elemen2 = st.selectbox(
            "Lihat Berdasarkan",
            df[pilih_elemen1].unique(),
            index=0, 
        )

        df_filtered = filter_data2(df, pilih_elemen1, pilih_elemen2)
        
        st.dataframe(df_filtered, hide_index=True)

        # hitung hasil
        df_hasil, indeks_up, iup_konversi, mutu, kinerja, Nilai_Konversi_Per_Unsur = buat_dataframe_hasil(df_filtered)

        st.subheader("📈 Hasil Perhitungan")
        df_hasil.index = range(1, len(df_hasil) + 1)
        st.dataframe(df_hasil, width='stretch', hide_index=True)

        col = col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Indeks Unit Pelayanan", value=round(indeks_up, 2))
        with col2:
            st.metric(label="Nilai Unit Pelayanan", value=round(iup_konversi, 2))
        with col3:
            st.metric(label="Mutu", value=(mutu))
        with col4:
            st.metric(label="Kinerja", value=(kinerja))

        st.subheader("KRITERIA RESPONDEN")
        fig_jk, fig_usia, fig_pd, fig_pk, fig_jl = grafik(df_filtered)
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            st.plotly_chart(fig_jk)
        with cols2:
            st.plotly_chart(fig_usia)
        with cols3:
            st.plotly_chart(fig_pd)

        cols4, cols5 = st.columns(2)
        with cols4:
            st.plotly_chart(fig_pk)
        with cols5:
            st.plotly_chart(fig_jl)

        plt1, plt2 = korelasi_spearman(df_filtered, Nilai_Konversi_Per_Unsur)
        cols6, cols7 = st.columns(2)
        with cols6:
            st.pyplot(plt1, width='stretch')
        with cols7:
            st.pyplot(plt2, width='stretch')
