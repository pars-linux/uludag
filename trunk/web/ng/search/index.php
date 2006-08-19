
    <form action="<?$PHP_SELF?>" method="GET">
        <input type="text" name="q" size=100>
        <input type="submit" name="search" value="search">
    </form>


<?php

    include_once '../config.php';
    include_once '../vezir.php';
    include_once '../Modules/pardus.php';


    $Vezir = new Vezir($CF);
    $Pardus = new Pardus($Vezir);

    class Sud {
        public $Encoding = "UTF-8";
        public $ReSize = 460;

        function Sud ($_RawData,$_SearchWords) {
            $this->RawData = $_RawData;
            $this->SearchWord  = $_SearchWords;
            $this->SearchWords = split(" ",$_SearchWords);
            $this->SearchWordsLower = split(" ",mb_strtolower(strip_tags($_SearchWords),$this->Encoding));
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
            return mb_strpos($Data,$Word,0,$this->Encoding);
        }

        function GetHighlighted($Word,$Data,$Color) {
            $Prefix = "<span style='background-color:$Color;color:#444'>";
            $Postfix= "</span>";
            $Return = mb_ereg_replace($Word,$Prefix.$Word.$Postfix,$Data);
            $Return = mb_ereg_replace($this->turnToEn($Word),$Prefix.$this->turnToEn($Word).$Postfix,$Return);
            return $Return;
        }

        function Highlight($Data,$FullText=false) {

            if ($FullText==true)
                $Piece = mb_strtolower($Data,$this->Encoding);

            else {
                $Data       = strip_tags($Data);
                $DataLower  = mb_strtolower($Data,$this->Encoding);
                $Size       = round ($this->ReSize/sizeof($this->SearchWords));
                foreach($this->SearchWordsLower as $Word) {
                    $Pos        = $this->GetPos($DataLower,$Word);
                    $Piece     .= "...".mb_substr($Data,$Pos,$Size,$this->Encoding);
                }
                $Piece      = mb_strtolower($Piece,$this->Encoding);
            }

            foreach ($this->SearchWordsLower as $Word)
                $Piece = $this->GetHighlighted($Word,$Piece,$this->GetWordColor($Word));

            return $Piece;
        }

        function GetWordColor($Word) {
            #FIX PreDefined Color Values.
            $bgcolors[0]='#FFFF00';
            $bgcolors[1]='#E6E6FA';
            $bgcolors[2]='#ADD8E6';
            $bgcolors[3]='#FFA07A';
            $bgcolors[4]='#9ACD32';
            $bgcolors[5]='#FFDAB9';
            $bgcolors[6]='#98FB98';
            $bgcolors[7]='#D8BFD8';
            return $bgcolors[array_search($Word,$this->SearchWordsLower)];
        }

        function Mod1(){
            foreach ($this->RawData as $Values){
                echo "<b><a href='?r=".$Values['NiceTitle']."&q=".$this->SearchWord."'>".$Values['Title']."</a></b><p class='searchresults'>".$this->Highlight($Values['Content'])."...</p>";
            }
        }
    }

    if (isset($_GET["q"])) {
        $SearchWord = $_GET["q"];
        $Results = $Pardus->Search($SearchWord);
        $Vezir->ShowLogs();
        $Search = new Sud($Results,$SearchWord);
        $Page = $Pardus->GetPage('DepoPolitikasi');
        echo $Search->Highlight($Page[0]['Content'],true);
        #$Search->Mod1();
    }

?>
