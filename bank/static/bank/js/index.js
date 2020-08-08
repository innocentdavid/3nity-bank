function showAccs() {
  $('.acc-type').show();
}

function closePopModal() {
  document.querySelector('.pop-model').style.display = 'none';
}

function rTransc(id) {
  document.querySelector('.pop-model').style.display = 'block';
  document.querySelector('.modal-body').innerHTML = id;
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