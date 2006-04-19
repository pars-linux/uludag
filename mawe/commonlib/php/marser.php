<?php

    // marser

    $rules = Array();

        // Standart Rules
        $rules[0]["node1"] = "#\[b\](.+?)\[/b\]#is";
        $rules[0]["node2"] = "<b>\\1</b>";

        $rules[1]["node1"] = "#\[i\](.+?)\[/i\]#is";
        $rules[1]["node2"] = "<i>\\1</i>";

        $rules[2]["node1"] = "#\[u\](.+?)\[/u\]#is";
        $rules[2]["node2"] = "<u>\\1</u>";

        $rules[3]["node1"] = "#\[br\]#is";
        $rules[3]["node2"] = "<br>";

        $rules[4]["node1"] = "#\[link\]www\.(.+?)\[/link\]#is";
        $rules[4]["node2"] = "<a href=\"http://www.\\1\">www.\\1</a>";

        $rules[5]["node1"] = "#\[link\](.+?)\[/link\]#is";
        $rules[5]["node2"] = "<a href=\"\\1\">\\1</a>";

        $rules[6]["node1"] = "#\[link=(.+?)\](.+?)\[/link\]#is";
        $rules[6]["node2"] = "<a href=\"\\1\">\\2</a>";

        $rules[7]["node1"] = "#\[img\](.+?)\[/img\]#is";
        $rules[7]["node2"] = "<img src=\"\\1\" alt=\"[image]\" style=\"margin: 5px 0px 5px 0px\" />";

        $rules[8]["node1"] = "#\[img-(.+?)\](.+?)\[/img\]#is";
        $rules[8]["node2"] = "<img src=\"\\2\" alt=\"[image]\" style=\"float: \\1; margin: 0px 5px 5px 0px\" />";

        $rules[9]["node1"] = "#\[style=(.+?)\]#is";
        $rules[9]["node2"] = "style=\"\\1\"";

        $rules[12]["node1"] = "#\[class=(.+?)\]#is";
        $rules[12]["node2"] = "class=\"\\1\"";

        $rules[10]["node1"] = "#\[h(.+?)\](.+?)\[/h\]#is";
        $rules[10]["node2"] = "<h\\1>\\2</h\\1>";

        // Pardus Rules
        $rules[11]["node1"] = "#\[table\](.+?)\[/table\]#is";
        $rules[11]["node2"] = "<img src=\"\\2\" alt=\"[image]\" style=\"float: \\1; margin: 0px 5px 5px 0px\" />";


    function bb2html($string)
    {
        global $rules;
        foreach($rules as $node) {
            $string = preg_replace($node["node1"],$node["node2"],$string);
        }

        return $string;
    }

    include 'marser_template/head.template';
    echo stripslashes(bb2html($_POST["text"]));
    include 'marser_template/foot.template';
?>