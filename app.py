import streamlit as st
import pandas as pd
import os
from datetime import date

# Initialize session state for transactions & general journal
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Date", "Category", "Details", "Amount (₹)"])

if "general_journal" not in st.session_state:
    st.session_state.general_journal = pd.DataFrame(columns=["Date", "Account Name", "Account Type", "Debit (₹)", "Credit (₹)"])

st.title("📊 Financial Transactions Management")

# ---- SECTION 1: Regular Transactions ---- #
st.subheader("📋 Add a New Transaction")
date = st.date_input("Select Date", key="transaction_date")
category = st.selectbox("Select Category", [
    # Assets and Liabilities (existing categories)
    "Current Asset", "Non-Current Asset", "Contra-Asset (Reduce asset value)",
    "Liabilities", "Contra-Liability Accounts (Reduce liability value)", "Equity Accounts / Capital",
    
    # Income Statement Categories
    "Sales / Service Revenue",
    "Sales Returns & Discounts",
    "Cost of Goods Sold (COGS)",
    "Salaries & Wages",
    "Rent Expense",
    "Utilities",
    "Depreciation",
    "Other Operating Expenses",
    "Other Income",
    "Other Expenses",
    "Tax Expense"
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

# Add Export buttons after transaction table
st.subheader("Export Transactions")
if st.button("Export Transactions to CSV"):
    if not st.session_state.transactions.empty:
        st.session_state.transactions.to_csv("transactions.csv", index=False)
        st.success("✅ Transactions exported to transactions.csv!")
    else:
        st.warning("⚠️ No transactions to export!")

# Add after export buttons
if st.button("Check CSV Files"):
    files = os.listdir()
    st.write("Files in current directory:")
    for file in files:
        if file.endswith('.csv'):
            st.write(f"Found CSV file: {file}")
            # Show file contents
            df = pd.read_csv(file)
            st.write(f"Contents of {file}:")
            st.dataframe(df)

# ---- SECTION 2: General Journal Entry ---- #
st.subheader("📖 General Journal Entry")

gj_date = st.date_input("Select Date for Journal Entry", key="journal_date")

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

# Add Export button after general journal table
st.subheader("Export General Journal")
if st.button("Export General Journal to CSV"):
    if not st.session_state.general_journal.empty:
        st.session_state.general_journal.to_csv("general_journal.csv", index=False)
        st.success("✅ General Journal exported to general_journal.csv!")
    else:
        st.warning("⚠️ No journal entries to export!")

# ---- SECTION 3: Income Statement ---- #
st.subheader("📄 Income Statement")

if not st.session_state.transactions.empty:
    # Summing up transaction amounts by category
    income = st.session_state.transactions.groupby("Category")["Amount (₹)"].sum()

    # Fetching relevant amounts
    revenue = income.get("Sales / Service Revenue", 0)  # Make sure this matches your category name
    sales_returns = income.get("Sales Returns & Discounts", 0)
    expenses = income.get("Operating Expenses", 0)

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

    # Creating Income Statement DataFrame with proper formatting
    income_statement = pd.DataFrame({
        "Particulars": [
            "Revenue:",
            "   Sales / Service Revenue",
            "   Less: Sales Returns & Discounts",
            "Net Revenue",
            "",
            "Less: Cost of Goods Sold (COGS)",
            "Gross Profit",
            "",
            "Operating Expenses:",
            "   Salaries & Wages",
            "   Rent Expense",
            "   Utilities",
            "   Depreciation",
            "   Other Operating Expenses",
            "Total Operating Expenses",
            "",
            "Operating Profit (EBIT)",
            "",
            "Other Items:",
            "   Add: Other Income",
            "   Less: Other Expenses",
            "Earnings Before Tax (EBT)",
            "",
            "   Less: Tax Expense",
            "Net Profit / (Loss)"
        ],
        "Amount (₹)": [
            "",
            revenue,
            sales_returns,
            net_revenue,
            "",
            cogs,
            gross_profit,
            "",
            "",
            salaries,
            rent,
            utilities,
            depreciation,
            other_operating_expenses,
            total_operating_expenses,
            "",
            operating_profit,
            "",
            "",
            other_income,
            other_expenses,
            ebt,
            "",
            tax_expense,
            net_profit
        ],
        "Total (₹)": [
            "",
            "",
            "",
            net_revenue,
            "",
            "",
            gross_profit,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            total_operating_expenses,
            "",
            operating_profit,
            "",
            "",
            "",
            "",
            ebt,
            "",
            "",
            net_profit
        ]
    })

    # Apply styling to the income statement
    st.markdown("### Income Statement")
    st.markdown("For the period ended " + str(date.today()))
    st.markdown("---")
    
    # Display the formatted income statement
    income_statement.index = [""] * len(income_statement)  # Hide index
    
    # Function to format numbers, handling empty strings
    def format_numbers(val):
        if isinstance(val, (int, float)):
            return f"{val:,.2f}"
        return val

    # Apply formatting
    formatted_statement = income_statement.copy()
    formatted_statement["Amount (₹)"] = formatted_statement["Amount (₹)"].apply(format_numbers)
    formatted_statement["Total (₹)"] = formatted_statement["Total (₹)"].apply(format_numbers)
    
    # Display table
    st.table(formatted_statement)

    # Display key metrics
    st.markdown("---")
    st.markdown("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gross Profit Margin", f"{(gross_profit/net_revenue*100 if net_revenue != 0 else 0):.1f}%")
    with col2:
        st.metric("Operating Margin", f"{(operating_profit/net_revenue*100 if net_revenue != 0 else 0):.1f}%")
    with col3:
        st.metric("Net Profit Margin", f"{(net_profit/net_revenue*100 if net_revenue != 0 else 0):.1f}%")

else:
    st.warning("⚠️ No transactions available for Income Statement.")
