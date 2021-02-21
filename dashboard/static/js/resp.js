burger =  document.querySelector('.burger')
navbar = document.querySelector('.navbar')
navList =  document.querySelector('.nav-list')
navList2 =  document.querySelector('.nav-list2')
rightNav = document.querySelector('.rightNav')

burger.addEventListener('click', ()=>{
    rightNav.classList.toggle('v-class-resp');
    navList2.classList.toggle('v-class-resp');
    navbar.classList.toggle('h-nav-resp');
    navList.classList.toggle('v-class-resp');
})