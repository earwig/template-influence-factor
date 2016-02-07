<%! from datetime import datetime %>\
<% this_year = datetime.now().year %>\
        </div>
        <footer>
            Copyright &copy; 2016${"&ndash;" + str(this_year) if this_year > 2016 else ""} <a href="//en.wikipedia.org/wiki/User:The_Earwig">Ben Kurtovic</a> &bull; \
            <a href="https://github.com/earwig/template-influence-factor">Source Code</a> &bull; \
            <a href="http://validator.w3.org/check?uri=referer">Valid HTML5</a>
        </footer>
    </body>
</html>
