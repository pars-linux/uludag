{{strip}}
{{*debug*}}
{{$SAYFA_TEMEL_UST_BOLUM}}
<table cellpadding=5 cellspacing=0 width=100% border=0 bgcolor="#FFFFFF" align="center" height="70%">
  <tr>
    <td valign=top width="{{$sistem_SayfaSoluEn}}" bgcolor="{{$sistem_SolSutunBg}}">{{$SAYFA_TEMEL_SOL_SUTUN}}</td>
    <td valign=top>
       {{$SAYFA_TEMEL_ORTA_SUTUN}}
    </td>
    {{if $SAYFA_TEMEL_DIGER_SUTUN_SAYI gt 0}}
    {{foreach item=SUTUN from=$SAYFA_TEMEL_DIGER_SUTUNLAR}}
     <td width="{{$sistem_SayfaSagiEn}}" valign=top id="sag" bgcolor="{{$sistem_SagSutunBg}}">
     {{$SUTUN}}
     </td>
    {{/foreach}}
   {{/if}}
</tr>
</table>
{{$SAYFA_TEMEL_ALT_BOLUM}}
{{/strip}}
