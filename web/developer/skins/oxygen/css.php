<?php
header("Content-type: text/css");

//  This script accepts the following URL parameters:
//  ?color=<colorname> or ?color=%23<hexadecimal> - Text color
//  ?background=<colorname> or ?background=%23<hexadecimal> - Background color
//  ?link=<colorname> or ?link=%23<hexadecimal> - link color
//  ?color&background&link - use browser colors only
//  ?mode=print - print stylesheet
//  ?mode=flat - show menu at the bottom, not at the left
//  ?site-image=<URL> - use a customised image in the header
//  ?css-inc=<path on this domain> - path to include a custom css.inc file
?>
/*
** HTML elements
*/

body {
    margin: 0; 
    padding: 0;
    text-align: center;
    font-size: 0.8em;
    font-family: "Bitstream Vera Sans", "Lucida Grande", "Trebuchet MS", sans-serif;
    <?php color ('#535353')?>
    <?php background ('#fff')?>
}

.clear {
	clear: both;
}

/* general styles */

table {
	background: white;
	font-size: 100%;
	color: black;
}


a:link, a:visited {
    padding-bottom: 0;
    text-decoration: none;
    <?php linkcolor ('#0057ae')?>
}

a:hover {
	text-decoration: underline;
}

a.title:link, a.title:visited, a.title:hover {
    text-decoration: none;
    <?php linkcolor ('#fff')?>
}

a:visited {
    <?php linkcolor ('#644a9b')?>
}
/*
a.stub {
	color: #772233;
}
a.new, #p-personal a.new {
	color: #ba0000;
}
a.new:visited, #p-personal a.new:visited {
	color: #a55858;
}
*/
h1, h2, h3, h4 {
    text-align: left;
    font-weight: bold;
    margin-top: 1.0em;
    <?php color ('#F7800A')?>
    <?php background ('transparent')?>
}

h1 {
    margin-top: 1.5em;
    font-size: 1.7em;
}

h1.firstHeading {
    margin-top: .5em;
    font-size: 1.7em;
}

h2 {
    font-size: 1.5em;
}

h3 {
    font-size: 1.2em;
    <?php color ('#e3ad00')?>
}

h4 {
    font-size: 1.1em;
}

h5 {
    font-size: 1.0em;
}



#right ul {
	line-height: 1.5em;
	list-style-type: square;
	margin: .3em 0 0 1.5em;
	padding: 0;
/*	list-style-image: url(bullet.gif);*/
}
ol {
	line-height: 1.5em;
	margin: .3em 0 0 3.2em;
	padding: 0;
	list-style-image: none;
}
li {
	margin-bottom: .1em;
}

hr {
    margin: 0.3em 1em 0.3em 1em;
    height: 1px;
    border: #dddddd dashed;
    border-width: 0 0 1px 0;
}

del {
    <?php color ('#800') ?>
    text-decoration: line-through;
}

dt {
    font-weight: bold;
    font-size: 1.05em;
    <?php color ('#0057ae')?>
}

dd {
    margin-left: 1em;
}

p {
    margin-top: 0.5em;
    margin-bottom: 0.9em;
    text-align: justify;
}

hr {
    margin: 0.3em 1em 0.3em 1em;
    height: 1px;
    <?php border ('#dddddd', 'dashed')?>
    border-width: 0 0 1px 0;
}

legend {
	background: white;
	padding: .5em;
	font-size: 95%;
}


input, textarea, select {
    margin: 0.2em;
    padding: 0.1em;
    font-size: 125%; /* for poor aaron */
    <?php color ('#000')?>
    <?php background ('#fff')?>
    border: 1px solid;
}

fieldset {
    <?php border ('#ccc', '1px solid')?>
}

li {
    text-align: justify;
}


form {
    margin: 0;
    padding: 0;
}

hr {
    height: 1px;
    <?php border ('gray', '1px solid')?>
}

img {
    border: 0;
}

table {
    border-collapse: collapse;
    font-size: 1em;
}

th {
    text-align: left;
    padding-right: 1em;
    <?php border ('#ccc', 'solid')?>
    border-width: 0 0 3px 0;
}




