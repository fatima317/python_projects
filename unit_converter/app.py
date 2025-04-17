import streamlit as st

conversions = {
    "meters_millimeters": 1000, # 1 meter = 1000 millimeters
    "millimeters_meters": 0.001, # 1 millimeter = 0.001 meters
    "meters_centimeters": 100, # 1 meter = 100 centimeters
    "centimeters_meters": 0.01, # 1 centimeter = 0.01 meters
    "meters_kilometers": 0.001, # 1 meter = 0.001 kilometer
    "kilometers_meters": 1000, # 1 kilometer = 1000 meters
    "meters_inches": 39.37, # 1 meter = 39.37 inches
    "inches_meters": 0.0254, # 1 inch = 0.0254 meters
    "meters_feet": 3.28084, # 1 meter = 3.28084 feet
    "feet_meters": 0.3048, # 1 foot = 0.3048 meters
    "meters_yards": 1.09361, # 1 meter = 1.09361 yards
    "yards_meters": 0.9144, # 1 yard = 0.9144 meters
    "feet_yards": 0.333333, # 1 foot = 0.333333 yards
    "yards_feet": 3, # 1 yard = 3 feet
    "feet_inches": 12, # 1 foot = 12 inches
    "inches_feet": 0.0833333, # 1 inch = 0.0833333 feet
    "grams_kilograms": 0.001, # 1 gram = 0.001 kilogram
    "kilograms_grams": 1000, # 1 kilogram = 1000 grams
    "grams_pounds": 0.00220462, # 1 gram = 0.00220462 pounds
    "pounds_grams": 453.592, # 1 pound = 453.592 grams
    "kilograms_pounds": 2.20462, # 1 kilogram = 2.20462 pounds
    "pounds_kilograms": 0.453592, # 1 pound = 0.453592 kilograms
    "kilograms_ounces": 35.274, # 1 kilogram = 35.274 ounces
    "ounces_kilograms": 0.0283495, # 1 ounce = 0.0283495 kilograms
    "pounds_ounces": 16, # 1 pound = 16 ounces
    "ounces_pounds": 0.0625, # 1 ounce = 0.0625 pounds
    "grams_ounces": 0.035274, # 1 gram = 0.035274 ounces
    "ounces_grams": 28.3495, # 1 ounce = 28.3495 grams
    
    
}

def convert_units(value, unit_from, unit_to):
    key = f"{unit_from}_{unit_to}" # Create a unique key for the conversion

    # Check if the conversion key exists in the conversions dictionary
    if key in conversions:
        conversion_factor = conversions[key]
        return value * conversion_factor # Return the converted value
    else:
        return "Conversion not found" # Return a message if the conversion key is not found

# Create a title for the app
st.title("Unit Converter")

# Create a number input for the value to convert
value = st.number_input("Enter the value to convert:", min_value=1.0, step=1.0)

# Create a dropdown for the unit to convert from
unit_from = st.selectbox("Select the unit to convert from:", ["meters", "millimeters", "centimeters", "kilometers", "grams", "kilograms", "feet", "yards", "inches", "pounds", "ounces"])

# Create a dropdown for the unit to convert to
unit_to = st.selectbox("Select the unit to convert to:", ["meters", "millimeters", "centimeters", "kilometers", "grams", "kilograms", "feet", "yards", "inches", "pounds", "ounces"])

# Create a button to trigger the conversion
if st.button("Convert"):
    result = convert_units(value, unit_from, unit_to)
    st.write(f"The converted value is: {result}")
        