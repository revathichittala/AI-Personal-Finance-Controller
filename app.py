import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI-Powered Personal Finance Controller")
st.write("Manage your income, expenses, budget and spending insights.")

# Sidebar
st.sidebar.header("💵 Monthly Finance")

income = st.sidebar.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    step=1000.0
)

budget = st.sidebar.number_input(
    "Monthly Budget (₹)",
    min_value=0.0,
    step=1000.0
)

st.header("➕ Add Expense")

category = st.selectbox(
    "Expense Category",
    ["Food", "Travel", "Education", "Shopping", "Bills", "Other"]
)

expense_date = st.date_input(
    "Expense Date"
)

amount = st.number_input(
    "Expense Amount (₹)",
    min_value=0.0,
    step=100.0
)

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if st.button("Add Expense"):
    if amount > 0:
        st.session_state.expenses.append({
            "Date": expense_date,
            "Category": category,
            "Amount": amount
        })
        st.success("Expense added successfully!")
    else:
        st.warning("Please enter a valid amount.")

# Expense data
df = pd.DataFrame(st.session_state.expenses)

st.header("📊 Financial Summary")

if not df.empty:
    total_expense = df["Amount"].sum()
else:
    total_expense = 0

balance = income - total_expense

col1, col2, col3 = st.columns(3)

col1.metric("💰 Income", f"₹{income:,.0f}")
col2.metric("💸 Total Expenses", f"₹{total_expense:,.0f}")
col3.metric("💵 Remaining Balance", f"₹{balance:,.0f}")

st.subheader("💰 Savings Summary")

if income > 0:
    savings_rate = (balance / income) * 100

    col4, col5 = st.columns(2)

    col4.metric(
        "💰 Potential Savings",
        f"₹{balance:,.0f}"
    )

    col5.metric(
        "📊 Savings Rate",
        f"{savings_rate:.1f}%"
    )

    if savings_rate >= 20:
        st.success("🎉 Great! You are maintaining a healthy savings rate.")
    elif savings_rate >= 10:
        st.info("💡 Good start! Try to increase your savings gradually.")
    elif savings_rate >= 0:
        st.warning("⚠️ Your savings are low. Consider reviewing your expenses.")
    else:
        st.error("🚨 Your expenses are higher than your income.")
else:
    st.info("Enter your monthly income to calculate savings.")

if budget > 0:
    budget_percentage = (total_expense / budget) * 100
    remaining_budget = budget - total_expense

    if total_expense > budget:
        st.error("⚠️ Your expenses have exceeded your monthly budget!")

    elif budget_percentage >= 80:
        st.warning(
            f"⚠️ You have used {budget_percentage:.0f}% of your budget. "
            f"Only ₹{remaining_budget:,.0f} remaining."
        )

    else:
        st.info(
            f"Budget used: {budget_percentage:.0f}% | "
            f"Remaining: ₹{remaining_budget:,.0f}"
        )

# Expense History
if not df.empty:
    st.subheader("📋 Expense History")
    st.dataframe(df, use_container_width=True)

    if st.button("🗑️ Delete Last Expense"):
        if st.session_state.expenses:
            st.session_state.expenses.pop()
            st.success("Last expense deleted successfully!")
            st.rerun()

    st.subheader("📈 Spending by Category")

    chart_data = df.groupby("Category")["Amount"].sum()
    st.bar_chart(chart_data)

    st.subheader("🤖 AI Spending Insight")

    highest_category = chart_data.idxmax()
    highest_amount = chart_data.max()

    spending_percentage = (highest_amount / total_expense) * 100

    st.write(
        f"Your highest spending category is **{highest_category}** "
        f"with ₹{highest_amount:,.0f}, which is "
        f"{spending_percentage:.0f}% of your total expenses."
    )

    if spending_percentage >= 50:
        st.warning(
            f"⚠️ {highest_category} is taking a large share of your spending. "
            "Consider setting a spending limit for this category."
        )
    elif spending_percentage >= 30:
        st.info(
            f"💡 Keep an eye on your {highest_category} expenses "
            "to maintain a balanced budget."
        )
    else:
        st.success(
            "✅ Your spending is reasonably distributed across categories."
        )

else:
    st.info("Add your first expense to see your financial insights.")