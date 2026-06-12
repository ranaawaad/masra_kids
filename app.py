# app.py

import streamlit as st
import base64
from channels_data import CHANNELS
import random
import urllib.parse

# إعدادات الصفحة الأساسية لتظهر بشكل جذاب مع أيقونة مناسبة
st.set_page_config(page_title="مسار | المحتوى الهادف للطفل", page_icon="🧭", layout="centered")

# دالة لتحويل صورة الشعار إلى Base64 لعرضها بشكل احترافي
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_image_as_base64("masar_logo.png")

# تهيئة حالة المفضلة ونصيحة اليوم في جلسة العمل
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# نصائح تربوية لأولياء الأمور
PARENT_TIPS = [
    "حدد وقتاً معيناً يومياً لاستخدام الشاشات (مثلاً ساعة واحدة) ويفضل أن يكون بعد إتمام الواجبات المنزلية.",
    "شارك طفلك مشاهدة المحتوى ومناقشته؛ هذا يعزز الفهم ويقوي أواصر التواصل بينكما.",
    "استخدم أدوات الرقابة الأبوية وتطبيقات التصفية لحجب المحتوى غير اللائق وضمان بيئة تصفح آمنة.",
    "شجع طفلك على ممارسة أنشطة حركية ورياضية في العالم الحقيقي للحد من إدمان الشاشات الرقمية.",
    "اجعل غرف النوم مناطق خالية من الأجهزة الذكية ليلاً لمساعدة طفلك في الحصول على نوم صحي وعميق.",
    "كن قدوة حسنة لطفلك في استخدام الهواتف الذكية؛ فالأطفال يقلدون سلوكيات آبائهم تلقائياً.",
    "ركز على القنوات التفاعلية التي تطلب من الطفل القيام بأنشطة يدوية أو حل مشكلات بدلاً من التلقي السلبي."
]

if "tip_index" not in st.session_state:
    st.session_state.tip_index = random.randint(0, len(PARENT_TIPS) - 1)

# إعداد السمات وتغيير ألوان التطبيق ديناميكياً
THEME_CONFIGS = {
    "سماوي كلاسيكي 🌊": {
        "bg_gradient": "linear-gradient(135deg, #f5f7fb 0%, #e4ecfa 100%)",
        "text_color": "#1e293b",
        "primary_color": "#1e3a8a",
        "card_bg": "rgba(255, 255, 255, 0.75)",
        "card_border": "rgba(255, 255, 255, 0.6)",
        "sidebar_bg": "#f8fafc",
        "desc_color": "#4b5563",
        "shadow": "0 10px 30px 0 rgba(31, 38, 135, 0.04)",
        "btn_visit_bg": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
        "stat_card_bg": "rgba(255, 255, 255, 0.5)",
    },
    "غروب دافئ 🌅": {
        "bg_gradient": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 50%, #fed7aa 100%)",
        "text_color": "#431407",
        "primary_color": "#ea580c",
        "card_bg": "rgba(255, 255, 255, 0.8)",
        "card_border": "rgba(255, 255, 255, 0.7)",
        "sidebar_bg": "#fffbeb",
        "desc_color": "#7c2d12",
        "shadow": "0 10px 30px 0 rgba(234, 88, 12, 0.05)",
        "btn_visit_bg": "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #ea580c 0%, #c2410c 100%)",
        "stat_card_bg": "rgba(255, 255, 255, 0.6)",
    },
    "نعناع هادئ 🌿": {
        "bg_gradient": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)",
        "text_color": "#0f2f1d",
        "primary_color": "#16a34a",
        "card_bg": "rgba(255, 255, 255, 0.8)",
        "card_border": "rgba(255, 255, 255, 0.7)",
        "sidebar_bg": "#f0fdf4",
        "desc_color": "#14532d",
        "shadow": "0 10px 30px 0 rgba(22, 163, 74, 0.05)",
        "btn_visit_bg": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #059669 0%, #047857 100%)",
        "stat_card_bg": "rgba(255, 255, 255, 0.6)",
    },
    "فضاء مظلم 🌌": {
        "bg_gradient": "linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%)",
        "text_color": "#f1f5f9",
        "primary_color": "#818cf8",
        "card_bg": "rgba(17, 24, 39, 0.7)",
        "card_border": "rgba(255, 255, 255, 0.08)",
        "sidebar_bg": "#0f172a",
        "desc_color": "#cbd5e1",
        "shadow": "0 10px 30px 0 rgba(0, 0, 0, 0.5)",
        "btn_visit_bg": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
        "btn_visit_hover": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
        "stat_card_bg": "rgba(30, 41, 59, 0.7)",
    }
}

