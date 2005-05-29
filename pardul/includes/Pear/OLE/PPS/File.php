<?php
/* vim: set expandtab tabstop=4 shiftwidth=4: */
// +----------------------------------------------------------------------+
// | PHP Version 4                                                        |
// +----------------------------------------------------------------------+
// | Copyright (c) 1997-2002 The PHP Group                                |
// +----------------------------------------------------------------------+
// | This source file is subject to version 2.02 of the PHP license,      |
// | that is bundled with this package in the file LICENSE, and is        |
// | available at through the world-wide-web at                           |
// | http://www.php.net/license/2_02.txt.                                 |
// | If you did not receive a copy of the PHP license and are unable to   |
// | obtain it through the world-wide-web, please send a note to          |
// | license@php.net so we can mail you a copy immediately.               |
// +----------------------------------------------------------------------+
// | Author: Xavier Noguer <xnoguer@php.net>                              |
// | Based on OLE::Storage_Lite by Kawai, Takanori                        |
// +----------------------------------------------------------------------+
//
// $Id: File.php,v 1.5 2003/08/21 19:39:55 xnoguer Exp $


require_once ("$KutuphaneDizin/Pear/OLE/PPS.php");

/**
* Class for creating File PPS's for OLE containers
*
* @author   Xavier Noguer <xnoguer@php.net>
* @category Structures
* @package  OLE
*/
class OLE_PPS_File extends OLE_PPS
{
    /**
    * The constructor
    *
    * @access public
    * @param string $name The name of the file (in Unicode)
    * @see OLE::Asc2Ucs()
    */
    function OLE_PPS_File($name)
    {
        $this->OLE_PPS(
            null, 
            $name,
            OLE_PPS_TYPE_FILE,
            null,
            null,
            null,
            null,
            null,
            '',
            array());
    }

    /**
    * Initialization method. Has to be called right after OLE_PPS_File().
    *
    * @access public
    * @return mixed true on success. PEAR_Error on failure
    */
    function init()
    {
        $this->_tmp_filename = tempnam("", "OLE_PPS_File");
        $fh = @fopen($this->_tmp_filename, "w+b");
        if ($fh == false) {
            $this->raiseError("Can't create temporary file");
        }
        $this->_PPS_FILE = $fh;
        if ($this->_PPS_FILE) {
            fseek($this->_PPS_FILE, 0);
        }
    }
    
    /**
    * Append data to PPS
    *
    * @access public
    * @param string $data The data to append
    */
    function append($data)
    {
        if ($this->_PPS_FILE) {
            fwrite($this->_PPS_FILE, $data);
        }
        else {
            $this->_data .= $data;
        }
    }
}
?>
