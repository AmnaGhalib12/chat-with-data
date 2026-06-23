import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import difflib
import re

# -----------------------------
# 1. LOAD DATA
# -----------------------------
def load_data(file_path):
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Only CSV or Excel supported")
    except Exception as e:
        return f"❌ Error loading file: {str(e)}"


# -----------------------------
# 2. CLEAN DATA
# -----------------------------
def clean_data(df):
    try:
        df = df.drop_duplicates()

        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].median())

        for col in df.select_dtypes(include="object").columns:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])

        return df
    except Exception as e:
        print(f"⚠️ Cleaning error: {str(e)}")
        return df


# -----------------------------
# 3. SMART QUERY UNDERSTANDING
# -----------------------------
def analyze_query(query):
    query = query.lower()

    keywords = {
        "sum": ["sum", "total", "overall"],
        "mean": ["average", "mean"],
        "max": ["max", "highest", "top", "most"],
        "min": ["min", "lowest", "least"],
        "count": ["count", "rows", "entries", "how many"],
        "trend": ["trend", "over time", "progress"]
    }

    for action, words in keywords.items():
        if any(word in query for word in words):
            return action

    return "unknown"


# -----------------------------
# 4. COLUMN MATCHING (SMART)
# -----------------------------
def find_column(query, columns):
    query = query.lower()

    # synonym dictionary
    synonyms = {
        "sales": ["revenue", "income"],
        "quantity": ["qty", "units"],
        "price": ["cost", "amount"]
    }

    # direct match
    for col in columns:
        if col.lower() in query:
            return col

    # synonym match
    for col in columns:
        for key, vals in synonyms.items():
            if key in col.lower():
                if any(word in query for word in vals + [key]):
                    return col

    # fuzzy match (word-by-word)
    words = re.findall(r'\w+', query)
    for word in words:
        match = difflib.get_close_matches(word, columns, n=1, cutoff=0.6)
        if match:
            return match[0]

    return None


# -----------------------------
# 5. CORE ENGINE
# -----------------------------
def process_query(df, query):
    try:
        action = analyze_query(query)

        numeric_cols = list(df.select_dtypes(include=np.number).columns)
        text_cols = list(df.select_dtypes(include="object").columns)

        if df.empty:
            return "❌ Dataset is empty"

        col = find_column(query, numeric_cols)

        # ---------------- SUM ----------------
        if action == "sum":
            if col:
                return f"Total {col}: {df[col].sum()}"
            return f"❌ Column not found. Available: {numeric_cols}"

        # ---------------- MEAN ----------------
        elif action == "mean":
            if col:
                return f"Average {col}: {df[col].mean()}"
            return f"❌ Column not found. Available: {numeric_cols}"

        # ---------------- MAX ----------------
        elif action == "max":
            if col:
                return f"Max {col}:\n{df.loc[df[col].idxmax()]}"
            return f"❌ Column not found. Available: {numeric_cols}"

        # ---------------- MIN ----------------
        elif action == "min":
            if col:
                return f"Min {col}:\n{df.loc[df[col].idxmin()]}"
            return f"❌ Column not found. Available: {numeric_cols}"

        # ---------------- COUNT ----------------
        elif action == "count":
            return f"Total rows: {len(df)}"

        # ---------------- TREND ----------------
        elif action == "trend":
            if not numeric_cols:
                return "❌ No numeric column for trend"

            col = col if col else numeric_cols[0]

            plt.figure()
            plt.plot(df[col])
            plt.title(f"Trend of {col}")
            plt.savefig("trend.png")
            plt.close()

            return f"📈 Trend saved as trend.png (column: {col})"

        return "❌ I couldn't understand. Try: total, average, max, count, trend,highest,lowest"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# -----------------------------
# 6. CHAT LOOP
# -----------------------------
def chat(df):
    if isinstance(df, str):
        print(df)
        return

    print("\n🤖 Smart AI Data Chat Ready!")
    print("Try: 'total sales', 'average revenue', 'how many rows'\n")

    while True:
        query = input("Ask: ")

        if query.lower() == "exit":
            print("👋 Goodbye!")
            break

        answer = process_query(df, query)
        print("\n👉", answer, "\n")


# -----------------------------
# 7. MAIN
# -----------------------------
if __name__ == "__main__":
    file_path = input("Enter file path: ")

    df = load_data(file_path)

    if isinstance(df, str):
        print(df)
    else:
        df = clean_data(df)

        print("\n📊 Data Preview:")
        print(df.head())

        chat(df)