# شريط جانبي مع اختيار السمة
with st.sidebar:
    if logo_base64:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 20px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 80px; height: 80px; border-radius: 50%; box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);">
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>🧭 تطبيق مَسَار</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; font-size: 0.9rem; line-height: 1.5;'>مرشدك الذكي لتوجيه الأبناء نحو محتوى هادف وبناء يعزز قدراتهم للمستقبل بدلاً من المحتوى غير المفيد.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    selected_theme = st.selectbox(
        "🎨 اختر سمة التطبيق:",
        options=list(THEME_CONFIGS.keys()),
        index=0
    )
    
    st.markdown("---")
    
    # نصيحة اليوم التربوية
    st.markdown("##### 💡 نصيحة اليوم لأولياء الأمور:")
    st.info(PARENT_TIPS[st.session_state.tip_index])
    if st.button("نصيحة أخرى 🔄", key="next_tip_btn"):
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(PARENT_TIPS)
        st.rerun()

    st.markdown("---")
    
    # معلومات المطور
    st.markdown("""
        <div class="dev-card">
            <p style="font-size: 0.95rem; font-weight: bold; margin-bottom: 8px;">💻 معلومات التطوير</p>
            <p style="font-size: 0.85rem; line-height: 1.6; margin: 0;">
                برمجة وتصميم وتطوير المهندسة المتخصصة في الذكاء الاصطناعي<br>
                <span style="font-weight: 600; font-size: 0.9rem;">رنا وعدالله محمد</span><br>
                © 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

# استرداد قيم السمة الحالية
tc = THEME_CONFIGS[selected_theme]

# استدعاء خط Cairo وتصميم واجهة تفاعلية عصرية جداً متوافقة مع الجوال
st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* تخصيص الخلفية والخط الرئيسي للتطبيق */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            font-family: 'Cairo', sans-serif !important;
            background: {tc['bg_gradient']} !important;
            color: {tc['text_color']} !important;
        }}

        /* محاذاة النصوص والاتجاه من اليمين إلى اليسار واستخدام الخصائص المنطقية للغات RTL */
        * {{
            direction: rtl;
            text-align: right;
        }}
        
        /* إخفاء شريط العنوان الافتراضي لـ Streamlit */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* تحديد الحاوية الرئيسية */
        .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 550px !important;
            margin: auto;
        }}

        /* تخصيص شريط الجانبي (Sidebar) */
        [data-testid="stSidebar"] {{
            background-color: {tc['sidebar_bg']} !important;
            border-inline-start: 1px solid {tc['card_border']} !important;
        }}
        [data-testid="stSidebar"] * {{
            direction: rtl;
            text-align: right;
        }}
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
            color: {tc['text_color']} !important;
        }}

        /* رأس الصفحة وتصميم الشعار */
        .app-header {{
            text-align: center !important;
            margin-bottom: 1.5rem;
            padding: 5px;
        }}
        .app-header h1 {{
            color: {tc['primary_color']} !important;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 0.3rem;
            text-align: center !important;
        }}
        .app-header p {{
            color: {tc['desc_color']} !important;
            font-size: 1.05rem;
            text-align: center !important;
            line-height: 1.6;
        }}

        /* تسميات حقول الاختيار */
        label[data-testid="stWidgetLabel"] {{
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: {tc['text_color']} !important;
            margin-bottom: 10px !important;
            display: block;
        }}

        /* تصميم بطاقات القنوات بتأثير الزجاج الضبابي */
        div[data-testid="stVerticalBlockBorderContainer"] {{
            background: {tc['card_bg']} !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid {tc['card_border']} !important;
            border-radius: 20px !important;
            padding: 20px !important;
            margin-bottom: 15px !important;
            box-shadow: {tc['shadow']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        div[data-testid="stVerticalBlockBorderContainer"]:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 35px 0 rgba(31, 38, 135, 0.08) !important;
            border: 1px solid {tc['primary_color']} !important;
        }}
        .channel-title {{
            color: {tc['primary_color']} !important;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
            line-height: 1.4;
        }}
        .channel-desc {{
            color: {tc['desc_color']} !important;
            font-size: 0.95rem;
            margin-bottom: 15px;
            line-height: 1.6;
        }}

        /* تصميم شارة القناة */
        .channel-badge {{
            background-color: {tc['primary_color']};
            color: white !important;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 8px;
            display: inline-block;
            margin-bottom: 8px;
            line-height: 1.2;
        }}
        
        /* تصميم زر الانتقال إلى يوتيوب */
        .btn-visit-link {{
            background: {tc['btn_visit_bg']} !important;
            color: white !important;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.2);
            width: 100%;
            height: 40px;
            text-align: center !important;
        }}
        .btn-visit-link:hover {{
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3);
            background: {tc['btn_visit_hover']} !important;
            color: white !important;
        }}

        /* تخصيص أزرار Streamlit العادية لتظهر كأزرار ثانوية أنيقة */
        div[data-testid="stButton"] button {{
            border-radius: 50px !important;
            border: 1px solid {tc['primary_color']} !important;
            color: {tc['primary_color']} !important;
            background: rgba(255, 255, 255, 0.1) !important;
            width: 100% !important;
            height: 40px !important;
            padding: 6px 16px !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            font-family: 'Cairo', sans-serif !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 6px !important;
        }}
        div[data-testid="stButton"] button:hover {{
            background: {tc['primary_color']} !important;
            color: white !important;
            border-color: {tc['primary_color']} !important;
        }}

        /* تصحيح اتجاه نصوص Streamlit الافتراضية */
        div[data-testid="stMarkdownContainer"] p {{
            text-align: right;
            color: {tc['text_color']} !important;
        }}
        
        /* تجميل تصميم أزرار الاختيار المقسمة (Segmented Control) */
        div[data-testid="stSegmentedControl"] button {{
            border-radius: 12px !important;
            padding: 10px 16px !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            font-family: 'Cairo', sans-serif !important;
        }}

        /* بطاقات الإحصائيات */
        .stat-card {{
            background: {tc['stat_card_bg']} !important;
            border: 1px solid {tc['card_border']} !important;
            border-radius: 16px;
            padding: 12px;
            text-align: center !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
            margin-bottom: 10px;
        }}
        .stat-val {{
            font-size: 1.4rem;
            font-weight: 700;
            color: {tc['primary_color']};
            text-align: center !important;
            line-height: 1.2;
        }}
        .stat-lbl {{
            font-size: 0.8rem;
            color: {tc['desc_color']};
            text-align: center !important;
            margin-top: 4px;
        }}

        /* تصميم قسم المفضلة */
        .favorites-section {{
            background: rgba(30, 58, 138, 0.03) !important;
            border: 1px dashed {tc['primary_color']} !important;
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 20px;
        }}

        /* بطاقة معلومات المطور الجانبية */
        .dev-card {{
            text-align: center !important;
            padding: 15px !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 16px !important;
            border: 1px solid {tc['card_border']} !important;
            margin-top: 15px !important;
        }}
        .dev-card p {{
            text-align: center !important;
            color: {tc['desc_color']} !important;
        }}
    </style>
""", unsafe_allow_html=True)

