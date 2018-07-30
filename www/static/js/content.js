/**
<li class="uc-comment-item">
    <div class="uc-user-infor">
        <span class="uc-username">{{comment[2]}}</span>
        <span class="uc-address">
            [国内网友]
        </span>
    </div>

    <div>
        {{comment[3]}}
    </div>
    <div class="uc-control">
        <a href="#">回复</a>
    </div>
    <div class="clear"></div>
</li>


<li class="uc-comment-item">
    <img class="userhead" src="res/userhead.png" alt="用户头像">
    <!--评论内容-->
    <div class="c-main">
        <div>
            这只是测试评论，并不具有意义
        </div>
        <div class="c-info">
            <span>小翠翠</span>
            <span>2018-07-26</span>
            <a href="#" style="color:#00a67c;">回复</a>
        </div>
    </div>
</li>
 */


/**
 * 递归生成评论
 * @param comments
 */
function recursion(comments) {
    // console.log('comments:' + comments);
    var li = '<li class="uc-comment-item">' +
            '    <img class="userhead" src="../static/res/userhead.png" alt="用户头像">' +
            '    <!--评论内容-->' +
            '    <div class="c-main">' +
            '        <div>' +
            '            {0}' +
            '        </div>' +
            '        <div class="c-info">' +
            '            <span>{1}</span>' +
            '            <span>{2}</span>' +
            '            <a href="javascript:void(0)" style="color:#00a67c;" ' +
            '                               onclick=\'comment({3},'+'"{4}"' + ')\'>回复</a>' +
            '        </div>' +
            '    </div>' +
            '   <ul class="c-subcomment">'+
            '   {5}'+
            '   </ul> '
            '</li>';
    var children = comments['children'];
    var lis = "";
    for(var i = 0; i < children.length; i++) {
        lis += recursion(children[i]);
    }
    // li = li.format(comments['username'], comments['content'], comments['id'], comments['username'], lis);
    li = li.format(comments['content'], comments['username'], comments['time'], comments['id'], comments['username'], lis);
    // console.log(li);
    return li;
}

/**
 * 评论
 */
function comment(id, username) {
    console.log('id:' + id + "\tusername:" + username);
    $("#pid").val(id);
    var obj = $("#input");
    obj.val("回复 " + username + ":");
    obj.focus();
}

/**
 * 处理出入内容
 * @returns {boolean}
 */
function processParams() {
    var obj = $("#input");
    var content = obj.val();
    var temp = content.split(":");
    var con = temp[1] ? temp[1] : temp[0];
    obj.val(con);
    return true;
}

/**
 * 得到路由参数，也就是最后一个参数
 * @returns {string}
 */
function getRouteParam() {
    var str = window.location.href.split("/");
    var pa = str[str.length - 1];
    console.log(pa);
    return pa;
}

/**
 * 获取评论
 */
function createComment() {
    var id = getRouteParam();

    $.ajax({
        url:"/getUserComment",
        method:"post",
        data:"articleId=" + id,
        success:function(result){
            // console.log(result);
            var obj = json2obj(result);
            console.log(obj);
            var lis = "";
            for(var i = 0; i < obj.length; i++) {
                var temp = obj[i];
                lis += recursion(temp);
            }
            $("#comments").html(lis);
            // recursion(result)
        }
    });
}

createComment();