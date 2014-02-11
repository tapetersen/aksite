$(function(){
    $("video,audio").mediaelementplayer({ pluginPath:"/static/mediaelement/" });
    $("#main-nav li:has(ul)").on("touchend", function(e) {
        if(!$(this).is(":hover"))
        {
            e.preventDefault();
        }
    });
});
