
    <form action="<?$PHP_SELF?>" method="GET">
        <input type="text" name="q" size=100>
        <input type="submit" name="search" value="search">
    </form>


<?php

    include_once '../utils.php';

    $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
    #$Res = $Pardus->GetPage(htmlspecialchars($_GET["r"]));

    class Sud {
        
        public $Encoding = "UTF-8";
        public $ReSize = 460;

        function Sud ($_RawData,$_SearchWords) {
            $this->RawData = $_RawData;
            $this->SearchWords = split(" ",$_SearchWords);
            $this->SearchWord  = $_SearchWords;
        }

        function turnToEn($Data){
            mb_regex_encoding($this->Encoding);
            $TR = Array ('İ','Ş','Ğ','Ö','Ü','Ç','ı','ş','ğ','ö','ü','ç');
            $EN = Array ('I','S','G','O','U','C','i','s','g','o','u','c');
            for ($i=0; $i<sizeof($TR); $i++)
                $Data = mb_ereg_replace($TR[$i],$EN[$i],$Data);
            return $Data;
        }

        function GetPos($Data,$Word) {
            #$Data must be lower.
            return mb_strpos($Data,mb_strtolower($Word,$this->Encoding),0,$this->Encoding); 
        }

        function GetHighlighted($Word,$Data,$Color) {
            $Prefix = "<span style='background-color:$Color;color:#444'>";
            $Postfix= "</span>";
            $Return = @mb_ereg_replace($Word,$Prefix.$Word.$Postfix,$Data);
            $Return = @mb_ereg_replace(turnToEn($Word),$Prefix.turnToEn($Word).$Postfix,$Return);
            return $Return;
        }

        function Highlight($Data) {
            $Data       = strip_tags($Data);
            $DataLower  = mb_strtolower($Data,$this->Encoding);
            $Size       = round ($this->ReSize/sizeof($this->SearchWords));
            
            foreach($this->SearchWords as $Word) {
                $Word       = strip_tags($Word);
                $WordLower  = mb_strtolower($Word,$this->Encoding);
                # I know it sucks.
                $Pos        = $this->GetPos($DataLower,$WordLower);
                /*
                if (!$Pos){
                    $Pos    = $this->GetPos($TempData,$this->turnToEn($TempWord,1));
                    $EnWord = $this->turnToEn($TempWord,1);
                }
                */
                $Piece     .= "...".mb_substr($Data,$Pos,$Size,$this->Encoding);
            }

            # $IData      = mb_strtolower($Piece,'UTF-8');
            foreach ($this->SearchWords as $Word) {
                $Piece      = $this->GetHighlighted($Word,$Piece,'#FFFF00');
                $Piece      = $this->GetHighlighted($WordLower,$Piece,'#FFFF00');
            }
            return $Piece;
        }

        function Mod1(){
            foreach ($this->RawData as $Values)
                echo "<b><a href='?r=".$Values['NiceTitle']."&q=".$this->SearchWord."'>".$Values['Title']."</a></b><p class='searchresults'>".$this->Highlight($Values['Content'])."...</p>";
        }
    }

    if (isset($_GET["q"])) {
        $SearchWord = $_GET["q"];
        $Results = $Pardus->Search($SearchWord);
        $Search = new Sud($Results,$SearchWord);
        $Search->Mod1();
    }

?>
    
