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

      let style = `<link rel="stylesheet" href="././static/bank/css/${page}.css">`;
      $('#customCss').html(style);
      let js = `<script src="././static/bank/js/${page}.js">`;
      $('#customJs').html(js);

      let pdToggle = '<a href="/" style="color:white; padding: 0 .3rem; border:1px solid; font-size: 1rem;">';
      pdToggle += '<i class="fa fa-arrow-left"></i><span> Dashboard </span></a>';
      $('#pdToggle').html(pdToggle);

      document.querySelector('#main-body').innerHTML = response.page;
      // history.pushState({'page':page}, "title", "to be pushed to the url");
      history.pushState({'page':page}, "", `#${page}`);
    });
}

window.addEventListener('DOMContentLoaded', function () {
  let page = (window.location.hash).slice(1);
  if (page != "main-body") {
    getPage(page);
  }
})

window.onpopstate = function(event) {
  getPage(event.state.page);
}