# حوار التحقق الأبوي (Parental Gate Dialog)
@st.dialog("🔓 بوابة التحقق لأولياء الأمور", dismissible=True)
def parent_gate_dialog():
    st.write("للدخول إلى دليل ومراجع أولياء الأمور، يرجى الإجابة على السؤال التالي لضمان عدم دخول الأطفال:")
    
    if "gate_question" not in st.session_state:
        num1 = random.randint(5, 9)
        num2 = random.randint(6, 9)
        st.session_state.gate_question = {
            "q": f"كم ناتج ضرب {num1} في {num2}؟",
            "a": num1 * num2
        }
        
    st.markdown(f"**السؤال:** {st.session_state.gate_question['q']}")
    ans = st.number_input("إجابتك:", min_value=0, step=1, key="gate_answer_input")
    
    if st.button("التحقق والتأكيد ✔️"):
        if ans == st.session_state.gate_question['a']:
            st.session_state.parent_authenticated = True
            st.success("تم التحقق بنجاح! يمكنك الآن استعراض أدوات الرقابة والدليل الأبوي.")
            del st.session_state.gate_question
            st.rerun()
        else:
            st.error("إجابة خاطئة! حاول مرة أخرى للتأكيد.")

# حساب الإحصائيات الحيوية
total_channels = 0
for age in CHANNELS:
    for interest in CHANNELS[age]:
        total_channels += len(CHANNELS[age][interest])

