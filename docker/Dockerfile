# Use Microsoft's official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install browsers
RUN playwright install chromium firefox webkit

# Copy the rest of the application
COPY . .

# Run tests by default
CMD ["pytest", "--browser", "chromium", "--html=reports/report.html"]
