window.onpopstate = function(event) {
  getPage(event.state.page);
}

function showAccs() {
  $('.acc-type').show();
}

function mainNav(page) {
  getPage(page);
}

function closePopModal() {
  document.querySelector('.pop-model').style.display = 'none';
}

function getPage(page) {

  fetch('/page/' + page, {
    method: 'POST',
    body: JSON.stringify({
      file_name: 'page'
    })
  })
    .then(response => response.json())
    .then(response => {
      // console.log(response);
      let style = `<link rel="stylesheet" href="{% static 'bank/css/t.css' %}">`;
      $('head').append(style);
      document.querySelector('#main-body').innerHTML = response.page;
      // history.pushState({'page':page}, "title", "to be pushed to the url");
      history.pushState({'page':page}, "", "");
    });
}

window.addEventListener('DOMContentLoaded', function () {
  let page = (window.location.hash).slice(1);
  if (page != "main-body") {
    getPage(page);
  }
})