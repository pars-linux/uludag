<?php
   
   include_once 'utils.php';

   function GiveScore($Data,$Word) {
        $Data = strip_tags($Data);
        $Len  = strlen($Word);
        $j    = 0;
        $Word = strtolower($Word);
        for ($i=0;$i<strlen($Data);$i++) {
            if($Word===strtolower(substr($Data,$i,$Len)))
                $j++;
        }
        return $j;
   }

   if (isset($_GET["q"])) {
        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
        $Results = $Pardus->Search($_GET["q"]);
        if ($Results) {
            foreach ($Results as $Values) {
                echo GiveScore($Values['Content'],$_GET["q"]);
                echo "-".$Values['Title']."<br>"; 
            }
        }
   }

?>
