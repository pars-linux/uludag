{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<script language="JavaScript" type="text/javascript">
function AcUlke () {
 	var SehirSec = document.UyeKayit.Vilayet;
 	var UlkeSec = document.UyeKayit.Ulke;
	secim = UlkeSec.options[UlkeSec.selectedIndex].value;
	if (secim == 'T�rkiye') {
		SehirSec.disabled = false;
		
	}
	else
	{
		SehirSec.disabled = true;
		SehirSec.selectedIndex = 0;
	}

}
</script>
<script language="JavaScript" type="text/javascript">
function AcOzellik () {
 	var TescilNo = document.UyeKayit.TescilNumarasi;
 	var Ciro = document.UyeKayit.Ciro;
 	var EANTip = document.UyeKayit.EANTip;
 	var MMNMDurum = document.UyeKayit.MMNMDurum;
	secim = MMNMDurum.options[MMNMDurum.selectedIndex].value;
	if (secim == 'Evet') {
		TescilNo.disabled = false;
		Ciro.disabled=true;
		EANTip.disabled=true;
		EANTip.selectedIndex = 0;
		Ciro.selectedIndex = 0;
	}
	else
	{
		if (secim == 'Hayir' ){
		TescilNo.disabled = true;
		Ciro.disabled=false;
		EANTip.disabled=false;
		}else{
		TescilNo.disabled = true;
		Ciro.disabled=true;
		EANTip.disabled=true;
		}
		
	}

}
</script>
<script language="JavaScript" src="jscript/popcalendar.js"></script>

<table width="100%" border=0 align=center cellpadding="4" cellspacing="1" style="border-collapse:collapse ">
   <form name="UyeKayit" action="{{$Burasi}}" method=post onsubmit="if (SifreKontrol()) return kontrol(this); else return false;">
     <tr class=tabbas1><td height=33 colspan=2>M��TER� EKLEME</td></tr>
      <tr bgcolor="#f4f4f4">
        <td width="150"><font color="#FF0000">*</font><b>Yetkili Ad Soyad</b></td>
        <td bgcolor="#f4f4f4"><input name="N_AdSoyad" type="text" value="" alt="Ad Soyad" size=30></td>
      </tr>
      <tr>
        <td width="150"><font color="#FF0000">*</font><b>Firma Unvan</b></td>
        <td><input name="N_FirmaUnvan" type="text" value="" alt="Firma �nvan" size=30></td>
      </tr>
       <tr bgcolor="#f4f4f4">
        <td width="150"><font color="#FF0000">*</font><b>Firma K�sa Ad</b></td>
        <td bgcolor="#f4f4f4"><input name="N_FirmaAd" type="text" value="" alt="Firma Ad" size=30></td>
      </tr>
      <tr>
       <td width="150"><font color="#FF0000">*</font><b>E-Posta Adresi</td>
       <td><input name="N_EPosta1" type="text" value="" alt="Kullan�c� Ad" size=30>&nbsp;
        Kullan�c� ad� olarak kullan�lacakt�r.
       </td>
     </tr>
      <tr bgcolor="#f4f4f4">
       <td width="150"><font color="#FF0000">*</font><b>�ifre</td>
       <td bgcolor="#f4f4f4"><input name="N_Sifre" type="password" value=""  alt="�ifre">&nbsp;
         �ifreniz en az 6 hane olmal�d�r.</td>
     </tr>
       <tr>
       <td width="150"><font color="#FF0000">*</font><b>�ifre Tekrar�</td>
       <td><input name="N_SifreTekrar" type="password" value=""  alt="Tekrar �ifre"></td>
     </tr>
      <tr bgcolor="#f4f4f4">
        <td width="150"><font color="#FF0000">*</font><b>Telefon Numaras�</b></td>
        <td bgcolor="#f4f4f4"><input name="N_Tel" type="text" onkeypress="HarfYok();" value="" alt="Telefon Numaras�" size=30></td>
      </tr>
      <tr>
        <td width="150"><b>Fax Numaras�</b></td>
        <td ><input name="Fax" type="text" value="" alt="Fax Numaras�" size=30 onkeypress="HarfYok();"></td>
      </tr>
      <tr bgcolor="#f4f4f4">
       <td width="150"><font color="#FF0000">*</font><b>Adres</td>
       <td><TEXTAREA name="N_Adres" alt="Adres" cols="30" rows="2" ALT="Adres"></TEXTAREA></td>
     </tr>
     
      <tr>
       <td><font color="#FF0000">*</font><b>�l</b></td>
       <td>
       <select name="N_Vilayet" alt="�l">
          {{html_options options=$Vilayetler}}
        </select>    
         E�er �lke alan�ndan T�rkiye'yi se�erseniz Vilayet se�ebilirsiniz.
         </td>
        </tr>
       <tr   bgcolor="#f4f4f4">
        <td width="150"><b>Web Adresi</b></td>
        <td ><input name="URL" type="text" value="http://" alt="Web Adresi" size=30></td>
      </tr>
       <tr>
        <td width="150"><b>Vergi Dairesi</b></td>
        <td bgcolor="#f4f4f4"><input name="VergiDaire" type="text" alt="Vergi Dairesi" size=30></td>
      </tr>
      <tr   bgcolor="#f4f4f4">
        <td width="150"><b>Vergi Numaras�</b></td>
        <td ><input name="VergiNo" type="text" alt="Vergi Numaras�" size=30 onkeypress="HarfYok();"></td>
      </tr>
      <tr>
      		<td>
      			<font color="#FF0000">*</font><b>Daha �nce Milli Mal Numaralama Merkezi'ne �ye olup Firman�z ad�na Barkod Numaras� Ald�n�z m�?</b>
      		</td>
      		<td>
      			<select name="MMNMDurum">
      				<option value="">L�tfen Se�iniz...
      				<option value="Evet">Evet
      				<option value="Hayir">Hay�r
      			</select>&nbsp;&nbsp;&nbsp;	
      		<input name="TescilNumarasi" onkeypress="HarfYok();" type="text" alt="Tescil Numaras�" size=20 value="Tescil Numaras�..." onfocus="if ( value == 'Tescil Numaras�...' ) { value = ''; }" onblur="if ( value == '' ) { value = 'Tescil Numaras�...'; }" maxlength="15">	
      		</td>
      </tr>
       <tr bgcolor="#f4f4f4">
      	<td>
      		<font color="#FF0000">*</font><b>Firman�z Ad�na Milli Mal Numaraland�rma Merkezine Ba�vurunuz Bizim Taraf�m�zdan Yap�ls�n m�?</b>
      	</td>
      	<td>
      		<select name="MMNMBasvuru">
      				<option value="">L�tfen Se�iniz...
      				<option value="Evet">Evet
      				<option value="Hayir">Hay�r
      			</select>
      	</td>
      </tr>
       <tr bgcolor="#f4f4f4">
        <td width="150"><b>Ciro/YTL</b></td>
        <td >
          <select name="Ciro">
          	<option value="">L�tfen Se�iniz...
        	<option value="A">100 Milyon ve �zeri
        	<option value="B">50-100 Milyon aras�
        	<option value="C">10-50 Milyon Aras�
        	<option value="D">1-10 Milyon Aras�
        	<option value="E">500 Bin- 1 Milyon Aras�
        	<option value="F">100-500 Bin  Aras�
        	<option value="G">25-100 Bin Aras�
        	<option value="H">0-25 Bin Aras� ve YEN� KURULANLAR
        	
         </select>
        </td>
      </tr>       
       
       <tr>
        <td width="150"><b>EAN.UCC Firma Numaras�</b></td>
        <td>
        <select name="EANTip" >
        	<option value="">L�tfen Se�iniz...
        	<option value="9">9 Basamakl�
        	<option value="8">8 Basamakl�
        	<option value="7">7 Basamakl�
        </select><br>
        	<table border="0">
        		<tr bgcolor="#FFFFFF">
        			<td>
        				* �r�n �e�itlerimin say�s� <b>1000</b>'i a�mad���ndan <b>9 basamakl�</b> EAN.UCC firma numaras� tahsis edilmesi uygundur.
        			</td>
        		</tr>
        		<tr>
        			<td>
        				* �r�n �e�itlerimin say�s� <b>1000</b>'i a�t���ndan 10.000 �e�it �r�n�m� numaraland�rmaya olanak tan�yan <b>8 basamakl�</b> EAN.UCC firma numaras� tahsis edilmesi uygundur.  
        			</td>
        		</tr>
        		<tr bgcolor="#FFFFFF">
        			<td>
        				* �r�n �e�itlerimin say�s� <b>10.000</b>'i a�t���ndan 100.000 �e�it �r�n�m� numaraland�rmaya olanak tan�yan <b>7 basamakl�</b> EAN.UCC firma numaras� tahsis edilmesi uygundur.  
        			</td>
        		</tr>
        	</table>
        </td>
      </tr>	
	   <tr>
        <td width="150" bgcolor="#f4f4f4"><font color="#FF0000">*</font><b>�r�n Say�s�</b></td>
        <td bgcolor="#f4f4f4"><input name="N_UrunCesit" onkeypress="HarfYok();" type="text" alt="�r�n �e�it" size=30> Firman�za ait �r�n �e�iti say�s�. </td>
      </tr>	

      <tr>
       <td width="150">
        Haber listesinde �yelik ister misiniz?        Sitemizdeki yenilikler ve yeni �r�nler adresinize g�nderilecektir. </td>
       <td>
        <input name="HaberListe" type=checkbox value="Evet" checked id="HaberUyelik">
        <label for="HaberUyelik">Evet �ye olmak istiyorum.</label> </td>
     </tr>
      <tr bgcolor="#f4f4f4">
   <td class=tdbaslik>MMNM Vekalet</td>
   <td><input type="checkbox" name="MMNMVekalet" {{if $Uye.MMNMVekalet}} checked {{/if}}></td>
 	</tr>
 	<tr>
   <td class=tdbaslik>TOF Belge</td>
   <td><input type="checkbox" name="TOFBelge" {{if $Uye.TOFBelge}} checked {{/if}}></td>
 </tr>
 <tr bgcolor="#f4f4f4">
   <td class=tdbaslik>�zel Vekalet</td>
   <td><input type="checkbox" name="OzelVekalet" {{if $Uye.OzelVekalet}} checked {{/if}}></td>
 </tr>
 	<tr>
   <td class=tdbaslik>Gelir Tablosu</td>
   <td><input type="checkbox" name="GelirTablosu" {{if $Uye.GelirTablosu}} checked {{/if}}></td>
 </tr>  
 <tr bgcolor="#f4f4f4">
   <td class=tdbaslik>Sicil Gazete</td>
   <td><input type="checkbox" name="SicilGazete" {{if $Uye.SicilGazete}} checked {{/if}}></td>
 </TR>
   
      <tr>
    <td colspan=10 align=right>
        <input name="UyeKayit" type="submit" value="K a y d e t" class="onay">   
        
        </td>
     </tr>
     
  </form>
</table>
   <br>

<SCRIPT language="javascript">
 function SifreKontrol()
  {
    var sifre=document.UyeKayit.N_Sifre.value;
    if((sifre.length<6)&&(sifre!=''))
    {
       alert('�ifreniz en az 6 haneli olmal�d�r!');
       return false;
    }

    if(document.UyeKayit.N_Sifre.value != document.UyeKayit.N_SifreTekrar.value)
     {
      alert("�ifreleriniz Uyu�mamakta!");
      return false;
     }
     else return true;
  }

</SCRIPT>

{{/strip}}