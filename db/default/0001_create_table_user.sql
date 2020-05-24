-- +migrate up
CREATE TABLE [user] (
    id          INT PRIMARY KEY IDENTITY,
    name        VARCHAR(256),
    last_name   VARCHAR(256)
)

INSERT INTO [user] (name, last_name) VALUES ('Jorge', 'Tolentino')
INSERT INTO [user] (name, last_name) VALUES ('Diego', 'Conga')

-- +migrate down
DROP TABLE [user]
