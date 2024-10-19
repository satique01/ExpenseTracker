import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load expenses from a CSV file (if it exists)
@st.cache_data
def load_expenses(file_path="expenses.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# Save expenses to a CSV file
def save_expenses(expenses, file_path="expenses.csv"):
    expenses.to_csv(file_path, index=False)

# Function to add a new expense
def add_expense(amount, category, description):
    new_expense = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d")],
        "Amount": [amount],
        "Category": [category],
        "Description": [description]
    })
    st.session_state["expenses"] = pd.concat([st.session_state["expenses"], new_expense], ignore_index=True)
    save_expenses(st.session_state["expenses"])  # Save after each addition

# Initialize expenses if not already in session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = load_expenses()

# App Title
st.title("Enhanced Expense Tracker")

# Sidebar for Adding New Expenses
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form"):
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Others"])
    description = st.text_input("Description (Optional)")
    submit_button = st.form_submit_button("Add Expense")

# Add new expense when form is submitted
if submit_button:
    if amount > 0:
        add_expense(amount, category, description)
        st.sidebar.success(f"Expense added: ${amount} to {category}")
    else:
        st.sidebar.error("Please enter a valid amount")

# Display all expenses
st.subheader("All Expenses")
if not st.session_state["expenses"].empty:
    st.dataframe(st.session_state["expenses"])
else:
    st.write("No expenses added yet.")

# Display total amount spent
st.subheader("Total Amount Spent")
if not st.session_state["expenses"].empty:
    total_spent = st.session_state["expenses"]["Amount"].sum()
    st.write(f"Total: ${total_spent:.2f}")
else:
    st.write("No expenses to calculate.")

# Filter by category
st.subheader("View Expenses by Category")
selected_category = st.selectbox("Select Category to View", options=["All"] + st.session_state["expenses"]["Category"].unique().tolist())

if selected_category != "All":
    filtered_expenses = st.session_state["expenses"][st.session_state["expenses"]["Category"] == selected_category]
else:
    filtered_expenses = st.session_state["expenses"]

st.write(f"Expenses in '{selected_category}' category:")
st.dataframe(filtered_expenses)

# Plotting Expenses by Category
st.subheader("Expense Distribution by Category")
if not st.session_state["expenses"].empty:
    category_totals = st.session_state["expenses"].groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    category_totals.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Expenses by Category")
    ax.set_ylabel("Amount ($)")
    st.pyplot(fig)
else:
    st.write("No expenses to plot.")

# Plotting Expenses Over Time
st.subheader("Expenses Over Time")
if not st.session_state["expenses"].empty:
    # Ensure Date column is in datetime format
    st.session_state["expenses"]["Date"] = pd.to_datetime(st.session_state["expenses"]["Date"])
    daily_totals = st.session_state["expenses"].groupby("Date")["Amount"].sum()

    fig, ax = plt.subplots()
    daily_totals.plot(kind="line", ax=ax, marker="o", color="orange")
    ax.set_title("Daily Expenses Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount ($)")
    st.pyplot(fig)
else:
    st.write("No expenses to plot.")
