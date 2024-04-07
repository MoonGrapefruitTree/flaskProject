const labels = document.querySelectorAll('.form-control label')

labels.forEach(label => {
    label.innerHTML = label.innerText
        .split('')
        .map((letter, idx) => `<span style="transition-delay:${idx * 50}ms">${letter}</span>`)
        .join('')
})


function cap_btn_off(){
    var cap_btn = document.getElementById('cap-btn');
    cap_btn.removeAttribute("onclick")
}
function cap_btn_on(){
    var cap_btn = document.getElementById('cap-btn');
    cap_btn.setAttribute("onclick","sendemail()")
}
function cap_btn_change(txt){
    var cap_btn = document.getElementById('cap-btn');
    if(txt>0){cap_btn.textContent = "获得验证码" +"("+txt+")"}
    else {cap_btn.textContent = "获得验证码"};

}

function sendemail(){
    var email = document.getElementById('captcha-email').value;
    var $this = this
    const url = '/auth/captcha/email?email='+email;
    fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                    }
            )
        .then(response => {
            if (response.ok) {
                // alert("验证码发送成功")
                cap_btn_off()
                var countdown = 60
                var timer = setInterval(function (){
                    if(countdown<=0){
                        clearInterval(timer);
                        cap_btn_on()
                    };
                    cap_btn_change(countdown)
                    countdown = countdown - 1
                },1000);
                // console.log(response); // 如果返回的是JSON数据

            }else{
                alert("发送失败")
            }

        })
        .then(data => {
            console.log('Data received:', data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}