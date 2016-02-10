<%include file="/support/header.mako" args="title='Error &ndash; TIF Calculator'"/>
<h2>Error!</h2>
<p>An error occurred. If it hasn't been reported (<a href="https://github.com/earwig/template-influence-factor/issues">try to check</a>), please <a href="https://github.com/earwig/template-influence-factor/issues/new">file an issue</a> or <a href="mailto:wikipedia.earwig@gmail.com">email me</a>. Include the following information:</p>
<div id="error">
    <pre>${traceback | trim,h}</pre>
</div>
<%include file="/support/footer.mako"/>
