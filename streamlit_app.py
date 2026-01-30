import streamlit as st
from supabase import create_client

# secrets から取得
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("Todo App（最小構成）")

# 追加
task = st.text_input("タスク名")
if st.button("追加"):
    supabase.table("todos").insert({
        "task": task
    }).execute()
    st.success("追加しました")

# 取得
res = supabase.table("todos").select("*").execute()

for todo in res.data:
    st.write(todo["task"], "✅" if todo["is_done"] else "")
