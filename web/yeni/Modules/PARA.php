<?php

    # Gökmen GÖKSEL

    class Para {

        var $Seperator;
        var $Codec;

        function Para ($_Words,$_Seperator=" ",$_Codec="UTF-8") {
            $this->Seperator=$_Seperator;
            $this->Codec=$_Codec;
            $this->SetVars($_Words);
        }

        function Highlight($Data,$LeftTag="<b>",$RightTag="</b>") {
            ##print_r ($this->PosList);
        }

        function SetSize($Data,$Size=400) {
            
            # Remove unnecessary tags
            $Data = strip_tags($Data);
            $TempData = mb_strtolower($Data,$this->Codec);
            
            # Get the length of Data and fit it
            $DataLen = mb_strlen($Data);
            if ($Size>$DataLen)
                $Size = $DataLen-round($Size/$DataLen);
            #echo $TempData;
            
            # Find actual set size
            # FIXME
            $SizeForWords = round($Size / sizeof($this->RawWords));
           
            # Find each word in given data, give them score, store their pos in array..
            for ($Pos=0;$Pos<$DataLen;$Pos++) {
                foreach ($this->RawWords as $Key=>$Word) {
                    if (ord($Word[0])==ord($TempData[$Pos])) {
                        if ($Word === mb_substr($TempData,$Pos,$this->RawSizes[$Key])) {
                            $this->Score[$Key]++;
                            $this->PosList[$Key][]=$Pos;
                        }
                    }
                }
            }
            
            # Set the data with the given Size..
            foreach ($this->Score as $Key=>$Score) {
                if ($Score>1)
                    $GetPos = round($Score/2);
                else
                    $GetPos = 0;
                $SettedData .= "...".mb_substr($Data,$this->PosList[$Key][$GetPos],$SizeForWords,$this->Codec);
            }

            $SettedData.="...";
            return $SettedData;
         
        }

        protected function SetVars($Words) {
            $Words = trim($Words);
            # Seperate words..
            $this->RawWords = split ($this->Seperator,$Words);
            # Find each word size, remove unnecessary tags and set them as Class var..
            foreach ($this->RawWords as $Key=>$Word) {
                $this->RawSizes[$Key]=strlen($Word);
                $this->RawWords[$Key]=mb_strtolower(htmlspecialchars(strip_tags($Word)),$this->Codec);
            }
        }
    }

?>
