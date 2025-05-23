import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io      #Redirect output from df.info() into a string so you can display it in the Streamlit UI

st.title("CSV Data Explorer")


uploaded_file = st.file_uploader("Upload a CSV file", type="csv")     # Upload CSV file

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🧾 Preview of Your Data")
    st.dataframe(df.head())

    st.subheader("🔍 Choose an Analysis")    # Analysis selection
    analysis = st.selectbox(
        "Select the type of analysis you want to perform:",
        [
            "Show Data Info",
            "Show Descriptive Statistics",
            "Show Null Value Count",
            "Correlation Heatmap",
            "Pairplot",
            "Histogram",
            "Boxplot",
            "Custom Query",
        ]
    )

    if analysis == "Show Data Info":
        buffer = io.StringIO()         #capture that output into a string
        df.info(buf=buffer)
        st.text(buffer.getvalue())    #reads the text

    elif analysis == "Show Descriptive Statistics":
        st.write(df.describe())

    elif analysis == "Show Null Value Count":
        st.write(df.isnull().sum())

    elif analysis == "Correlation Heatmap":
        st.subheader("📈 Correlation Heatmap")
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")  #annotate each square with the actual numeric #cmap(sets the color palette)
        st.pyplot(plt.gcf())  #Get Current Figure
        plt.clf()

    elif analysis == "Pairplot":
        st.subheader("🔗 Pairplot")
        numeric_df = df.select_dtypes(include=np.number)
        if numeric_df.shape[1] > 1:
            fig = sns.pairplot(numeric_df)
            st.pyplot(fig)
            plt.clf()
        else:
            st.warning("You need at least two numeric columns to generate a pairplot.")

    elif analysis == "Histogram":
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Select a column to plot a histogram", numeric_cols)
            plt.figure()
            sns.histplot(df[col].dropna(), kde=True)
            st.pyplot(plt.gcf())
            plt.clf()
        else:
            st.warning("No numeric columns found for histogram.")

    elif analysis == "Boxplot":
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Select a column to plot a boxplot", numeric_cols)
            plt.figure()
            sns.boxplot(x=df[col].dropna())
            st.pyplot(plt.gcf())
            plt.clf()
        else:
            st.warning("No numeric columns found for boxplot.")

    elif analysis == "Custom Query":
        st.subheader("🧠 Run a Custom Query")
        query = st.text_input("Enter your query (e.g., `Salary > 70000 and Age < 40`):")
        if query:
            try:
                result = df.query(query)
                st.write(result)
            except Exception as e:
                st.error(f"Query Error: {e}")
else:
    st.info(" Upload a CSV file to get started.")
