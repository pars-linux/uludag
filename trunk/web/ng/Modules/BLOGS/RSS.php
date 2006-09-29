<?php

    /* RSS Module For PW */
    /* Gökmen GÖKSEL <gokmen at pardus.org.tr> */


    # Module RSS Class

    class RssRead {

    public $RssContent;

        function RssRead($file=""){
            # FIXME incase of File Not Found
            if (!$file) return 0;
            $trans_xml = @fopen($file,"rb");
            $xml_content = stream_get_contents($trans_xml);
            $this->RssContent=simplexml_load_string($xml_content);
        }

        function utf8_substr($str,$from,$len){
        return preg_replace('#^(?:[\x00-\x7F]|[\xC0-\xFF][\x80-\xBF]+){0,'.$from.'}'.
                       '((?:[\x00-\x7F]|[\xC0-\xFF][\x80-\xBF]+){0,'.$len.'}).*#s',
                       '$1',$str);
        }

        function ShowList($Count,$CharLen){
            if ($this->RssContent) {
                $i=0;
                foreach($this->RssContent->channel->item as $blog) {
                    $Return.= "<li><a target='_blank' href='".$blog->link."'>".$this->utf8_substr($blog->title,0,$CharLen)."..</a></li>";
                    if ($i>=$Count) break; else $i++;
                }
            }
            return $Return;
        }
    }

?>
