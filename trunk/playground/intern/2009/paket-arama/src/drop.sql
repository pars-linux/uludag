DROP TABLE IF EXISTS `packages`;
CREATE TABLE `packages` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `repo` varchar(30) NOT NULL,
    `package` varchar(60) NOT NULL,
    `path` varchar(200) NOT NULL
);
COMMIT;
