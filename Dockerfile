FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y nginx gettext-base && rm -rf /var/lib/apt/lists/*

# Copy app
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

COPY nginx.template.conf /etc/nginx/nginx.template.conf

# Expose common ports
EXPOSE 8501 10000 80

# Final entrypoint
CMD sh -c "\
  python create_db.py && \
  python run_app.py & \
  echo 'Waiting for Streamlit on 8501...' && \
  while ! nc -z localhost 8501; do sleep 1; done && \
  echo 'Streamlit up!' && \
  envsubst '\$PORT' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf && \
  nginx -g 'daemon off;'"

