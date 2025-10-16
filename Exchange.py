import streamlit as st
import requests
import pandas as pd

st.title("💱 Currency Converter (แปลงสกุลเงิน)")

API_KEY = "082828a3b4122f9b8ef6cca7"

url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        st.error("❌ ไม่สามารถดึงข้อมูลจาก API ได้")
    else:
        rates = data["conversion_rates"]
        currencies = sorted(rates.keys())

        col1, col2 = st.columns(2)
        with col1:
            from_currency = st.selectbox("จากสกุลเงิน (From):", currencies, index=currencies.index("USD"))
        with col2:
            to_currency = st.selectbox("เป็นสกุลเงิน (To):", currencies, index=currencies.index("THB"))

        amount = st.number_input("จำนวนเงิน:", min_value=0.0, value=1.0, format="%.2f")

        url_convert = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
        res2 = requests.get(url_convert)
        res2.raise_for_status()
        rates2 = res2.json()["conversion_rates"]

        if to_currency in rates2:
            converted = amount * rates2[to_currency]
            st.success(f"{amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}")
        else:
            st.error("ไม่พบอัตราแลกเปลี่ยนของสกุลเงินนี้")

        st.subheader(f"📊 อัตราแลกเปลี่ยนทั้งหมด")
        df = pd.DataFrame(list(rates2.items()), columns=["Currency", "Rate"])
        st.dataframe(df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
