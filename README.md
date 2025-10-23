# CORD-19 Data Explorer 🦠

🚀 **Live Demo**: [https://covid-19-analysis-aeql88fgdehfnzkijiyebz.streamlit.app/](https://covid-19-analysis-aeql88fgdehfnzkijiyebz.streamlit.app/)

An interactive Streamlit application for exploring COVID-19 research papers from the CORD-19 dataset.

## 📋 Overview

This project provides an interactive web application to analyze and visualize COVID-19 research publications. The app allows users to explore trends, journal distributions, publication patterns, and perform text analysis on research paper titles and abstracts.

## 🚀 Features

### Interactive Visualizations
- **Time Trends**: Publication trends over years and months
- **Journal Analysis**: Top journals and their publication patterns
- **Word Analysis**: Word clouds and frequency analysis of paper titles
- **Source Distribution**: Breakdown of papers by data source
- **Abstract Analysis**: Word count distributions and patterns

### Interactive Controls
- **Year Range Slider**: Filter papers by publication year
- **Journal Filter**: Select specific journals to analyze
- **Source Filter**: Filter by data sources
- **Dynamic Metrics**: Real-time statistics based on filters

### Data Exploration
- **Sample Data Viewer**: Browse filtered dataset with customizable columns
- **Download Functionality**: Export filtered data as CSV
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd covid-19-explorer
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure data file is present**
   - Place `new_data.csv` in the project root directory
   - This file should contain the processed CORD-19 dataset

## 🏃‍♂️ Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 Data Requirements

The application expects a CSV file named `new_data.csv` with the following columns:
- `title`: Paper titles
- `journal`: Journal names
- `publish_time`: Publication timestamps
- `publish_year`: Publication year (extracted from publish_time)
- `abstract`: Paper abstracts
- `abs_word_count`: Word count in abstracts
- `source_x`: Data source information

## 🎯 Usage Guide

### Navigation
The app is organized into five main tabs:

1. **📊 Overview**: Dataset statistics and source distribution
2. **📈 Time Trends**: Publication patterns over time
3. **📰 Journals**: Journal analysis and rankings
4. **☁️ Word Analysis**: Text analysis and word clouds
5. **📋 Data Sample**: Browse and download data samples

### Filtering Data
Use the sidebar controls to filter the dataset:
- **Year Range**: Adjust the slider to focus on specific time periods
- **Journal Selection**: Choose specific journals from the top 20 most active
- **Source Filter**: Select data sources to include in analysis

### Interpreting Visualizations
- **Line Charts**: Show trends over time
- **Bar Charts**: Display rankings and distributions
- **Pie Charts**: Show proportional breakdowns
- **Word Clouds**: Highlight frequently used terms
- **Histograms**: Show data distributions

## 📈 Key Insights from Analysis

### Publication Trends
- COVID-19 research showed significant growth during pandemic years
- Peak publication periods correlate with major pandemic waves
- Research output varies significantly across different journals

### Journal Analysis
- Certain journals became primary outlets for COVID-19 research
- Publication patterns vary between high-impact and specialized journals
- Cross-disciplinary collaboration increased during the pandemic

### Text Analysis
- Common themes in titles reflect evolving research priorities
- Abstract lengths vary significantly across different research areas
- Terminology evolution tracks with scientific understanding

## 🔧 Technical Implementation

### Architecture
- **Frontend**: Streamlit for interactive web interface
- **Data Processing**: Pandas for data manipulation
- **Visualizations**: Plotly for interactive charts, Matplotlib for static plots
- **Text Analysis**: WordCloud for text visualization
- **Styling**: Custom CSS for enhanced UI/UX

### Performance Optimizations
- **Data Caching**: `@st.cache_data` decorator for efficient data loading
- **Lazy Loading**: Visualizations generated on-demand
- **Memory Management**: Efficient data filtering and processing

### Code Structure
```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── new_data.csv       # Processed dataset
├── README.md          # Project documentation
└── .venv/             # Virtual environment (optional)
```

## 🚧 Challenges and Learning

### Technical Challenges
1. **Large Dataset Handling**: Implemented caching and efficient filtering to handle large CSV files
2. **Interactive Performance**: Optimized visualization rendering for smooth user experience
3. **Data Quality**: Handled missing values and inconsistent data formats
4. **Cross-platform Compatibility**: Ensured app works across different operating systems

### Solutions Implemented
- **Caching Strategy**: Used Streamlit's caching to prevent repeated data loading
- **Progressive Loading**: Implemented tabs to load visualizations on-demand
- **Error Handling**: Added graceful error handling for missing data files
- **Responsive Design**: Created layouts that work on different screen sizes

### Key Learnings
1. **Data Preprocessing**: Importance of clean, well-structured data for effective visualization
2. **User Experience**: Balance between feature richness and simplicity
3. **Performance**: Caching and optimization strategies for data-heavy applications
4. **Visualization Design**: Choosing appropriate chart types for different data patterns

## 🔮 Future Enhancements

### Planned Features
- **Advanced Filtering**: Author-based filtering and collaboration networks
- **Machine Learning**: Topic modeling and research trend prediction
- **Export Options**: PDF reports and presentation-ready visualizations
- **Real-time Data**: Integration with live research databases

### Technical Improvements
- **Database Integration**: Move from CSV to database for better performance
- **API Development**: REST API for programmatic access
- **Testing Suite**: Comprehensive unit and integration tests
- **Deployment**: Cloud deployment with CI/CD pipeline

## 📚 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **matplotlib**: Static plotting library
- **seaborn**: Statistical data visualization
- **plotly**: Interactive plotting library
- **numpy**: Numerical computing
- **wordcloud**: Word cloud generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CORD-19 Dataset**: Allen Institute for AI and collaborators
- **Streamlit Community**: For excellent documentation and examples
- **Open Source Libraries**: All the amazing libraries that made this project possible

---

**Note**: This application is for educational and research purposes. The insights generated should be interpreted in the context of the dataset's limitations and scope.