import streamlit as st
from groq import Groq
from streamlit_option_menu import option_menu
import time

# 1. ХУУДАСНЫ ТОХИРГОО (Заавал хамгийн дээр байх ёстой)
st.set_page_config(
    page_title=" Next Level AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. GROQ API ХОЛБОЛТ
# Өөрийн GSK түлхүүрийг доорх хашилтан дотор заавал тавиарай
client = Groq(api_key="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")

# 3. DARK MODE БОЛОН ЧАТНЫ ДИЗАЙН (CSS)
st.markdown("""
    <style>
/* Асуулт бичдэг талбарын дизайн */
.stChatInputContainer {
    padding-bottom: 20px;
}

.stChatInputContainer > div {
    background-color: #1E1E1E !important; /* Дотор талын өнгө - хар саарал */
    border: 1px solid #2e7d32 !important; /* Хүрээний өнгө - ногоон */
    border-radius: 15px !important; /* Буланг нь бөөрөнхийлөх */
}

.stChatInputContainer textarea {
    color: #ffffff !important; /* Бичиж буй үсгийн өнгө */
    caret-color: #4CAF50 !important; /* АНИВЧДАГ ЗУРААСНЫ ӨНГӨ (Курсор) */
}

/* Бичиж байхад анивчдаг курсорыг илүү тод болгох */
textarea::after {
    content: "▌";
    animation: blink 1s infinite;
}

@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
    </style>
    """, unsafe_allow_html=True)

# 4. ХАЖУУГИЙН ЦЭС (SIDEBAR)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100) # Жишээ лого
    st.title("Next Level AI")
    
    # Цэс (Option Menu)
    selected = option_menu(
        menu_title=None,
        options=["AI багш", "Хичээл", "Профайл"],
        icons=["robot", "book-half", "person-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#111B21"},
            "icon": {"color": "#00A884", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "color": "#D1D7DB"},
            "nav-link-selected": {"background-color": "#2A3942"},
        }
    )
    
    st.markdown("---")
    if st.button("🗑️ Яриаг цэвэрлэх", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. ЧАТНЫ ЛОГИК (CHAT ENGINE)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Өмнөх мессежүүдийг дэлгэцэнд харуулах
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Хэрэглэгч шинэ мессеж бичих үед
if prompt := st.chat_input("Мессеж илгээх..."):
    # Хэрэглэгчийн мессежийг харуулах
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI-д өгөх "Сэтгэлтэй" заавар (System Instructions)
    messages_to_ai = [
        {
            "role": "system", 
            "content": """Чи бол 'Next Level Mongol AI' нэртэй, монгол хүний сэтгэлгээ, дурсамжинд суурилсан туслах багш байна. 
            Чиний гол онцлог бол үгсийг зөвхөн шууд орчуулах биш, тухайн үгтэй холбоотой монгол ахуйн дурсамж, мэдрэмжээр баяжуулж тайлбарлах явдал юм.

            Хэрэглэгч 'tree' гэж юу гэсэн үг вэ? гэж асуувал чи заавал дараах байдлаар хариулна: 
            'Tree' гэдэг нь монгол хэлээр 'Мод' гэсэн үг. Гэхдээ энэ бол зүгээр нэг ургамал биш юм. Санаж байна уу, чи багадаа модны мөчир дамжиж авирч байгаад хальтирч унан өвдгөө шалбалчихаад, уйлаад гэр рүүгээ гүйхэд чинь ээж чинь чамайг яаж чанга тэвэрч аргаддаг байлаа даа? Мод бол тэр л дулаахан дурсамжийг хадгалж байдаг амьд байгаль юм.

            Бусад үгсийг тайлбарлахдаа ч гэсэн иймэрхүү монгол хүний амьдрал, сэтгэл хөдлөл, дурсамжтай холбож маш дотноор хариулж бай."""
        }
    ]
    
    # Түүхийг нэмэх
    for m in st.session_state.messages:
        messages_to_ai.append({"role": m["role"], "content": m["content"]})

    # Groq-аас хариу авах хэсэг
    try:
        with st.chat_message("assistant"):
            with st.spinner("AI бодож байна..."):
                chat_completion = client.chat.completions.create(
                    messages=messages_to_ai,
                    model="llama-3.3-70b-versatile",
                    temperature=0.4, # Бага зэрэг уран сэтгэмж нэмнэ
                    max_tokens=2048
                )
                answer = chat_completion.choices[0].message.content
               # --- АНИВЧДАГ ЭФФЕКТ НЭМЭХ ХЭСЭГ ---
        placeholder = st.empty() 
        displayed_text = ""
        
        # answer дотор байгаа текстийг үг үгээр нь салгаж харуулна
        for word in answer.split():
            displayed_text += word + " "
            time.sleep(0.04) 
            placeholder.markdown(displayed_text + "▌")
        
        placeholder.markdown(displayed_text) 
        # -------------------------------
        
        # Хариуг хадгалах
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Алдаа гарлаа: {e}")
  
# 6. ХӨЛИЙН ХЭСЭГ (FOOTER)#python -m streamlit run nlaiv3.py
st.sidebar.markdown("---")
st.sidebar.caption("By алтансүх, чандмань эрдэнэ, мягмаржаргал, номинзаяа | Graphics & AI")
