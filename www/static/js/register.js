/**
 * 在输入用户对话框失去焦点时执行，验证用户是否已存在
 */
function asyValidUser(self) {
    var field = $(self)
    var username = field.val()
    console.log(username)
    // 如果用户为空
    if( !username ) {
        $(".null-warning").show()
        return;
    }
    $(".null-warning").hide()
    $.ajax({
        type:"POST",
        url:"/hasUser",
        data:{"username":username},
        success:function(data) {//成功
            //200代表有值，201代表没有这个用户
                console.log(data)
            //json字符串转对象
            var obj = eval('(' + data + ')');
            console.log("data.code\t" + data.code);
            if( obj.code == 200 ) {
                console.log("当前用户不可注册！");
                // field.focus();
                $(".username-valid").hide()
                $(".warning").show()
            } else {
                console.log("当前用户可以注册！");
                $(".warning").hide()
                $(".username-valid").show()
            }
        }, error:function(data) {//失败
            //打印出错信息
            console.log(data);
        }
    });
}

function validField(self) {
    var field = $(self);
    // 如果字段为空
    if( !field.val() )
        return;
    if( field.attr("id") == "confirm") {
        var password = $("#password").val();
        var confirm = $("#confirm").val();
        if( password != confirm)  {
            $(".confirm-valid").hide();
            $(".nomatching-warning").show();
            $(".btn").attr({"disabled":"disabled"});
            return;
        }
        $(".btn").removeAttr("disabled")
        $(".nomatching-warning").hide();
        $(".confirm-valid").show();
    } else if( field.attr("id") == "password") {

        $(".password-valid").show();
    }
}

// 验证表单
function validate() {
    console.log('开始验证');
    var password = $("#password").val();
    var confirm = $("#confirm").val();
    if( confirm != password ) {
        alert("两次密码不匹配！");
        return false;
    }
    return true;
}