abbr, acronym, .explain {
	border-bottom: 1px dotted black;
	color: black;
	background: none;
	cursor: help;
}
q {
	font-family: Times, "Times New Roman", serif;
	font-style: italic;
}
/* disabled for now
blockquote {
	font-family: Times, "Times New Roman", serif;
	font-style: italic;
}*/
code {
        font-family: 'Bitstream Vera Sans Mono', Courier;
	background-color: #f9f9f9;
	padding: 0 0.5em 0 0.5em;
	border: 1px solid #b5cfe9;
}
pre {
	padding: 1em;
/*/	border: 1px dashed #2f6fab;
	color: black;
	background-color: #f9f9f9;*/
	font-size: 1.1em;
	line-height: 1.1em;
	overflow: auto;
}

/*
**The main area for structural Layout
*/

/* Main Header Navigation */
#header {
    <?php width ('100%')?>
    <?php color ('#535353')?>
    <?php background ('#eee')?>
    border-bottom: 1px solid #bcbcbc;
}

#header_top {
    margin: 0 auto;
    padding: 0;
    <?php width ('60em')?>
    <?php minWidth ('870px')?>
    <?php maxWidth ('45em')?>
    vertical-align: middle;
    <?php color ('#fff')?>
    <?php background ('url(top.jpg) repeat-x bottom', '#0057AE')?>
    min-height: 51px;
}

#header_top div {
    margin: 0 auto;
    padding: 0;
    <?php background ('url(top-left.jpg) no-repeat bottom left')?>
    min-height: 51px;
}

#header_top div div {
    margin: 0 auto;
    padding: 0;
    vertical-align: middle;
    text-align: left;
    font-size: 1.4em;
    font-weight: bold;
    <?php background ('url(top-right.png) no-repeat bottom right')?>
    min-height: 51px;
}

#header_top div div img {
    margin:8px 0 8px 18px;
    vertical-align: middle;
}

#header_bottom {
    <?php noprint()?>
    margin: 0 auto;
    padding: 0.6em 0em 0.3em 0;
    <?php width ('60em')?>
    <?php minWidth ('770px')?>
    <?php maxWidth ('45em')?>
    vertical-align: middle;
    text-align: right;
    <?php background ('#eeeeee')?>
}

#location {
    padding: 0 0 0 1.5em;
    text-align: left;
    line-height: normal;
    font-size: 1.1em;
    font-weight:bold;
    float: left;
}

#location ul {
    display: inline;
    margin: 0;
    padding: 0;
    list-style: none;
}

#location ul li {
    display: inline;
    white-space : nowrap;
    margin: 0;
    padding: 0 1em 0 0;
}

#body_wrapper {
    margin: 0 auto;
    <?php width ('60em')?>
    min-width: 900px;
    <?php maxWidth ('45em')?>
    

}

#body {
    <?php float ('left')?>
    margin: 0;
    padding: 0;
    <?php width ('60em')?>
    <?php minHeight ('40em')?>
    <?php minWidth ('970px')?>
    <?php maxWidth ('45em')?>
    <?php border ('#dddddd', 'solid')?>
    border-width: 0 0 0 1px;

}

#main {
    <?php width ('100%')?>
    padding: 10px;
    text-align: left;
}

/* Container for the right content that gets floated right */
#right {
    <?php float ('right')?>
    margin: 0;
    padding: 0;
    <?php width ('77%')?>
}


/*
** Left Navigation for Wiki
*/

#left {
    <?php noprint()?>
    <?php float ('left')?>
    margin: 0;
    padding: 0;
    <?php width ('20%')?>
}


/*
** Top Menu UL Based Menu
*/

#menu {
    margin: 0 0 0 0;
    text-align: right;
    line-height: normal;
    font-size: 1.1em;
    font-weight: bold;

}

#menu ul {
    display: inline;
    list-style: none;
    margin: 0;
    padding: 0;
    text-align: right;
}

#menu ul li {
    display: inline;
    white-space : nowrap;
    margin: 0 0 0 0;
    padding: 0 0 0 0;
    text-align: center;	
	max-height: 1.6em;
	}	
#menu ul li a, #menu ul li.selected a{ 
	padding: 0.2em 8px 0.3em 0;
}

#menu ul li a {
	<?php background ('url(tab-right.png) no-repeat top right')?>
 	<?php color ('#5d5d5d')?>
	text-decoration:none;
}

#menu ul li.new a {
	<?php background ('url(tab-right.png) no-repeat top right')?>
 	<?php color ('#bbbbbb')?>
	text-decoration:none;
}

