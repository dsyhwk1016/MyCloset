const curPw = document.getElementById('current-pw');
const newPw = document.getElementById('new-pw');
const newPwCheck = document.getElementById('pwd-check');

//현재 비밀번호 확인
function currentPw() {
  if (curPw.value !== '') {
    $.ajax({
      type: "POST",
      url: '/login/pw_update',
      enctype: "multipart/form-data",
      data: {cur_pw: curPw.value},
      success: function (response) {
        if (response['status'] == true) {
          curPw.disabled = false;
          document.getElementById('checkpw-now').innerHTML = '비밀번호 확인 완료';

        } else {
          document.getElementById('checkpw-now').innerHTML = '현재 비밀번호와 일치하지 않습니다.';
          document.getElementById('checkpw-now').style.color = 'red';
          curPw.value = ''
          curPw.focus()
        }
      }
    })

  } else {
    document.getElementById('checkpw-now').innerHTML = '현재 비밀번호를 입력해주세요';
    document.getElementById('checkpw-now').style.color = 'red';
    curPw.focus()

  }

}

//현재비밀번호와 새 비밀번호 비교
//     비밀번호
function comparePw() {
    if (newPw.value.length < 4 || newPw.value.length > 8) {
        alert('비밀번호는 최소 4자 ~최대 8자로 설정해주세요')
        newPw.value = '';
        newPw.focus();
    }
    if (newPw.value !== '' && curPw.value !== '') {
        if (newPw.value === curPw.value) {
            document.getElementById('comparepw').innerHTML = '현재 비밀번호와 동일합니다.';
            document.getElementById('comparepw').style.color = 'red';
            curPw.focus();
        }
    }
}
function sendNewPw(){
    if (newPw.value !== '' && newPwCheck.value !== '') {
        if (newPw.value === newPwCheck.value) {
             $.ajax({
                 type: "POST",
                 url: '/login/pw_update',
                 enctype: "multipart/form-data",
                 data: {
                     cur_pw: curPw.value,
                     new_pw: newPw.value
                 },
                 success: function (response) {
                 alert(response['msg'])
                 window.location.href = '/'
                 }
             })
        }else {
            document.getElementById('check-new').innerHTML = '새로운 비밀번호가 일치하지 않습니다.';
            document.getElementById('check-new').style.color = 'red';
            pwCheck.value = '';
            pwCheck.focus();
        }
    }

}
