<?php

    // Test Cases

    require_once('classes.php');

    $Pages = Array ('Title','Content','PType');
    $Values= Array ('Baslik','Icerik','D');
    $PP = new Pardus();
    $PP->DbLogDetail = 3;
    $PP->DbConnect('Host','User','Pass','DB');
    $PP->UpdateField('Pages','Title','Pardus 1.1');
    echo $PP->InsertRecord('Pages',$Pages,$Values);
    
?>
