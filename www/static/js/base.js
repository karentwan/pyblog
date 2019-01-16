/**
 * json 转对象
 * @param str
 * @returns {any}
 */
function json2obj(str) {
    return eval('(' + str + ')');
}

function timestamp2time(n1) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
}

/**
 * 获取地址栏的参数
 * @param name
 * @returns {*}
 */
function getQueryString(name) {
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null) {
         return  unescape(r[2]);
     } else {
          return null;
    }
}

/**
 * js扩展占位符
 * @returns {String}
 */
String.prototype.format= function() {
    if(arguments.length === 0) return this;
    var param = arguments[0], str= this;
    if(typeof(param) === 'object') {
        for(var key in param)
            str = str.replace(new RegExp("\\{" + key + "\\}", "g"), param[key]);
        return str;
    } else {
        for(var i = 0; i < arguments.length; i++)
            str = str.replace(new RegExp("\\{" + i + "\\}", "g"), arguments[i]);
        return str;
    }
}