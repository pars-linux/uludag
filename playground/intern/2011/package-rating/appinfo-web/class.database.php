<?php

/**
 * Appinfo MySQL database class
 *
 * @author Onur Güzel <guzelmu@itu.edu.tr>
 * @copyright Copyright (C) 2011, TUBITAK/BILGEM
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License
 * @package appinfo
 */
class Database {
    private $db_host = 'localhost';
    private $db_user = 'guzelmu_appinfo';
    private $db_pass = 'appinfo';
    private $db_base = 'guzelmu_appinfo';

    private $dbh = null;

    private $username = null;
    private $key = null;

    /**
     * Connects to database
     *
     * @param array $db_info
     */
    public function __construct($db_info = null) {
        // Database config can be overwritten on construction.
        if (!is_null($db_info) && is_array($db_info)) {
            foreach ($db_info as $k => $v) {
                if (inarray($k, array('db_host', 'db_user', 'db_pass', 'db_base'))) {
                    $this->$k = $v;
                }
            }
        }
        try {
            $this->dbh = new PDO(sprintf('mysql:host=%s;dbname=%s', $this->db_host, $this->db_base), $this->db_user, $this->db_pass);
        } catch(PDOException $e) {
            echo $e->getMessage();
        }
    }

    /**
     * Closes database connection
     */
    public function __destruct() {
        $this->dbh = null;
    }

    /**
     * Checks login info over OpenDesktop.org Public API
     *
     * @param string $username
     * @param string $password
     *
     * @return string|false key hash on success, false on failure
     */
    public function checkLogin($username, $password) {
        require_once('class.opendesktop.php');
        $od = new OpenDesktop();
        $check = $od->PersonCheck($username, $password)->statuscode;
        switch ($check) {
            /*
             * OpenDesktop.org Status codes:
             * 100: Valid login
             * 101: Required fields cannot be blank
             * 102: Invalid login
             */
            case 100:
                $this->username = $username;
                if ($this->userExists()) {
                    if ($this->getKey() !== $this->createKey($password)) {
                        $this->processKey($password, 'update');
                    }
                } else {
                    $this->processKey($password);
                }
                $this->key = $this->getKey();
                return $this->key;
                break;
            case 102:
                return false;
                break;
            default:
                return false;
                break;
        }
    }

    /**
     * Creates a hash string using username and password
     *
     * @access private
     *
     * @param string $password
     *
     * @return string key hash
     */
    private function createKey($password) {
        return sha1(sprintf('^%s:%s$', $this->username, $password));
    }

    /**
     * Retrieves info from database
     *
     * @access private
     *
     * @return string|false requested column data on success, false on failure
     */
    private function getInfo($column, $key, $by = 'username') {
        if (in_array($by, array('id', 'username', 'key'))) {
            $r = $this->dbh->query(sprintf("SELECT `%s` FROM `users` WHERE `%s` = %s;", $column, $by, $this->dbh->quote($key)))->fetch(PDO::FETCH_ASSOC);
            return $r[$column];
        } else {
            return false;
        }
    }

    /**
     * Gets unique user key from DB
     *
     * @return string key hash
     */
    public function getKey() {
        return $this->getInfo('key', $this->username);
    }

    /**
     * Inserts or updates user information
     *
     * @access private
     *
     * @param string $password
     * @param string $action
     *
     * @return string|false key hash on success, false on failure
     */
    private function processKey($password, $action = 'insert') {
        $key = $this->createKey($password);
        switch ($action) {
            case 'insert':
                $sql = sprintf("INSERT INTO `users` (`username`, `key`) VALUES (%s, %s);", $this->dbh->quote($this->username), $this->dbh->quote($key));
                break;
            case 'update':
                $sql = sprintf("UPDATE `users` SET `key` = %2$s WHERE `username` = %1$s;", $this->dbh->quote($this->username), $this->dbh->quote($key));
                break;
            default:
                return false;
        }
        return ($this->dbh->exec($sql)) ? $key : false;
    }

    /**
     * Searchs the DB for given username
     *
     * @return bool
     */
    public function userExists() {
        return ($this->getInfo('id', $this->username)) ? true : false;
    }
}

?>
