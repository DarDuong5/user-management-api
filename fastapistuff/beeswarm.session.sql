show tables;

-- @block
DESCRIBE inventory;

--@block
DESCRIBE users;

--@block
use bss;
alter table inventory
MODIFY COLUMN data JSON NOT NULL DEFAULT (JSON_ARRAY());
