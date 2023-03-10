CREATE TABLE IF NOT EXISTS dates (
    id SERIAL PRIMARY KEY,
    date VARCHAR(250) NOT NULL,
    comment VARCHAR(500),
    exercise_id integer NOT NULL REFERENCES exercises(id) ON DELETE CASCADE REFERENCES exercises(id) DEFERRABLE INITIALLY DEFERRED,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED
);

