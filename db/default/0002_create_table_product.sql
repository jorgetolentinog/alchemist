-- +migrate up
CREATE TABLE [product] (
    id          INT PRIMARY KEY IDENTITY,
    name        VARCHAR(256)
)

-- +migrate down
DROP TABLE [product]
