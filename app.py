import streamlit as st
from core.policyholder import Policyholder
from core.claims import create_claim
from core.risk_analysis import analyze_risk
from core.reports import generate_reports
from utils.storage import save_data, load_data

# Load existing data
policyholders = load_data()

st.title("🏥 Insurance Claims Management")

menu = st.sidebar.selectbox("Menu", ["Register Policyholder", "Add Claim", "Risk Analysis", "Reports"])

if menu == "Register Policyholder":
    st.header("Register Policyholder")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    policy_type = st.selectbox("Policy Type", ["Health", "Vehicle", "Life"])
    sum_insured = st.number_input("Sum Insured")

    if st.button("Register"):
        pid = f"PH{len(policyholders)+1}"
        holder = Policyholder(pid, name, age, policy_type, sum_insured)
        policyholders.append(holder)
        save_data(policyholders)
        st.success(f"Policyholder {name} registered.")

elif menu == "Add Claim":
    st.header("Add Claim")
    if not policyholders:
        st.warning("Register policyholders first.")
    else:
        holder_id = st.selectbox("Policyholder ID", [p.id for p in policyholders])
        cid = st.text_input("Claim ID")
        amt = st.number_input("Claim Amount")
        reason = st.text_input("Reason")
        status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
        date = st.date_input("Date of Claim").strftime("%Y-%m-%d")

        if st.button("Submit Claim"):
            success = create_claim(policyholders, cid, holder_id, amt, reason, status, date)
            if success:
                save_data(policyholders)
                st.success("Claim added.")
            else:
                st.error("Policyholder not found.")

elif menu == "Risk Analysis":
    st.header("High Risk Policyholders")
    risky = analyze_risk(policyholders)
    for r in risky:
        st.write(r.to_dict())

elif menu == "Reports":
    st.header("Reports")
    month_totals, avg_claims, highest, pending = generate_reports(policyholders)

    st.subheader("📅 Total Claims Per Month")
    st.write(month_totals)

    st.subheader("📊 Average Claim by Policy Type")
    st.write(avg_claims)

    st.subheader("🏆 Highest Claim Filed")
    st.write(highest)

    st.subheader("⏳ Pending Claims")
    for p in pending:
        st.write(p.to_dict())
