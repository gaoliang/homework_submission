/* #####################################################################
 #
 #   Project       : Modal Login with jQuery Effects
 #   Author        : Rodrigo Amarante (rodrigockamarante)
 #   Version       : 1.0
 #   Created       : 07/29/2015
 #   Last Change   : 08/04/2015
 #
 ##################################################################### */

$(function () {

    var $formLogin = $('#login-form');
    var $formLost = $('#lost-form');
    var $formRegister = $('#register-form');
    var $divForms = $('#div-forms');
    var $modalAnimateTime = 300;
    var $msgAnimateTime = 150;
    var $msgShowTime = 2000;

    $("form").submit(function () {
        switch (this.id) {
            case "login-form":
                var $lg_username = $('#login_username').val();
                var $lg_password = $('#login_password').val();
                var $lg_remember = $('#remember_login').prop("checked");
                $.ajax({
                    url: "/accounts/login/",
                    type: "POST",
                    data: {
                        'username': $lg_username,
                        'passwd': $lg_password,
                        'remember_login': $lg_remember,
                    },
                    dataType: "json",
                    success: function (data) {
                        if (data.valid) {
                            msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "success", "glyphicon-ok", "登录成功！");
                            setTimeout("location.replace('/');", 1000);
                        } else {
                            msgChange($('#div-login-msg'), $('#icon-login-msg'), $('#text-login-msg'), "error", "glyphicon-remove", data.info);
                        }
                    },
                    error: function (jqXHR) {
                        alert("发生错误：" + jqXHR.status);
                    }
                });
                return false;
                break;
            case "lost-form":
                var $ls_email = $('#lost_email').val();
                $.ajax({
                    url: "/accounts/forgetpassword/",
                    type: "POST",
                    data: {
                        'email': $ls_email
                    },
                    dataType: "json",
                    success: function (data) {
                        if (data.valid) {
                            msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), "success", "glyphicon-ok", "成功！请到邮箱里面查收相关邮件");
                        } else {
                            msgChange($('#div-lost-msg'), $('#icon-lost-msg'), $('#text-lost-msg'), "error", "glyphicon-remove", data.info);
                        }
                    },
                    error: function (jqXHR) {
                        alert("发生错误：" + jqXHR.status);
                    }
                });
                return false;
                break;
            case "register-form":
                var $rg_username = $('#register_username').val();
                var $rg_nickname = $("#register_nickname").val();
                var $rg_email = $('#register_email').val();
                var $rg_password = $('#register_password').val();
                var $rg_password2 = $("#register_password2").val();
                if ($rg_password != $rg_password2) {
                    msgChange($('#div-register-msg'), $('#icon-register-msg'), $('#text-register-msg'), "error", "glyphicon-remove", "两次输入的密码不一致");
                    return false;
                }
                $.ajax({
                    url: "/accounts/register/",
                    type: "POST",
                    data: {
                        'nickname': $rg_nickname,
                        'username': $rg_username,
                        'password': $rg_password,
                        'email': $rg_email
                    },
                    dataType: "json",
                    success: function (data) {
                        if (data.valid) {
                            msgChange($('#div-register-msg'), $('#icon-register-msg'), $('#text-register-msg'), "success", "glyphicon-ok", "注册成功！");
                            setTimeout("location.replace('/');", 1000);
                        } else {
                            msgChange($('#div-register-msg'), $('#icon-register-msg'), $('#text-register-msg'), "error", "glyphicon-remove", data.info);
                        }
                    },
                    error: function (jqXHR) {
                        alert("发生错误：" + jqXHR.status);
                    }
                });
                return false;
                break;
            default:
                return false;
        }
    });

    $('#login_register_btn').click(function () {
        modalAnimate($formLogin, $formRegister)
    });
    $('#register_login_btn').click(function () {
        modalAnimate($formRegister, $formLogin);
    });
    $('#login_lost_btn').click(function () {
        modalAnimate($formLogin, $formLost);
    });
    $('#lost_login_btn').click(function () {
        modalAnimate($formLost, $formLogin);
    });
    $('#lost_register_btn').click(function () {
        modalAnimate($formLost, $formRegister);
    });
    $('#register_lost_btn').click(function () {
        modalAnimate($formRegister, $formLost);
    });

    function modalAnimate($oldForm, $newForm) {
        var $oldH = $oldForm.height();
        var $newH = $newForm.height();
        $divForms.css("height", $oldH);
        $oldForm.fadeToggle($modalAnimateTime, function () {
            $divForms.animate({height: $newH}, $modalAnimateTime, function () {
                $newForm.fadeToggle($modalAnimateTime);
            });
        });
    }

    function msgFade($msgId, $msgText) {
        $msgId.fadeOut($msgAnimateTime, function () {
            $(this).text($msgText).fadeIn($msgAnimateTime);
        });
    }

    function msgChange($divTag, $iconTag, $textTag, $divClass, $iconClass, $msgText) {
        var $msgOld = $divTag.text();
        msgFade($textTag, $msgText);
        $divTag.addClass($divClass);
        $iconTag.removeClass("glyphicon-chevron-right");
        $iconTag.addClass($iconClass + " " + $divClass);
        setTimeout(function () {
            msgFade($textTag, $msgOld);
            $divTag.removeClass($divClass);
            $iconTag.addClass("glyphicon-chevron-right");
            $iconTag.removeClass($iconClass + " " + $divClass);
        }, $msgShowTime);
    }
});