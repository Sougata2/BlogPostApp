const showUsersbtn = document.querySelector(".show-user-btn")
const userList = document.querySelector('.user-list')
// show the user list.
const showUser = function(){
  userList.classList.toggle('hidden')
}
showUsersbtn.addEventListener("click",showUser)
