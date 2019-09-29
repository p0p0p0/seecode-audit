/**
 * AdminLTE Demo Menu
 * ------------------
 * You should not use this file in production.
 * This file is for demo purposes only.
 */
$(function () {
    'use strict'

    $("#action-toggle").click(function () {
        if (this.checked) {
            var i = 0;
            $("input[name='_selected_action']:checkbox").each(function () {
                $(this).attr("checked", true);
                i++;
            })
        } else {
            $("input[name='_selected_action']:checkbox").each(function () {
                $(this).attr("checked", false);
                i = 0;
            })
        }
    });
    $("#multi_select1").change(function () {
        $("#multi_select1 option:selected").each(function () {
            $("#multi_select2").append($(this));
        });
    });

    $("#multi_select2").change(function () {
        $("#multi_select2 option:selected").each(function () {
            $("#multi_select1").append($(this).attr('selected', true));
        });
    });

    // policy template del
    $("#p_t_d").click(function () {
        var ps = ''
        if (!confirm('确定删除选中的模板吗?')) return false;
        $("input[name='_selected_action']:checkbox:checked").each(function () {
            ps = ps + $(this).attr("value") + ",";
        });

        var csrftoken = getCookie('csrftoken');
        if (ps == '' || ps == undefined) return false;
        $.post("/policy/template/del",
            {"ids": ps, "csrfmiddlewaretoken": csrftoken},
            function (data) {
                window.location.href = '/policy/template';
            });
    });

    // add filter
    $("#platform").change(function () {
        var csrftoken = getCookie('csrftoken');
        $("#platform option:selected").each(function () {
            $.get("/policy/template/search", {
                "origin_id": $("#origin").val(),
                'platform_id': $(this).val(),
                "csrfmiddlewaretoken": csrftoken
            }, function (data) {
                for (var i in data) {
                    if (data[i].event_id != '')
                        $("#policy_template").append("<option value=\"" + data[i].id + "\" >" + data[i].name + "(event_id: " + data[i].event_id + ")</option>")
                    else
                        $("#policy_template").append("<option value=\"" + data[i].id + "\" >" + data[i].name + "</option>")
                }
            });
        });
    });

    $("#del-f-r").click(function () {
        var ps = ''
        if (!confirm('确定删除选中的数据吗?')) return false;
        $("input[name='_selected_action']:checkbox:checked").each(function () {
            ps = ps + $(this).val() + ",";
        });

        var csrftoken = getCookie('csrftoken');
        var tt = $(this).attr("data-type")
        if (ps == '' || ps == undefined) return false;
        $.post("/policy/del?t=" + tt,
            {"ids": ps, "csrfmiddlewaretoken": csrftoken},
            function (data) {
                if (tt == "1")
                    window.location.href = '/policy/filter';
                else
                    window.location.href = '/policy/rule';
            });
    });

    $("#policy_template").change(function () {
        showField();
    });
    $(".field-del").click(function () {
        var elm_id = $(this).attr('for-id');
        $("#row-" + elm_id).remove();
    });

    $("#sub-field-btn").click(function () {
        var id = $("#fields").children("div").length;
        if (id == 1) return false;
        $("#fields > div:last-child").remove();
    });

    $("#submit-rule").click(function () {
        // TODO same field
        var fields = []
        //return false
        /*$('.fields').each(function () {
            var c_value = $(this).val()
            if ($.inArray(c_value, fields) == -1){
                fields.push(c_value)
            }else{
                alert(/same field!!!/)
            }

        })*/
        return true
    });

    $("#raw-btn").click(function () {
        var v = $(this).val()
        if (v == "JSON") {
            $("#raw-list").hide();
            $("#raw-div").children().remove()
            $.get("/policy/json/" + $(this).attr('data-id'), {}, function (data) {
                $("<br /><span>").text(data.replace(/"/g, "")).appendTo($("#raw-div"));
            });
            $("#raw-div").show();
            $(this).val('RAW')
        } else {
            $("#raw-list").show();
            $("#raw-div").hide();
            $(this).val('JSON')
        }

    });

    $('.raw-show-btn').click(function () {
        var f_id = $(this).attr('for-id');
        $("#" + f_id).toggle("slow");
        if ($(this).hasClass('fa-angle-double-up'))
            $(this).removeClass('fa-angle-double-up').addClass('fa-angle-double-down');
        else
            $(this).addClass('fa-angle-double-up').removeClass('fa-angle-double-down');
    })

    // rule search
    $("#search-platform").change(function () {
        $("#event-type").children().remove();
        $("#event-type").append("<option value=\"0\" >所有事件</option>");
        $("#search-platform option:selected").each(function () {
            $.get("/policy/template/search", {
                "origin_id": $("#search-origin").val(),
                'platform_id': $(this).val(),
                "csrfmiddlewaretoken": getCookie('csrftoken')
            }, function (data) {
                for (var i in data) {
                    if (data[i].event_id != '')
                        $("#event-type").append("<option value=\"" + data[i].eid + "\" >" + data[i].ename + "(event_id: " + data[i].event_id + ")</option>");
                    else
                        $("#event-type").append("<option value=\"" + data[i].eid + "\" >" + data[i].ename + "</option>")
                }
            });
        });
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showField(fields) {
    $("#policy_template option:selected").each(function () {
        $.get("/policy/fieldtemplate/" + $(this).val(), {}, function (data) {
            $(".fields").children().remove();
            for (var i in data) {
                $(".fields").append("<option value=\"" + data[i].id + "\" >" + data[i].name + "</option>");
            }
        });
    })
}


function getDateTimeStamp(dateStr){
 return Date.parse(dateStr.replace(/-/gi,"/"));
}
function getDateDiff(dateTimeStamp) {
    //JavaScript函数：
    var minute = 1000 * 60;
    var hour = minute * 60;
    var day = hour * 24;
    var halfamonth = day * 15;
    var month = day * 30;
    var year = month * 12;
    var now = new Date().getTime();
    var diffValue = now - dateTimeStamp;
    if (diffValue < 0) {
        //若日期不符则弹出窗口告之
        //alert("结束日期不能小于开始日期！");
    }
    var yearC = diffValue / year;
    var monthC = diffValue / month;
    var weekC = diffValue / (7 * day);
    var dayC = diffValue / day;
    var hourC = diffValue / hour;
    var minC = diffValue / minute;
    if (yearC >= 1) {
        result = "" + parseInt(yearC) + " 年前";
    }else if (monthC >= 1) {
        result = "" + parseInt(monthC) + " 个月前";
    }
    else if (weekC >= 1) {
        result = "" + parseInt(weekC) + " 周前";
    }
    else if (dayC >= 1) {
        result = "" + parseInt(dayC) + " 天前";
    }
    else if (hourC >= 1) {
        result = "" + parseInt(hourC) + " 个小时前";
    }
    else if (minC >= 1) {
        result = "" + parseInt(minC) + " 分钟前";
    } else
        result = "刚刚";
    return result;
}