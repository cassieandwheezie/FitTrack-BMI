# FitTrack BMI

An interactive BMI tracking application built with Python and Streamlit, featuring PostgreSQL storage, interactive visualizations, BMI history and downloadable PDF reports.

## Features

- BMI calculation with multiple height and weight units
- BMI category classification
- Interactive Plotly BMI gauge
- PostgreSQL storage for BMI records
- Searchable BMI history
- PDF health report generation
- General diet, fitness, and hydration information
- Input validation and duplicate-submission handling

## Technology Stack

- Python
- Streamlit
- PostgreSQL
- psycopg2
- Plotly
- ReportLab

## Local Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies using `pip install -r requirements.txt`.
4. Configure PostgreSQL credentials locally using `database.ini`.
5. Create the database and initialize the `bmi_records` table.
6. Run the application using `streamlit run calculator.py`.

Never commit database credentials or private health information.

## Limitations

BMI is a general screening measure and does not directly measure body fat or provide a complete assessment of health. Hydration estimates and lifestyle suggestions are general information, not personalized medical advice.

## Author

Manmeet Kaur

## Disclaimer

FitTrack BMI is an educational project. It does not provide a medical diagnosis or replace professional healthcare advice.