{{strip}}
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}

<table align=center border=0 width=70% cellpadding=5>
<tr>
<td colspan="2">
<FIELDSET style="display:block; position:relative; top:0; width=100%">
<LEGEND>{{t}}Site Ýçi Arama{{/t}}</LEGEND>
        <form method="POST" action="{{$Burasi}}">
<br>
<table border=0 width=100% cellpadding=3>
<tr>
<td>
arama, bu site ici aramadir... haberler, vs.. icin. donanim ile karstirmayalim...
</td>
</tr>
</table>
<br><br>
<center><b>{{t}}Anahtar Kelime:{{/t}}&nbsp;&nbsp;&nbsp;&nbsp;</b><input type="text" size="27" name="N_Anahtar" maxlength="30" value="{{t}}Aranacak Kelimeler...{{/t}}" onfocus="if ( value ==
'{{t}}Aranacak Kelimeler...{{/t}}' ) { value = ''; }" onblur="if ( value == '' ) { value = '{{t}}Aranacak Kelimeler...{{/t}}'; }">
&nbsp;&nbsp;&nbsp;<input type="submit" name="HaberAra" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{t}}Ara{{/t}}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"></center>
</form>
</fieldset>
<br>
</td>
</tr>
{{if $TumHaberler}}
<script language="Javascript">
function SayfaGonder(No)
        {
        document.ListeForm.SayfaNo.value = No;
        document.ListeForm.submit();
        }
</script>
<tr><td colspan="3" class="ModulArama">{{t}}Haberler{{/t}}</td></tr>
    {{foreach item=TumHaber from=$TumHaberler name=TumHaber}}
       <tr>
       	<td colspan="6"><li><a href="{{$SSayfa}}Haberler&HaberNo={{$TumHaber.No}}">{{$TumHaber.Baslik}}</a> {{$TumHaber.Tarih}}</td>
       </tr>
    {{/foreach}}
{{/if}}
 </table>
   {{if $Bulunamadi}}
        <center><b>{{t}}Kayýt Bulunamadý...{{/t}}</b></center>
   {{/if}}
{{include file="TableFoot.tpl"}}
{{/strip}}