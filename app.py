import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the COVID-19 research data"""
    try:
        data = pd.read_csv('new_data.csv')
        # Convert publish_time to datetime if it's not already
        if 'publish_time' in data.columns:
            data['publish_time'] = pd.to_datetime(data['publish_time'], errors='coerce')
        if 'publish_year' not in data.columns and 'publish_time' in data.columns:
            data['publish_year'] = data['publish_time'].dt.year
        return data
    except FileNotFoundError:
        st.error("Data file 'new_data.csv' not found. Please ensure the file is in the correct directory.")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🦠 CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive exploration of COVID-19 research papers")
    
    # Load data
    data = load_data()
    if data is None:
        st.stop()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controls")
    
    # Year range slider
    if 'publish_year' in data.columns:
        min_year = int(data['publish_year'].min()) if not pd.isna(data['publish_year'].min()) else 2019
        max_year = int(data['publish_year'].max()) if not pd.isna(data['publish_year'].max()) else 2022
        year_range = st.sidebar.slider(
            "Select year range",
            min_year, max_year,
            (min_year, max_year),
            help="Filter papers by publication year"
        )
        filtered_data = data[
            (data['publish_year'] >= year_range[0]) & 
            (data['publish_year'] <= year_range[1])
        ]
    else:
        filtered_data = data
        st.sidebar.warning("Year information not available")
    
    # Journal filter
    if 'journal' in data.columns:
        top_journals = data['journal'].value_counts().head(20).index.tolist()
        selected_journals = st.sidebar.multiselect(
            "Select journals",
            options=top_journals,
            default=top_journals[:5],
            help="Filter by specific journals"
        )
        if selected_journals:
            filtered_data = filtered_data[filtered_data['journal'].isin(selected_journals)]
    
    # Source filter
    if 'source_x' in data.columns:
        sources = data['source_x'].unique()
        selected_sources = st.sidebar.multiselect(
            "Select sources",
            options=sources,
            default=sources,
            help="Filter by data sources"
        )
        if selected_sources:
            filtered_data = filtered_data[filtered_data['source_x'].isin(selected_sources)]
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", f"{len(filtered_data):,}")
    
    with col2:
        if 'journal' in filtered_data.columns:
            unique_journals = filtered_data['journal'].nunique()
            st.metric("Unique Journals", f"{unique_journals:,}")
    
    with col3:
        if 'publish_year' in filtered_data.columns:
            year_span = filtered_data['publish_year'].max() - filtered_data['publish_year'].min()
            st.metric("Year Span", f"{int(year_span)} years" if not pd.isna(year_span) else "N/A")
    
    with col4:
        if 'abs_word_count' in filtered_data.columns:
            avg_words = filtered_data['abs_word_count'].mean()
            st.metric("Avg Abstract Length", f"{int(avg_words)} words" if not pd.isna(avg_words) else "N/A")
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "📈 Time Trends", "📰 Journals", "☁️ Word Analysis", "📋 Data Sample"
    ])
    
    with tab1:
        st.subheader("Dataset Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Publications by source
            if 'source_x' in filtered_data.columns:
                source_counts = filtered_data['source_x'].value_counts()
                fig_source = px.pie(
                    values=source_counts.values,
                    names=source_counts.index,
                    title="Distribution by Source"
                )
                st.plotly_chart(fig_source, use_container_width=True)
        
        with col2:
            # Abstract word count distribution
            if 'abs_word_count' in filtered_data.columns:
                fig_words = px.histogram(
                    filtered_data,
                    x='abs_word_count',
                    title="Abstract Word Count Distribution",
                    nbins=50
                )
                fig_words.update_layout(xaxis_title="Word Count", yaxis_title="Frequency")
                st.plotly_chart(fig_words, use_container_width=True)
    
    with tab2:
        st.subheader("Publication Trends Over Time")
        
        if 'publish_year' in filtered_data.columns:
            # Publications per year
            yearly_counts = filtered_data.groupby('publish_year').size().reset_index(name='count')
            
            fig_timeline = px.line(
                yearly_counts,
                x='publish_year',
                y='count',
                title="Publications Over Time",
                markers=True
            )
            fig_timeline.update_layout(
                xaxis_title="Year",
                yaxis_title="Number of Publications"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Monthly trend (if we have month data)
            if 'publish_time' in filtered_data.columns:
                monthly_data = filtered_data.copy()
                monthly_data['month'] = monthly_data['publish_time'].dt.to_period('M')
                monthly_counts = monthly_data.groupby('month').size().reset_index(name='count')
                monthly_counts['month_str'] = monthly_counts['month'].astype(str)
                
                if len(monthly_counts) > 1:
                    fig_monthly = px.bar(
                        monthly_counts.tail(24),  # Last 24 months
                        x='month_str',
                        y='count',
                        title="Monthly Publication Trend (Last 24 Months)"
                    )
                    fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Publications")
                    st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.warning("Time information not available in the dataset")
    
    with tab3:
        st.subheader("Journal Analysis")
        
        if 'journal' in filtered_data.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Top journals
                top_journals_data = filtered_data['journal'].value_counts().head(15)
                fig_journals = px.bar(
                    x=top_journals_data.values,
                    y=top_journals_data.index,
                    orientation='h',
                    title="Top 15 Journals by Publication Count"
                )
                fig_journals.update_layout(
                    xaxis_title="Number of Publications",
                    yaxis_title="Journal",
                    height=600
                )
                st.plotly_chart(fig_journals, use_container_width=True)
            
            with col2:
                # Journal productivity over time
                if 'publish_year' in filtered_data.columns:
                    journal_year = filtered_data.groupby(['journal', 'publish_year']).size().reset_index(name='count')
                    top_5_journals = filtered_data['journal'].value_counts().head(5).index
                    journal_year_top = journal_year[journal_year['journal'].isin(top_5_journals)]
                    
                    fig_journal_trend = px.line(
                        journal_year_top,
                        x='publish_year',
                        y='count',
                        color='journal',
                        title="Top 5 Journals: Publication Trends"
                    )
                    st.plotly_chart(fig_journal_trend, use_container_width=True)
        else:
            st.warning("Journal information not available in the dataset")
    
    with tab4:
        st.subheader("Word Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Word cloud
            if 'title' in filtered_data.columns:
                st.write("**Word Cloud of Paper Titles**")
                titles_text = ' '.join(filtered_data['title'].dropna().astype(str))
                
                if titles_text.strip():
                    wordcloud = WordCloud(
                        width=400, 
                        height=300, 
                        background_color='white',
                        colormap='viridis'
                    ).generate(titles_text)
                    
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                else:
                    st.warning("No title data available for word cloud")
        
        with col2:
            # Most common words in titles
            if 'title' in filtered_data.columns:
                st.write("**Most Common Words in Titles**")
                all_words = []
                for title in filtered_data['title'].dropna():
                    words = str(title).lower().split()
                    # Filter out common stop words
                    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
                    words = [word for word in words if word not in stop_words and len(word) > 2]
                    all_words.extend(words)
                
                if all_words:
                    word_freq = pd.Series(all_words).value_counts().head(15)
                    fig_words = px.bar(
                        x=word_freq.values,
                        y=word_freq.index,
                        orientation='h',
                        title="Top 15 Words in Titles"
                    )
                    fig_words.update_layout(yaxis_title="Words", xaxis_title="Frequency")
                    st.plotly_chart(fig_words, use_container_width=True)
    
    with tab5:
        st.subheader("Data Sample")
        
        # Display options
        col1, col2 = st.columns(2)
        with col1:
            sample_size = st.selectbox("Sample size", [10, 25, 50, 100], index=1)
        with col2:
            show_columns = st.multiselect(
                "Select columns to display",
                options=filtered_data.columns.tolist(),
                default=['title', 'journal', 'publish_year', 'abstract'][:4] if len(filtered_data.columns) >= 4 else filtered_data.columns.tolist()
            )
        
        if show_columns:
            sample_data = filtered_data[show_columns].head(sample_size)
            st.dataframe(sample_data, use_container_width=True)
            
            # Download button
            csv = sample_data.to_csv(index=False)
            st.download_button(
                label="Download sample as CSV",
                data=csv,
                file_name=f"covid_research_sample_{sample_size}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Please select at least one column to display")
    
    # Footer with insights
    st.markdown("---")
    st.subheader("📋 Key Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("**Dataset Characteristics:**")
        st.write(f"• Total papers analyzed: {len(filtered_data):,}")
        if 'journal' in filtered_data.columns:
            st.write(f"• Unique journals: {filtered_data['journal'].nunique():,}")
        if 'publish_year' in filtered_data.columns:
            year_range_text = f"{int(filtered_data['publish_year'].min())}-{int(filtered_data['publish_year'].max())}"
            st.write(f"• Publication years: {year_range_text}")
    
    with insights_col2:
        st.markdown("**Research Trends:**")
        if 'publish_year' in filtered_data.columns:
            peak_year = filtered_data['publish_year'].mode().iloc[0] if not filtered_data['publish_year'].mode().empty else "N/A"
            st.write(f"• Peak publication year: {int(peak_year) if peak_year != 'N/A' else peak_year}")
        if 'journal' in filtered_data.columns:
            top_journal = filtered_data['journal'].mode().iloc[0] if not filtered_data['journal'].mode().empty else "N/A"
            st.write(f"• Most active journal: {top_journal}")

if __name__ == "__main__":
    main()