var boo1 = false;
var boo2 = false;
var boo3 = false;
var boo4 = false;
var boo5 = false;
var str = "<div class=\"wrap-input100 validate-input m-b-16\" data-validate=\"user_auth_number is required\">\n" +
    "                    <input id='user_auth_number' class=\"input100\" type=\"text\" name=\"user_auth_number\"\n" +
    "                           placeholder=\"인증번호를 입력해주세요\">\n" +
    "                    <span class=\"focus-input100\"></span>\n" +
    "                </div>\n" +
    "                <br>"

var list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
var username_list, nickname_list, phone_number_list, email_id_list;
username_list = [
    {% for i in username_list %}
        '{{ i }}',
    {% endfor %}
];
nickname_list = [
    {% for i in nickname_list %}
        '{{ i }}',
    {% endfor %}
];
phone_number_list = [
    {% for i in phone_number_list %}
        '{{ i }}',
    {% endfor %}
];
email_id_list = [
    {% for i in email_id_list %}
        '{{ i }}',
    {% endfor %}
];

function real_submit(){
    if (!(boo1 && boo2 && boo3 && boo4 && boo5)) {
        alert("올바른 형태로 정보를 입력해주세요.")
    } else {
        document.signup_form.submit()
    }
}

function validation_check(string) {
    var bool1 = string.slice(0, 3) === '010' && string.length === 11;
    var bool2 = true;
    for (var i = 0; i < string.length; i++) {
        if (!(string.charAt(i) in list)) {
            bool2 = false;
            break;
        }
    }
    var bool3 = !(phone_number_list.indexOf(string) > -1);
    return bool1 && bool2 && bool3
}

var auth_number;

function send() {
    var imdiv = document.querySelector('#imdiv');
    imdiv.innerHTML = str;
    var user_phone_number = document.getElementById("phone_number").value;
    $.ajax({
        type: "POST",
        url: "send_sms",
        data: {
            'user_phone_number': user_phone_number,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function () {
            alert('입력하신 휴대폰 번호로 인증번호가 전송되었습니다.');
        }

    })
}

function sms() {
    var user_phone_number = document.getElementById("phone_number").value;
    if ( !(phone_number_list.indexOf(user_phone_number) > -1)&& validation_check(user_phone_number) ){
        send();
        boo5 = true
    } else {
        alert('올바른 휴대폰 번호를 입력해주세요.')
    }
}

$(".alert").hide();
$("input").keyup(function () {
    var pwd1 = $("#password1").val();
    var pwd2 = $("#password2").val();
    if (pwd1 != "" || pwd2 != "") {
        if (pwd1 == pwd2) {
            $("#password-alert-success").show();
            $("#password-alert-danger").hide();
            boo2 = true
        } else {
            $("#password-alert-success").hide();
            $("#password-alert-danger").show();
        }
    }

    var username = $("#username").val();
    if (username !== "") {
        if (username_list.indexOf(username) > -1) {
            $("#username-alert-success").hide();
            $("#username-alert-danger").show();
        } else {
            $("#username-alert-success").show();
            $("#username-alert-danger").hide();
            boo1 = true
        }
    }

    var nickname = $("#nickname").val();
    if (nickname !== "") {
        if (nickname_list.indexOf(nickname) > -1) {
            $("#nickname-alert-success").hide();
            $("#nickname-alert-danger").show();

        } else {
            $("#nickname-alert-success").show();
            $("#nickname-alert-danger").hide();
            boo3 = true
        }
    }

    var email_id = $("#email_id").val();
    if (email_id !== "") {
        if (email_id_list.indexOf(email_id) > -1) {
            $("#email_id-alert-success").hide();
            $("#email_id-alert-danger").show();

        } else {
            $("#email_id-alert-success").show();
            $("#email_id-alert-danger").hide();
            boo4 = true
        }
    }

    var phone_number = $("#phone_number").val();
    console.log('validation check result:' + validation_check(phone_number));

    if (phone_number !== "") {
        if (!validation_check(phone_number)) {
            $("#phone_number-alert-success").hide();
            $("#phone_number-alert-danger").show();

        } else {
            $("#phone_number-alert-success").show();
            $("#phone_number-alert-danger").hide();
        }
    }


})