total_interests = sum(len(CHANNELS[age]) for age in CHANNELS)
fav_count = len(st.session_state.favorites)

# عرض الشعار بشكل دائري متناسق في منتصف الصفحة
if logo_base64:
    st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 100px; height: 100px; border-radius: 50%; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15); margin-bottom: 10px;">
        </div>
    """, unsafe_allow_html=True)

# رأس الصفحة الترحيبي
st.markdown("""
    <div class="app-header">
        <h1>🧭 مَسَار</h1>
        <p>منصتك الذكية لتوجيه الأبناء نحو محتوى مرئي هادف ومفيد لبناء نسخة أفضل من أنفسهم.</p>
    </div>
""", unsafe_allow_html=True)

# عرض لوحة الإحصائيات
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">📺 {total_channels}</div>
            <div class="stat-lbl">قناة تعليمية</div>
        </div>
    """, unsafe_allow_html=True)
with col_stat2:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">💡 {total_interests}</div>
            <div class="stat-lbl">مجالاً وتصنيفاً</div>
        </div>
    """, unsafe_allow_html=True)
with col_stat3:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">⭐ {fav_count}</div>
            <div class="stat-lbl">قناة محفوظة</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# عرض قسم المفضلة في الأعلى إذا كان يحتوي على قنوات محفوظة
if st.session_state.favorites:
    with st.expander(f"⭐ القنوات المحفوظة لديك ({len(st.session_state.favorites)})", expanded=False):
        st.markdown("<div class='favorites-section'>", unsafe_allow_html=True)
        for fav in st.session_state.favorites:
            col_fav_name, col_fav_btn = st.columns([3, 1])
            with col_fav_name:
                st.markdown(f"**📺 {fav['name']}**")
            with col_fav_btn:
                if st.button("إزالة", key=f"remove_fav_{fav['name']}", icon="🗑️"):
                    st.session_state.favorites = [f for f in st.session_state.favorites if f['name'] != fav['name']]
                    st.rerun()
        
        # إنشاء خيار مشاركة وتصدير المفضلة
        st.markdown("<hr style='border-top: 1px dashed rgba(0,0,0,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
        share_text = "🧭 قنواتي المفضلة المقترحة من تطبيق مَسَار:\n\n"
        for i, fav in enumerate(st.session_state.favorites, 1):
            share_text += f"{i}. {fav['name']} - {fav['url']}\n"
        share_text += "\nتم اختيار هذه القنوات عبر تطبيق مَسَار لتوجيه الأطفال نحو محتوى تعليمي مفيد."
        
        whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
        
        col_wa, col_txt = st.columns([1, 1])
        with col_wa:
            st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank" class="btn-visit-link" style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.25);">
                    💬 شارك عبر الواتساب
                </a>
            """, unsafe_allow_html=True)
        with col_txt:
            st.text_area("نسخ قائمة القنوات المحفوظة:", value=share_text, height=100)
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 1. إعداد شريط البحث
col_search, col_scope = st.columns([2, 1])
with col_search:
    search_query = st.text_input("🔍 ابحث عن قناة أو منصة تعليمية:", placeholder="اكتب اسم القناة أو الكلمات المفتاحية...")
with col_scope:
    search_scope = st.selectbox("نطاق البحث:", ["القسم الحالي", "كل الفئات"])

st.markdown("<br>", unsafe_allow_html=True)

# تصفية وعرض القنوات
matching_channels = []
if search_query:
    if search_scope == "كل الفئات":
        for age in CHANNELS:
            for interest in CHANNELS[age]:
                for ch in CHANNELS[age][interest]:
                    if search_query.lower() in ch['name'].lower() or search_query.lower() in ch['description'].lower():
                        ch_copy = ch.copy()
                        ch_copy['badge_info'] = f"{age} | {interest}"
                        matching_channels.append(ch_copy)

# قراءة معلمات العنوان (Query Params) ومزامنتها
q_age = st.query_params.get("age", None)
q_interest = st.query_params.get("interest", None)

# 2. اختيار القسم الرئيسي
age_groups = list(CHANNELS.keys())
default_age = age_groups[0]
if q_age in age_groups:
    default_age = q_age

