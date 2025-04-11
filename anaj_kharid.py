import streamlit as st
import requests
import json
import pandas as pd



SecretKey = st.text_input("Enter your name:")
st.write(f"Secret Key: {SecretKey}")

url = "https://vtsapi.anaajkharid.in/api/VechileRegistration/Ins_VechileRegistration"
headers = {
    "Content-Type": "application/json",
    "SecretKey": SecretKey
}
st.write("CSV File Uploader")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None and SecretKey:
    try:
        df = pd.read_csv(uploaded_file)
        st.write(f"### Preview of CSV File: and count:  {len(df)}")
        df['api_response'] = None
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error: The uploaded file is not a valid CSV. Please try again.")

    if st.button("Upload Data to API") and SecretKey:
        for index, row in df.iterrows():
            data = {
                "id": row["id"],
                "modeoftransporter": row["modeoftransporter"],
                "vehicleNumber": row["vehicleNumber"],
                "engineNumber": row["engineNumber"],
                "chassisNumber": row["chassisNumber"],
                "gpsDeviceId": row["gpsDeviceId"],
                "driverName": row["driverName"],
                "driverMobileNumber": row["driverMobileNumber"],
                "vehicleCapacity": row["vehicleCapacity"],
                "companyPanNo": row["companyPanNo"],
                "rcCopy": row["rcCopy"],
                "vehicleImagePath": row["vehicleImagePath"],
                "createdBy": row["createdBy"],
                "device_SimNumber": row["device_SimNumber"],
                "device_DataValidity": row["device_DataValidity"],
                "type": row["type"]
            }
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                # response = response.json()
                st.write(response.status_code)  
                df.at[index, 'api_response'] = f"{str(response.status_code), {response.text}}"
            except requests.exceptions.RequestException as e:
                # st.error(f"An error occurred: {e}")
                st.write(response.status_code) 
                df.at[index, 'api_response'] = f"{response.status_code}: {str(e)}"
            


    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
                label="Download Updated CSV",
                data=csv,
                file_name="updated_data.csv",
                mime="text/csv"
            )



    
