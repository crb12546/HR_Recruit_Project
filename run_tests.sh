#!/bin/bash

# Set environment variables
export TESTING=True
export MOCK_SERVICES=True

# Build and start the test containers
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up

# Clean up after tests
docker-compose -f docker-compose.test.yml down -v
