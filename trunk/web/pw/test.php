<?php

    // Test Cases

    require_once('classes.php');

    $Pages = Array ('Title','Content','PType');
    $Values= Array ('Baslik','Icerik','D');
    $PP = new Pardus();
    $PP->DbLogDetail = 3;
    $PP->DbConnect('','','','');
    //$PP->UpdateField('Pages','Title','Pardus 1.5',3);
    //$PP->InsertRecord('Pages',$Pages,$Values);
    //$Records = $PP->GetRecord('Pages','Content',3);
    //$Records = $PP->FindRecord('Pages','Title','1.1','Title');
    //print_r($Records);

?>
