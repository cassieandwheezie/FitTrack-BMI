import streamlit as st
import plotly.graph_objects as go
from insert_data import insert_data
from view_data import view_data
from pdf import generate_pdf
import pandas as pd
import plotly.express as px
from auth import login_user, register_user

st.set_page_config(page_title="FitTrack BMI", page_icon="🏋️", layout="centered")
# Initialize session state for user authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# If user is NOT logged in, show authentication forms and stop further execution
if not st.session_state.logged_in:
    st.title("🏋️ FitTrack BMI")
    tab_login, tab_register = st.tabs(["🔒 Log In", "📝 Register"])

    with tab_login:
        st.subheader("Login to Your Account")
        login_email = st.text_input("Email", key="login_email")
        login_pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Log In", type="primary"):
            success, user_id_or_msg = login_user(login_email, login_pwd)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id_or_msg
                st.session_state.user_email = login_email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error(user_id_or_msg)

    with tab_register:
        st.subheader("Create a New Account")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pwd = st.text_input("Password (min 8 characters)", type="password", key="reg_pwd")
        if st.button("Register Account"):
            success, user_id_or_msg = register_user(reg_email, reg_pwd)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id_or_msg
                st.session_state.user_email = reg_email
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error(user_id_or_msg)

    st.stop()  # Prevents rendering calculator until logged in
@st.dialog("📊 BMI Categories Chart")
def show_bmi_chart():
    st.write("BMI categories are general screening classifications "
    "based on height and weight. BMI alone cannot determine "
    "a person's overall health or body composition.")
    st.table({
        "BMI Range": ["Below 18.5", "18.5 – 24.9", "25.0 – 29.9", "30.0 and above"],
        "Weight Classification": ["Underweight 🟡", "Normal Weight 🟢", "Overweight 🟠", "Obesity 🔴"]
    })
    st.info("Note: BMI is a general screening tool and may not account for muscle mass, bone density, or overall body composition.")

col1, col2 = st.columns([0.75, 0.25], vertical_alignment="center")
with col1:
    st.header(" 🏋️ BMI Calculator", divider='rainbow')
with col2:
    if st.button("View chart 📊", use_container_width=True):
        show_bmi_chart()

st.write("Calculate your Body Mass Index (BMI)")
name = st.text_input("👤Enter your name: ")
age = st.number_input("🎂 Enter your age", min_value=1, max_value=120, step=1)
gender = st.selectbox("⚧ Select your gender", ["Male", "Female", "Other"])

col1, col2 = st.columns([3, 1], vertical_alignment="center")
with col1:
    weight_value = st.number_input("⚖️Enter your weight", min_value=1.0)
with col2:
    weight_unit = st.selectbox("Unit", ["kg", "g", "lb"])
if weight_unit == "kg":
    weight = weight_value
elif weight_unit == "g":
    weight = weight_value / 1000
else:
    weight = weight_value * 0.453592

col1, col2 = st.columns([3, 1], vertical_alignment="center")
with col1:
    height_value = st.number_input("📏Enter your height", min_value=0.1)
with col2:
    height_unit = st.selectbox("Unit", ["m", "cm", "ft", "in"])
if height_unit == "m":
    height = height_value
elif height_unit == "cm":
    height = height_value / 100
elif height_unit == 'ft':
    height = height_value * 0.3048
else:
    height = height_value * 0.0254

