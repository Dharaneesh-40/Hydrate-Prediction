# 💧 Hydrate+
# Know Your Hydration. Improve Your Health.

import streamlit as st
import pandas as pd
import joblib

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Hydrate+",
    page_icon="💧",
    layout="wide"
)


# LOAD MODEL
@st.cache_resource
def load_model():
    model = joblib.load("hydration_model.pkl")
    encoders = joblib.load("label_encoders.pkl")
    return model, encoders

model, encoders = load_model()

gender_encoder = encoders["gender"]
activity_encoder = encoders["activity"]
weather_encoder = encoders["weather"]
target_encoder = encoders["target"]

# LOAD DATASET
@st.cache_data
def load_data():
    return pd.read_csv("Hydration_Updated.csv")

data = load_data()

# SIDEBAR
st.sidebar.title("💧 Hydrate+")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "💧 Assessment",
        "ℹ About"
    ]
)

# CUSTOM CSS
st.markdown(
    """
    <style>

    .stApp{
        background:#F4F9FC;
    }

    .hero{
        background:linear-gradient(90deg,#0077B6,#00B4D8);
        padding:45px;
        border-radius:20px;
        text-align:center;
        color:white;
        margin-bottom:30px;
    }

    .feature-card{
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
        text-align:center;
        font-weight:bold;
    }

    .footer{
        text-align:center;
        color:gray;
        padding:20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# HOME PAGE
if page == "🏠 Home":
    st.markdown(
        """
        <div class="hero">
        <h1>💧 Hydrate+</h1>
        <h3>Know Your Hydration.</h3>
        <h3>Improve Your Health.</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Welcome")
    st.write(
        """
Hydrate+ is a smart hydration assessment system that helps users
evaluate their hydration status using Machine Learning and
standard health guidelines.

Receive personalized hydration insights,
BMI evaluation,
and daily water recommendations through a simple
and interactive dashboard.
"""
    )

    st.write("")
    col1, col2 = st.columns(2)
    with col1:

        st.success("✔ Personalized Hydration Assessment")
        st.success("✔ BMI Evaluation")

    with col2:
        st.success("✔ Daily Water Recommendation")
        st.success("✔ Smart Health Report")
    st.markdown("---")
    st.subheader("💙 Health Benefits")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("❤️ Heart Health", "Healthy")
    c2.metric("🧠 Brain Function", "Optimal")
    c3.metric("🏃 Physical Activity", "Active")
    c4.metric("🚰 Daily Goal", "2-3 L")

    st.markdown("---")
    st.info(
        """
Healthy adults should generally consume around **2–3 litres of water per day**.

Actual water requirements vary depending on body weight,
physical activity level and weather conditions.
"""
    )
# ASSESSMENT PAGE
elif page == "💧 Assessment":
    st.markdown(
        """
        <div class="hero">
        <h1>💧 Hydrate+</h1>
        <h3>Hydration Assessment</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
Enter your personal information below to receive a
personalized hydration assessment and health report.
"""
    )

    st.markdown("---")

    left, right = st.columns(2)

    # LEFT COLUMN
    with left:
        age = st.slider(
            "Age",
            18,
            70,
            25
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        height = st.slider(
            "Height (cm)",
            140,
            210,
            170
        )

        weight = st.slider(
            "Weight (kg)",
            40,
            120,
            70
        )

    # RIGHT COLUMN
    with right:
        water = st.slider(
            "Daily Water Intake (Litres)",
            0.5,
            8.0,
            2.5,
            0.1
        )

        activity = st.selectbox(
            "Physical Activity Level",
            [
                "Low",
                "Moderate",
                "High"
            ]
        )

        weather = st.selectbox(
            "Weather Condition",
            [
                "Cold",
                "Normal",
                "Hot"
            ]
        )

    st.markdown("---")

    # BMI CALCULATION
   
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"

    elif bmi < 25:
        bmi_status = "Normal"

    elif bmi < 30:
        bmi_status = "Overweight"

    else:
        bmi_status = "Obese"

    recommended_water = round((weight * 35) / 1000, 2)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "BMI",
            round(bmi, 1)
        )

    with c2:
        st.metric(
            "BMI Status",
            bmi_status
        )

    with c3:
        st.metric(
            "Recommended Water",
            f"{recommended_water} L"
        )

    st.markdown("---")

    analyze = st.button(
        "🔍 Analyze Hydration",
        use_container_width=True
    )

    if analyze:

        gender_encoded = gender_encoder.transform(
            [gender]
        )[0]

        activity_encoded = activity_encoder.transform(
            [activity]
        )[0]

        weather_encoded = weather_encoder.transform(
            [weather]
        )[0]

        input_data = pd.DataFrame({

            "Age": [age],
            "Gender": [gender_encoded],
            "Weight (kg)": [weight],
            "Daily Water Intake (liters)": [water],
            "Physical Activity Level": [activity_encoded],
            "Weather": [weather_encoded]

        })

        prediction = model.predict(input_data)

        prediction = target_encoder.inverse_transform(
            prediction
        )[0]

        st.session_state["prediction"] = prediction
        st.session_state["water"] = water
        st.session_state["recommended"] = recommended_water
        st.session_state["bmi"] = round(bmi, 1)
        st.session_state["bmi_status"] = bmi_status

        difference = round(recommended_water - water, 2)

              
        # HYDRATION ANALYSIS
        if gender == "Male":

            if water < 2.5:
                hydration_status = "🔴 Low Hydration"
                score = 45
                risk = "High"

            elif 2.5 <= water <= 3.5:
                hydration_status = "🟢 Healthy Hydration"
                score = 95
                risk = "Low"

            elif 3.5 < water <= 4.0:
                hydration_status = "🔵 Well Hydrated"
                score = 85
                risk = "Low"

            else:
                hydration_status = "🟠 Excessive Water Intake"
                score = 60
                risk = "Moderate"

        else:

            if water < 2.0:
                hydration_status = "🔴 Low Hydration"
                score = 45
                risk = "High"

            elif 2.0 <= water <= 2.7:
                hydration_status = "🟢 Healthy Hydration"
                score = 95
                risk = "Low"

            elif 2.7 < water <= 3.5:
                hydration_status = "🔵 Well Hydrated"
                score = 85
                risk = "Low"

            else:
                hydration_status = "🟠 Excessive Water Intake"
                score = 60
                risk = "Moderate"

        st.markdown("---")

        st.subheader("📋 Hydration Assessment Report")

        st.success(hydration_status)

        st.progress(score / 100)

        st.write("")

        card1, card2, card3 = st.columns(3)

        with card1:
            st.metric(
                "Hydration Score",
                f"{score}/100"
            )

        with card2:
            st.metric(
                "BMI",
                round(bmi, 1)
            )

        with card3:
            st.metric(
                "Risk Level",
                risk
            )

        st.markdown("---")

        info1, info2 = st.columns(2)

        with info1:
            st.info(f"""
### Current Water Intake

{water} Litres
""")

        with info2:
            st.info(f"""
### Recommended Water Intake

{recommended_water} Litres
""")

        st.markdown("---")

        if difference > 0:

            st.warning(f"""
### 🎯 Today's Goal

Drink **{difference} Litres** more water today to
reach your recommended daily intake.
""")

        else:

            st.success("""
### 🎯 Today's Goal

Excellent!

Your water intake meets today's recommendation.
""")

        st.markdown("---")

        st.subheader("💡 Personalized Recommendations")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("""
🥗 Nutrition

✔ Eat watermelon

✔ Eat cucumber

✔ Include citrus fruits

✔ Eat fresh vegetables
""")

        with col2:
            st.info("""
🚰 Hydration Habits

✔ Carry a water bottle

✔ Drink every 1-2 hours

✔ Avoid skipping water

✔ Track daily intake
""")

        with col3:
            st.warning("""
🏃 Lifestyle

✔ Drink after exercise

✔ Stay hydrated outdoors

✔ Sleep well

✔ Reduce sugary drinks
""")

        st.markdown("---")
        st.subheader("📊 Summary")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.metric("BMI Status", bmi_status)
        with s2:
            st.metric("Current Intake", f"{water} L")
        with s3:
            st.metric("Recommended", f"{recommended_water} L")
        st.markdown("---")
        report = f"""
Hydrate+

Know Your Hydration. Improve Your Health.

-------------------------------------

Hydration Status : {hydration_status}

Hydration Score : {score}/100

BMI : {round(bmi,1)}

BMI Status : {bmi_status}

Current Water Intake : {water} L

Recommended Water Intake : {recommended_water} L

Risk Level : {risk}

-------------------------------------

Stay Hydrated • Stay Healthy • Stay Active
"""

        st.download_button(
            "📄 Download Report",
            data=report,
            file_name="Hydrate_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

# ABOUT PAGE
elif page == "ℹ About":

    st.markdown(
        """
        <div class="hero">
        <h1>💧 Hydrate+</h1>
        <h3>Know Your Hydration.</h3>
        <h3>Improve Your Health.</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📖 About Hydrate+")

    st.write(
        """
Hydrate+ is a Smart Hydration Assessment System that helps users
evaluate their daily hydration status using Machine Learning and
standard health guidelines.

The application combines personal information, lifestyle factors,
and hydration habits to generate easy-to-understand hydration
insights and personalized recommendations.
"""
    )

    st.markdown("---")
    st.subheader("🌟 Why Hydrate+")
    col1, col2 = st.columns(2)
    with col1:
        st.success("✔ Personalized Hydration Assessment")
        st.success("✔ BMI Evaluation")
        st.success("✔ Daily Water Recommendation")

    with col2:
        st.success("✔ Smart Health Report")
        st.success("✔ Easy-to-Understand Dashboard")
        st.success("✔ Lifestyle Recommendations")

    st.markdown("---")
    st.subheader("💧 Healthy Hydration Tips")
    tip1, tip2, tip3 = st.columns(3)
    with tip1:
        st.info(
            """
🥗 Nutrition

• Eat watermelon

• Eat cucumber

• Eat oranges

• Include soups
"""
        )

    with tip2:

        st.info(
            """
🚰 Daily Habits

• Carry a water bottle

• Drink every 2 hours

• Track your intake

• Avoid dehydration
"""
        )

    with tip3:

        st.info(
            """
🏃 Lifestyle

• Drink after exercise

• Stay hydrated outdoors

• Sleep well

• Reduce sugary drinks
"""
        )
    st.markdown("---")
    st.subheader("⚠ Disclaimer")
    st.warning(
        """
This application is intended for educational purposes only.

Hydration assessments are generated using machine learning
predictions and standard health guidelines and should not
replace professional medical advice.
"""
    )
    st.markdown("---")
    st.subheader("👨‍💻 Developer")
    st.info(
        """
**Dharaneeshwar Reddy**
Artificial Intelligence & Machine Learning
Mini Project
💧 Hydrate+
Know Your Hydration. Improve Your Health.
"""
    )

# FOOTER
st.markdown("---")
st.markdown(
    """
<div style="text-align:center; color:#555; padding:20px;">
<h3>💧 Hydrate+</h3>
<p><b>Know Your Hydration. Improve Your Health.</b></p>
<p>Stay Hydrated • Stay Healthy • Stay Active</p>
<p>© 2026 Dharaneeshwar Reddy</p>
</div>
""",
    unsafe_allow_html=True,
)