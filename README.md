# KinanCity-Resend

This tool is used to figure out which accounts did not get activation links in [KinanCity](https://github.com/drallieiv/KinanCity) and attempt to resend the activation link.
The information from the account file and the logged links is compared to determine which accounts do not have a link recorded.

Thanks to [Gustavo Momente](https://github.com/gustavo-momente/KinanCity/blob/gm-resend-activation-email/KinanCity-extras/resender.py) for the original script that this one is based on.

# Get Started With Python
This script was written with Python3.6.

To get started using the python script, you can download the files or `git clone https://github.com/Kneckter/KinanCity-Resend` this repository.

You will need a few Python3 modules to run this script so run this command: `pip3 install -r requirements.txt`

Review the other options of the script with `python3 resender.py -h`

```
usage: resender.py [-h] [-a ACCTS_FILE] [-l LINKS_FILE] [-s SEPARATOR]
                   [-pn PROXY_NAME]

Resend PTC accounts activation e-mail

optional arguments:
  -h, --help            show this help message and exit
  -a ACCTS_FILE, --accts_file ACCTS_FILE
                        KinanCity Core account file, that is, a csv with
                        username;password;email
  -l LINKS_FILE, --links_file LINKS_FILE
                        KinanCity Mail links file, that is, a csv with
                        type;link;email;status
  -s SEPARATOR, --separator SEPARATOR
                        File separator, defaults to ;
  -pn PROXY_NAME, --proxy_name PROXY_NAME
                        The URL to the proxy like
                        'username:password@ip:port' or 'ip:port'
```

## Notes
This has been tested on Ubuntu 18.04. 

Activation links are only good for 48 hours so you must target that window to resend them.

You should have your mail server (KinanCity-Mail) running before executing this script.

If the activation emails do not come through, the account might not have been created. You can copy the output of the script into a new account file for KinanCity-Core to try to recreate.
