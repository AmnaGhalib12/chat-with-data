Project Description

Chat With Your Data is an AI-powered desktop application that enables users to analyze datasets using natural language queries instead of writing code or complex spreadsheet formulas. The application allows users to upload CSV or Excel files, automatically cleans and preprocesses the data, and provides instant insights through a conversational interface. By combining intelligent query understanding, smart column detection, data analysis, and visualization capabilities, the system acts as a personal AI data analyst that makes data exploration accessible to both technical and non-technical users.

Algorithm Information

1. Data Loading:
User uploads a CSV (.csv) or Excel (.xlsx) file.
The dataset is loaded into memory using Pandas.
2. Data Preprocessing:
The system automatically cleans the dataset by:
Removing duplicate records:
Filling missing numerical values using the median.
Filling missing categorical values using the mode.
Preparing the dataset for accurate analysis.
3. Natural Language Processing:
User enters a question in plain English.
The system processes the query using text parsing and regular expressions (Regex).
The query intent is identified (e.g., sum, average, maximum, minimum, count, trend).
4. Smart Column Detection:
Keywords are extracted from the query.
Synonym mapping is applied (e.g., sales → revenue, quantity → qty).
Fuzzy matching (Difflib) is used to find the most relevant dataset column even when exact column names are not provided.
5. Data Analysis Engine:
Based on the detected intent, the system performs the appropriate operation:
Sum → Total value calculation.
Average → Mean calculation.
Maximum → Highest value extraction.
Minimum → Lowest value extraction.
Count → Number of records.
Trend Analysis → Time-based pattern analysis.
6. Visualization Generation:
For trend-related queries, the system generates line charts using Matplotlib.
Graphs are automatically saved and displayed to help users understand data patterns visually.
7. Result Generation:
The computed result or visualization is presented to the user through an interactive chat interface.
Users can continue asking questions until they choose to exit the application.
