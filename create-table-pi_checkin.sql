CREATE TABLE pi_checkin (
    pi TEXT PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    notified BOOLEAN NOT NULL
);