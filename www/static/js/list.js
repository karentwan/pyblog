function modifyNav() {
    var lists = $(".nav li");
    $(lists[0]).removeAttr("class");
    $(lists[1]).removeAttr("class");
    $(lists[2]).attr("class", "active");
}

/**
 * 点赞函数
 */
function great(self, id) {
    console.log("待点赞的id:" + id);
    //ajax的简化版，不能返回错误信息
    $.get("/great?id=" + id, function(data) {
        console.log(data);
        var obj = eval( '(' + data + ')');
        if( obj.code == 200) {
            var a = $(self).find(".num")
            var num = parseInt(a.text());
            console.log(num)
            a.text(num + 1);
        } else {
            alert("点赞失败！");
        }
    });
}

(function() {
    window.onload = modifyNav;
})();