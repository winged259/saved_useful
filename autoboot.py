import io
import pathlib

import pycdlib

ubuntu = pathlib.Path('ubuntu-22.10-live-server-amd64.iso')
new_iso_path = pathlib.Path('abc.iso')

iso = pycdlib.PyCdlib()
iso.open(ubuntu)

extracted = io.BytesIO()
iso.get_file_from_iso_fp(extracted, iso_path='/BOOT/GRUB/GRUB.CFG;1')
extracted.seek(0)
data = extracted.read()
print(data.decode())

new = data.replace(b' ---', b'quiet autoinstall ds=nocloud\;s=/cdrom/nocloud/ ---')
new = new.replace(b'set timeout=30', b'set timeout=1')
print(new.decode())

iso.rm_file(iso_path='/BOOT/GRUB/GRUB.CFG;1', rr_name='grub.cfg')
iso.add_fp(io.BytesIO(new), len(new), '/BOOT/GRUB/GRUB.CFG;1', rr_name='grub.cfg')

iso.add_directory('/NOCLOUD', rr_name='nocloud')

user_data = b"""#cloud-config
autoinstall:
    version: 1
    identity:
        hostname: ubuntu-server
        password: "$6$N.tk92S/ii$3c7KQNM9CqWbQZsUkYIkfjFbunj.AD.zaY3WcXBMfH3YHuk1GY9a6j8eqjgu5xJ75g5LqsJYtCMu/KghQwf9R1"
        username: ubuntu777
    late-commands:
        - echo ubuntu-$(openssl rand -hex 3) > /target/etc/hostname
"""

iso.add_fp(io.BytesIO(user_data), len(user_data), '/NOCLOUD/USER_DATA;1', rr_name='user-data')
iso.add_fp(io.BytesIO(b''), len(b''), '/NOCLOUD/META_DATA;1', rr_name='meta-data')
iso.write(new_iso_path)
iso.close()
