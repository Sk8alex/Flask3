PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('0ddc960cfaf1');
CREATE TABLE authors (
	id INTEGER NOT NULL, 
	name VARCHAR(32) NOT NULL, surname VARCHAR(32), 
	PRIMARY KEY (id)
);
INSERT INTO authors VALUES(1,'Shashka1 123MArtynov',NULL);
INSERT INTO authors VALUES(2,'Shashkera1 343',NULL);
INSERT INTO authors VALUES(3,'Shashkera1 123MArtynov',NULL);
INSERT INTO authors VALUES(4,'5Mark Twen',NULL);
CREATE TABLE quotes (
	id INTEGER NOT NULL, 
	author_id INTEGER NOT NULL, 
	text VARCHAR(255) NOT NULL, rating INTEGER DEFAULT '1' NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES authors (id)
);
INSERT INTO quotes VALUES(6,2,'cvvdvewfefef',1);
INSERT INTO quotes VALUES(7,2,'cvvd4546vewfefef',1);
INSERT INTO quotes VALUES(8,2,'cvvd4546vewfefef',1);
CREATE UNIQUE INDEX ix_authors_name ON authors (name);
COMMIT;
