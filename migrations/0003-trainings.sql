CREATE TABLE IF NOT EXISTS trainings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED
);