// 로그인 회원가입 화면 바꾸기
const signinBtn = document.querySelector('.signup')
const signupBtn = document.querySelector('.signin')
const signinEl =document.querySelector('.container .signin')
const signupEl =document.querySelector('.container .signup')
const subSignin =document.querySelector('.wrap .submit-signin')
const subSignup =document.querySelector('.wrap .submit-signup')
signinBtn.addEventListener('click',function(){
  signinBtn.classList.add('show');
  signinEl.classList.remove('show');
  signupBtn.classList.remove('show');
  signupEl.classList.add('show');
  subSignin.classList.remove('show');
  subSignup.classList.add('show');
})

signupBtn.addEventListener('click',function(){
  signupBtn.classList.add('show')
  signupEl.classList.remove('show')
  signinBtn.classList.remove('show')
  signinEl.classList.add('show')
  subSignup.classList.remove('show');
  subSignin.classList.add('show');
})

// 아이디 확인 비밀번호확인

function confirmForm(){
  const pw =document.getElementById('signup-pwd').value
  const pwCheck=document.getElementById('pwd-check').value
  if (pw.length < 4 || pw.length >8){
    alert('비밀번호는 최소 4자 ~최대 8자로 설정해주세요')
    return false;
  }
  if(pw!= '' && pwCheck!='') {
    if(pw === pwCheck) {
        document.getElementById('same').innerHTML='비밀번호가 일치합니다.';
        document.getElementById('same').style.color='black';
    }
    else {
        document.getElementById('same').innerHTML='비밀번호가 일치하지 않습니다.';
        document.getElementById('same').style.color='red';
    }
  }
  }


  function validId(){
    alert('test')
  }
  function formSubmit(){

    alert("회원가입 완료!")
  }
  function login() {
    alert("로그인 완료!")
  }