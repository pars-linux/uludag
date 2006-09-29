<?php

    include_once ("../config.php");
    if ($CF["Tools"]["Pic"]["Enable"]) {

        header("Content-type: image/gif");

        #make an image,define colors bla bla
        $im = imagecreatetruecolor(200, 24);
        $white = imagecolorallocate($im, 255, 255, 255);
        $blue = imagecolorallocate($im, 25, 133, 197);
        $black = imagecolorallocate($im, 0, 0, 0);

        #fill the image with white
        imagefilledrectangle($im, 0, 0, 399, 40, $white);

        #get the text which will write on the image
        $text = $_GET["q"];

        #set the font, Alternate Gothic we use in Pardus's Web
        $font = 'alto.ttf';

        #set the text
        imagettftext($im, 17, 0, 0, 20, $blue, $font, $text);

        #show image as png
        imagegif($im);

        #destroy the image
        imagedestroy($im);
    }

?>
