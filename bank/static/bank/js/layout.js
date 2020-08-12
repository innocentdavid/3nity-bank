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
    // js not working
    // let js = `<script src="././static/bank/js/${page}.js">`;
    // $('body').append(js);

    let pdToggle = '<a href="/" style="color:white; padding: 0 .3rem; border:1px solid; font-size: 1rem;">';
    pdToggle += '<i class="fa fa-arrow-left"></i><span> Dashboard </span></a>';
    $('#pdToggle').html(pdToggle);

    document.querySelector('#main-body').innerHTML = response.page;
    // history.pushState({'page':page}, "title", "to be pushed to the url");
    history.pushState({
      'page': page
    }, "", `#${page}`);
  });
}

window.addEventListener('DOMContentLoaded', function () {
  let page = (window.location.hash).slice(1);
  if (page != "main-body") {
    getPage(page);
  }
})

window.onpopstate = function (event) {
  getPage(event.state.page);
}


// profile js start

function addSrc() {
  $('.add-exp').css('background',
    'rgb(17, 184, 128)');
  $('.add-src').css('background',
    'black');
  $('.add-exp-box').css('display',
    'none');
  $('.toggle-add-box').css('display',
    'block');
  $('.add-src-box').css('display',
    'block');
}
function addExp() {
  $('.add-src').css('background',
    'rgb(17, 184, 128)');
  $('.add-exp').css('background',
    'black');
  $('.add-src-box').css('display',
    'none');
  $('.toggle-add-box').css('display',
    'block');
  $('.add-exp-box').css('display',
    'block');
}
function toggleAddBox() {
  $('.add-exp').css('background',
    'rgb(17, 184, 128)');
  $('.add-src').css('background',
    'rgb(17, 184, 128)');
  $('.add-exp-box').css('display',
    'none');
  $('.add-src-box').css('display',
    'none');
  $('.toggle-add-box').css('display',
    'none');
}

function expandCatg(catgId) {
  document.getElementsByClassName('cr' + catgId)[0].style.display = 'none';
  document.getElementsByClassName('cd' + catgId)[0].style.display = 'block';
  document.getElementsByClassName('catgSumBox' + catgId)[0].style.display = 'block';
}
function compressCatg(catgId) {
  document.getElementsByClassName('cd' + catgId)[0].style.display = 'none';
  document.getElementsByClassName('cr' + catgId)[0].style.display = 'block';
  document.getElementsByClassName('catgSumBox' + catgId)[0].style.display = 'none';
}

function drawChart() {

  var data = google.visualization.arrayToDataTable([
    ['Task',
      'total expenditure'],
    ['Work',
      40],
    ['Nap',
      10],
    ['Eat',
      11],
    ['Eat',
      11],
    ['Watch TV',
      14],
    ['Watch TV',
      14],
    ['Sleep',
      15]
  ]);

  var chart = new google.visualization.PieChart(document.getElementById('piechart'));

  chart.draw(data,
    {
      title: 'My Weekly Expenditures',
      is3D: true,
    });
}

google.charts.load('current', {
  'packages': ['corechart']
});
google.charts.setOnLoadCallback(drawChart);

$(document).ready(function () {})

// profile js end



// transfer js start

// let accNum = document.querySelector('#accountNum');
// alert(accNum);
// if (accNum != Null){
//   accNum.addEventListener('keyup',function () {
//     alert('keyup');
//   })
// }


// all this wiil only work if bank == 3nity bank
function checkAccNum() {
  let accNum = document.querySelector('#accountNum').value;
  if (accNum.length >= 10) {
    // send a fetch requsts
    fetch('/check', {
      method: 'POST',
      body: JSON.stringify({
        check: "accountNumber",
        accNum: accNum
      })
    })
    .then(response => response.json())
    .then(response => {
      if (response.accName == 'None') {
        document.querySelector('#accountName').value = '';
        document.querySelector('#accNumError').innerHTML = "Account Number Not Found! (Hint: Account Number must be 10!)";
      } else {
        document.querySelector('#accNumError').innerHTML = '';
        document.querySelector('#accountName').value = response.accName;
      }
    })
  }
}

function checkTransPin() {
  let transPin = document.querySelector('#transPin').value;
  if (transPin.length >= 4) {
    // send a fetch requsts
    fetch('/check', {
      method: 'POST',
      body: JSON.stringify({
        check: "transPin",
        transPin: transPin
      })
    })
    .then(response => response.json())
    .then(response => {
      if (response.message == "ok") {
        document.querySelector('#transPinError').innerHTML = "";
        // ok
        setInterval(() => {
          stf();
        }, 500)
      } else {
        document.querySelector('#transPinError').innerHTML = "Incorrect Transaction Pin";
      }
    })
  }
}

function stf() {
  let bank = document.querySelector('#bank').value;
  let accNum = document.querySelector('#accountNum').value;
  let accName = document.querySelector('#accountName').value;
  let amount = document.querySelector('#amount').value;
  let naration = document.querySelector('#naration').value;
  let transPin = document.querySelector('#transPin').value;
  let transPinError = document.querySelector('#transPinError').innerHTML;
  let accNumError = document.querySelector('#accNumError').innerHTML;

  if (accNum.length == 10) {
    if (transPin.length == 4) {
      if (naration != '') {
        if (accNumError == '') {
          if (transPinError == '') {
            $('#transferFormSubmit').show()
          } else {
            $('#transferFormSubmit').hide()}
        } else {
          $('#transferFormSubmit').hide()}
      } else {
        $('#transferFormSubmit').hide()}
    } else {
      $('#transferFormSubmit').hide()}
  } else {
    $('#transferFormSubmit').hide()}
}


function transferFormSubmit() {

  fetch('/transfer', {
    method: 'POST',
    body: JSON.stringify({
      bank: document.querySelector('#bank').value,
      accNum: document.querySelector('#accountNum').value,
      accName: document.querySelector('#accountName').value,
      amount: document.querySelector('#amount').value,
      catg: document.querySelector('#catg').value,
      naration: document.querySelector('#naration').value,
      transPin: document.querySelector('#transPin').value
    })
  })
  .then(response => response.json())
  .then(response => {
    alert(response.message);
    document.querySelector('#accountNum').value = '';
    document.querySelector('#accountName').value = '';
    document.querySelector('#amount').value = '';
    document.querySelector('#naration').value = '';
    document.querySelector('#transPin').value = '';

    $('.tsc').show();
  })
}

function closeTsc() {
  $('.tsc').hide();
}

// transfer js end