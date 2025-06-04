import streamlit as st
import pandas as pd

# Initialize session state for storing customer data
if 'customers' not in st.session_state:
    st.session_state.customers = []
if 'meter_readings' not in st.session_state:
    st.session_state.meter_readings = []

# Function to calculate water bill (example: Rp 5000 per cubic meter)
def calculate_bill(meter_reading):
    rate_per_cubic_meter = 5000  # Example rate
    return meter_reading * rate_per_cubic_meter

# Streamlit app layout
st.title("Aplikasi Pendataan Meteran Air")

# Tabs for navigation
tab1, tab2 = st.tabs(["Pencatatan Meteran", "Manajemen Pelanggan"])

# Tab 1: Pencatatan Meteran
with tab1:
    st.header("Pencatatan Meteran")
    
    # Search customer
    search_term = st.text_input("Kode Pelanggan atau Nama:")
    if search_term:
        filtered_customers = [
            c for c in st.session_state.customers
            if search_term.lower() in c['kode'].lower() or search_term.lower() in c['nama'].lower()
        ]
        if filtered_customers:
            selected_customer = st.selectbox(
                "Pilih Pelanggan",
                options=[f"{c['kode']} - {c['nama']}" for c in filtered_customers],
                format_func=lambda x: x
            )
            selected_kode = selected_customer.split(" - ")[0]
            customer = next((c for c in filtered_customers if c['kode'] == selected_kode), None)
        else:
            st.warning("Pelanggan tidak ditemukan.")
            customer = None
    else:
        customer = None

    # Meter reading input
    meter_reading = st.number_input("Meter Bulan Ini:", min_value=0.0, step=0.1)
    
    # Calculate and display total bill
    if meter_reading > 0:
        total_bill = calculate_bill(meter_reading)
        st.write(f"Total Biaya: Rp {total_bill:,.0f}")
    else:
        st.write("Total Biaya: Rp 0")

    # Payment input
    payment = st.number_input("Jumlah Dibayar:", min_value=0.0, step=1000.0)

    # Buttons for actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hitung"):
            if customer and meter_reading > 0:
                st.success(f"Total biaya untuk {customer['nama']}: Rp {total_bill:,.0f}")
            else:
                st.error("Masukkan data pelanggan dan meter yang valid.")
    with col2:
        if st.button("Simpan"):
            if customer and meter_reading > 0:
                st.session_state.meter_readings.append({
                    'kode': customer['kode'],
                    'nama': customer['nama'],
                    'meter': meter_reading,
                    'total_biaya': total_bill,
                    'dibayar': payment
                })
                st.success("Data meteran berhasil disimpan!")
            else:
                st.error("Masukkan data pelanggan dan meter yang valid.")

# Tab 2: Manajemen Pelanggan
with tab2:
    st.header("Manajemen Pelanggan")
    
    # Add new customer
    with st.form("tambah_pelanggan_form"):
        st.subheader("Tambah Pelanggan Baru")
        kode = st.text_input("Kode Pelanggan:")
        nama = st.text_input("Nama:")
        kampung = st.text_input("Kampung:")
        rt_rw = st.text_input("RT/RW:")
        tabungan = st.number_input("Tabungan (opsional):", min_value=0.0, step=1000.0, value=0.0)
        
        if st.form_submit_button("Tambah Pelanggan"):
            if kode and nama and kampung and rt_rw:
                if any(c['kode'] == kode for c in st.session_state.customers):
                    st.error("Kode pelanggan sudah ada!")
                else:
                    st.session_state.customers.append({
                        'kode': kode,
                        'nama': nama,
                        'kampung': kampung,
                        'rt_rw': rt_rw,
                        'tabungan': tabungan
                    })
                    st.success("Pelanggan berhasil ditambahkan!")
            else:
                st.error("Lengkapi semua kolom wajib!")

    # Display customer list
    st.subheader("Daftar Pelanggan")
    if st.session_state.customers:
        df = pd.DataFrame(st.session_state.customers)
        st.dataframe(df[['kode', 'nama', 'kampung', 'rt_rw', 'tabungan']])
    else:
        st.write("Belum ada pelanggan terdaftar.")
