-- +migrate up
CREATE TABLE [profile] (
    id          INT PRIMARY KEY IDENTITY,
    name        VARCHAR(256),
    last_name   VARCHAR(256)
)

-- +migrate down
DROP TABLE [profile]