#menu ul li.selected a{
	<?php background ('url(taba-right.png) no-repeat top right')?>
	border-bottom: 1px solid white;	
}
#menu ul li span, #menu ul li.selected span {
	padding: 0.2em 0.6em 0.3em 1em;
}
#menu ul li span {

	<?php background ('url(tab-left.png) no-repeat top left')?>
	}
#menu ul li.selected span {
	<?php background ('url(taba-left.png) no-repeat top left')?>
	<?php color ('#1357a4') ?>
	border-bottom: 1px solid white;
	}



/*
** Menu CSS code goes in this section
*/
.menu_box {
    padding: 0.7em 0 0.5em 0;
	text-align: left;
	
}

.menu_box ul {
    text-align: left;
	margin-left: -10px;
}

.menu_box li {
    list-style-type: none;
    text-align: left;
	
}
.menu_box .active{
    <?php color ('#cf4913')?>
}

.menutitle {
    text-align: left;
    margin: 0.6em 0 0 0;
    padding:0;
    color: white;
    <?php color ('white')?>
    <?php background ('url(block_title_mid.png) repeat-y right', '#0057AE')?>
}

.menutitle div {
    margin: 0;
    padding:0;
    <?php background ('url(block_title_top.png) no-repeat top right')?>
}
.menutitle div h2 {
    margin: 0;
    padding: 0.2em 0 0.3em 0.5em;
    line-height:1.2em;
    font-size: 120%;
    font-weight: normal;
    <?php color ('white')?>
    <?php background ('url(block_title_bottom.png) no-repeat bottom right')?>
}

/* Search Button Classes go here */
.menu_box form {
margin-top: 0.6em;
text-align:center;
}
.menu_box form #searchInput{
width: 8em;
border: 2px solid #dddddd;
color: #aaa;
font-size:75%
}
.menu_box input.searchButton {
	/*confirm the colours used in here */
	margin-top: 1px;
	width: 4em;
	background-color: #888a85;
	color: #fff;
	border: 1px solid #bcbdba;
        font-size:75%
}

#footer {
    <?php noprint()?>
    <?php width ('100%')?>
    <?php background ('#eeeeee')?>
    border-bottom:1px solid #BCBCBC;
    border-top:1px solid #BCBCBC;
}

#footer_text {
    margin: 0 auto; 
    padding: 1em 0 1em 3.5em;
    <?php width ('51.5em')?>
    text-align: left;
    <?php color ('#000000')?>
    <?php background ('#eeeeee')?>
}

#footer a:link, #footer a:visited {
    <?php color ('#4d88c3')?>
}

.printfooter {
    <?php onlyprint(); ?>
}

img.tex {
        vertical-align: middle;
}
span.texhtml {
        font-family: serif;
}

/* emulate center */
.center {
        width: 100%;
        text-align: center;
}
*.center * {
        margin-left: auto;
        margin-right: auto;
}
/* small for tables and similar */
.small, .small * {
        font-size: 94%;
}
table.small {
        font-size: 100%;
}


/*
** Diff rendering
*/
table.diff, td.diff-otitle, td.diff-ntitle {
	background-color: white;
}
td.diff-addedline {
	background: #cfc;
	font-size: smaller;
}
td.diff-deletedline {
	background: #ffa;
	font-size: smaller;
}
td.diff-context {
	background: #eee;
	font-size: smaller;
}
span.diffchange {
	color: red;
	font-weight: bold;
}

div.floatright, table.floatright {
	clear: right;
	float: right;
	position: relative;
	margin: 0 0 .5em .5em;
	border: 0;
/*
	border: .5em solid white;
	border-width: .5em 0 .8em 1.4em;
*/
}
div.floatright p { font-style: italic; }
div.floatleft, table.floatleft {
	float: left;
	position: relative;
	margin: 0 .5em .5em 0;
	border: 0;
/*
	margin: .3em .5em .5em 0;
	border: .5em solid white;
	border-width: .5em 1.4em .8em 0;
*/
}
div.floatleft p { font-style: italic; }


/* rounded infobox */

.rbroundbox { }
.rbtop div { background: url(tl.png) no-repeat top left; }
.rbtop { background: url(tr.png) no-repeat top right; }
.rbbot div { background: url(bl.png) no-repeat bottom left; }
.rbbot { background: url(br.png) no-repeat bottom right; }

 .rbtopwrap { 
     color: #fff; 
     background-color: #0071bc; 
     padding-bottom: 0.5em;
     font-weight: bold;
     text-align: center;
}
 
