<?php

    // marser


    function coded($string)
    {
        $rules = Array();

        $rules[0]["replace"] = "#\[b\](.+?)\[/b\]#is";
        $rules[0]["to"]      = "<b>\\1</b>";

        $rules[1]["replace"] = "#\[i\](.+?)\[/i\]#is";
        $rules[1]["to"]      = "<i>\\1</i>";

        $rules[2]["replace"] = "#\[u\](.+?)\[/u\]#is";
        $rules[2]["to"]      = "<u>\\1</u>";

        $rules[3]["replace"] = "#\[br\]#is";
        $rules[3]["to"]      = "<br>";

        $rules[4]["replace"] = "#\[link\]www\.(.+?)\[/link\]#is";
        $rules[4]["to"]      = "<a href=\"http://www.\\1\">www.\\1</a>";

        $rules[5]["replace"] = "#\[link\](.+?)\[/link\]#is";
        $rules[5]["to"]      = "<a href=\"\\1\">\\1</a>";

        $rules[6]["replace"] = "#\[link=(.+?)\](.+?)\[/link\]#is";
        $rules[6]["to"]      = "<a href=\"\\1\">\\2</a>";

        $rules[7]["replace"] = "#\[img\](.+?)\[/img\]#is";
        $rules[7]["to"]      = "<img src=\"\\1\" alt=\"[image]\" style=\"margin: 5px 0px 5px 0px\" />";

        $rules[8]["replace"] = "#\[img-(.+?)\](.+?)\[/img\]#is";
        $rules[8]["to"]      = "<img src=\"\\2\" alt=\"[image]\" style=\"float: \\1; margin: 0px 5px 5px 0px\" />";

        foreach($rules as $node) {
            $string = preg_replace($node["replace"],$node["to"],$string);
        }

        return $string;
    }

    echo coded($_POST["text"]);

?>