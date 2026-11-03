import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Social Media Engagement Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Social Media Engagement Analysis")
st.write(
    "Analyze social media performance across Instagram and YouTube."
)

# Load dataset
st.sidebar.header("Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("social_media_engagement_final.csv")
        st.sidebar.success("Default dataset loaded.")
    except FileNotFoundError:
        st.warning("Please upload a CSV dataset to begin.")
        st.stop()

# Clean column names
df.columns = df.columns.str.strip().str.lower()

required_columns = [
    "platform", "content_type", "likes",
    "comments", "shares", "reach", "views"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# Convert numerical columns
numeric_columns = [
    "likes", "comments", "shares", "reach", "views"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Sidebar filters
st.sidebar.header("Filters")

platforms = st.sidebar.multiselect(
    "Select Platform",
    options=sorted(df["platform"].dropna().unique()),
    default=sorted(df["platform"].dropna().unique())
)

content_types = st.sidebar.multiselect(
    "Select Content Type",
    options=sorted(df["content_type"].dropna().unique()),
    default=sorted(df["content_type"].dropna().unique())
)

filtered_df = df[
    df["platform"].isin(platforms) &
    df["content_type"].isin(content_types)
]

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# Dashboard metrics
st.subheader("📌 Engagement Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Posts", len(filtered_df))
col2.metric("Total Likes", f"{filtered_df['likes'].sum():,}")
col3.metric("Total Comments", f"{filtered_df['comments'].sum():,}")
col4.metric("Total Shares", f"{filtered_df['shares'].sum():,}")

col5, col6 = st.columns(2)

col5.metric("Total Reach", f"{filtered_df['reach'].sum():,}")
col6.metric("Total Views", f"{filtered_df['views'].sum():,}")

st.divider()

# Platform analysis
st.subheader("📱 Platform Comparison")

platform_data = filtered_df.groupby("platform")[
    ["likes", "comments", "shares"]
].mean()

st.bar_chart(platform_data)

# Content type analysis
st.subheader("🎬 Content Type Performance")

content_data = filtered_df.groupby("content_type")[
    ["likes", "comments", "shares"]
].mean()

st.bar_chart(content_data)

# Engagement rate
if "engagement_rate_percent" in filtered_df.columns:
    st.subheader("📈 Engagement Rate Analysis")

    filtered_df["engagement_rate_percent"] = pd.to_numeric(
        filtered_df["engagement_rate_percent"],
        errors="coerce"
    )

    rate_data = filtered_df.groupby("platform")[
        "engagement_rate_percent"
    ].mean()

    st.bar_chart(rate_data)

# Visualization
st.subheader("❤️ Likes Distribution")

fig, ax = plt.subplots(figsize=(9, 4))
sns.histplot(filtered_df["likes"], bins=15, kde=True, ax=ax)
ax.set_xlabel("Likes")
ax.set_ylabel("Number of Posts")
st.pyplot(fig)
plt.close(fig)

# Top performing posts
st.subheader("🏆 Top 10 Posts")

top_posts = filtered_df.sort_values(
    by="likes", ascending=False
).head(10)

display_columns = [
    col for col in [
        "post_id", "platform", "content_type",
        "likes", "comments", "shares", "reach", "views"
    ] if col in top_posts.columns
]

st.dataframe(
    top_posts[display_columns],
    use_container_width=True
)

# Download filtered dataset
st.subheader("⬇️ Download Analysis Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="social_media_analysis.csv",
    mime="text/csv"
)

st.success("Analysis completed successfully!")