with st.sidebar:
    st.header("🏋️ About FitTrack BMI")
    st.write("FitTrack BMI is a simple health and fitness application built using Streamlit. It helps users calculate their Body Mass Index (BMI) based on their height and weight and provides insights into their health status.")
    st.title("Features")
    st.write("✅ BMI Calculation")
    st.write("✅ BMI Category Classification")
    st.write("✅ Personalized Health Tips")
    st.write("✅ Water Intake Recommendation")
    st.write("✅ Simple and Interactive User Interface")
    search_name = st.text_input("🔍 Search by Name")
    st.write(f"👤 Logged in as: **{st.session_state.user_email}**")
    if st.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_email = ""
        st.rerun()
        st.divider()
    
    if st.button("📜 View BMI History"):
        history = view_data(st.session_state.user_id, search_name)
        if history is not None and len(history) > 0:
            st.dataframe(
                history,
                use_container_width=True
            )
        else:
            st.info("No BMI records found, or the database is unavailable.")
    if st.checkbox("Know about BMI"):
        st.text("Body Mass Index (BMI) is a measure that uses a person's height and weight to estimate whether their body weight falls within a healthy range.")
        st.header("BMI Formula")
        st.text("BMI = Weight (kg) / [Height (m)]²")
        st.header("Water intake")
        st.text("There is no initial water intake formula but the commonly followed guideline is")
        st.text("Illustrative estimate: weight (kg) × 35 ml/day")
        st.caption(
            "This is a simplified estimate, not a universal requirement. "
            "Water needs vary with activity, climate and individual health."
)

st.write("---")

# Initialize the calculation state if it doesn't exist
if "calculated" not in st.session_state:
    st.session_state["calculated"] = False

calculate = st.button("Calculate BMI", type="primary")

if calculate:
    st.session_state["calculated"] = False
    st.session_state.pop("bmi_result", None)
    if not name.strip():
        st.error("Please enter your name")
        st.stop()
    if weight < 10.0 or weight > 300.0:
        st.error("❌ Invalid weight! Converted weight must be between 10 kg and 300 kg. Please check your value and selected unit.")
        st.session_state["calculated"] = False
        st.stop()
    if height < 0.5 or height > 2.5:
        st.error("❌ Invalid height! Converted height must be between 0.5 m and 2.5 m. Please check your value and selected unit.")
        st.session_state["calculated"] = False
        st.stop()
    st.session_state["calculated"] = True

    # Calculate current values
    bmi_val = round(weight / (height ** 2), 2)
    # Simplified daily water intake estimate, not a medical requirement
    water_val = round(weight * 35)
    
    if bmi_val < 18.5:
        category_val = "underweight"
    elif 18.5 <= bmi_val < 25.0:
        category_val = "normal weight"
        st.snow()
        st.balloons()
    elif 25.0 <= bmi_val < 30.0:
        category_val = "overweight"
    else:
        category_val = "obesity"

    # Save to session state so the UI can read it outside this block
  
    st.session_state["bmi_result"] = {
        "name": name.strip(),
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "bmi": bmi_val,
        "water": water_val,
        "category": category_val
    }

    st.session_state["calculated"] = True


 
    # Save the record using the database-level duplicate check
    save_status = insert_data(
    st.session_state.user_id,
    name.strip(), age, gender, height, weight,
    bmi_val, category_val, water_val
)

    if save_status is True:
        st.toast("Data saved successfully! 💾")

    elif save_status is False:
        st.info(
            "This record was already saved within "
            "the last 30 seconds."
        )

    else:
        st.error(
            "Could not save your BMI record. "
            "Please check the database connection."
        )

# Keep the results rendered if calculated is True

