
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀な内科医です。  
入力される文章は医者が患者を診察しているときの会話です。  
この内容をカルテ用に出力してください。  

1.会話の内容を注意深く読み、医療用語に関する誤字や脱字を修正してください。  
2.会話の内容を「患者の訴え」と「医者の考え・話」に分け、患者の訴えは"S)"の下に、医者の考え・話は"A/P"の下に、それぞれ箇条書きで整理してください。  
3.各項目は点（・）で始め、項目の最後には句読点（。）をつけてください。  最後は改行してください。
4.読みやすい話し言葉を保ちながら箇条書きにしてください。  
5.修正前の会話は不要です。結果だけを出力してください。  
  
出力の文章は  

S)  
・  
・  
   
A/P  
・  
・    
  
となります。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
