json = [
    {
        'SenderName': '25-Abhay Patel',
        'SenderEmail': '200020116025ait@gmail.com',
        'Subject': 'Welcoming mail',
        'Date': '27/01/2024',
        'Time': '23:44',
        'Attachments': [],
        'Body': '<p>Hello Pop Star 1552!</p>'
    },
    {
        'SenderName': 'Google',
        'SenderEmail': 'no-reply@accounts.google.com',
        'Subject': 'Security alert',
        'Date': '31/01/2024',
        'Time': '05:52',
        'Attachments': [],
        'Body': "<p>[image: Google]</p><p>Phone number added for 2-Step Verification</p><p>popstar1552@gmail.com</p><p>Codes to sign in to your account now go to a new phone number. If you</p><p>didn't add this number, someone else might be using your account. Check and</p><p>secure your account now.</p><p>Check activity</p><p><a href='https://accounts.google.com/AccountChooser?Email=popstar1552@gmail.com&continue=https://myaccount.google.com/alert/nt/1706680328893?rfn%3D259%26rfnc%3D1%26eid%3D6595464560177604629%26et%3D0'>Click Here</a></p><p>You can also see security activity at</p><p>https://myaccount.google.com/notifications</p><p>You received this email to let you know about important changes to your</p><p>Google Account and services.</p><p>© 2024 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA</p>"
    },
    {
        'SenderName': 'Google',
        'SenderEmail': 'no-reply@accounts.google.com',
        'Subject': 'Security alert',
        'Date': '31/01/2024',
        'Time': '05:52',
        'Attachments': [],
        'Body': "<p>[image: Google]</p><p>App password created to sign in to your account</p><p>popstar1552@gmail.com</p><p>If you didn't generate this password for python_project, someone else might</p><p>be using your account. Check and secure your account now.</p><p>Check activity</p><p><a href='https://accounts.google.com/AccountChooser?Email=popstar1552@gmail.com&continue=https://myaccount.google.com/alert/nt/1706680358647?rfn%3D20%26rfnc%3D1%26eid%3D4015037382295405580%26et%3D0'>Click Here</a></p><p>You can also see security activity at</p><p>https://myaccount.google.com/notifications</p><p>You received this email to let you know about important changes to your</p><p>Google Account and services.</p><p>© 2024 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA</p>"
    },
    {
        'SenderName': 'Jenil Jani',
        'SenderEmail': 'jeniljani14@gmail.com',
        'Subject': 'Bezaati',
        'Date': '31/01/2024',
        'Time': '11:25',
        'Attachments': [],
        'Body': '<p>Kaisa hai gadhe 😂</p>'
    },
    {
        'SenderName': '25-Abhay Patel',
        'SenderEmail': '200020116025ait@gmail.com',
        'Subject': 'Summarization Content',
        'Date': '31/01/2024',
        'Time': '11:28',
        'Attachments': [],
        'Body': '<p>All arguments to commands are converted to strings, except for</p><p>AUTHENTICATE, and the last argument to APPEND which is passed as an IMAP4</p><p>literal. If necessary (the string contains IMAP4 protocol-sensitive</p><p>characters and isn’t enclosed with either parentheses or double quotes)</p><p>each string is quoted. However, the password argument to the LOGIN command</p><p>is always quoted. If you want to avoid having an argument string quoted</p><p>(eg: the flags argument to STORE) then enclose the string in parentheses.</p>'
    },
    {
        'SenderName': 'HyDrA Gaming',
        'SenderEmail': 'gamerspropaganda143@gmail.com',
        'Subject': 'Fwd: Phone Number',
        'Date': '31/01/2024',
        'Time': '11:30',
        'Attachments': [],
        'Body': '<p>---------- Forwarded message ---------</p><p>From: HyDrA Gaming <gamerspropaganda143@gmail.com></p><p>Date: Wed, 31 Jan 2024 at 11:27</p><p>Subject: Phone Number</p><p>To: <popstar1552@gmaiil.com></p><p>Below is my phone number. Must access that for the project.</p><p>Regards,</p><p>Abhay Patel</p><p>7007267441</p>'
    },
    {
        'SenderName': 'Darshan Gupta',
        'SenderEmail': 'darshangupta404@gmail.com',
        'Subject': 'Reminder: Team Meeting Tomorrow',
        'Date': '31/01/2024',
        'Time': '11:32',
        'Attachments': [],
        'Body': '<p>Hi Team,</p><p>Just a quick reminder that we have our weekly team meeting scheduled for</p><p>tomorrow at 10:00 AM in the conference room. Please make sure to bring any</p><p>updates or questions you have regarding ongoing projects.</p><p>Looking forward to seeing you all there!</p><p>Best,</p><p>Darshan</p>'
    }
]

import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

df = pd.DataFrame(json)

print(df['SenderName'].unique())
