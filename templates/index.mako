<%include file="/support/header.mako" args="title='TIF Calculator'"/>
<form id="main-form" action="${request.script_root}" method="get">
    % if "title" in result:
        <input type="text" name="title" value="${result['page'].title if 'page' in result else result['title'] | h}" />
    % else:
        <input type="text" name="title" />
    % endif
    <button type="submit">Submit</button>
</form>

% if "error" in result:
    <div id="error">
        % if result["error"] == "no page":
            <p>Can't find the given page: <a href="${result['page'].url}">${result["page"].title | h}</a>.</p>
        % else:
            An unknown error occurred.
        % endif
    </div>
% endif

% if "tif" in result:
    <div id="result">
        <div class="result-page"><a href="${result['page'].url}">${result["page"].title | h}</a></div>
        <table>
            <tr>
                <td>TIF</td>
                <td>${"{0:.2f}".format(result["tif"])} <span class="unit">views/min</span></td>
            </tr>
            <tr>
                <td>Transclusions</td>
                <td>${result["transclusions"]} <span class="unit">pages</span></td>
            </tr>
            <tr>
                <td>Protection</td>
                % if result["protection"]:
                    <td><span class="prot-level prot-${result['protection']['level']}">${result["protection"]["level"]}</span> until <span class="prot-expiry">${result["protection"]["expiry"]}</span></td>
                % else:
                    <td><span class="prot-none">none</span></td>
                % endif
            </tr>
        </table>
        % if "cache_time" in result:
            <div id="result-cache">Pageview data is cached from up to <abbr title="${result['cache_time']}">${result["cache_age"]} ago</abbr>.</div>
        % endif
    </div>
% endif
<%include file="/support/footer.mako"/>