selected_age = st.segmented_control(
    "🧭 اختر الفئة العمرية أو القسم الرئيسي:", 
    options=age_groups, 
    selection_mode="single",
    default=default_age
)

# تحديث معلمات العنوان
if selected_age:
    st.query_params["age"] = selected_age

st.markdown("<br>", unsafe_allow_html=True)

# 3. اختيار الاهتمام بطريقة تفاعلية ممتازة متكيفة مع الجوال
if selected_age:
    interests = list(CHANNELS[selected_age].keys())
    default_interest = interests[0]
    if q_interest in interests:
        default_interest = q_interest

    selected_interest = st.segmented_control(
        "💡 اختر مجال الاهتمام:",
        options=interests,
        selection_mode="single",
        default=default_interest
    )

    if selected_interest:
        st.query_params["interest"] = selected_interest

    st.markdown("<br><br>", unsafe_allow_html=True)

    # إتمام منطق البحث للقسم الحالي إذا كان مفعلاً
    if search_query and search_scope == "القسم الحالي" and selected_interest:
        for ch in CHANNELS[selected_age][selected_interest]:
            if search_query.lower() in ch['name'].lower() or search_query.lower() in ch['description'].lower():
                ch_copy = ch.copy()
                ch_copy['badge_info'] = selected_interest
                matching_channels.append(ch_copy)

    # 4. عرض النتائج بناءً على البحث أو التصفح العادي مع التحقق الأبوي
    if selected_age == "🛡️ دليل وأدوات أولياء الأمور" and not st.session_state.get("parent_authenticated", False):
        # عرض شاشة قفل البوابة الأبوية
        st.warning("⚠️ هذا القسم يحتوي على أدوات ومراجع تقنية مخصصة لأولياء الأمور فقط.")
        if st.button("🔓 فتح بوابة أولياء الأمور"):
            parent_gate_dialog()
            
    else:
        # عرض زر قفل البوابة الأبوية في حال الدخول لهذا القسم
        if selected_age == "🛡️ دليل وأدوات أولياء الأمور" and st.session_state.get("parent_authenticated", False):
            if st.button("🔒 قفل بوابة أولياء الأمور"):
                st.session_state.parent_authenticated = False
                st.rerun()

        if search_query:
            st.markdown(f"##### 🔍 نتائج البحث عن **'{search_query}'** ({len(matching_channels)} نتيجة):")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not matching_channels:
                st.warning("عذراً، لم نجد قنوات تطابق بحثك. جرب كلمات مفتاحية أخرى أو غير نطاق البحث.")
            else:
                channels_to_display = matching_channels
        else:
            if selected_interest:
                channels_to_display = []
                for ch in CHANNELS[selected_age][selected_interest]:
                    ch_copy = ch.copy()
                    ch_copy['badge_info'] = selected_interest
                    channels_to_display.append(ch_copy)
                st.markdown(f"##### 📺 القنوات المقترحة في مجال **{selected_interest}**:")
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                channels_to_display = []

        # رندرة القنوات المصفاة
        for channel in channels_to_display:
            with st.container(border=True):
                # عرض الشارة
                st.markdown(f"<span class='channel-badge'>📌 {channel['badge_info']}</span>", unsafe_allow_html=True)
                # عنوان القناة ووصفها
                st.markdown(f"<div class='channel-title'>📺 {channel['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='channel-desc'>{channel['description']}</div>", unsafe_allow_html=True)
                
                # صف أزرار التفاعل (زيارة القناة + إضافة/إزالة المفضلة)
                col_btn_visit, col_btn_fav = st.columns([1, 1])
                
                with col_btn_visit:
                    st.markdown(f"""
                        <a href="{channel['url']}" target="_blank" class="btn-visit-link">
                            زيارة القناة ➔
                        </a>
                    """, unsafe_allow_html=True)
                
                with col_btn_fav:
                    is_fav = channel['name'] in [f['name'] for f in st.session_state.favorites]
                    
                    if is_fav:
                        if st.button("محفوظ", icon="❤️", key=f"fav_btn_{channel['name']}"):
                            st.session_state.favorites = [f for f in st.session_state.favorites if f['name'] != channel['name']]
                            st.rerun()
                    else:
                        if st.button("حفظ", icon="🤍", key=f"fav_btn_{channel['name']}"):
                            st.session_state.favorites.append(channel)
                            st.rerun()
