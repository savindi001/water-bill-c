import streamlit as st
import pandas as pd

st.title("Water Bill Calculator",width="stretch")

#Initialize Variables
noOfUnits=0

#Create columns to control layout
col1,col2,col3=st.columns([3,1,1])

with col1: 

    #input logic
    
    initReading =st.number_input("Enter last month reading",key="init",min_value=0,step=1,format="%d")  # step=1 ඉහළ/පහළ ඊතල ක්ලික් කිරීමෙන් සංඛ්‍යාව 1 කින් වැඩි වේ/අඩු වේ.
    finReading=st.number_input("Enter this month reading",key="fin",min_value=0,step=1,format="%d")

    if initReading and finReading:
            initReading=int(initReading)
            finReading =int(finReading)

            if finReading > initReading:
                noOfUnits=finReading - initReading
            else:
                st.warning("Current reading must be greater than or equal to previous reading.")

    #Calculation part
    if st.button("Calculate") and noOfUnits > 0:
        try:
            row = []

            monthly_charges = round(100.00,2)
            units_bill = 0.00
            remaining_units = noOfUnits

            # First 25 units at Rs.5
            if remaining_units > 0:
                units = min(25, remaining_units)
                cost = round(units * 5, 2) 
                row.append(["First 25 units", units, 5.00, cost])
                units_bill += cost
                remaining_units -= units

            # Next 25 units at Rs.7
            if remaining_units > 0:
                units = min(25, remaining_units)
                cost = round(units * 7, 2)
                row.append(["Next 25 units", units, 7.00, cost])
                units_bill += cost
                remaining_units -= units

            # Remaining units at Rs.15
            if remaining_units > 0:
                cost = round(remaining_units * 15, 2)
                row.append(["Remaining units", remaining_units, 15.00, cost])
                units_bill += cost

            total_bill = monthly_charges + units_bill

        
                #add fixed charge
            row.append(["Fixed Charge", "--","--",monthly_charges])

            total_cost=round(units_bill + monthly_charges,2)
            row.append(["Total Charge","--","--",total_cost])

                #show result
            st.info(f"Total Charge: Rs.{total_cost:.2f}")

                #convert to dataframe and show table
            df=pd.DataFrame(row,columns=["Description","Units","Rate (Rs.)","Cost (Rs.)"])

                #format the rate and cost columns
            df["Rate (Rs.)"] = df["Rate (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
            df["Cost (Rs.)"] = df["Cost (Rs.)"].apply(lambda x: f"{x:.2f}" if isinstance(x,(int,float))else x)
            st.table(df)

        except Exception as e:
            st.error(f"Error calculating bill:{e}")
