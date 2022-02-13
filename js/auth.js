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

// 회원가입창(우선 method get으로 함 잘 보이질 않아서/....)


const userid = document.getElementById('signup-id');
const pw  = document.getElementById('signup-pwd');
const pwCheck = document.getElementById('pwd-check');
const nickname = document.getElementById('nickname')
let validnum = 0 //나중에 서버에서 값 반환받고 form 버튼 누를때 변수로 쓰기  
let check = 'example@email.com'// 혹시 서버에서 아이디 중복확인할때 필요할까봐 우선 만들어 놓음 지금체크용

//    아이디 중복체크 -통신 아직이해못함ㅜㅜ
function validId(){
  if (userid.value !== check && userid.value !==''){
    document.getElementById('valid-id').innerHTML= '사용 가능한 아이디입니다.';
    validnum = 1
    pw.focus()
  }
  else if(userid.value ==='') {
    document.getElementById('valid-id').innerHTML= '아이디를 입력해주세요';
    userid.focus()

  }
  else{
    document.getElementById('valid-id').innerHTML= '이미 존재하는 아이디 입니다.';
    userid.value = null;
    userid.focus()

  }
}
//     비밀번호
function checkPw(){
  if (pw.value.length < 4 || pw.value.length >8){
    alert('비밀번호는 최소 4자 ~최대 8자로 설정해주세요')
    pw.value = null;
    pw.focus;
  }
  if(pw.value!== '' && pwCheck.value!=='') {
    if(pw.value === pwCheck.value) {
        document.getElementById('same').innerHTML='비밀번호가 일치합니다.';
        document.getElementById('same').style.color='black';
        nickname.focus;
    }
    else {
        document.getElementById('same').innerHTML='비밀번호가 일치하지 않습니다.';
        document.getElementById('same').style.color='red';
        pwCheck.value = null;
        pwCheck.focus()
    }
  }
}
//     닉네임 
function checkNickname(){
  if (nickname.value === ''){
    alert('닉네임을 입력해주세요')
    nickname.focus;
  }
  else if(nickname.value < 2 || nickname.value >8){
    alert('닉네임은 2~8자 까지 가능합니다.')

  }
} 
//    회원가입 버튼
function submitSignUp() { //통신 못함, 수정필요해요 쓸데없는거 지우기
  if (validnum === 1 && (pw.value.length >= 4 && pw.value.length <= 8) && pw.value === pwCheck.value && nickname.value != '') {
    //통신 여기에 
    alert('회원가입 완료')
  } else if (validnum !== 1) {
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

const id = document.getElementById('signin-id');
const pwd = document.getElementById('signin-pwd');
function submitSignin(){
 if (id.value===''&& pwd.value===""){
   alert('아이디 혹은 비밀번호를 입력하세요')
 }
 else{
   //여기에 ajax
   alert('로그인 완료')
 }

}
