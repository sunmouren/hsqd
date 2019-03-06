var tips = function ($msg, $type, $icon, $from, $align) {
	$type  = $type || 'info';
	$from  = $from || 'top';
	$align = $align || 'center';
	$enter = $type == 'success' ? 'animated fadeInUp' : 'animated shake';

	jQuery.notify({
		icon: $icon,
		message: $msg
	},
	{
		element: 'body',
		type: $type,
		allow_dismiss: true,
		newest_on_top: true,
		showProgressbar: false,
		placement: {
			from: $from,
			align: $align
		},
		offset: 20,
		spacing: 10,
		z_index: 10800,
		delay: 3000,
		timer: 1000,
		animate: {
			enter: $enter,
			exit: 'animated fadeOutDown'
		}
	});
};

/**
 * 页面加载等待
 * @param $mode 'show', 'hide'
 * @author yinq
 */
var pageLoader = function ($mode) {
	var $loadingEl = jQuery('#loader-wrapper');
	$mode          = $mode || 'show';

	if ($mode === 'show') {
		if ($loadingEl.length) {
			$loadingEl.fadeIn(250);
		} else {
			jQuery('body').prepend('<div id="loader-wrapper"><div id="loader"></div></div>');
		}
	} else if ($mode === 'hide') {
		if ($loadingEl.length) {
			$loadingEl.fadeOut(250);
		}
	}

	return false;
};


$(document).ready(function () {
    // 登录
    $('button.user-login').click(function () {
        var username =  $.trim($('input.username').val());
        var password =  $.trim($('input.password').val());

        // var isEmail = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        // if (!(isEmail.test(username))){
        //     tips('邮箱格式不正确~', 'danger');
        //     return false;
        // }

        if (username == '' || password == ''){
            tips('邮箱或用户名、密码都不能为空', 'danger');
            return false;
        }

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/user/login/',
            data: {'username': username, 'password': password},
            async: true,
            success: function (data) {
                if (data['msg'] == 'ok'){
                    tips('登录成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                } else {
                    tips('登录失败，请检查用户名或邮箱、密码，再试一次吧。', 'danger');
                    return false;
                }
            }
        });
    });
    // 注册
    $('button.user-register').click(function () {
        var email =  $.trim($('input.register-emial').val());
        var password1 =  $.trim($('input.register-password1').val());
        var password2 =  $.trim($('input.register-password2').val());
        var isEmail = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;

        if (!(isEmail.test(email))){
            tips('邮箱格式不正确~', 'danger');
            return false;
        }

        console.log(email);
        console.log(password1);
        console.log(password2);

        if (email == '' || password1 == '' || password2 == ''){
            tips('邮箱、密码、确认密码都不能为空', 'danger');
            return false;
        }

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/user/register/',
            data: {'email': email, 'password1': password1, 'password2': password2},
            async: true,
            success: function (data) {
                if (data['msg'] == 'ok'){
                    tips('注册成功，页面即将刷新~', 'success');
                    setTimeout(function () {
                        location.reload();
                    }, 1500);
                    return true;
                }
                if (data['msg'] == 'ko'){
                    tips('诶呀~，注册失败，请重新检查邮箱和密码，再试一次吧。', 'danger');
                    return false;
                }

                if (data['msg'] == 'exists'){
                    tips('诶呀~，邮箱已经被注册。', 'danger');
                    return false;
                }

                 if (data['msg'] == 'mismatch'){
                    tips('诶呀~，两次密码不一致。', 'danger');
                    return false;
                }
            }
        });
    });



    // 问答模态
    $('#review-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var title = button.data('title');
        var pid = button.data('pid');
        var postid = button.data('postid');
        var modal = $(this);
        var sendReviewBtn = modal.find('.modal-body button');

        modal.find('.modal-title').text(title);
        sendReviewBtn.data('pid', pid);
        sendReviewBtn.data('postid', postid);
    });
    $('button.send-review').click(function () {
        var $this = $(this);
        var pid = $this.data('pid');
        var postid = $this.data('postid');
        var content = $.trim($('textarea.review-content').val());

        if (content == ''){
            tips('内容不能为空~', 'danger');
            return false;
        }

        $.ajax({
            cache: false,
            type: 'POST',
            url: '/post/comment/add/',
            data: {'pid': pid, 'postid': postid, 'content': content},
            async: true,
            success: function (data) {
                if (data['msg'] == 'ok'){
                    var reviewCount = $('span.review-count');
                    reviewCount.text(parseInt(reviewCount.text()) + 1);
                    $('div.review-list').prepend(data['cmt']);
                    $('textarea.review-content').val("");
                    $('div#review-modal').modal('hide');
                    $('p.no-review').remove();
                    tips('发布成功~', 'success');
                    return true;
                } else {
                    tips('发布失败, 请刷新后重试', 'danger');
                }
            }
        });
    });

});
