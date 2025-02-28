import streamlit as st

def length_converter(value, from_unit, to_unit):
    conversion_factors = {
        "meters": 1,
        "kilometers": 0.001,
        "miles": 0.000621371,
        "feet": 3.28084
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def weight_converter(value, from_unit, to_unit):
    conversion_factors = {
        "kilograms": 1,
        "grams": 1000,
        "pounds": 2.20462,
        "ounces": 35.274
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def temperature_converter(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return (value - 273.15) * 9/5 + 32
    return value

def main():
    st.title("Unit Converter")
    
    category = st.selectbox("Select category", ["Length", "Weight", "Temperature"])
    value = st.number_input("Enter value", min_value=0.0, format="%f")
    
    if category == "Length":
        units = ["meters", "kilometers", "miles", "feet"]
        from_unit = st.selectbox("From", units)
        to_unit = st.selectbox("To", units)
        result = length_converter(value, from_unit, to_unit)
    
    elif category == "Weight":
        units = ["kilograms", "grams", "pounds", "ounces"]
        from_unit = st.selectbox("From", units)
        to_unit = st.selectbox("To", units)
        result = weight_converter(value, from_unit, to_unit)
    
    elif category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
        from_unit = st.selectbox("From", units)
        to_unit = st.selectbox("To", units)
        result = temperature_converter(value, from_unit, to_unit)
    
    st.write(f"Converted value: {result:.4f} {to_unit}")

if __name__ == "__main__":
    main()
