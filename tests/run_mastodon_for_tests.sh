#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/mastodon/"
  exit 1
fi

TOOTCTL_DIR="$1"
SETUP_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Start services
sudo /etc/init.d/redis-server start && sleep 3
sudo /etc/init.d/postgresql start && sleep 3
sudo redis-cli flushall && sleep 3 && \
sudo /etc/init.d/redis-server restart

# Change to tootctl dir
cd "$TOOTCTL_DIR" || { echo "Directory $TOOTCTL_DIR not found"; exit 1; }

# Database setup & accounts
RAILS_ENV=development rails db:drop && \
RAILS_ENV=development rails db:setup && \
RAILS_ENV=development bin/tootctl accounts create admin2 --email zerocool@example.com --confirmed --approve --role Owner && \
RAILS_ENV=development bin/tootctl accounts create mastodonpy_test --email mastodonpy_test@localhost --approve --confirmed && \
RAILS_ENV=development bin/tootctl accounts create mastodonpy_test_2 --email mastodonpy_test_2@localhost --approve --confirmed && \
RAILS_ENV=development bin/tootctl settings registrations open

# Run setup.sql from original dir
psql -d mastodon_development < "$SETUP_DIR/setup.sql" && sleep 4

# Seed annual report so we can test that
RAILS_ENV=development bin/rails runner "$SETUP_DIR/seed_annual_report.rb" || exit 1

# Launch services
RAILS_ENV=development LAUNCHY_DRY_RUN=true DB_PASS="1234" foreman start
