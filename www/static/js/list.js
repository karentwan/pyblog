function modifyNav() {
    var lists = $(".nav li");
    $(lists[0]).removeAttr("class");
    $(lists[1]).removeAttr("class");
    $(lists[2]).attr("class", "active");
}


(function() {
    window.onload = modifyNav;
})();