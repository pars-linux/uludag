{{strip}}
{{include file="Header.tpl"}}
   <table border=0 width=100% cellpadding=5>		   
	 <tr class=tabbas1><td colspan=2 align=center>Z�YARET�� SAYISI</td></tr>
	 <tr class=tabloliste1><td><b>�ye Say�s�</b></td><td align=center><b>{{$UyeGirisSayi}}</b></td></tr>
	 <tr><td><b>Misafir Say�s�</b></td><td align=center><b>{{$AnonimGirisSayi}}</b></td></tr>
	 <tr class=tabloliste1><td><b>TOPLAM</b></td><td align=center><b><font color=red>{{$ToplamZiyaretci}}</font></b></td></tr>
   </table>	
   <br>
   <table border=0 width=100% cellpadding=5>		   
	 <tr class=tabbas1><td colspan=2 align=center>GENEL</td></tr>
	 <tr class=tabloliste1><td><b><a href="javascript:OzelPencere('{{$ASSayfa}}Yorumlar','Yorumlar',500,600,1,1)">�ye Yorumlar�</a></b></td><td align=center><b>{{$UyeYorumSayi}}</b></td></tr>
	 <tr class=tabloliste1><td><b><a href="{{$ASSayfa}}UyeGorus">�ye G�r�� ve �nerileri</a></b></td><td align=center><b>{{$GorusSayi}}</b></td></tr>
   </table>	
	<br><br>
   <table border=0 cellpadding=0 cellspacing=0 style="border-collapse:collapse;" width=100%>
     <tr><td align=center><a href="{{$ASSayfa}}YonetimMenu">Y�netim Men� D�zenleme</a></td></tr>
	 <tr><td>&nbsp;</td></tr>
     <tr><td align=center><a href="{{$ASSayfa}}YonetimDegiskenler">Sistem De�i�kenleri</a></td></tr>
   </table>
</td>
<td valign=top>
{{if $Uyarilar}}
  <table align=center border=0 cellspacing=0 cellpadding=2 width=100% style="border-collapse:collapse;">
  <tr class=tabbas1 height=33>
        <td>Uyar�</td>
        <td>Son Ger�ekle�me Zaman�</td>
        <td>Ger�ekle�me Say�s�</td>
        <td>��lem</td> 
  </tr>
  {{foreach item=Uyari from=$Uyarilar name=Uyarilar}}
  {{if $smarty.foreach.Uyarilar.iteration is odd}} <tr class=tabloliste1>{{else}}<tr class=tabloliste2>{{/if}}
        <td>{{$Uyari.Mesaj}}</td>
        <td align=center>{{$Uyari.TarihSaat}}</td>
        <td align=center>{{$Uyari.GerceklesmeSayi}}</td>
        <td align=center>
         <a href="{{$Burasi}}&SilUyariNo={{$Uyari.No}}" onclick="return confirm('Uyar� mesaj�n� silmek istedi�inize emin misiniz?');"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Uyar�y� Sil"></a>
        </td>
  </tr>
  {{/foreach}}
  </table>
 {{/if}}
</td>
</tr>
</table>
<!-- Header da acilan tablo kapatiliyor...-->
</td>
</tr>
</table>
{{/strip}}
