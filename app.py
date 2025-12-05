import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="단어 암기 앱", page_icon="📚", layout="centered")
st.markdown("<h1 style='text-align:center; color:#4CAF50;'>📚 영어 단어 암기 앱</h1>", unsafe_allow_html=True)
CSV_PATH = "vocab.csv"

if os.path.exists(CSV_PATH):
    vocab_df = pd.read_csv(CSV_PATH)
else:
    default_words = [
        {"word": "apple", "meaning": "사과"},
        {"word": "banana", "meaning": "바나나"},
        {"word": "cat", "meaning": "고양이"}
    ]
    vocab_df = pd.DataFrame(default_words)
    vocab_df.to_csv(CSV_PATH, index=False)
if "current_word" not in st.session_state:
    st.session_state.current_word = None

if "current_meaning" not in st.session_state:
    st.session_state.current_meaning = None

if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
def word_card(word):
    st.markdown(
        f"""
        <div style="
            background-color:#f0f7ff;
            padding:20px;
            border-radius:15px;
            border: 2px solid #4CAF50;
            text-align:center;
            font-size:24px;
            margin-top:20px;
        ">
        <b>단어: {word}</b>
        </div>
        """,
        unsafe_allow_html=True
    )
if st.button("🎯 단어 뽑기", use_container_width=True):
    selected = vocab_df.sample(1).iloc[0]
    st.session_state.current_word = selected["word"]
    st.session_state.current_meaning = selected["meaning"]
    st.session_state.user_answer = ""
if st.session_state.current_word:
    word_card(st.session_state.current_word)

    user_input = st.text_input(
        "뜻을 입력하세요",
        value=st.session_state.user_answer,
        key="answer_input"
    )

    if st.button("✔ 정답 확인", use_container_width=True):
        st.session_state.user_answer = user_input
        correct = st.session_state.current_meaning.lower().strip()
        answer = user_input.lower().strip()

        if answer == correct:
            st.success("🎉 정답입니다! 잘했어요!")
        else:
            st.error(f"❌ 오답! 정답은: **{st.session_state.current_meaning}**")
with st.expander("📖 저장된 단어 보기"):
    st.dataframe(vocab_df)
st.subheader("➕ 단어 추가")

new_word = st.text_input("새 영어 단어")
new_meaning = st.text_input("뜻")

if st.button("💾 저장하기"):
    if new_word.strip() == "" or new_meaning.strip() == "":
        st.warning("⚠ 단어와 뜻을 모두 입력하세요.")
    else:
        new_row = pd.DataFrame([{"word": new_word, "meaning": new_meaning}])
        vocab_df = pd.concat([vocab_df, new_row], ignore_index=True)
        vocab_df.to_csv(CSV_PATH, index=False)
        st.success(f"✔ '{new_word}' 단어가 저장되었습니다!")
streamlit run app.py
python -m streamlit run app.py

