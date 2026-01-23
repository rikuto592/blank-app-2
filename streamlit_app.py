import streamlit as st
from supabase import create_client

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("📝 Todo リスト（Supabase版）")

# ---- Todo追加 ----
task = st.text_input("新しいタスクを入力")

if st.button("追加"):
    if task:
        supabase.table("todos").insert({"task": task}).execute()
        st.success("追加しました")
        st.rerun()

# ---- Todo取得 ----
response = supabase.table("todos").select("*").order("created_at").execute()
todos = response.data

st.subheader("Todo一覧")

for todo in todos:
    col1, col2 = st.columns([3, 1])

    with col1:
        if todo["is_done"]:
            st.markdown(f"~~{todo['task']}~~")
        else:
            st.write(todo["task"])

    with col2:
        if not todo["is_done"]:
            if st.button("完了", key=todo["id"]):
                supabase.table("todos") \
                    .update({"is_done": True}) \
                    .eq("id", todo["id"]) \
                    .execute()
                st.rerun()
