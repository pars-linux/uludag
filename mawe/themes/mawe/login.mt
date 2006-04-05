{include file="head.mt"}
<div id="loginbox">
    {if $error}{assign var="errorstyle" value="style='border: 1px solid #FF0000';"}{/if}
    <form action="login.php" method="post">
    <fieldset id="loginFieldSet" style="width: 300px;">
        <legend>Login</legend>
        <div class="bebox">
            <span class="label"><label for="maweUsername">Username:&nbsp;</label></span>
            <span class="input"><input {$errorstyle} type="text" name="maweUserName" id="maweUserName" title="Username" /></span>
        </div>
        <br />
        <div class="bebox">
            <span class="label"><label for="mawePassword">Password:&nbsp;</label></span>
            <span class="input"><input {$errorstyle} type="password" name="mawePassword" id="mawePassword" title="Password" /></span>
        </div>
        <br />
        <div class="bebox">
            <button type="submit" name="DoLogin" id="DoLogin" value="Login" style="float: right;">Login</button>
        </div>
        <br />
    </fieldset>
    </form>
    {if $error}
    <code>
    <b>An error occured : </b><span style='color: red'>Username or Password Wrong !</span>
    </code>
    {/if}
</div>
</center>
</body>
</html>
