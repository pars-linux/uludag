{{strip}}
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}
<h3>{{t}}Terimler S�zl���{{/t}}Terimler S�zl���(*)</h3>
<!-- Haber Icerikleri -->
 {{include file="abc.tpl"}}
<form method="POST" action="{{$Burasi}}">
<FIELDSET style="display:block; position:relative; top:0; width=100%">
<LEGEND>{{t}}S�zc�k Arama{{/t}}</LEGEND>
<center><b>{{t}}Aranacak Kelime{{/t}} &nbsp;&nbsp;:&nbsp;&nbsp;</b><input type="text" size="27" name="N_Anahtar" maxlength="30" value="Aranacak Kelime..." onfocus="if ( value == 'Aranacak Kelime...' ) { value = ''; }" onblur="if ( value == '' ) { value = 'Aranacak Kelime...'; }">&nbsp;&nbsp;
<input type="submit" name="Ara" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{t}}Ara{{/t}}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"></center>
</fieldset>
</form>
 <br>
 {{if $Anahtar}}
         {{if $Sayi neq 0}}
 {{t}}Aratm�� oldu�unuz kelime :{{/t}} <b>{{$Anahtar}}</b><br>
 {{t}}Toplam Sonu�:{{/t}} <b>{{$Sayi}}</b><hr noshade size=1px>
         {{/if}}
 {{/if}}
<table border=0 width=100% cellpadding=5>
{{if $Harfler}}
{{if $Sayi neq 0}}
        {{if $Arama eq 1}}
<tr><td colspan="2" align="left"> <b>{{t}}Toplam Sonu�:{{/t}}</b>
{{$Sayi}}</center><hr noshade size=1px></td></tr>
         {{/if}}
 {{/if}}
 {{foreach item=Harf from=$Harfler name=Harf}}
<tr>
    <td valign="top">&#187;</td>
    <td><b>{{$Harf.Kelime}} :</b> {{$Harf.Aciklama}}</td></tr>
 {{/foreach}}
{{/if}}
{{if $Sayi eq 0 and $Ara}}
         <tr><td align=center><b>{{t}}Kay�tl� S�zc�k bulunamad�...{{/t}}</b></td></tr>
{{/if}}
</table>
{{include file="TableFoot.tpl"}}
{{/strip}}
