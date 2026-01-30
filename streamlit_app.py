import streamlit as st
from supabase import create_client

# --- Supabase 接続 ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("📝 Todo リスト（Supabase・改良版）")

# =========================
# タスク追加
# =========================
with st.form("add_task", clear_on_submit=True):
    task = st.text_input("新しいタスクを入力")
    submitted = st.form_submit_button("追加")

    if submitted:
        if task.strip() == "":
            st.warning("タスクを入力してください")
        else:
            supabase.table("todos").insert({
                "task": task,
                "is_done": False
            }).execute()
            st.success("タスクを追加しました！")
            st.rerun()

st.divider()

# =========================
# 表示切り替え
# =========================
view = st.radio(
    "表示切り替え",
    ["未完了", "完了済み", "すべて"],
    horizontal=True
)

query = supabase.table("todos").select("*").order("created_at")

if view == "未完了":
    query = query.eq("is_done", False)
elif view == "完了済み":
    query = query.eq("is_done", True)

todos = query.execute().data

# =========================
# 件数表示
# =========================
count = supabase.table("todos") \
    .select("*", count="exact") \
    .eq("is_done", False) \
    .execute().count

st.caption(f"🕒 未完了タスク：{count} 件")

# =========================
# Todo 表示
# =========================
if not todos:
    st.info("該当するタスクはありません 🎉")
else:
    for todo in todos:
        checked = st.checkbox(
            todo["task"],
            value=todo["is_done"],
            key=todo["id"]
        )

        # 状態が変わったら更新
        if checked != todo["is_done"]:
            supabase.table("todos") \
                .update({"is_done": checked}) \
                .eq("id", todo["id"]) \
                .execute()
            st.rerun()

