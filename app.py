
import streamlit as st
import pandas as pd
import joblib

# إعداد الصفحة
st.set_page_config(
    page_title="نظام توقع المعدل التراكمي",
    page_icon="🎓",
    layout="wide"
)

# تحميل الموديل والملفات
model = joblib.load("gpa_model.pkl")
features = joblib.load("gpa_features.pkl")
medians = joblib.load("gpa_medians.pkl")

# تصميم الصفحة
st.markdown("""
<style>
    .main {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, p, label {
        text-align: right;
    }
    div[data-testid="stMetric"] {
        direction: rtl;
        text-align: center;
    }
    .result {
        background-color: #e8f5e9;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: #1b5e20;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 نظام التنبؤ بالمعدل الفصلي للطلاب")
st.markdown("""
يساعد هذا النظام في توقع المعدل الفصلي القادم للطالب
باستخدام بياناته الأكاديمية السابقة والحالية.
""")

st.divider()

st.subheader("📚 البيانات الأكاديمية")

# تقسيم المدخلات إلى مجموعات
col1, col2 = st.columns(2)

with col1:
    st.markdown("### المعدلات التراكمية والفصلية")

    term_index = st.number_input(
        "رقم الفصل الدراسي",
        min_value=1,
        max_value=20,
        value=6
    )

    level_by_hours = st.number_input(
        "المستوى الدراسي حسب الساعات",
        min_value=1,
        max_value=10,
        value=4
    )

    cum_gpa = st.number_input(
        "المعدل التراكمي الحالي",
        min_value=0.0,
        max_value=4.0,
        value=2.55,
        step=0.01
    )

    term_gpa = st.number_input(
        "معدل الفصل الدراسي الحالي",
        min_value=0.0,
        max_value=4.0,
        value=2.93,
        step=0.01
    )

    prev_term_gpa = st.number_input(
        "معدل الفصل السابق",
        min_value=0.0,
        max_value=4.0,
        value=3.21,
        step=0.01
    )

    prev2_term_gpa = st.number_input(
        "معدل الفصل قبل السابق",
        min_value=0.0,
        max_value=4.0,
        value=2.56,
        step=0.01
    )

    earned_hours = st.number_input(
        "إجمالي الساعات المجتازة",
        min_value=0,
        value=105
    )

    registered_hours = st.number_input(
        "الساعات المسجلة في الفصل الحالي",
        min_value=0,
        value=18
    )

with col2:
    st.markdown("### الأداء الأكاديمي")

    failed_courses_cum = st.number_input(
        "إجمالي المقررات التي سبق الرسوب فيها",
        min_value=0,
        value=1
    )

    failed_this_term = st.number_input(
        "عدد المقررات التي رسب فيها الطالب هذا الفصل",
        min_value=0,
        value=0
    )

    withdrawn_this_term = st.number_input(
        "عدد المقررات المنسحب منها",
        min_value=0,
        value=0
    )

    retakes_this_term = st.number_input(
        "عدد المقررات المعادة هذا الفصل",
        min_value=0,
        value=0
    )

    avg_attendance = st.number_input(
        "متوسط نسبة الحضور (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0
    )

    total_warnings = st.number_input(
        "إجمالي الإنذارات الأكاديمية",
        min_value=0,
        value=0
    )

    consecutive_warnings = st.number_input(
        "عدد الإنذارات المتتالية",
        min_value=0,
        value=0
    )

    high_school_percentage = st.number_input(
        "نسبة الثانوية العامة (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0
    )

st.divider()

st.subheader("🔮 توقع المعدل الفصلي القادم")

if st.button("احسب المعدل المتوقع", use_container_width=True):

    # حساب اتجاه المعدل
    gpa_trend = term_gpa - prev_term_gpa

    # تجميع البيانات
    input_data = {
        "term_index": term_index,
        "level_by_hours": level_by_hours,
        "cum_gpa": cum_gpa,
        "term_gpa": term_gpa,
        "prev_term_gpa": prev_term_gpa,
        "prev2_term_gpa": prev2_term_gpa,
        "gpa_trend": gpa_trend,
        "earned_hours": earned_hours,
        "registered_hours": registered_hours,
        "failed_courses_cum": failed_courses_cum,
        "failed_this_term": failed_this_term,
        "withdrawn_this_term": withdrawn_this_term,
        "retakes_this_term": retakes_this_term,
        "avg_attendance": avg_attendance,
        "total_warnings": total_warnings,
        "consecutive_warnings": consecutive_warnings,
        "high_school_percentage": high_school_percentage
    }

    # تجهيز البيانات بنفس ترتيب التدريب
    input_df = pd.DataFrame([input_data])
    input_df = input_df[features]

    # معالجة القيم المفقودة إن وجدت
    input_df = input_df.fillna(medians)

    # التوقع
    prediction = model.predict(input_df)[0]

    # عرض النتيجة
    prediction = max(0, min(4, prediction))

    st.markdown("### 📊 نتيجة التوقع")

    st.markdown(
        f"""
        <div class="result">
            <h3>المعدل الفصلي المتوقع</h3>
            <h1>{prediction:.2f} / 4.00</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "هذه النتيجة تقديرية وتعتمد على البيانات التي تم إدخالها "
        "وأداء نموذج تعلم الآلة، ولا تمثل المعدل الرسمي للطالب."
    )

st.divider()

st.caption("مشروع التنبؤ بالمعدل التراكمي باستخدام تعلم الآلة")
st.caption("إعداد: Mohamed Eita")
