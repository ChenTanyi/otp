#!/usr/bin/env python3
import os
import sys
import rumps
import pyotp
import logging
import urllib.parse
import pyperclip


class OTPApp(rumps.App):

    def __init__(self, otp, *args, **kwargs):
        self._otp = otp
        super().__init__(*args, **kwargs)

    @rumps.clicked('OTP')
    def otp(self, sender):
        otp_str = self._otp.now()
        logging.debug(f'Get OTP: {otp_str}')
        pyperclip.copy(otp_str)


def get_otp():
    import qr
    cwd = os.path.abspath(os.path.dirname(__file__))
    qr_code = qr.scan_qr(os.path.join(cwd, 'qr.png'))[0]
    url = urllib.parse.urlparse(qr_code.data.decode())
    if url.scheme != 'otpauth' and url.netloc != 'totp':
        logging.exception(
            f'ERR! url scheme: {url.scheme} net loc: {url.netloc}')

    query = urllib.parse.parse_qs(url.query)
    if 'secret' not in query:
        logging.exception('secret not exists')

    secret = query['secret']
    if isinstance(secret, list):
        secret = secret[0]

    otp = pyotp.TOTP(secret)
    return otp


def main():
    otp = get_otp()
    logging.debug(f'Test OTP: {otp.now()}')
    OTPApp(otp, 'OTP').run()


if __name__ == '__main__':
    logging.basicConfig(
        level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s')
    main()