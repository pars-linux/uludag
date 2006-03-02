<?php
/**
 * @author Hans Deragon, hans@deragon.biz
 * @version 1.0
 * Internationalization tag
 *
 *
 * Type: function<br>
 * Name: i18n<br>
 * Purpose: Choose proper internationalization string according to $locale.<br> *
 * Consider the following in your .tpl file:
 *
 * <p><blockquote>
 *
 * {i18n def="Greetings" fr="Bonjour" de="GuttenTag?"}
 *
 * </blockquote><p>
 *
 * If the php global variable $locale is set to "fr_ca", then
 * the tag will be replaced by "Bonjour" in the final output.
 * <p>
 * You must set the php global $locale variable prior using
 * the tag.
 *
 * You can provide as many locale definitions (parameters) as required.
 *
 * @param def="<text>" Set the default text if no match is made between
 * $locale and the list of parameters in the i18n
 * command.
 *
 * @param <locale>="<text>" Set the text for the corresponding locale. The
 * locale follows the format <lang>[_<country].
 * Example: "fr", "en_US".
 *
 * @return string Returns the proper text for the given locale.
 */

function smarty_function_i18n_printDefault($params)
 { 
// Locale is not set. Returning default.
 if($params['def']=="")
 {
 return "i18n php tag error: No def parameter set.";
 }
 else
 return $params['def'];
 } 

function smarty_function_i18n($params, &$smarty)
 { 
global $locale;
 if(!isset($locale))
 {
 return smarty_function_i18n_printDefault($params);
 }
 else
 {
 list($lang, $country)=split('_', $locale);
 $bestid="";
 foreach(array_keys($params) as $id)
 {
 list($id_lang, $id_country)=split('_', $id);
 if($id_lang==$lang)
 {
 if($id_country==$country)
 // Got a perfect match here. We return.
 return $params[$id];
 else
 $besttext=$params[$id];
 }
 }
 if($besttext!="")
 // Here, we have not found an exact match, but we found something
 // pretty close where the language matches.
 // This occurs for instance if the locale is set to fr_ca, but
 // the tag is {i18n def="Greetings", fr="Bonjour"}. There is no
 // fr_ca in the tag, but we still match it with fr.
 return $besttext;
 else
 // No match found, not even semi-exact. Printing the default.
 return smarty_function_i18n_printDefault($params);
 }
 } 
?>
