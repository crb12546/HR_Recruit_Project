#!/bin/bash

# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run database migrations
cd backend
alembic upgrade head

# Run initial tests
pytest -v

# Start frontend tests
cd ../frontend
npm run test

echo "Test environment setup complete!"
