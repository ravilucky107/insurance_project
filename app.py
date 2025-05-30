import streamlit as st
from core.policyholder import Policyholder
from core.claims import create_claim
from core.risk_analysis import analyze_risk
from core.reports import generate_reports
from utils.storage import save_data, load_data
from datetime import datetime

# Load existing data
policyholders = load_data()

st.title("🏥 Insurance Claims Management")

menu = st.sidebar.selectbox("Menu", ["Register Policyholder", "Add Claim", "Risk Analysis", "Reports"])

if menu == "Register Policyholder":
    st.header("Register Policyholder")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    policy_type = st.selectbox("Policy Type", ["Health", "Vehicle", "Life"])
    sum_insured = st.number_input("Sum Insured")

    if st.button("Register"):
        pid = f"PH{len(policyholders)+1}"
        holder = Policyholder(pid, name, age, gender, policy_type, sum_insured)
        policyholders.append(holder)
        save_data(policyholders)
        st.success(f"Policyholder {name} registered.")

elif menu == "Add Claim":
    st.header("➕ Add Claim")

    if not policyholders:
        st.warning("No policyholders found. Please register first.")
    else:
        holder_ids = [ph.id for ph in policyholders]
        holder_id = st.selectbox("Select Policyholder ID", holder_ids)
        claim_id = st.text_input("Claim ID")
        amount = st.number_input("Claim Amount", min_value=0.0)
        reason = st.text_input("Claim Reason")
        status = st.selectbox("Claim Status", ["Pending", "Approved", "Rejected"])
        date = st.date_input("Date of Claim", format="YYYY-MM-DD")

        if st.button("Submit Claim"):
            success = create_claim(
                policyholders, claim_id, holder_id, amount, reason, status, str(date)
            )
            if success:
                save_data(policyholders)
                st.success("Claim added successfully.")
            else:
                st.error("Policyholder ID not found.")

elif menu == "Risk Analysis":
    st.header("📉 Risk Analysis")
    risky = analyze_risk(policyholders)

    if not risky:
        st.success("No high-risk policyholders found.")
    else:
        st.warning(f"{len(risky)} high-risk policyholder(s) found:")
        for holder in risky:
            st.markdown(f"### ⚠️ {holder.name} (ID: `{holder.id}`)")
            st.markdown(f"- Age: {holder.age}")
            st.markdown(f"- Gender: {holder.gender}")
            st.markdown(f"- Policy Type: {holder.policy_type}")
            st.markdown(f"- Sum Insured: ₹{holder.sum_insured}")
            st.markdown(f"- Total Claims: {len(holder.claims)}")
            st.markdown("---")

elif menu == "Reports":
    st.header("📋 Reports")

    month_totals, avg_claims, highest, pending = generate_reports(policyholders)

    st.subheader("📅 Total Claims Per Month")
    for month, total in month_totals.items():
        st.markdown(f"- **{month}**: ₹{total:.2f}")

    st.subheader("📊 Average Claim by Policy Type")
    for ptype, avg in avg_claims.items():
        st.markdown(f"- **{ptype}**: ₹{avg:.2f}")

    st.subheader("🏆 Highest Claim Filed")
    if highest:
        st.markdown(f"- **Claim ID**: `{highest.get('claim_id', '')}`")
        st.markdown(f"- **Amount**: ₹{highest.get('amount', 0):.2f}")
        st.markdown(f"- **Reason**: {highest.get('reason', '')}")
        st.markdown(f"- **Status**: {highest.get('status', '')}")
        st.markdown(f"- **Date**: {highest.get('date', '')}")
    else:
        st.info("No claims available.")

    st.subheader("⏳ Pending Claims")
    if not pending:
        st.info("No pending claims.")
    else:
        seen = set()
        for holder in pending:
            if holder.id in seen:
                continue
            seen.add(holder.id)
            st.markdown(f"### 👤 {holder.name} (ID: `{holder.id}`)")
            st.markdown(f"- **Age**: {holder.age}")
            st.markdown(f"- **Gender**: {holder.gender}")
            st.markdown(f"- **Policy Type**: {holder.policy_type}")
            st.markdown(f"- **Sum Insured**: ₹{holder.sum_insured}")
            st.markdown("**Claims:**")
            for claim in holder.claims:
                if claim["status"].lower() == "pending":
                    st.markdown(f"  - 🧾 **Claim ID**: `{claim['claim_id']}`")
                    st.markdown(f"    - 💰 Amount: ₹{claim['amount']}")
                    st.markdown(f"    - 📝 Reason: {claim['reason']}")
                    st.markdown(f"    - 📅 Date: {claim['date']}")
            st.markdown("---")
