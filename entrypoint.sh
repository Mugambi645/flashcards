#!/bin/bash
# entrypoint.sh

set -e

# Run migrations using uv
echo "Running migrations..."
uv run python manage.py migrate --noinput

# Create superuser if needed (optional)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | uv run python manage.py shell 2>/dev/null || true

echo "Starting server..."

# Execute the command
exec "$@"