import streamlit as st
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# =========================
# Supabase 接続
# =========================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("📝 Todo リスト（Supabase版）")

# =========================
# タスク追加
# =========================
with st.form("add_task", clear_on_submit=True):
    task = st.text_input("タスク名")
    due_date = st.date_input("締切日", value=date.today())
    priority = st.selectbox("優先度", ["高", "中", "低"])
    submitted = st.form_submit_button("追加")

    if submitted:
        if task.strip() == "":
            st.warning("タスク名を入力してください")
        else:
            supabase.table("todos").insert({
                "task": task,
                "is_done": False,
                "priority": priority,
                "due_date": due_date.isoformat()
            }).execute()
            st.success("タスクを追加しました")
            st.rerun()

st.divider()

# =========================
# 表示切り替え
# =========================
status = st.radio(
    "表示状態",
    ["未完了", "完了済み", "すべて"],
    horizontal=True
)

query = supabase.table("todos").select("*").order("due_date")

if status == "未完了":
    query = query.eq("is_done", False)
elif status == "完了済み":
    query = query.eq("is_done", True)

todos = query.execute().data

# =========================
# Todo 一覧
# =========================
st.subheader("📋 Todo一覧")

if not todos:
    st.info("表示するタスクがありません")
else:
    for todo in todos:
        checked = st.checkbox(
            f"【{todo['priority']}】{todo['task']}（締切: {todo['due_date']}）",
            value=todo["is_done"],
            key=todo["id"]
        )

        if checked != todo["is_done"]:
            supabase.table("todos") \
                .update({"is_done": checked}) \
                .eq("id", todo["id"]) \
                .execute()
            st.rerun()

st.divider()

# =========================
# 📊 完了率グラフ
# =========================
st.subheader("📊 タスク完了率")

all_tasks = supabase.table("todos").select("*").execute().data
df = pd.DataFrame(all_tasks)

if df.empty:
    st.info("まだデータがありません")
else:
    done = df["is_done"].sum()
    not_done = len(df) - done

    fig, ax = plt.subplots()
    ax.pie(
        [done, not_done],
        labels=["完了", "未完了"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")

    st.pyplot(fig)
