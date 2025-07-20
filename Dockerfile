FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y nginx gettext-base && rm -rf /var/lib/apt/lists/*

# Copy app
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Log to stdout
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Expose common ports
EXPOSE 8501 10000 80

# Final entrypoint
CMD sh -c "\
    python create_db.py && \
    python run_app.py & \
    echo 'Render PORT is: $PORT' && \
    envsubst '\$PORT' < /nginx.template.conf > /etc/nginx/nginx.conf && \
    nginx -g 'daemon off;'"
