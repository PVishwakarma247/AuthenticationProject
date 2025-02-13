// script.js
// Example: Toggle sidebar on smaller screens
const sidebar = document.querySelector('.sidebar');
const toggleBtn = document.createElement('button');
toggleBtn.textContent = '☰';
toggleBtn.classList.add('toggle-btn');
document.querySelector('.header').appendChild(toggleBtn);

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('active');
});

// for flash message
function hideFlashMessages() {
  const flashMessages = document.querySelectorAll('.flash-message');
  flashMessages.forEach(message => {
    setTimeout(() => {
      message.style.display = 'none';
    }, 1000);
  });
}

window.onload = hideFlashMessages;