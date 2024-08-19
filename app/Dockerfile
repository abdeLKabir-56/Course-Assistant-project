FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]