.rbtop div, .rbtop, .rbbot div, .rbbot {
    width: 100%;
    height: 7px;
    font-size: 1px;
}

.rbcontent { margin: 0 7px; padding-top: 0.5em; }
.rbroundbox { width: 50%; margin: 1em auto; background-color: #dadde0;}

/* rounded codebox */

div.rtop, div.rbottom { display: block; }
div.rtop b, div.rbottom b { display: block; height: 1px; overflow: hidden; }
div.rtop b.r1, div.rbottom b.r1 { margin: 0 5px; background: #555753; }
b.r2 {margin: 0 3px; border-left: 2px solid #555753; border-right: 2px solid #555753;}
b.r3 {margin: 0 2px; border-left: 1px solid #555753; border-right: 1px solid #555753;}
div.rtop b.r4, div.rbottom b.r4 
{ margin: 0 1px; height: 2px; border-left: 1px solid #555753; border-right: 1px solid #555753; }
div.rmiddle { border-left: 1px solid #555753; border-right: 1px solid #555753; padding: 0 5px; }
div.rcode p, pre { margin: 0; } 
div.codebox { margin-bottom: 1em; } 

div.rcode { 
  margin: 0; 
  padding: 0;
  display: block;
  overflow:auto;
  font-family: 'Bitstream Vera Sans Mono', monospace;
  white-space: pre;
}

.codebarbg {
  background-image: url(codebarbg.png);
  background-position: center right;
  background-repeat: no-repeat;
  background-color: #f1f1f1;
  font-family: 'Bitstream Vera Sans Mono', monospace;
  font-weight: bold;
  font-size: 14px;
  color: #555753;
  padding: 0em 0.5em 0em 0.5em;
  margin-bottom: 0.5em;
}

<?php

if (isset ($_GET ['css-inc']) && file_exists ($_SERVER ['DOCUMENT_ROOT'].$_GET ['css-inc'].'/css.inc'))
    include $_SERVER ['DOCUMENT_ROOT'].$_GET ['css-inc'].'/css.inc';

function color ($color) {
    if (! isset ($_GET ['color']))
        echo "color: ".$color.";\n";
    elseif ($_GET ['color'])
        echo "color: ".$_GET ['color'].";\n";
    else
       echo "color: WindowText;\n";
}

function background ($background, $color = false) {
    if (! isset ($_GET ['background'])) {
        echo "background: ".$background.";\n";
        if ($color)
            echo "background-color: ".$color.";\n";
    }
    elseif ($_GET ['background'])
        echo "background-color: ".$_GET ['background'].";\n";
    else
       echo "background: Window;\n";
}

function border ($color, $other = '') {
    if (! isset ($_GET ['color']))
        echo "border: ".$color." ".$other.";\n";
    else
        echo "border: ".$_GET ['color']." ".$other.";\n";
}

function linkcolor ($color) {
    if (! isset ($_GET ['link']))
        echo "color: ".$color.";\n";
    elseif ($_GET ['link'])
        echo "color: ".$_GET ['link'].";\n";
}

function noprint () {
    if (isset ($_GET ['mode']) && $_GET ['mode'] == "print")
        echo "display: none;\n";
}

function onlyprint () {
    if (isset ($_GET ['mode']) && $_GET ['mode'] != "print")
        echo "display: none;\n";
}

function noflat () {
    if (isset ($_GET ['mode']) && $_GET ['mode'] == "flat")
        echo "display: none;\n";
}

function float ($float) {
    if (! isset ($_GET ['mode']) || $_GET ['mode'] != "flat")
        echo "float: ".$float.";\n";
}

function width ($width) {
    if (! isset ($_GET ['mode']) || $_GET ['mode'] == "normal")
        echo "width: ".$width.";\n";
}

function minWidth ($minwidth) {
    if (! isset ($_GET ['mode']) || $_GET ['mode'] == "normal")
        echo "min-width: ".$minwidth.";\n";
}

function maxWidth ($maxwidth) {
    if (! isset ($_GET ['mode']) || $_GET ['mode'] == "normal")
        echo "max-width: ".$maxwidth.";\n";
}

function minHeight ($minHeight) {
    if (! isset ($_GET ['mode']) || $_GET ['mode'] == "normal")
        echo "min-height: ".$minHeight.";\n";
}

?>
