<?php

    // marser

    function coded($string)
    {

        $string = preg_replace("#\[b\](.+?)\[/b\]#is", "<b>\\1</b>", $string);
        $string = preg_replace("#\[i\](.+?)\[/i\]#is", "<i>\\1</i>", $string);
        $string = preg_replace("#\[u\](.+?)\[/u\]#is", "<u>\\1</u>", $string);

        $string = preg_replace("#\[br\]#is", "<br>", $string);


        $string = preg_replace("#\[link\]www\.(.+?)\[/link\]#is", "<a href=\"http://www.\\1\">www.\\1</a>", $string);
        $string = preg_replace("#\[link\](.+?)\[/link\]#is", "<a href=\"\\1\">\\1</a>", $string);
        $string = preg_replace("#\[link=(.+?)\](.+?)\[/link\]#is", "<a href=\"\\1\">\\2</a>", $string);

        $string = preg_replace("#\[img\](.+?)\[/img\]#is", "<img src=\"\\1\" alt=\"[image]\" style=\"margin: 5px 0px 5px 0px\" />", $string);
        $string = preg_replace("#\[img-l\](.+?)\[/img\]#is", "<img src=\"\\1\" alt=\"[image]\" style=\"float: left; margin: 0px 5px 5px 0px\" />", $string);
        $string = preg_replace("#\[img-r\](.+?)\[/img\]#is", "<img src=\"\\1\" alt=\"[image]\" style=\"float: right; margin: 0px 0px 5px 5px\" />", $string);

        return $string;
    }

    echo coded($_POST["text"]);

?>