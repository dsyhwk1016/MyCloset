// 로그인 회원가입 화면 바꾸기
const signinBtn = document.querySelector('.signup')
const signupBtn = document.querySelector('.signin')
const signinEl = document.querySelector('.container .signin')
const signupEl = document.querySelector('.container .signup')
const subSignin = document.querySelector('.wrap .submit-signin')
const subSignup = document.querySelector('.wrap .submit-signup')
const snsLogin = document.querySelector('.sns-login')
signinBtn.addEventListener('click', function () {
    signinBtn.classList.add('show');
    snsLogin.classList.remove('show');
    signinEl.classList.remove('show');
    signupBtn.classList.remove('show');
    signupEl.classList.add('show');
    subSignin.classList.remove('show');
    subSignup.classList.add('show');
})

signupBtn.addEventListener('click', function () {
    signupBtn.classList.add('show')
    signupEl.classList.remove('show')
    signinBtn.classList.remove('show')
    snsLogin.classList.add('show')
    signinEl.classList.add('show')
    subSignup.classList.remove('show');
    subSignin.classList.add('show');
})

// 회원가입창
const userid = document.getElementById('signup-id');
const pw = document.getElementById('signup-pwd');
const pwCheck = document.getElementById('pwd-check');
const nickname = document.getElementById('nickname')
let validid = false
let checkid = ''


//    아이디 중복체크
function validId() {

    if (userid.value !== '') {
        $.ajax({
            type: "GET",
            url: '/login/register',
            enctype: "multipart/form-data",
            async : false,
            data: {user_id: userid.value},
            success: function (response) {
                validid = response['status']

                if (validid == true) {
                    document.getElementById('already').innerHTML = '사용 가능한 아이디입니다.';
                    checkid = userid.value
                    pw.focus()
                } else {
                    console.log(validid)
                    document.getElementById('already').innerHTML = '이미 존재하는 아이디 입니다.';
                    document.getElementById('already').style.color = 'red';
                    userid.value = ''
                    userid.focus()
                }
            }//ajax
        })

    } else {
        document.getElementById('already').innerHTML = '아이디를 입력해주세요';
        document.getElementById('already').style.color = 'red';
        userid.focus()

    }

}

//     비밀번호
function checkPw() {
    if (pw.value.length < 4 || pw.value.length > 8) {
        alert('비밀번호는 최소 4자 ~최대 8자로 설정해주세요')
        pw.value = '';
        pw.focus();
    }
    if (pw.value !== '' && pwCheck.value !== '') {
        if (pw.value === pwCheck.value) {
            document.getElementById('same').innerHTML = '비밀번호가 일치합니다.';
            document.getElementById('same').style.color = 'black';
            nickname.focus();
        } else {
            document.getElementById('same').innerHTML = '비밀번호가 일치하지 않습니다.';
            document.getElementById('same').style.color = 'red';
            pwCheck.value = '';
            pwCheck.focus();
        }
    }
}

//     닉네임
function checkNickname() {
    if (nickname.value === '') {
        alert('닉네임을 입력해주세요')
        nickname.focus();
    } else if (nickname.value < 2 || nickname.value > 8) {
        alert('닉네임은 2~8자 까지 가능합니다.')

    }
}

//    회원가입 버튼
function submitSignUp() { //수정필요해요 switch문 사용할까 고민중
    if (validid === true && (pw.value.length >= 4 && pw.value.length <= 8) && pw.value === pwCheck.value && nickname.value != '') {
        if (checkid !== userid.value) {
            alert('아이디를 다시 확인해주세요')
            return false
        }//아이디 중복 체크하고 다른 아이디로 변경했을 경우 대비
        else {
            $.ajax({
                type: "POST",
                url: '/login/register',
                enctype: "multipart/form-data",
                data: {
                    user_id: userid.value,
                    user_pw: pw.value,
                    user_name: nickname.value
                },
                success: function (response) {
                    alert(response['msg']);
                    window.location.href = '/'
                }
            })
        }
    } else if (validid !== true) {
        alert('아이디 중복체크를 해주세요!')
        return false
    } else if (pw.value.length < 4 || pw.value.length > 8) {
        alert('비밀번호는 최소 4자 ~최대 8자로 설정해주세요')
        return false
    } else if (pw.value !== pwCheck.value) {
        alert('비밀번호를 확인해주세요')
        return false
    } else if (nickname.value === '') {
        alert('닉네임을 설정해주세요')
        return false
    } else {
        alert('회원가입 폼을 기입해주세요')
        return false
    }
}


// 로그인

const signinId = document.getElementById('signin-id');
const signinPw = document.getElementById('signin-pwd');

function submitSignin() {
    if (signinId.value === '' && signinPw.value === "") {
        alert('아이디 혹은 비밀번호를 입력하세요')
    } else {
        $.ajax({
            type: "POST",
            url: '/login/login',
            enctype: "multipart/form-data",
            data: {user_id: signinId.value,
                   user_pw: signinPw.value},
            success: function (response) {
                if (response['id_chk']== false){
                    alert('해당 아이디가 존재하지 않습니다')
                    signinId.value=''
                    signinPw.value=''
                    signinId.focus()
                }
                if (response['status'] == false) {
                    alert(response['msg'])
                    signinId.value=''
                    signinPw.value=''
                    signinId.focus()

                } else{
                    window.location.href = '/'
                }
            }
        })
    }
}

function fPwWindow(){
     document.querySelector('.modal-wrap').style.display ='block';
     document.querySelector('.modal-bg').style.display ='block';
}
function fPwClose(){
     document.querySelector('.modal-wrap').style.display ='none';
     document.querySelector('.modal-bg').style.display ='none';
}
function find_pw() {
    let user_id = document.getElementById('findpw-id');

            $.ajax({
                type: "GET",
                url: '/login/find_pw?user_id='+user_id,
                enctype: "multipart/form-data",
                async: false,
                data: {},
                success: function (response) {
                    alert(response['msg']);
                    fPwClose();
                }
            })
        }