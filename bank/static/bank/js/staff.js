function allCustomers() {

    let email = 'paulinnocent@email.com';
    let tel = '+2348112659304';
    let userEmail = `<a href="mailto:${email}"><i class="fa fa-envelope" aria-hidden="true"></i></a>`;
    let userTel = `<a href="tel:${tel}"><i class="fa fa-phone" aria-hidden="true"></i></a>`
    $('#user').html(`Paul Innocent ${userEmail} ${userTel}`);
    $('#transfer').text('2, 000 .00');
    $('#transferDate').text('08:43 AM 13|08|2020');
    $('#receive').text('1, 000 .00');
    $('#receiveDate').text('11:04 PM 13|08|2020');
    $('#complaints').text('I can\'t access my account');
    $('#complaintDate').text('09:04 PM 12|08|2020');
    // use case statement to say: after 3 loop show more button.
    // onclick of the more it will act as if staff search for the customer 
    // i.e it will display max output of 10 or 20 data about that customer on a single view
    $('#tbody').append('<br/><br/><br/><div class="btn btn-primary" style="width: 100%;">More</div>')
}
$('document').ready(function () {
    allCustomers();
})