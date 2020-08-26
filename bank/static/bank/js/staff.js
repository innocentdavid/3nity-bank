// alert();

function modify(action, fname, tel, email) {
    if (action == 'show') {
        let menuBtn = document.querySelector('#menu-btn' + fname);
        menuBtn.style.display = 'none';
        let closeMenuBtn = document.querySelector('#close-menu-btn' + fname);
        closeMenuBtn.style.display = 'block';

        let result = '<ul>';
        result += `<li title="${tel}"><a href="tel:${tel}"><i class="btn btn-primary fa fa-phone-square" aria-hidden="true"> Call Customer</i></a></li>`;
        result += `<li title="${email}"><a href="mailto:${email}"></a><i class="btn btn-primary fa fa-envelope" aria-hidden="true"> Send Email</i></a></li>`;
        result += `<li onclick="accSummary('block', '${email}')" title="${email}"><i class="btn btn-primary fa fa-pencil-square" aria-hidden="true"> Acct Summary</i></li>`;
        result += '</ul>';
        document.querySelector('#' + fname).innerHTML = result;
    } else {
        let menuBtn = document.querySelector('#menu-btn' + fname);
        menuBtn.style.display = 'block';
        let closeMenuBtn = document.querySelector('#close-menu-btn' + fname);
        closeMenuBtn.style.display = 'none';
        document.querySelector('#' + fname).innerHTML = '';
    }
}

// get total income and expenditure for the week 
function totalExp(action, user) {
    fetch('/totalIncome', {
        method: 'POST',
        body: JSON.stringify({ user: user, action: action })
    })
        .then(res => res.json())
        .then(res => {
            if (res.totalIncome.amount__sum != null) {
                $('#total-' + action).text(res.totalIncome.amount__sum);
            } else {
                $('#total-' + action).text(0);
            }
        })
}

// get total expenditure per category
function totalCatgExp(catg, user) {
    fetch('/totalCatgExp', {
        method: 'POST',
        body: JSON.stringify({ catg: catg, user: user })
    })
        .then(res => res.json())
        .then(res => {
            // console.log(res.totalCatgExp);
            if (res.totalCatgExp.amount__sum != null) {
                $('#amount' + catg).text(res.totalCatgExp.amount__sum);
            } else {
                $('#amount' + catg).text(0);
            }

            let a = $('#total-expenditure').text();
            let b = res.totalCatgExp.amount__sum * 100;
            let c = Math.round((b / a));

            if (a >= c) {
                $('#npercent' + catg).text(res.totalCatgExp.amount__sum);
            } else {
                $('#npercent' + catg).text(0);
            }
        })
}

function totalCatgExpb(catg) {
    let res = $('#npercent' + catg).text();
    
    if (res >= 0) {
        return res;
    } else {
        return 0;
    }
}

function AccountSummary(user, action, summary) {
    fetch('/AcctSummary', {
        method: 'POST',
        body: JSON.stringify({ user: user, action: action, summary: summary })
    })
        .then(res => res.json())
        .then(res => {
            // console.log(res);
            if (action == 'get') {
                $('#summaryTextarea')[0].value = res.summary;
            } else {
                location.reload();
            }
        })
}

$('#summaryForm').on('submit', function (e) {
    e.preventDefault();
    let summary = $('#summaryTextarea')[0].value;
    let user = $('#summaryUser')[0].value;
    AccountSummary(user, 'sumbitSummary', summary)
})

function accSummary(action, user) {
    document.querySelector('#acctSummary').style.display = action;
    if (action == 'block') {
        // get total income and expenditure for the week
        totalExp('income', user);
        totalExp('expenditure', user);

        // get total expenditure per category
        totalCatgExp('Properties', user);
        totalCatgExp('Investment', user);
        totalCatgExp('Food', user);
        totalCatgExp('Shelter', user);
        totalCatgExp('Miscellaneous', user);

        // get
        let p = 0;
        let i = 0;
        let f = 0;
        let s = 0;
        let m = 0;
        let getExcess = setInterval(() => {
            let a = $('#total-income').text();
            let b = $('#total-expenditure').text();
            let c = `Excess of RECEIPTS over EXPENDITURE: <b>NGN <span id="excess">${a - b}</span></b>`;
            $('#excess-wrapper').html(c);

            p += Math.round($('#npercentProperties').text());
            i += Math.round($('#npercentInvestment').text());
            f += Math.round($('#npercentFood').text());
            s += Math.round($('#npercentShelter').text());
            m += Math.round($('#npercentMiscellaneous').text());
            
        }, 2000);
        setTimeout(() => {
            clearInterval(getExcess);
        }, 4000);

        let xy = setInterval(() => {
            if (p >= 0){pp=p}else{pp=0}
            if (i >= 0){ii=i}else{ii=0}
            if (f >= 0){ff=f}else{ff=0}
            if (s >= 0){ss=s}else{ss=0}
            if (m >= 0){mm=m}else{mm=0}
            // console.log(mm);
            let res = pp + ii + ff + ss + mm;
            // console.log(res);
            $('#percentProperties').text(((pp*100)/res).toFixed(2));
            $('#percentInvestment').text(((ii*100)/res).toFixed(2));
            $('#percentFood').text(((ff*100)/res).toFixed(2));
            $('#percentShelter').text(((ss*100)/res).toFixed(2));
            $('#percentMiscellaneous').text(((mm*100)/res).toFixed(2));
        }, 2500);
        setTimeout(() => {
            clearInterval(xy)
        }, 5000);

        // get Account Summary
        AccountSummary(user, 'get', 'summary');
        // update Account Summary
        $('#summaryUser')[0].value = user;
    }
}

function allCustomers() {
    document.querySelectorAll('#user').forEach(users => {
        let user = users.dataset.user;
        let fname = String(users.dataset.fname);
        if (user == '') { } else {
            fetch('/allCustomer', {
                method: 'POST',
                body: JSON.stringify({
                    user: user
                })
            })
                .then(response => response.json())
                .then(response => {
                    // console.log(response);
                    if (response.message == undefined) {
                        let result = '';
                        response.forEach(history => {
                            result += '<div class="row" style="margin: 1rem 0">'
                            result += '<div class="col-9">'
                            result += '<ul style="list-style-type: disc;">';
                            result += '<li>';
                            result += `<b>NGN ${history.amount}</b>  `;
                            if (history.transcType == 'Income') {
                                result += `<span class="btn-sm btn-success">Received:</span> `;
                            } else {
                                result += `<span class="btn-sm btn-danger">Transfered:</span> `;
                            }
                            result += `${history.naration}`;
                            result += '</li></ul></div>';
                            result += `<div class="col-3" style="text-align:right; font-size: .8rem;">${history.timestamp}</div>`;
                            result += '</div>'
                        });
                        $('#details' + fname).html(result);
                    } else {
                        document.querySelector('#details' + fname).innerHTML = `<center><h1>${response.message}</h1></center>`;
                    }
                })
        }
    });
}

function closeErr() {
    let x = document.querySelector('#err-msg');
    x.style.display='none';
}

$('document').ready(function () {
    allCustomers();
})