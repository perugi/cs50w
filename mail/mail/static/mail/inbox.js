document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(replied_mail) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // This is a new mail, clear out the compose fields.
  if (replied_mail === undefined) {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    // We should not add a new "Re: ", if the subject already contains it.
    if (!(replied_mail.subject.startsWith("Re: "))) {
      replied_mail.subject = `Re: ${replied_mail.subject}`;
    }

    document.querySelector('#compose-recipients').value = replied_mail.sender;
    document.querySelector('#compose-subject').value = replied_mail.subject;
    document.querySelector('#compose-body').value =
      `\n\nOn ${replied_mail.timestamp} ${replied_mail.sender} wrote:\n${replied_mail.body}`;
  }

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
        load_mailbox('sent');
      })

    return false;
  }
}


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-name').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Clear any existing emails that are displayed
  document.querySelector('#emails-table').innerHTML = "";

  // Fetch the mail data and generate the table
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      emails.forEach(email => {
        const row = document.createElement('div');
        row.className = "row email-display";
        if (email.read === true) {
          row.className += " read";
        };
        row.addEventListener('click', () => {
          read_mail(email);
        });

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

function read_mail(email) {
  // Mark the mail as read
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });

  // Show the mail display and hide other views
  document.querySelector('#read-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear any existing email info that is displayed
  document.querySelector('#read-info').innerHTML = "";

  // Populate the mail info
  const sender = document.createElement('div');
  sender.innerHTML = `<b>From:</b> ${email.sender} `;
  const recipients = document.createElement('div');
  recipients.innerHTML = `<b>To:</b> ${email.recipients} `;
  const subject = document.createElement('div');
  subject.innerHTML = `<b>Subject:</b> ${email.subject} `;
  const timestamp = document.createElement('div');
  timestamp.innerHTML = `<b>Timestamp:</b> ${email.timestamp} `;

  const reply_button = document.createElement('button');
  reply_button.innerHTML = "Reply";
  reply_button.className = "btn btn-sm btn-outline-primary";
  reply_button.id = "reply-button";
  reply_button.addEventListener('click', () => {
    compose_email(email);
  });

  document.querySelector('#read-info').append(sender, recipients, subject, timestamp,
    reply_button);

  console.log(email.sender, document.querySelector('#user-id').innerHTML);
  if (email.sender !== document.querySelector('#user-id').innerHTML) {
    const archive_button = document.createElement('button');
    if (email.archived === false) {
      archive_button.innerHTML = "Archive";
    } else {
      archive_button.innerHTML = "Unarchive";

    }
    archive_button.className = "btn btn-sm btn-outline-primary";
    archive_button.id = "archive-button";
    archive_button.addEventListener('click', () => {
      archive_mail(email);
    });
    document.querySelector('#read-info').append(archive_button)
  }


  // Populate the mail body
  document.querySelector('#read-body').innerHTML = email.body
  console.log(email.body)
}

function archive_mail(email) {

  // Change the state of the archived value of the mail.
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !(email.archived)
    })
  })
    .then(() => {
      load_mailbox('inbox');
    })
}