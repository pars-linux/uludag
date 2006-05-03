<?php
/**
*  Simple class for using Google's WebAPI and PHP5's SOAP extension
*
*  Requirements:
*     PHP 5 and the SOAP extension
*     Google licence key - get an account at http://www.google.com/apis/
*
*  I know this class is dirty, but it's a quick hack, it's just an example.
*/
class googleClient extends SOAPClient {

  private $exception = '';
  private $licenceKey = '';

  public  $results;

  function __construct($licenceKey) {
    $this->licenceKey = $licenceKey;
    parent::__construct('GoogleSearch.wsdl');
  }

  function search($query, $start = 0, $maxResults = 10, $filter = 'false', $restrict = '', $safeSearch = 'false',
  $languageRestrict = '', $inputEncoding = 'utf8', $outputEncoding = 'utf8') {
    try {
      $this->results = $this->doGoogleSearch($this->licenceKey, $query, $start, $maxResults, $filter, $restrict, $safeSearch, $languageRestrict, $inputEncoding, $outputEncoding);
      return true;
    } catch (SoapFatal $exception) {
      $this->exception = $exception;
      return false;
    }
  }

  function error() {
    return $this->exception;
  }
}
?>