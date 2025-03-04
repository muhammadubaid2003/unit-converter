import google.generativeai as genai
import streamlit as st

# --- Configure Gemini with your API key ---
genai.configure(api_key=st.secrets["Gemini"])

# ✅ Find available and supported models
models = genai.list_models()
available_model_names = [model.name for model in models]

# ✅ Prefer the latest supported model
preferred_models = ["models/gemini-1.5-pro", "models/gemini-1.5-flash"]
selected_model_name = next((m for m in preferred_models if m in available_model_names), None)

if not selected_model_name:
    st.error("❌ No supported Gemini model found. Please check your API key or Google Generative AI access.")
else:
    model = genai.GenerativeModel(selected_model_name)

# --- Page layout ---
st.set_page_config(page_title="Unit Converter with Chatbot", layout="wide")

# --- Toggle state ---
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# --- Layout with two columns ---
col1, col2 = st.columns([3, 2])

# --- Unit Converter App ---
with col1:
    st.title("🔎 Unit Converter")

    category = st.selectbox("Select category", ["Length", "Weight", "Temperature"])
    value = st.number_input("Enter value", min_value=0.0, format="%f")

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


    if st.button("Open Chat with AI 🤖"):
        st.session_state.show_chat = not st.session_state.show_chat

# --- Chatbot Interface ---
import streamlit as st

# Custom CSS for border

with col2:
    if st.session_state.show_chat:

            if selected_model_name:
                st.title("💬 Chat with Gemini 🤖")

                if "messages" not in st.session_state:
                    st.session_state.messages = []

                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                if prompt := st.chat_input("Ask me anything!"):
                    st.session_state.messages.append({"role": "user", "content": prompt})

                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        response = model.generate_content(prompt)
                        st.markdown(response.text)

                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("💡 Chatbot is unavailable because no supported Gemini model was found.")


