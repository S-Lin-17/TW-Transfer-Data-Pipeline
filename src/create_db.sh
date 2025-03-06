#!/bin/bash

source secrets.sh

# Use the variables
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_USER: $DB_USER"
echo "DB_PASSWORD: $DB_PASSWORD"
echo "DB_NAME: $DB_NAME"

# Check if the database already exists, else create it
if psql -h $DB_HOST -p $DB_PORT -U postgres -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Database '$DB_NAME' already exists."
else
    echo "Creating database '$DB_NAME'..."
    createdb -h $DB_HOST -p $DB_PORT -U postgres $DB_NAME
    if [ $? -eq 0 ]; then
        echo "Database '$DB_NAME' created successfully."
    else
        echo "Failed to create database '$DB_NAME'."
        exit 1
    fi
fi

# Check if the user already exists, else create it
if psql -h $DB_HOST -p $DB_PORT -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    echo "User '$DB_USER' already exists."
else
    echo "Creating user '$DB_USER'..."
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    if [ $? -eq 0 ]; then
        echo "User '$DB_USER' created successfully."
    else
        echo "Failed to create user '$DB_USER'."
        exit 1
    fi
fi

# Grant privileges to user on the db
echo "Granting privileges to user '$DB_USER' on database '$DB_NAME'..."
psql -h $DB_HOST -p $DB_PORT -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
if [ $? -eq 0 ]; then
    echo "Privileges granted successfully."
else
    echo "Failed to grant privileges."
    exit 1
fi

echo "Database setup completed successfully."