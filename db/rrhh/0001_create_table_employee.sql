-- +migrate up
CREATE TABLE [employee] (
    id          INT PRIMARY KEY IDENTITY,
    name        VARCHAR(256),
    last_name   VARCHAR(256)
)

INSERT INTO [employee] (name, last_name) VALUES ('Carlos', 'Chilet')
INSERT INTO [employee] (name, last_name) VALUES ('Victor', 'Mora')

-- +migrate down
DROP TABLE [employee]
