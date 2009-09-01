CREATE INDEX package_index USING BTREE on packages(package);
CREATE INDEX repo_index USING BTREE on packages(repo);
COMMIT;
