import os
import pathlib

abc = pathlib.Path.home()
file = 'MailSift'

joining = os.path.join(abc, file)

# os.makedirs(joining)

print(joining, "done!")
