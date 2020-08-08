function showAccs() {
    $('.acc-type').show();
  }
  
  function closePopModal() {
    document.querySelector('.pop-model').style.display = 'none';
  }
  
  function pageToggle(page) {
  
    fetch('/page/'+page, {
      method: 'POST',
      body: JSON.stringify({
        file_name: 'page'
      })
    })
    .then(response => response.json())
    .then(response => {
      // console.log(response);
      document.querySelector('#main-body').innerHTML = response.page;
    });
  }
  
  window.addEventListener('DOMContentLoaded', function () {
  })