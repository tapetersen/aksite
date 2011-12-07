$(document).ready(function() {
    //$("input[type=file]").attr("id", "upload_field");
    $("input[type=file]:not([id])").attr("multiple", "multiple");
    $("input[type=file]:not([id])").map(function(){
        this.previousSibling.nodeValue = "Bulk upload multiple files (use Ctrl to select multiple): ";
    });
    /*$('<div id="progress_report">\
        <div id="progress_report_name"></div>\
        <div id="progress_report_status" style="font-style: italic;"></div>\
        <div id="progress_report_bar_container" style="width: 90%; height: 5px;">\
            <div id="progress_report_bar" style="background-color: blue; width: 0; height: 100%;"></div>\
        </div>\
    </div>').insertAfter($("#upload_field"));
    $("#upload_field").html5_upload({
            url: $("#upload_field").get(0).form.action,
            fieldName: "data",
            sendBoundary: window.FormData || $.browser.mozilla,
            onStart: function(event, total) {
                    return confirm("You are trying to upload " + total + " files. Are you sure?");
            },
            setName: function(text) {
                            $("#progress_report_name").text(text);
            },
            setStatus: function(text) {
                    $("#progress_report_status").text(text);
            },
            setProgress: function(val) {
                    $("#progress_report_bar").css('width', Math.ceil(val*100)+"%");
            },
            onFinishOne: function(event, response, name, number, total) {
                    //alert(response);
            }
    });*/

});

