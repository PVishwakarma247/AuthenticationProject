function hideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
      setTimeout(() => {
        message.style.display = 'none';
      }, 1000);
    });
  }

  window.onload = hideFlashMessages;