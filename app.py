import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

# LLMの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 専門家の種類 ("A" または "B")
    
    Returns:
        str: LLMからの回答
    """
    # 専門家の種類に応じてシステムメッセージを設定
    if expert_type == "A":
        system_content = "あなたは子どもの育て方についての専門家です。子育てに関する質問に対して、経験豊富で親切に回答してください。"
    elif expert_type == "B":
        system_content = "あなたは高齢者の介護についての専門家です。介護に関する質問に対して、経験豊富で親切に回答してください。"
    else:
        system_content = "あなたは役立つアシスタントです。"
    
    # メッセージの作成
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=input_text),
    ]
    
    # LLMからの回答を取得
    result = llm(messages)
    return result.content

# StreamlitアプリケーションのUI
def main():
    st.title("専門家相談アプリ")
    st.write("専門家に質問してみましょう！")
    
    # ラジオボタンで専門家の種類を選択
    expert_type = st.radio(
        "専門家の種類を選択してください:",
        ["A", "B"],
        format_func=lambda x: "子どもの育て方専門家" if x == "A" else "高齢者介護専門家"
    )
    
    # 入力フォーム
    user_input = st.text_area(
        "質問を入力してください:",
        placeholder="専門家に聞きたいことを入力してください...",
        height=100
    )
    
    # 送信ボタン
    if st.button("質問を送信"):
        if user_input.strip():
            with st.spinner("専門家が回答を考えています..."):
                try:
                    # LLM関数を呼び出して回答を取得
                    response = get_llm_response(user_input, expert_type)
                    
                    # 回答を表示
                    st.success("回答:")
                    st.write(response)
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
        else:
            st.warning("質問を入力してください。")

if __name__ == "__main__":
    main()
