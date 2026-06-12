# app.py

import streamlit as st
import base64
from channels_data import CHANNELS

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

# استدعاء خط Cairo وتصميم واجهة تفاعلية عصرية جداً متوافقة مع الجوال
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* تخصيص الخلفية والخط الرئيسي للتطبيق */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            font-family: 'Cairo', sans-serif !important;
            background: linear-gradient(135deg, #f5f7fb 0%, #e4ecfa 100%) !important;
        }

        /* محاذاة النصوص والاتجاه من اليمين إلى اليسار */
        * {
            direction: rtl;
            text-align: right;
        }
        
        /* إخفاء شريط العنوان الافتراضي لـ Streamlit لإعطاء مظهر تطبيق ويب متكامل */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* تحديد الحاوية الرئيسية لمحاكاة واجهة الهاتف المحمول الأنيقة على الشاشات الكبيرة */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 550px !important;
            margin: auto;
        }

        /* تخصيص شريط الجانبي (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-left: 1px solid #e2e8f0 !important;
        }
        [data-testid="stSidebar"] * {
            direction: rtl;
            text-align: right;
        }

        /* رأس الصفحة وتصميم الشعار */
        .app-header {
            text-align: center !important;
            margin-bottom: 1.5rem;
            padding: 5px;
        }
        .app-header h1 {
            color: #1e3a8a;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 0.3rem;
            text-align: center !important;
        }
        .app-header p {
            color: #4b5563;
            font-size: 1.05rem;
            text-align: center !important;
            line-height: 1.6;
        }

        /* تسميات حقول الاختيار */
        label[data-testid="stWidgetLabel"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #1e293b !important;
            margin-bottom: 10px !important;
            display: block;
        }

        /* تصميم بطاقات القنوات بتأثير الزجاج الضبابي (Glassmorphism) وتخصيص حاويات Streamlit */
        div[data-testid="stVerticalBlockBorderContainer"] {
            background: rgba(255, 255, 255, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 20px !important;
            padding: 20px !important;
            margin-bottom: 15px !important;
            box-shadow: 0 10px 30px 0 rgba(31, 38, 135, 0.04) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stVerticalBlockBorderContainer"]:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 35px 0 rgba(31, 38, 135, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
        }
        .channel-title {
            color: #1e3a8a;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
            line-height: 1.4;
        }
        .channel-desc {
            color: #4b5563;
            font-size: 0.95rem;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        /* تصميم زر الانتقال إلى يوتيوب */
        .btn-visit-link {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
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
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.25);
            width: 100%;
            height: 40px;
            text-align: center !important;
        }
        .btn-visit-link:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(220, 38, 38, 0.35);
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
            color: white !important;
        }

        /* تخصيص أزرار Streamlit العادية لتظهر كأزرار ثانوية أنيقة */
        div[data-testid="stButton"] button {
            border-radius: 50px !important;
            border: 1px solid #1e3a8a !important;
            color: #1e3a8a !important;
            background: rgba(255, 255, 255, 0.6) !important;
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
        }
        div[data-testid="stButton"] button:hover {
            background: #1e3a8a !important;
            color: white !important;
            border-color: #1e3a8a !important;
        }

        /* تصحيح اتجاه نصوص Streamlit الافتراضية */
        div[data-testid="stMarkdownContainer"] p {
            text-align: right;
        }
        
        /* تجميل تصميم أزرار الاختيار المقسمة (Segmented Control) لتكون مناسبة للمس بالإصبع */
        div[data-testid="stSegmentedControl"] button {
            border-radius: 12px !important;
            padding: 10px 16px !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            font-family: 'Cairo', sans-serif !important;
        }

        /* تصميم قسم المفضلة */
        .favorites-section {
            background: rgba(30, 58, 138, 0.05) !important;
            border: 1px dashed rgba(30, 58, 138, 0.2) !important;
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 20px;
        }

        /* بطاقة معلومات المطور الجانبية */
        .dev-card {
            text-align: center !important;
            padding: 15px !important;
            background: rgba(30, 58, 138, 0.04) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(30, 58, 138, 0.08) !important;
            margin-top: 15px !important;
        }
        .dev-card p {
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# تهيئة حالة المفضلة في جلسة العمل
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# إعداد محتويات الشريط الجانبي (Sidebar)
with st.sidebar:
    if logo_base64:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 20px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 80px; height: 80px; border-radius: 50%; box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);">
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>🧭 تطبيق مَسَار</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; font-size: 0.9rem; color: #4b5563; line-height: 1.5;'>مرشدك الذكي لتوجيه الأبناء نحو محتوى هادف وبناء يعزز قدراتهم للمستقبل بدلاً من المحتوى غير المفيد.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # إضافة معلومات التطوير وتوقيع المهندسة في شريط المعلومات
    st.markdown("""
        <div class="dev-card">
            <p style="font-size: 0.95rem; color: #1e3a8a; font-weight: bold; margin-bottom: 8px;">💻 معلومات التطوير</p>
            <p style="font-size: 0.85rem; color: #4b5563; line-height: 1.6; margin: 0;">
                برمجة وتصميم وتطوير المهندسة المتخصصة في الذكاء الاصطناعي<br>
                <span style="color: #1e3a8a; font-weight: 600; font-size: 0.9rem;">رنا وعدالله محمد</span><br>
                © 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

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
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 1. اختيار الفئة العمرية باستخدام أزرار مقسمة عصرية
age_groups = list(CHANNELS.keys())
selected_age = st.segmented_control(
    "👶 اختر الفئة العمرية للطفل:", 
    options=age_groups, 
    selection_mode="single",
    default=age_groups[0]
)

st.markdown("<br>", unsafe_allow_html=True)

# 2. اختيار الاهتمام بطريقة تفاعلية ممتازة متكيفة مع الجوال
if selected_age:
    interests = list(CHANNELS[selected_age].keys())
    selected_interest = st.segmented_control(
        "💡 اختر مجال الاهتمام:",
        options=interests,
        selection_mode="single",
        default=interests[0]
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 3. عرض نتائج التوصية داخل بطاقات بتأثير زجاجي وتنسيق ممتاز
    if selected_interest:
        recommended_channels = CHANNELS[selected_age][selected_interest]
        
        st.markdown(f"##### 📺 القنوات المقترحة في مجال **{selected_interest}**:")
        st.markdown("<br>", unsafe_allow_html=True)
        
        for channel in recommended_channels:
            # استخدام حاويات Streamlit مع الحدود (Border Container)
            with st.container(border=True):
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
                    # تحقق إذا كانت القناة محفوظة مسبقاً
                    is_fav = channel['name'] in [f['name'] for f in st.session_state.favorites]
                    
                    if is_fav:
                        if st.button("محفوظ", icon="❤️", key=f"fav_btn_{channel['name']}"):
                            st.session_state.favorites = [f for f in st.session_state.favorites if f['name'] != channel['name']]
                            st.rerun()
                    else:
                        if st.button("حفظ", icon="🤍", key=f"fav_btn_{channel['name']}"):
                            st.session_state.favorites.append(channel)
                            st.rerun()
