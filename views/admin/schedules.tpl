% rebase('admin/base.tpl')
<h1>Schedule Management</h1>

<form class="form-inline" method="post">
    <div class="form-group">
        <select class="form-control" id="channel" name="channel">
        % for channel in channels['channels']:
            % if channel['number'] == selected_channel:
            <option value="{{ channel['number'] }}" selected>{{ channel['name'] }}</option>
            % else:
            <option value="{{ channel['number'] }}">{{ channel['name'] }}</option>
            % end
        % end
        </select>

        <select class="form-control" id="day" name="day">
        % for day in days:
            % if str(day) == str(selected_day):
            <option value="{{ day }}" selected>{{ day }}</option>
            % else:
            <option value="{{ day }}">{{ day }}</option>
            % end
        % end
        </select>
    </div>
    <div class="form-group ml-2 ">
        <div class="custom-control custom-switch">
            <input type="checkbox" class="custom-control-input" id="switch">
            <label class="custom-control-label" for="switch">Enable Manual Mode</label>
        </div>

        <button id="fetcher" class="btn btn-primary ml-2 ">Fetch Scraper</button>
        <button id="fetcher-man" class="btn btn-primary ml-2 ">Fetch Manual</button>
    </div>
    <textarea disabled name="schedule" class="form-control mt-3" style="min-width: 100%;" rows="30">
    </textarea>
    <button type="submit" class="btn btn-primary btn-lg btn-block">Submit</button>
</form>

<script>
$('select#day option').each(function(i, el) {
    m = moment(el.text)
    el.text = m.format("YYYY-MM-DD (dddd)")
})

template = [{"starts": "0000", "duration": 30, "program_name": ""}];

function update_textarea(param = "") {
    channel = $("#channel").val();
    day     = $("#day").val();

    checkManual()

    $.get("/live-tv/schedule/"+channel+"/"+day + (param ? `?${param}=true` : ""), function(data, status) {
        if(data) {
            $("textarea").val(JSON.stringify(data, null, 3));
        }
    })
    .fail(function() {
        $("textarea").val(JSON.stringify(template, null, 3));
        alert("Server Error for this channel and day combination. Setting empty JSON template in textarea.")
    });
}

function checkManual() {
    
    channel = $( "#channel" ).val();
    day = $( "#day" ).val();

    $.ajax( {
        url: "/live-tv/schedule/" + channel + "/" + day + "/" + "manual",
        success: function ( data, status ) {
            if ( data.isManual) {
                document.querySelector( "#switch").checked = true
                $( "textarea" ).attr( "disabled", false )
            } else {
                document.querySelector( "#switch").checked = false
                $( "textarea" ).attr( "disabled", true )
            }
        } ,
    } );


    
}

$("#fetcher").on('click', function(e) { 
    e.preventDefault()
    update_textarea("scr")
});
$("#fetcher-man").on('click', function(e) { 
    e.preventDefault()
    update_textarea("man")
});
$("#channel").on('change', function() { update_textarea() });
$("#day").on('change', function() { update_textarea() });
$("#switch").on('change', function() { 
    if (   this.checked) {
        $("textarea").attr( "disabled", false)
    } else {
        $("textarea").attr( "disabled", true )
    }
});
$('form').on('submit', function(e) {
    try {

        e.preventDefault()
        if (!confirm("Are you sure?")) return
        
        const isManualMode = $("#switch").is( ":checked" )
        const scheduleData = JSON.parse($('textarea').val())
        
        const channel = $( "#channel" ).val();
        const day = $( "#day" ).val();



        const body = {
            isManual: isManualMode ? true : false,
            schedule: scheduleData 
        }

        const bodyStr = JSON.stringify(body)

        $.ajax( {
            url: "/live-tv/schedule/" + channel + "/" + day,
            data: bodyStr,
            method: "POST",
            contentType:"application/json; charset=utf-8",
            success: function ( ) {
                alert("Done!")
            },
            error: function(a,b,c) {
                alert("Server error")
            }
            
        } );






        // if (!isManualMode) {
        //     // TODO save changes
        //     alert("Changes saved but this channel is still in Scraper mode. Enable manual mode for changes to be displayed to the site users.")
        // } else {
        //     // TODO save changes
        //     alert("Changes saved.")

        // }

    }
    catch (e) {
        alert(e)
        return false;
    }
})
update_textarea();
checkManual()

</script>
