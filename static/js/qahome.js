const toggles = document.querySelectorAll('.faq-toggle')

toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
        toggle.parentNode.classList.toggle('active')
        if(toggle.textContent=="关闭"){
            toggle.textContent="展开"
        }else{
            toggle.textContent="关闭"
        }

    })
})