import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "expenses_database.csv"

# Web Page Setup (Mobile Friendly)
st.set_page_config(page_title="Pocket Expense Tracker", page_icon="💰", layout="centered")

st.markdown("<h2 style='text-align: center; color: #00FFCC;'>💰 POCKET EXPENSE TRACKER</h2>", unsafe_allow_html=True)

# --- KHARCHE DAALNE KA FORM ---
st.markdown("### ➕ Add New Expense")
with st.form("expense_form", clear_on_submit=True):
    category = st.text_input("Where did you spend? (e.g., Food, Clothes)").strip().title()
    amount = st.number_input("Amount Spent (Rs.)", min_value=0.0, step=10.0)
    submit = st.form_submit_button("💾 Save Expense")

if submit:
    if category and amount > 0:
        now = datetime.now()
        current_time = now.strftime("%d-%b-%Y %I:%M %p")
        month_year = now.strftime("%b-%Y")
        
        # New Row
        new_row = pd.DataFrame([[current_time, month_year, category, amount]], 
                               columns=["Date & Time", "Month", "Category", "Amount"])
        
        # CSV File database mein save karna
        if not os.path.exists(DATA_FILE):
            new_data = pd.DataFrame(columns=["S.No", "Date & Time", "Month", "Category", "Amount"])
            new_row.insert(0, "S.No", [1])
            new_row.to_csv(DATA_FILE, index=False)
        else:
            df_old = pd.read_csv(DATA_FILE)
            next_sno = len(df_old) + 1
            new_row.insert(0, "S.No", [next_sno])
            new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
            
        st.success(f"Saved: {category} - Rs.{amount}")
    else:
        st.error("Please enter a valid category and amount!")

st.markdown("---")

# --- SPREADSHEET & GRAPH VIEW ---
if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
    df = pd.read_csv(DATA_FILE)
    
    # 1. Excel/Spreadsheet Table View
    st.markdown("### 📊 Expense Spreadsheet")
    st.dataframe(df, use_container_width=True)
    
    # Total history spent
    total_all = df["Amount"].sum()
    st.metric(label="📉 Total Spent (All Time)", value=f"Rs. {total_all}")
    
    st.markdown("---")
    
    # 2. Monthly Comparison Analytics & Graph
    st.markdown("### 📈 Month-wise Analytics")
    monthly_totals = df.groupby("Month")["Amount"].sum()
    
    # Auto Graph Maker for Web/Mobile
    st.bar_chart(monthly_totals)
    
    st.markdown("---")
    
    # 3. Danger Zone (Delete Option)
    st.markdown("### 🗑️ Danger Zone")
    if st.button("Delete All History Permanently", type="primary"):
        os.remove(DATA_FILE)
        st.warning("All history deleted! Refreshing...")
        st.rerun()
else:
    st.info("No expenses recorded yet! Add your first expense above.")
