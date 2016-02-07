<%include file="/support/header.mako" args="title='TIF Calculator'"/>
<form action="${request.script_root}" method="get">
    % if result["title"]:
        <input type="text" name="title" value="${query['page'].title if 'page' in query else query['title'] | h}" />
    % else:
        <input type="text" name="title" />
    % endif
    <button type="submit">Submit</button>
</form>

% if "error" in result:
    <div id="error">
        % if result["error"] == "no page":
            <p>Can't find the given page: <a href="${result['page'].url}">${result["page"].title | h}</a>.</p>
        % else
            An unknown error occurred.
        % endif
    </div>
% endif

% if "tif" in result:
    <div id="result">
        <div id="result-page"><a href="${result['page'].url}">${result["page"].title | h}</a></div>
        <table>
            <tr>
                <td>TIF</td>
                <td>${result["tif"]}</td>
            </tr>
            <tr>
                <td>Transclusions</td>
                <td>${result["transclusions"]}</td>
            </tr>
            <tr>
                <td>Protection</td>
                <td>${result["protection"]}</td>
            </tr>
        </table>
        % if "cache" in result and result["cache"]:
            <div id="result-cache">Pageview data is cached from up to <abbr title="${result['cache_time']}">${result["cache_age"]} ago</abbr>.</div>
        % endif
    </div>
% endif
<%include file="/support/footer.mako"/>
