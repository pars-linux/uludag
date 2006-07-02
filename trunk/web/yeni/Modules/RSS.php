<?php

    /* RSS Module For PW */
    /* Gökmen GÖKSEL <gokmen at pardus.org.tr> */

    class RssRead {

    public $RssContent;

        function RssRead($file=""){
            # FIXME incase of File Not Found
            if (!$file) return 0;
            $trans_xml = @fopen($file,"rb");
            $xml_content = stream_get_contents($trans_xml);
            $this->RssContent=simplexml_load_string($xml_content);
        }

        function ShowList($Count,$CharLen){
            if ($this->RssContent) {
                $i=0;
                foreach($this->RssContent->channel->item as $blog) {
                    echo "<li><a href='".$blog->link."'>".substr($blog->title,0,$CharLen)."..</a><br>";
                    if ($i>=$Count) break; else $i++;
                }
            }
        }
    }

?>
