import streamlit as st
import pandas as pd

st.title("Water Bill Calculator", width="stretch")

# Initialize variables
noOfUnits = 0

# Create Columns to Control layout
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    

    # Input logic
   
    initReading = st.number_input("Enter pre meter reading", key="init",min_value=0, step=1, format="%d")
    finReading = st.number_input("Enter monthly meter reading", key="fin",min_value=0, step=1, format="%d")

    if initReading and finReading:
            initReading = int(initReading)
            finReading = int(finReading)

            if finReading > initReading:
                noOfUnits = finReading - initReading

            else:
                st.warning("current reading must be greater than or equal to previous reading.")

 
  
    # Calculate button
    if st.button("Calculate") and noOfUnits > 0:
        try:
            row = []

          # monthly charge
            monthly_charges = round(100.00,2)
            units_bill = 0.00
            remaining_units = noOfUnits

          # For first 25 units
            if remaining_units > 0:
                units = min(25, remaining_units)
                cost = round(units * 5, 2)
                row.append(["First 25 units", units, 5.00, cost])
                units_bill += cost
                remaining_units -= units

          # For second 25 units
            if remaining_units > 0:
                units = min(25,remaining_units)
                cost = round(units * 7, 2)
                row.append(["Next 25 units", units, 7.00,cost])
                units_bill += cost
                remaining_units-= units

             # Remaining units
            if remaining_units> 0:
                cost = round(remaining_units * 15, 2)
                row.append(["Remaining units", remaining_units, 15.00, cost])
                units_bill += cost

            total_bill = monthly_charges + units_bill

             # Add monthly charge
            row.append(["Fixed charge", "--", " --", monthly_charges])

            total_cost = round(units_bill + monthly_charges, 2)
            row.append(["Total charge", "--", "--", total_cost])

             # show result
            st.info(f"Total charge: Rs.{total_cost:.2f}")

             # convert to dataframe and show table
            df=pd.DataFrame(row,columns=["Description", "Units(KWh)", "Rate (Rs.)","cost (Rs.)"])

             #format the rate and cost columns
            df["Rate (Rs.)"] = df["Rate (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
            df["Cost (Rs.)"] = df["Cost (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
            st.table(df)

        except Exception as e:
            st.error(f"Error calculating bill:{e}")