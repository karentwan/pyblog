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
 */


/**
 * 递归生成评论
 * @param comments
 */
function recursion(comments) {
    // console.log('comments:' + comments);
    var li = '<li class="uc-comment-item">'+
                '<div class="uc-user-infor">'+
                '<span class="uc-username">{0}</span>'+
                '<span class="uc-address">'+
                '   [国内网友]'+
                '</span>'+
                '</div>'+
                '<div>{1}</div>'+
                '<div class="uc-control">'+
                    '<a href="javascript:void(0)" onclick=\'comment({2},'+'"{3}"' + ')\'>回复</a>'+
                '</div>'+
                '<div class="subcomment" style="margin-top:20px;">\n' +
                '     <ul style="width:96%;float:right;padding:0;background: #FAFAFA;padding:0 20px;">\n' +
                '{4}'+
                '   </ul>\n' +
                '</div>' +
                '<div class="clear"></div>'+
            '</li>';
    var children = comments['children'];
    var lis = "";
    for(var i = 0; i < children.length; i++) {
        lis += recursion(children[i]);
    }
    li = li.format(comments['username'], comments['content'], comments['id'], comments['username'], lis);
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
 * 获取评论
 */
function createComment() {
    var id = getQueryString('id')
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