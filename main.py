#Main Script Insurance should Blank.


import pandas as pd
import json

excel_file = r'C:\Users\truvi\workspace\CareHigh-Python Related Projects\JsonStructure\SearchDataSet.xlsx'

df = pd.read_excel(excel_file, sheet_name='Sheet1')

# List of columns to capitalize
columns_to_capitalize = ['First Name', 'Last Name', 'Full Name', 'Street Name', 'Business Name', 'City']

# Capitalize specified columns
for column in columns_to_capitalize:
    # df[column] = df[column].apply(lambda x: str(x).capitalize())
    df[column] = df[column].apply(lambda x: str(x).title())

grouped_data = []

grouped = df.groupby(['Full Name'])

for full_name, full_name_group in grouped:
    npi_number_value = full_name_group['NPI Number'].values[0]
    npi_number_str = str(int(npi_number_value)) if not pd.isna(npi_number_value) and npi_number_value != 'Not Available' else ''

    zip_code_value = full_name_group['Zip Code'].values[0]
    zip_code_str = str(int(zip_code_value)) if not pd.isna(zip_code_value) else ''

    # Collect all clinics for the current person
    clinic_addresses = []
    for clinic_idx in range(len(full_name_group)):
        clinic_address = {
            'cid': (clinic_idx + 1),
            'clinicName': str(full_name_group['Business Name'].values[clinic_idx]),
            'streetName': str(full_name_group['Street Name'].values[clinic_idx]),
            'stateCode': str(full_name_group['State Code'].values[clinic_idx]),
            'zipCode': zip_code_str,
            'phoneNumber': str(int(full_name_group['Phone Number'].values[clinic_idx])) if not pd.isna(full_name_group['Phone Number'].values[clinic_idx]) else '',
            'clinicEmail':[str(full_name_group['Email'].str.lower().values[0]) if not pd.isna(full_name_group['Email'].values[0]) else ''],
            'npiNumber': npi_number_str,
            'npiType': 'organization' if full_name_group['NPI Type'].values[clinic_idx] == '2-Organization' else '',
            'commercial': str(full_name_group['Commercial'].values[clinic_idx]) if not pd.isna(full_name_group['Commercial'].values[clinic_idx]) else '',
            'active': str(full_name_group['Active'].values[clinic_idx]) if not pd.isna(full_name_group['Active'].values[clinic_idx]) else '',
            'verified': str(full_name_group['Verified'].values[clinic_idx]) if not pd.isna(full_name_group['Verified'].values[clinic_idx]) else '',
            'confidenceScore': str(full_name_group['Confidence Score'].values[clinic_idx]) if not pd.isna(full_name_group['Confidence Score'].values[clinic_idx]) else '',
            'claimed': str(full_name_group['Claimed'].values[clinic_idx]) if not pd.isna(full_name_group['Claimed'].values[clinic_idx]) else '',
            'geoLocation': {
                'type': 'Point',
                'coordinates': [
                    (full_name_group['Longitude'].values[clinic_idx]) if not pd.isna(full_name_group['Longitude'].values[clinic_idx]) else '',
                    (full_name_group['Latitude'].values[clinic_idx]) if not pd.isna(full_name_group['Latitude'].values[clinic_idx]) else '',
                ],
            },
            'insurances': [],
            "longitude": (full_name_group['Longitude'].values[clinic_idx]) if not pd.isna(full_name_group['Longitude'].values[clinic_idx]) else '',
            "latitude": (full_name_group['Latitude'].values[clinic_idx]) if not pd.isna(full_name_group['Latitude'].values[clinic_idx]) else '',
        }
        clinic_addresses.append(clinic_address)

    provider = {
        'firstName': str(full_name_group['First Name'].values[0]) if not pd.isna(full_name_group['First Name'].values[0]) else '',
        'lastName': str(full_name_group['Last Name'].values[0]) if not pd.isna(full_name_group['Last Name'].values[0]) else '',
        'fullName': str(full_name_group['Full Name'].values[0]) if not pd.isna(full_name_group['Full Name'].values[0]) else '',
        'phoneNumber': str(int(full_name_group['Phone Number'].values[0])) if not pd.isna(full_name_group['Phone Number'].values[0]) else '',
        'city': str(full_name_group['City'].values[0]) if not pd.isna(full_name_group['City'].values[0]) else '',
        'email': [str(full_name_group['Email'].str.lower().values[0]) if not pd.isna(full_name_group['Email'].values[0]) else ''],
        'gender': str(full_name_group['Gender'].values[0]) if not pd.isna(full_name_group['Gender'].values[0]) else '',
        'npiNumber': npi_number_str,
        'npiType': 'Individual' if full_name_group['NPI Type'].values[0] == '1-Individual' else '',
        'specialties': [
            {
                'sid': (idx + 1),
                'name': str(specialty)
            }
            for idx, specialty in enumerate(full_name_group['Specialties'].dropna().unique())
        ],
        'clinicAddresses': clinic_addresses
    }

    grouped_data.append(provider)

json_data = json.dumps(grouped_data, indent=2)

# Save
with open('bhavan1.json', 'w') as outfile:
    outfile.write(json_data)

# Print
print("JSON Ready Bhavan!")
