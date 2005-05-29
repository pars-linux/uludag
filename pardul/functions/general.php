<?
  /**
   *  functions.php
   *  This is a good place for end-user GUI specific functions.
   *
   */

     
   /**
    *   Looks for if there is any FAQ in DB
    *   @param integer $KategoriNo
    *   @return bool
    */
    
    function SssSoruVarmi($KategoriNo)
    {
    $Sql = "SELECT * FROM SssSorular WHERE KatNo='$KategoriNo'";
    $Sonuc = sorgula($Sql);
    if ($Sonuc->numRows()>0)
        return true;
    else
        return false;
    } // end SssSoruVarmi


?>
