const openModal = document.querySelector('.modal-on');
const modal = document.querySelector('.modal-inscripcion');
const closeModal = document.querySelector('.modal-off');

openModal.addEventListener('click', (e)=>{
    e.preventDefault();
    modal.classList.add('modal-show');
})

closeModal.addEventListener('click', (e)=>{
    e.preventDefault();
    modal.classList.remove('modal-show');
})