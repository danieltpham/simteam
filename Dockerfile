# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install NGINX, envsubst, and Python build tools
RUN apt-get update && \
    apt-get install -y nginx gettext-base && \
    rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Logging to Docker stdout/stderr
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Copy template-based NGINX config
COPY /nginx.conf /nginx.conf

# Expose default ports for local testing
EXPOSE 80 10000 8501

# Start app: run Python services in background, then render + launch nginx
CMD sh -c "\
    python create_db.py && \
    python run_app.py & \
    echo 'Binding to PORT=${PORT}' && \
    envsubst '\$PORT' < /nginx.conf > /nginx.conf && \
    nginx -g 'daemon off;'"