if st.session_state.get("calculated", False):
    result = st.session_state["bmi_result"]

    name = result["name"]
    age = result["age"]
    gender = result["gender"]
    height = result["height"]
    weight = result["weight"]
    bmi = result["bmi"]
    water = result["water"]
    category = result["category"]


    tab1, tab2, tab3 = st.tabs(["📊 Results", "💡 Health tips", "📈 Progress Chart"])
    with tab1:
        st.metric(label="Calculated BMI", value=f"{bmi:.1f}")
        fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=bmi,

        title={"text":"BMI Gauge"},

        gauge={

            "axis":{"range":[0,40]},

            "steps":[
                {"range":[0,18.5],"color":"yellow"},

                {"range":[18.5,25],"color":"green"},

                {"range":[25,30],"color":"orange"},

                {"range":[30,40],"color":"red"}

            ]

        }

    )

)
        st.plotly_chart(fig, use_container_width=True)
       
        min_weight = 18.5 * (height ** 2)
        max_weight = 25 * (height ** 2)

        st.info(f"💡A normal healthy weight range is: {min_weight:.1f} kg - {max_weight:.1f} kg")

        if category == "underweight":
            st.error("Category : Underweight 🟡")
            st.info("Tip: Consider consulting a healthcare provider or nutritionist to discuss healthy weight gain strategies.")
        elif category == "normal weight":
            st.success("Category :Normal Weight 🟢")
            st.info("Tip: Great job! Maintain your current lifestyle with balanced nutrition and regular physical activity.")
        elif category == "overweight":
            st.warning("Category: Overweight 🟠")
            st.info("Tip: Incorporating more whole foods and active minutes into your day can help manage your weight.")
        else:
            st.error("Category: Obesity 🔴")
            st.info("Tip: It may be beneficial to discuss tailored health plans with a healthcare professional.")
    
    
        if st.button("📄 Generate PDF Report"):
            try:
                filename = "BMI_REPORT.pdf"

                pdf_file = generate_pdf(
                    filename, name, age, gender,
                    height, weight, bmi, category, water
                )

                with open(pdf_file, "rb") as file:
                    pdf_bytes = file.read()

                if pdf_bytes.startswith(b"%PDF-"):
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_bytes,
                        file_name="BMI_Report.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.error("The generated file is not a valid PDF.")

            except Exception as e:
                st.error(f"PDF generation failed: {e}")

                st.write("Returned:", pdf_bytes)
                with open(pdf_bytes, "rb") as file: 
                    st.download_button(label="⬇ Download PDF",data=pdf_bytes,file_name="BMI_Report.pdf",mime="application/pdf")


    with tab2:
        with st.expander("🏃 Fitness Recommendations"):
            st.header("🚴 Fitness Tips")
            st.write("• Exercise at least 30 minutes daily")
            st.write("• Sleep 7-8 hours")
            st.write("• Eat fruits and vegetables")
            st.write("• Drink enough water")

            
        with st.expander("🍽️ Diet Suggestions"):
            if category == "underweight":
                st.header("🍯 Recommended Foods", divider='rainbow')
                st.write("🥛 Milk, yogurt, and paneer")
                st.write("🍌 Bananas, mangoes, and dried fruits")
                st.write("🥜 Nuts and seeds (almonds, walnuts, peanuts)")
                st.write("🍚 Rice, whole wheat bread, and potatoes")
                st.write("🥚 Eggs, chicken, fish, tofu, and legumes")
                with st.expander("💡 Healthy Habits"):
                    st.write("• Eat 5–6 smaller meals throughout the day.")
                    st.write("• Include a source of protein with every meal.")
                    st.write("• Add healthy fats like nuts, seeds, and peanut butter.")
                    st.write("• Strength training can help build muscle mass.")
                    st.write("• Get adequate sleep for recovery.")
            elif category == "normal weight":
                st.header("🍽️ Recommended Foods", divider='rainbow')
                st.write("🥗 Plenty of vegetables and fruits")
                st.write("🌾 Whole grains (brown rice, oats, whole wheat)")
                st.write("🍗 Lean protein (chicken, fish, eggs, legumes)")
                st.write("🥛 Low-fat dairy products")
                st.write("🥜 Healthy fats from nuts and seeds")
                with st.expander("💡 Healthy Habits"):
                    st.write("• Exercise for at least 30 minutes most days.")
                    st.write("• Drink enough water throughout the day.")
                    st.write("• Limit sugary drinks and processed foods.")
                    st.write("• Get 7–9 hours of quality sleep.")
                    st.write("• Continue eating a balanced diet.")
            elif category == "overweight":
                st.header("🍽️ Recommended Foods", divider='rainbow')
                st.write("🥦 Green vegetables and salads")
                st.write("🍎 Fresh fruits instead of sweets")
                st.write("🍗 Lean protein such as chicken, fish, tofu, and beans")
                st.write("🌾 Whole grains instead of refined flour")
                st.write("💧 Plenty of water and unsweetened beverages")
                with st.expander("💡 Healthy Habits"):
                    st.write("• Reduce sugary snacks and soft drinks.")
                    st.write("• Control portion sizes during meals.")
                    st.write("• Aim for at least 150 minutes of exercise per week.")
                    st.write("• Avoid late-night overeating.")
                    st.write("• Walk whenever possible.")
            else:
                st.header("🍽️ Recommended Foods", divider='rainbow')
                st.write("🥬 Leafy green vegetables")
                st.write("🫘 Beans, lentils, and other legumes")
                st.write("🍓 Low-sugar fruits such as berries and apples")
                st.write("🐟 Lean protein sources")
                st.write("🌾 High-fiber whole grains")
                with st.expander("💡 Healthy Habits"):
                    st.write("• Focus on gradual, sustainable weight loss.")
                    st.write("• Choose home-cooked meals more often.")
                    st.write("• Stay physically active according to your fitness level.")
                    st.write("• Keep track of meals and daily activity.")
                    st.write("• Consult a healthcare professional for a personalized plan if needed.")
            st.warning("**Disclaimer**: These recommendations are for general guidance only. Individual nutritional needs vary based on age, medical conditions, activity level, and other factors. Consult a qualified healthcare professional or registered dietitian for personalized advice.")

        with st.expander("💪 Exercise Recommendations"):
            st.header(" 💡 Exercise Tips", divider='rainbow')
            st.write("• Warm up before every workout.")
            st.write("• Stay hydrated.")
            st.write("• Increase intensity gradually.")
            st.write("• Rest at least one day each week.")
            st.write("• Stop exercising if you feel pain or dizziness.")
                            
        with st.expander("🌊 Water Intake Recommendation"):
            st.metric(
    label="💧 Estimated Daily Water Intake",
    value=f"{water:.0f} ml/day"
)
            st.caption(
                "This is a rough estimate, not a prescribed target. "
                "Individual hydration needs vary."
            )
   
            
            waterhad = st.number_input("Enter water consumed today(ml): ", min_value=0, step=100, key="water_input")
            
            progress = waterhad / water
            st.write(f"Consumed: **{waterhad} ml**")
            st.progress(min(progress, 1.0))
            
            remaining = max(water - waterhad, 0.0)
            st.write(f"Remaining: **{remaining:.0f} ml**")
            
            if waterhad >= water:
                st.success("🎉 Goal achieved!")
            elif waterhad >= water * 0.75:
                st.info("👍 You're close to your goal.")
            elif waterhad > 0:
                 st.warning("💧 Drink some more water.")
    # TAB 3: PROGRESS CHART
    with tab3:
        st.header("📈 Your BMI Trend Over Time", divider='rainbow')
        user_records = view_data(st.session_state.user_id)

        if user_records:
            df = pd.DataFrame(
                user_records, 
                columns=["Name", "Age", "Gender", "Height", "Weight", "BMI", "Category", "Water", "Date Recorded"]
            )
            df["Date Recorded"] = pd.to_datetime(df["Date Recorded"])
            df = df.sort_values("Date Recorded")

            fig_trend = px.line(
                df, 
                x="Date Recorded", 
                y="BMI", 
                markers=True, 
                title="BMI History Progress",
                labels={"BMI": "BMI Value", "Date Recorded": "Date"}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No recorded BMI entries available to chart yet.")
    
                

st.caption("Developed by Manmeet Kaur")
st.caption("Built with streamlit & PostgreSQL")
st.warning(
    "Health Disclaimer: FitTrack BMI is intended for general "
    "informational and educational purposes only. BMI is a "
    "screening measure, not a medical diagnosis. Water intake "
    "and lifestyle suggestions are general estimates and may "
    "not be suitable for everyone. This application does not "
    "replace professional medical advice, diagnosis or treatment. "
    "Consult a qualified healthcare professional for "
    "personalized guidance."
)
