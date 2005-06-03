<?php
include("$AdminAnaDizin/jscript/fckeditor.php");

function editorArea ($Name) {
	global $AdminAnaSayfa;
	$oFCKeditor->BasePath	= "$AdminAnaSayfa/jscript";
	$oFCKeditor->Value		= "Yaz buraya...";
	
	$EditorArea = "<script type=\"text/javascript\" src=\"$AdminAnaSayfa/jscript/fckeditor.js\"></script>
	<script type=\"text/javascript\">
	window.onload = function()
	{
	var oFCKeditor = new FCKeditor( '$Name' );
	oFCKeditor.BasePath	= $oFCKeditor->BasePath;
	oFCKeditor.ReplaceTextarea();
	}
	</script>";
	echo $EditorArea;
// 	$oFCKeditor->Create();
}

// $oFCKeditor = new FCKeditor('FCKeditor1') ;
// $oFCKeditor->BasePath	= $sBasePath ;
?>