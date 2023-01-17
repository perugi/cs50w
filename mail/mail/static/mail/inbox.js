document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = () => {
    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;
    console.log(recipients, subject, body);

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
      .then(response => response.json())
      .then(result => {
        console.log(result)
      })

    load_mailbox('sent');

  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#mailbox-name').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Clear any existing that are displayed
  document.querySelector('#emails-table').innerHTML = "";
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      emails.forEach(email => {
        const row = document.createElement('div');
        row.className = "row email-display";
        if (email.read === true) {
          row.className += " read";
        }

        const sender = document.createElement('div');
        sender.innerHTML = email.sender;
        sender.className = "col";
        const subject = document.createElement('div');
        subject.innerHTML = email.subject;
        subject.className = "col-6";
        const timestamp = document.createElement('div');
        timestamp.innerHTML = email.timestamp;
        timestamp.className = "col text-right timestamp";

        row.append(sender, subject, timestamp);
        document.querySelector('#emails-table').append(row);

      });
    });
}