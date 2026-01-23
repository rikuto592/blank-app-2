import streamlit as st
from supabase import create_client

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("📝 Todo リスト（Supabase版）")

# --- タスク追加 ---
task = st.text_input("新しいタスクを入力")

if st.button("追加"):
    if task:
        supabase.table("todos").insert({
            "task": task,
            "is_done": False
        }).execute()
        st.success("タスクを追加しました！")
        st.rerun()

st.divider()

# --- 未完了タスク取得 ---
response = (
    supabase
    .table("todos")
    .select("*")
    .eq("is_done", False)   # ← 未完了のみ
    .order("created_at")
    .execute()
)

todos = response.data

st.subheader("📋 Todo一覧（チェックで完了）")

if not todos:
    st.info("未完了のタスクはありません 🎉")
else:
    for todo in todos:
        checked = st.checkbox(
            todo["task"],
            key=todo["id"]
        )

        if checked:
            # 完了したら削除
            supabase.table("todos") \
                .delete() \
                .eq("id", todo["id"]) \
                .execute()
            st.rerun()

