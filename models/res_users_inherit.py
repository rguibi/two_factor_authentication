# -*- coding: utf-8 -*-

from odoo import api, models, fields
import random
import hashlib
import qrcode
import base64
from io import StringIO, BytesIO
import io

class Users(models.Model):
    _inherit = 'res.users'
    
    is_2fa_enable = fields.Boolean(string="2FA Status", default=False, copy=False)
    secret_key = fields.Char(string="Secret Key", readonly=True, copy=False)
    qr_code = fields.Binary(String="QR Code", copy=False)
    file_name = fields.Char(string="File Name", copy=False)
    
    #TODO: create secret key while creating user if 2fa enabled
    def _generate_secret_key(self):
        """Generate 16 digit secret key for 2FA"""
        valid_letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        secret_key = ''.join((random.choice(valid_letters) for i in range(16)))
        find_key = self.env['res.users'].search([('secret_key', '=', secret_key)])
        if find_key:
            self._generate_secret_key()
        secret_key = ' '.join(secret_key[i:i+4] for i in range(0,len(secret_key),4))
        return secret_key
    
    def _generate_qr_code(self, key):
        #generate qr code
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=20,border=4,)
        base_url = base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        new_key = "otpauth://totp/" + str(base_url) + "?secret=" + key.replace(" ", "")
        qr.add_data(new_key) #you can put here any attribute in my case

        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        encode_img = base64.b64encode(buffer.getvalue())
        return encode_img
    
    @api.model
    def create(self, vals):
        if vals.get('is_2fa_enable') == True:
            key = self._generate_secret_key()
            encode_img = self._generate_qr_code(key)
            vals.update({'secret_key': key, 'qr_code': encode_img, 'file_name': "QR Code"})
        return super(Users, self).create(vals)
    
    def write(self, vals):
        if vals.get('is_2fa_enable') == False:
            vals.update({'secret_key': '', 'qr_code': False, 'file_name': ''})
        if vals.get('is_2fa_enable') == True:
            key = self._generate_secret_key()
            encode_img = self._generate_qr_code(key)
            vals.update({'secret_key': key, 'qr_code': encode_img, 'file_name': "QR Code"})
        return super(Users, self).write(vals)
        
    
    def send_two_factor_auth_mail(self):
        if self.is_2fa_enable:
            attachment = {
                'name': str(self.file_name),
                'datas': self.qr_code,
                'name': self.file_name + ".png",
                'res_model': 'res.users',
                'type': 'binary'
            }
            attachment_id = self.env['ir.attachment'].create(attachment)
            try:
                mail_id = self.env.ref('two_factor_authentication.two_factor_auth_template')
                mail_id.attachment_ids = [(4, attachment_id.id)]
                mail_id.send_mail(self.id, force_send=True)
                attachment_id.unlink()
            except:
                pass
