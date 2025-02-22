


import streamlit as st
import pandas as pd

# Initialize session state for transactions & general journal
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Date", "Category", "Details", "Amount (₹)"])

if "general_journal" not in st.session_state:
    st.session_state.general_journal = pd.DataFrame(columns=["Date", "Account Name", "Account Type", "Debit (₹)", "Credit (₹)"])

st.title("📊 Financial Transactions Management")

# ---- SECTION 1: Regular Transactions ---- #
st.subheader("📋 Add a New Transaction")
date = st.date_input("Select Date")
category = st.selectbox("Select Category", [
    "Current Asset", "Non-Current Asset", "Contra-Asset (Reduce asset value)",
    "Liabilities", "Contra-Liability Accounts (Reduce liability value)", "Equity Accounts / Capital",
    "Revenue Accounts", "Contra-Revenue Accounts (Reduce revenue)", "Operating Expenses (Day-to-day business costs)",
    "Non-Operating Expenses (Not part of core operations)"
])
details = st.text_input("Enter Transaction Details")
amount = st.number_input("Enter Amount (₹)", min_value=0.0, format="%.2f")

if st.button("Add Transaction"):
    if amount > 0:
        new_data = pd.DataFrame({"Date": [date], "Category": [category], "Details": [details], "Amount (₹)": [amount]})
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_data], ignore_index=True)
        st.success("✅ Transaction Added Successfully!")
    else:
        st.warning("⚠️ Please enter a valid amount!")

# Display Transactions Table
st.subheader("📋 Transactions Table")
st.dataframe(st.session_state.transactions)

# ---- SECTION 2: General Journal Entry ---- #
st.subheader("📖 General Journal Entry")

gj_date = st.date_input("Select Date for Journal Entry")

# Debit Entry
st.markdown("### **Debit Entry**")
debit_account = st.text_input("Enter Debit Account Name (e.g., Cash, Accounts Receivable)")
debit_type = st.selectbox("Select Debit Account Type", [
    "Current Asset", "Non-Current Asset", "Contra-Asset (Reduce asset value)",
    "Liabilities", "Contra-Liability Accounts (Reduce liability value)", "Equity Accounts / Capital",
    "Revenue Accounts", "Contra-Revenue Accounts (Reduce revenue)", "Operating Expenses (Day-to-day business costs)",
    "Non-Operating Expenses (Not part of core operations)"
], key="debit_type")
debit_amount = st.number_input("Enter Debit Amount (₹)", min_value=0.0, format="%.2f", key="debit_amount")

# Credit Entry
st.markdown("### **Credit Entry**")
credit_account = st.text_input("Enter Credit Account Name (e.g., Sales, Accounts Payable)")
credit_type = st.selectbox("Select Credit Account Type", [
    "Current Asset", "Non-Current Asset", "Contra-Asset (Reduce asset value)",
    "Liabilities", "Contra-Liability Accounts (Reduce liability value)", "Equity Accounts / Capital",
    "Revenue Accounts", "Contra-Revenue Accounts (Reduce revenue)", "Operating Expenses (Day-to-day business costs)",
    "Non-Operating Expenses (Not part of core operations)"
], key="credit_type")
credit_amount = st.number_input("Enter Credit Amount (₹)", min_value=0.0, format="%.2f", key="credit_amount")

if st.button("Add to General Journal"):
    if debit_amount == credit_amount and debit_amount > 0:
        new_entries = pd.DataFrame({
            "Date": [gj_date, gj_date], 
            "Account Name": [debit_account, credit_account], 
            "Account Type": [debit_type, credit_type], 
            "Debit (₹)": [debit_amount, 0], 
            "Credit (₹)": [0, credit_amount]
        })
        
        st.session_state.general_journal = pd.concat([st.session_state.general_journal, new_entries], ignore_index=True)
        st.success("✅ General Journal Entry Added Successfully!")
    else:
        st.error("⚠️ Debit and Credit amounts must be equal!")

# Display General Journal Table
st.subheader("📖 General Journal Table")
st.dataframe(st.session_state.general_journal)



# ---- SECTION 3: Income Statement ---- #
st.subheader("📄 Income Statement")

if not st.session_state.transactions.empty:
    # Summing up transaction amounts by category
    income = st.session_state.transactions.groupby("Category")["Amount (₹)"].sum()

    # Fetching relevant amounts
    revenue = income.get("Revenue Accounts", 0)  # Make sure this matches your category name
    sales_returns = income.get("Contra-Revenue Accounts (Reduce revenue)", 0)
    expenses = income.get("Operating Expenses (Day-to-day business costs)", 0) + income.get("Non-Operating Expenses (Not part of core operations)", 0)

    # Define additional expense items (ensure these exist in transactions)
    cogs = income.get("Cost of Goods Sold (COGS)", 0)
    salaries = income.get("Salaries & Wages", 0)
    rent = income.get("Rent Expense", 0)
    utilities = income.get("Utilities", 0)
    depreciation = income.get("Depreciation", 0)
    other_operating_expenses = income.get("Other Operating Expenses", 0)
    other_income = income.get("Other Income", 0)
    other_expenses = income.get("Other Expenses", 0)
    tax_expense = income.get("Tax Expense", 0)

    # Calculating Income Statement values
    net_revenue = revenue - sales_returns
    gross_profit = net_revenue - cogs
    total_operating_expenses = salaries + rent + utilities + depreciation + other_operating_expenses
    operating_profit = gross_profit - total_operating_expenses
    ebt = operating_profit + other_income - other_expenses
    net_profit = ebt - tax_expense

    # Creating Income Statement DataFrame
    income_statement = pd.DataFrame({
        "Particulars": [
            "Sales / Service Revenue",
            "Less: Sales Returns & Discounts",
            "Net Revenue",
            "Less: Cost of Goods Sold (COGS)",
            "Gross Profit",
            "Less: Operating Expenses:",
            "- Salaries & Wages",
            "- Rent Expense",
            "- Utilities",
            "- Depreciation",
            "- Other Operating Expenses",
            "Total Operating Expenses",
            "Operating Profit (EBIT)",
            "Add: Other Income",
            "Less: Other Expenses",
            "Earnings Before Tax (EBT)",
            "Less: Tax Expense",
            "Net Profit / (Loss)"
        ],
        "Amount (₹)": [
            revenue,
            -sales_returns,
            net_revenue,
            -cogs,
            gross_profit,
            "",
            -salaries,
            -rent,
            -utilities,
            -depreciation,
            -other_operating_expenses,
            -total_operating_expenses,
            operating_profit,
            other_income,
            -other_expenses,
            ebt,
            -tax_expense,
            net_profit
        ]
    })

    st.table(income_statement)
else:
    st.warning("⚠️ No transactions available for Income Statement.")
