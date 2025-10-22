# if Jenis Layanan
def filter_data(df, pilih_elemen):
    kolom_dipilih = [pilih_elemen] + list(df.columns[7:])
    hapus_kolom = [col for col in df.columns if col not in kolom_dipilih]
    df = df.drop(columns=hapus_kolom)
    df = df.sort_values(by=[pilih_elemen], ascending=[True])

    return df


def filter_data2(df, kolom, nilai):
    """
    Memfilter DataFrame berdasarkan nilai tertentu dari suatu kolom.
    
    Parameter:
    - df : pandas.DataFrame
    - kolom : str → nama kolom yang akan difilter
    - nilai : nilai yang akan dicari dalam kolom tersebut
    
    Return:
    - DataFrame yang hanya berisi baris dengan nilai sesuai
    """
    if kolom not in df.columns:
        raise ValueError(f"Kolom '{kolom}' tidak ditemukan di DataFrame.")
    
    df_filtered = df[df[kolom] == nilai].reset_index(drop=True)

    return df_filtered