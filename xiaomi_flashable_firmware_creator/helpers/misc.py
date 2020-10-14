import re


def extract_codename(updater_script):
    # codename = str(i.readlines()[7].split('/', 3)[2]).split(':', 1)[0].replace('_', '-')
    codename = ''
    match = re.findall(r'/.*:[0-9]', updater_script)
    if match:
        codename = match[0].split('/')[-1].split(':')[0]
    else:
        match = re.search(r'get_device_compatible\(\"([a-z]*)|\\\"([a-z]*)\\\"',
                          updater_script)
        if match:
            codename = match.group(1)
    if not codename:
        codename = "codename"
    if codename.find('_') > 1:
        codename = codename.replace('_', '-')
    return codename
